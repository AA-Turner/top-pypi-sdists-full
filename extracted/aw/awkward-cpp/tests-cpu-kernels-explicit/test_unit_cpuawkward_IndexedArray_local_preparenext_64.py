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

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_1():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    nextlen = 4
    nextparents = [0, 0, 0, 0]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parentslength = 5
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, parents, parentslength, nextparents, nextlen)
    pytest_tocarry = [0, 1, 2, 3, -1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_2():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    nextlen = 7
    nextparents = [0, 0, 0, 0, 1, 1, 1]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parentslength = 11
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, parents, parentslength, nextparents, nextlen)
    pytest_tocarry = [0, 1, 2, 3, -1, -1, 4, 5, 6, -1, -1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_3():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    nextlen = 0
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parentslength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, parents, parentslength, nextparents, nextlen)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    nextlen = 9
    nextparents = [0, 0, 0, 2, 2, 3, 4, 4, 4]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parentslength = 17
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5, 8, 11, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, parents, parentslength, nextparents, nextlen)
    pytest_tocarry = [0, 1, 2, -1, -1, -1, -1, -1, 3, 4, -1, 5, -1, -1, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_local_preparenext_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    nextlen = 10
    nextparents = [0, 0, 0, 1, 2, 2, 3, 4, 4, 4]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parentslength = 17
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5, 8, 11, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray_local_preparenext_64')
    ret_pass = funcC(tocarry, starts, parents, parentslength, nextparents, nextlen)
    pytest_tocarry = [0, 1, 2, -1, -1, 3, -1, -1, 4, 5, -1, 6, -1, -1, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

