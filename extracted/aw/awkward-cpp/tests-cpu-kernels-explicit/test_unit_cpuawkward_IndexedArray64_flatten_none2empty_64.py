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

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_1():
    outoffsets = [123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 1
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 0
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_2():
    outoffsets = [123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 0
    outindex = [0]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 1
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    assert funcC(outoffsets, outindex, outindexlength, offsets, offsetslength).str.decode('utf-8') == "flattening offset out of range"

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_3():
    outoffsets = [123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 1, 1, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, 1, 2, 1]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 1, 1, 6, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_4():
    outoffsets = [123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 1, 1, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, 1, 2, 1]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 1, 1, 6, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_5():
    outoffsets = [123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 1, 1, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, -1, 2, -1]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 1, 1, 6, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_6():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, 1, 1, 1, 2]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 3, 3, 3, 3, 5]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_7():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, -1, 1, -1, 2]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 3, 3, 3, 3, 5]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_8():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 3, 3, 4, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 5
    outindex = [0, 1, 2, 1, 3]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 3, 3, 4, 4, 7]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_9():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 3, 3, 4, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 5
    outindex = [0, -1, 2, -1, 3]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 3, 3, 4, 4, 7]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_10():
    outoffsets = [123, 123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 3, 3, 5, 6, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 7
    outindex = [0, 1, 2, 3, 4, 1, 5]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 3, 3, 5, 6, 6, 6, 10]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_11():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 4, 4, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    outindex = [0, 1, 1, 1, 2, 1]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 4, 4, 4, 4, 6, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_12():
    outoffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 4, 4, 6, 7, 7, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 7
    outindex = [0, 1, 1, 1, 2, 3, 4, 5, 1]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 9
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 4, 4, 4, 4, 6, 7, 7, 12, 12]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_none2empty_64_13():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    offsets = [0, 5, 5, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 5
    outindex = [0, 1, 1, 2, 1, 3]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    outindexlength = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_none2empty_64')
    ret_pass = funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)
    pytest_outoffsets = [0, 5, 5, 5, 6, 6, 9]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

