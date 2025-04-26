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

def test_unit_cpuawkward_IndexedArray_fill_to64_count_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    base = 0
    length = 0
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_fill_to64_count_2():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    base = 0
    length = 5
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_fill_to64_count_3():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    base = 0
    length = 3
    toindexoffset = 3
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [123, 123, 123, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_fill_to64_count_4():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    base = 3
    length = 4
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [3, 4, 5, 6]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_fill_to64_count_5():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    base = 3
    length = 5
    toindexoffset = 2
    funcC = getattr(lib, 'awkward_IndexedArray_fill_to64_count')
    ret_pass = funcC(toindex, toindexoffset, length, base)
    pytest_toindex = [123, 123, 3, 4, 5, 6, 7]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

