#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
Test-wide **circular submodule import** data subpackage.

This subpackage defines two submodules that circularly import one another when
either is imported, raising the standard :class:`ImportError` exception whose
message resembles:

.. code-block:: python

   ImportError: cannot import name 'FromOverStrainedMight' from partially
   initialized module
   'beartype_test.a00_unit.data.util.module.circular.data_utilmodcircular_gates'
   (most likely due to a circular import)
   (/home/leycec/py/beartype/beartype_test/a00_unit/data/util/module/circular/data_utilmodcircular_gates.py)   
'''
