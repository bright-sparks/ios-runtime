//
//  TNSReturnsRetained.h
//  NativeScriptTests
//
//  Created by Jason Zhekov on 5/10/15.
//  Copyright (c) 2014 Jason Zhekov. All rights reserved.
//

id functionReturnsNSRetained() NS_RETURNS_RETAINED;
id functionReturnsCFRetained() CF_RETURNS_RETAINED;

@interface TNSReturnsRetained : NSObject
+ (id)methodReturnsNSRetained NS_RETURNS_RETAINED;
+ (id)methodReturnsCFRetained CF_RETURNS_RETAINED;
@end
