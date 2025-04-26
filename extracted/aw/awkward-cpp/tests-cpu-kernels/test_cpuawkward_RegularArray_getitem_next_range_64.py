# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import numpy as np
import pytest

from awkward_cpp.cpu_kernels import lib

def test_cpuawkward_RegularArray_getitem_next_range_64_1():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    regular_start = 3
    step = 3
    length = 3
    size = 3
    nextsize = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [3, 6, 9, 6, 9, 12, 9, 12, 15]
    assert not ret_pass.str

