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

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_1():
    tooffsets = []
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = []
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 0
    fromoffsets = []
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = []
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_2():
    tooffsets = []
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 1
    fromoffsets = []
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = []
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_3():
    tooffsets = [123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = []
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 0
    fromoffsets = [0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_4():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [-1, -1, -1, -1, -1, -1, -1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 7
    fromoffsets = [0, 2, 3, 5, 7]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_5():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [-1, 0, -1, 0, 0, -1, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 7
    fromoffsets = [0, 2, 3, 5, 7]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 1, 1, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_6():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 6
    fromoffsets = [0, 2, 3, 5, 6]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 2, 3, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_7():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 6
    fromoffsets = [0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_8():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 6
    fromoffsets = [0, 2, 3, 3, 6]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 2, 3, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_drop_none_indexes_32_9():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [-1, -1, -1, -1, -1, -1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    length_indexes = 6
    fromoffsets = [0, 2, 3, 3, 6]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 5
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

