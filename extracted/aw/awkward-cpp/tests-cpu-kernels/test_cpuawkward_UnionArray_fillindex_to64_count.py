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

def test_cpuawkward_UnionArray_fillindex_to64_count_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length)
    pytest_toindex = [123, 123, 123, 0, 1, 2]
    assert not ret_pass.str

