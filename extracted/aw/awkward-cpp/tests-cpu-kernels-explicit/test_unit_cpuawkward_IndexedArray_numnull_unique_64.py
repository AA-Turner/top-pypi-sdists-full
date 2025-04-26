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

def test_unit_cpuawkward_IndexedArray_numnull_unique_64_1():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray_numnull_unique_64')
    ret_pass = funcC(toindex, lenindex)
    pytest_toindex = [0, 1, 2, 3, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_numnull_unique_64_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray_numnull_unique_64')
    ret_pass = funcC(toindex, lenindex)
    pytest_toindex = [0, 1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_numnull_unique_64_3():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    lenindex = 0
    funcC = getattr(lib, 'awkward_IndexedArray_numnull_unique_64')
    ret_pass = funcC(toindex, lenindex)
    pytest_toindex = [-1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_numnull_unique_64_4():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray_numnull_unique_64')
    ret_pass = funcC(toindex, lenindex)
    pytest_toindex = [0, 1, 2, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_numnull_unique_64_5():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray_numnull_unique_64')
    ret_pass = funcC(toindex, lenindex)
    pytest_toindex = [0, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

