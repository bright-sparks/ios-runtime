#!/usr/bin/env python

import os.path
from codegen import *
import json
#from models import *

_PRIMITIVE_TO_TS_NAME_MAP = {
    'integer': 'number',
    'object': 'Object'
}

def ts_name_for_primitive_type(_type):
    ts_name = _PRIMITIVE_TO_TS_NAME_MAP.get(_type.raw_name())
    if ts_name:
        return ts_name
    return _type.raw_name()


def load_specification(protocol, filepath, isSupplemental=False):
    try:
        with open(filepath, "r") as input_file:
            parsed_json = json.load(input_file)
            protocol.parse_specification(parsed_json, isSupplemental)
    except ValueError as e:
        raise Exception("Error parsing valid JSON in file: " + filepath)

protocol = models.Protocol("JavaScriptCore")

load_specification(protocol, "/Users/koeva/work/temp/CombinedDomains.json");

protocol.resolve_types()

# reuse me
# A writer that only updates file if it actually changed.
class IncrementalFileWriter:
    def __init__(self, filepath, force_output):
        self._filepath = filepath
        self._output = ""
        self.force_output = force_output

    def write(self, text):
        self._output += text

    def close(self):
        text_changed = True
        self._output = self._output.rstrip() + "\n"

        try:
            if self.force_output:
                raise

            read_file = open(self._filepath, "r")
            old_text = read_file.read()
            read_file.close()
            text_changed = old_text != self._output
        except:
            # Ignore, just overwrite by default
            pass

        if text_changed or self.force_output:
            out_file = open(self._filepath, "w")
            out_file.write(self._output)
            out_file.close()

class TypeScriptInterfaceGenerator(Generator):
    def __init__(self, model):
        Generator.__init__(self, model, "")
        self.type_def_member_names = []
    
    def output_filename(self):
        return "InspectorBackendCommands.ts"

    def domains_to_generate(self):
        def should_generate_domain(domain):
            domain_enum_types = filter(lambda declaration: isinstance(declaration.type, EnumType), domain.type_declarations)
            return len(domain.commands) > 0 or len(domain.events) > 0 or len(domain_enum_types) > 0

        return filter(should_generate_domain, Generator.domains_to_generate(self))

    def generate_output(self):
        sections = []
        sections.extend(map(self.generate_domain, self.domains_to_generate()))
        return "\n\n".join(sections)

    def generate_domain(self, domain):
        lines = []
        args = {
            'domain': domain.domain_name
        }

        lines.append('// %(domain)s.' % args)
        lines.append('namespace %(domain)s {' % args)

        lines.extend(self.generate_domain_type_declarations(domain))

        lines.append("interface %(domain)sDomainDispatcher { }" % args);
        lines.append('}')
        return "\n".join(lines)

    def generate_domain_type_declarations(self, domain):
        lines = []
        # generate typedefs
        primitive_declarations = filter(lambda decl: isinstance(decl.type, AliasedType), domain.type_declarations)
        object_declarations = filter(lambda decl: isinstance(decl.type, ObjectType), domain.type_declarations)

        for primitive_declaration in primitive_declarations:
            type_def_args = { 
                'type_def_name': primitive_declaration.type_name,
                'type_def_type': ts_name_for_primitive_type(primitive_declaration.type.aliased_type)
            }
            # self.type_def_member_names.append(primitive_declaration.type_name)
            lines.append('export type %(type_def_name)s = %(type_def_type)s' % type_def_args)
            # self.type_def_member_names.append(primitive_declaration.type.raw_name());

        lines.append('')

        for declaration in object_declarations:
            declaration_args = {
                'type_name': declaration.type.raw_name() 
            } 
            lines.append('export interface %(type_name)s {' % declaration_args)
            
            primitive_types =  filter(lambda member: isinstance(member.type, PrimitiveType) and not any(type_def_member_name.lower() == member.member_name.lower() for type_def_member_name in self.type_def_member_names), declaration.type_members)
            aliased_types =  filter(lambda member: isinstance(member.type, (AliasedType, ObjectType)) and not any(type_def_member_name.lower() == member.member_name.lower() for type_def_member_name in self.type_def_member_names), declaration.type_members)

            # self.type_def_member_names.append(declaration.type.raw_name());
            for primitive_type_member in primitive_types:
                member_args = {
                    'name': primitive_type_member.member_name,
                    'type': ts_name_for_primitive_type(primitive_type_member.type)
                }
                lines.append('\t%(name)s: %(type)s;' % member_args)

            for aliased_type_member in aliased_types:
                type_raw_name = aliased_type_member.type.raw_name()
                if aliased_type_member.type.type_domain() != domain:
                    aliased_type_member_args = {
                        'domain': aliased_type_member.type.type_domain().domain_name,
                        'type': type_raw_name
                    }
                    type_raw_name = '%(domain)s.%(type)s' % aliased_type_member_args
                else:
                    type_raw_name = ts_name_for_primitive_type(aliased_type_member.type)

                member_args = {
                    'name': aliased_type_member.member_name,
                    'type': type_raw_name
                }
                lines.append('\t%(name)s: %(type)s;' % member_args)

            lines.append('}\n')

        return lines


generator = TypeScriptInterfaceGenerator(protocol)
output = generator.generate_output()
output_file = IncrementalFileWriter(os.path.join("/Users/koeva/work/temp/shit", generator.output_filename()), False)
output_file.write(output)
output_file.close()
# print(output)