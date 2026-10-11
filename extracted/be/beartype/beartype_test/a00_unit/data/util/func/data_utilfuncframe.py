#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **call stack frame utilities** test data submodule.

This submodule defines low-level callables and classes class validating known
edge cases on behalf of the higher-level
:mod:`beartype_test.a00_unit.a20_util.func.test_utilfuncframe` submodule.
'''

# ....................{ IMPORTS                            }....................
from beartype._util.func.utilfuncframe import (
    GET_FRAME_CALLER,
    get_frame_or_none,
    # get_frame_locals,
    get_frame_parent_object_or_none,
    is_frame_module,
)
from beartype._util.module.utilmodget import get_module_imported_or_none

# ....................{ GLOBALS                            }....................
# This current module.
module_current = get_module_imported_or_none(__name__)

# Stack frame encapsulating the global scope (i.e., body) of this module.
frame_module_current = get_frame_or_none(ignore_frames=GET_FRAME_CALLER)

# ....................{ CALLABLES                          }....................
def the_heavens_through() -> None:
    '''
    Arbitrary function internally asserting that the
    :func:`.get_frame_parent_object_or_none` getter returns the current function
    object when passed a frame encapsulating the local scope (i.e., body) of
    this function.
    '''

    # ....................{ LOCALS                         }....................
    # Stack frame encapsulating the local scope (i.e., body) of this current
    # function.
    frame_func_current = get_frame_or_none(ignore_frames=GET_FRAME_CALLER)

    # ....................{ PASS                           }....................
    # Assert that this getter returns this current function when called from the
    # body of this function.
    frame_func_current_parent_object = get_frame_parent_object_or_none(
        frame_func_current)
    assert frame_func_current_parent_object is the_heavens_through

# ....................{ CLASSES                            }....................
class FromEastToWest(object):
    '''
    Arbitrary class internally asserting that the
    :func:`.get_frame_parent_object_or_none` getter returns the current class
    object when passed a frame encapsulating the class scope (i.e., body) of
    this class.
    '''

    # ....................{ CLASS VARS                     }....................
    # Stack frame encapsulating the class scope (i.e., body) of this current
    # class.
    frame_type_current = get_frame_or_none(ignore_frames=GET_FRAME_CALLER)
    # print(f'type locals: {repr(get_frame_locals(frame_type_current))}')

    # None. Why? Because this current class has yet to be defined until the body
    # of this class has been executed to completion. It is what it is.
    frame_type_current_parent_object = get_frame_parent_object_or_none(
        frame_type_current)

# ....................{ PASS ~ module                      }....................
# Assert that this tester returns true when passed a stack frame encapsulating
# the global scope of a module. Why? Basic sanity smoke check. If this fails,
# everything below is likely to fail as well. *shrug*
assert is_frame_module(frame_module_current) is True

# Assert that this getter returns the current module object when passed a stack
# frame encapsulating the global scope of a module.
frame_module_current_parent_object = get_frame_parent_object_or_none(
    frame_module_current)
assert frame_module_current_parent_object is module_current

# ....................{ PASS ~ function                    }....................
# Implicitly assert that all local assertions performed by the body of the
# callables defined above pass as well.
the_heavens_through()

# ....................{ FAIL ~ type                        }....................
# Assert that this getter returns "None" when passed a stack frame encapsulating
# the class scope of a class. See above for discussion.
# print(f'FromEastToWest.frame_type_current_parent_object: {FromEastToWest.frame_type_current_parent_object}')
assert FromEastToWest.frame_type_current_parent_object is None
