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

def test_unit_cpuawkward_Index_nones_as_index_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_2():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 1
    toindex = [0]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_3():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 1
    toindex = [-1]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    toindex = [-1, -1, -1]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_5():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    toindex = [0, 1, 2, 3, 4]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_6():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    toindex = [0, -1, -1, 1, -1]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [0, 2, 3, 1, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_Index_nones_as_index_64_7():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 7
    toindex = [-1, 0, -1, -1, 1, -1, 2]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    funcC = getattr(lib, 'awkward_Index_nones_as_index_64')
    ret_pass = funcC(toindex, length)
    pytest_toindex = [3, 0, 4, 5, 1, 6, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

