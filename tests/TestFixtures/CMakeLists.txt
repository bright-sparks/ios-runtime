set(HEADER_FILES
    TestFixtures-Prefix.h
    TestFixtures.h

    Api/TNSApi.h
    Api/TNSDeclarationConflicts.h
    Api/TNSVersions.h
    Functions/TNSFunctions.h
    Interfaces/TNSClassWithPlaceholder.h
    Interfaces/TNSConstructorResolution.h
    Interfaces/TNSInheritance.h
    Interfaces/TNSMethodCalls.h
    Marshalling/TNSFunctionPointers.h
    Marshalling/TNSObjCTypes.h
    Marshalling/TNSPrimitivePointers.h
    Marshalling/TNSPrimitives.h
    Marshalling/TNSRecords.h
    TNSTestCommon.h
    TNSTestNativeCallbacks.h
)

set(SOURCE_FILES
    Api/TNSApi.m
    Api/TNSDeclarationConflicts.m
    Api/TNSVersions.m
    Functions/TNSFunctions.m
    Interfaces/TNSClassWithPlaceholder.m
    Interfaces/TNSConstructorResolution.m
    Interfaces/TNSInheritance.m
    Interfaces/TNSMethodCalls.m
    Marshalling/TNSFunctionPointers.m
    Marshalling/TNSObjCTypes.m
    Marshalling/TNSPrimitivePointers.m
    Marshalling/TNSPrimitives.m
    Marshalling/TNSRecords.m
    TNSTestCommon.m
    TNSTestNativeCallbacks.m
)

set_source_files_properties(Interfaces/TNSClassWithPlaceholder.m PROPERTIES COMPILE_FLAGS -fno-objc-arc)

add_library(TestFixtures STATIC ${HEADER_FILES} ${SOURCE_FILES})

set_target_properties(TestFixtures PROPERTIES COMPILE_FLAGS "
    -fobjc-arc
    -Werror -Wall -Wextra
    -Wno-error=incomplete-implementation
    -Wno-unused-parameter
")

set_target_properties(TestFixtures PROPERTIES XCODE_ATTRIBUTE_ENABLE_NS_ASSERTIONS YES)

include(SetActiveArchitectures)
SetActiveArchitectures(TestFixtures)

include(GroupSources)
GroupSources(TestFixtures)

include(PrecompiledHeaders)
SetPrecompiledHeader(TestFixtures TestFixtures-Prefix.h)
