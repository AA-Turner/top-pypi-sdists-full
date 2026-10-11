#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **circular submodule import** data submodule.

This submodule circularly imports its sibling submodule in this subpackage.
'''

# ....................{ IMPORTS                            }....................
# Circularly import our sibling submodule in this subpackage.
from beartype_test.a00_unit.data.util.module.circular.data_utilmodcircular_hours import (
    ReleasedHeFled)

# ....................{ SUBCLASSES                         }....................
class FromOverStrainedMight(ReleasedHeFled):
    '''
    Arbitrary type subclassing another arbitrary type circularly imported above
    from our sibling submodule.
    '''

    pass
