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

def test_unit_cpuawkward_RegularArray_localindex_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_localindex_64_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_localindex_64_3():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 2
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_localindex_64_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 1, 2, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_localindex_64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_localindex_64')
    ret_pass = funcC(toindex, size, length)
    pytest_toindex = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

