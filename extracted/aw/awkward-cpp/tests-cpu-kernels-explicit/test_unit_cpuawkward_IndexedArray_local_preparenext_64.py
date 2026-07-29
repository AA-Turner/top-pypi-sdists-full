# AUTO GENERATED ON 2026-07-28 AT 17:37:39
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

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_1():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    nextoffsets = [0, 4]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, offsets, nextoffsets, outlength)
    pytest_tocarry = [0, 1, 2, 3, -1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_2():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 6, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    nextoffsets = [0, 4, 7]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outlength = 2
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, offsets, nextoffsets, outlength)
    pytest_tocarry = [0, 1, 2, 3, -1, -1, 4, 5, 6, -1, -1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_3():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    nextoffsets = [0]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outlength = 0
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, offsets, nextoffsets, outlength)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    starts = [0, 5, 8, 11, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 8, 11, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    nextoffsets = [0, 3, 3, 5, 6, 9]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, offsets, nextoffsets, outlength)
    pytest_tocarry = [0, 1, 2, -1, -1, -1, -1, -1, 3, 4, -1, 5, -1, -1, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    starts = [0, 5, 8, 11, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 8, 11, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    nextoffsets = [0, 3, 4, 6, 7, 10]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, offsets, nextoffsets, outlength)
    pytest_tocarry = [0, 1, 2, -1, -1, 3, -1, -1, 4, 5, -1, 6, -1, -1, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

