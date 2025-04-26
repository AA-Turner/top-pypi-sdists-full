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

def test_cpuawkward_UnionArray_fillindex_to64_from32_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_from32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [123, 123, 123, 1, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray_fillindex_to64_from32_2():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_from32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [123, 123, 123, 1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray_fillindex_to64_from32_3():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_from32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [123, 123, 123, 1, 3, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray_fillindex_to64_from32_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_from32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [123, 123, 123, 1, 4, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray_fillindex_to64_from32_5():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    toindexoffset = 3
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_from32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [123, 123, 123, 0, 0, 0]
    assert not ret_pass.str

