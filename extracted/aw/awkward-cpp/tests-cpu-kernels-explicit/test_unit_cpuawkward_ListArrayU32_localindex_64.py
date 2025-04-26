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

def test_unit_cpuawkward_ListArrayU32_localindex_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    offsets = [0]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_2():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 1
    offsets = [0, 1]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_3():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    offsets = [0, 2, 3, 5]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 0, 0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_4():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 4
    offsets = [0, 2, 3, 3, 6]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 0, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 2
    offsets = [0, 2, 3]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_6():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 1
    offsets = [0, 2]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_7():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 4
    offsets = [0, 3, 3, 4, 5]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_8():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 7
    offsets = [0, 3, 3, 5, 6, 10, 10, 13]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_9():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    offsets = [0, 3, 3, 5, 6, 10]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_10():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    offsets = [0, 3, 3, 5, 6, 6, 10]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_11():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_localindex_64_12():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    offsets = [0, 4, 4, 7, 8, 13]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListArrayU32_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 2, 3, 0, 1, 2, 0, 0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

