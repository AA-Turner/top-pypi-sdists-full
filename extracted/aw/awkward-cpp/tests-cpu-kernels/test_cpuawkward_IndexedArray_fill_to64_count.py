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

def test_cpuawkward_IndexedArray_fill_to64_count_1():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_count_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_count_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_count_4():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [123, 3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_count_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [3, 4, 5]
    assert not ret_pass.str

