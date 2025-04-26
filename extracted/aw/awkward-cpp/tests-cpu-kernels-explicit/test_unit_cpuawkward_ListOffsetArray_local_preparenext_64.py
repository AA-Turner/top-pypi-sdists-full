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

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_3():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_4():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_5():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 2, 3, 5, 7]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_6():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [7, 5, 3, 2, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [4, 3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_7():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 2, 7, 5, 3]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [0, 1, 4, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_local_preparenext_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 0, 2, 4, 3, 6, 5, 7]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 8
    funcC = getattr(lib, 'awkward_ListOffsetArray_local_preparenext_64')
    ret_pass = funcC(tocarry, fromindex, length)
    pytest_tocarry = [1, 0, 2, 4, 3, 6, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

