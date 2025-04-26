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

def test_cpuawkward_ListOffsetArray32_toRegularArray_1():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray32_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray32_toRegularArray_2():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray32_toRegularArray')
    assert funcC(size, fromoffsets, offsetslength).str

def test_cpuawkward_ListOffsetArray32_toRegularArray_3():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray32_toRegularArray')
    assert funcC(size, fromoffsets, offsetslength).str

def test_cpuawkward_ListOffsetArray32_toRegularArray_4():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray32_toRegularArray')
    assert funcC(size, fromoffsets, offsetslength).str

def test_cpuawkward_ListOffsetArray32_toRegularArray_5():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray32_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [0]
    assert not ret_pass.str

