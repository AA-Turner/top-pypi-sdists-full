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

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_1():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_2():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [2, 2, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_3():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [2, 1, 0, -1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_4():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [1, 3, 2, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_5():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_6():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_7():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_8():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_9():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_10():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_11():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_12():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_13():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_14():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_15():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_16():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_17():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_18():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_19():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_20():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_21():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_22():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [2, 3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_23():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [2, 1, 0, -1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_24():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [1, 0, -1, -2]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_flatten_none2empty_64_25():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindex = (ctypes.c_uint32*len(outindex))(*outindex)
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 0, 0, 0]
    assert not ret_pass.str

