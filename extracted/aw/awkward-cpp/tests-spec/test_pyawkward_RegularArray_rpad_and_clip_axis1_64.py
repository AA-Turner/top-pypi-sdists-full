# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_RegularArray_rpad_and_clip_axis1_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    target = 3
    size = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    funcPy(toindex=toindex, target=target, size=size, length=length)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

