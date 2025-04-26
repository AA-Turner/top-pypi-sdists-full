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

def test_cpuawkward_ListArray32_localindex_64_1():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int32*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [123, 123, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_localindex_64_2():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int32*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_localindex_64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int32*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 0]
    assert not ret_pass.str

