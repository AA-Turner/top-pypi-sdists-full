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

def test_cpuawkward_RegularArray_localindex_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    size = 3
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_localindex_64_2():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    size = 2
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 1, 0, 1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_localindex_64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    size = 1
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_localindex_64_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    size = 2
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 1, 0, 1, 0, 1]
    assert not ret_pass.str

