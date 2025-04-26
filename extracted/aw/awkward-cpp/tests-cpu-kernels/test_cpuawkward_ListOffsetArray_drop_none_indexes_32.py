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

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_1():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_2():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_3():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_4():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_5():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_6():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_7():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_8():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_9():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_10():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_11():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_12():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_13():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_14():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_15():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_16():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_17():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_18():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_19():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_20():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_21():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_22():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_23():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_24():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray_drop_none_indexes_32_25():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noneindexes = (ctypes.c_int32*len(noneindexes))(*noneindexes)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int32*len(fromoffsets))(*fromoffsets)
    length_offsets = 3
    length_indexes = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_drop_none_indexes_32')
    ret_pass = funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

