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

def test_cpuawkward_IndexedArray_fill_to64_fromU32_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length, base)
    pytest_toindex = [123, 123, 123, 4, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_fromU32_2():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length, base)
    pytest_toindex = [123, 123, 123, 4, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_fromU32_3():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length, base)
    pytest_toindex = [123, 123, 123, 4, 6, 3]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_fromU32_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length, base)
    pytest_toindex = [123, 123, 123, 4, 7, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArray_fill_to64_fromU32_5():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length, base)
    pytest_toindex = [123, 123, 123, 3, 3, 3]
    assert not ret_pass.str

