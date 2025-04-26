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

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = []
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 0
    target = 0
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_2():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [0, 0]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 1
    target = 2
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [-1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [1, 3]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 1
    target = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [1, 2, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [0, 1, 2, 3, 5, 7, 11]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 6
    target = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [0, -1, -1, 1, -1, -1, 2, -1, -1, 3, 4, -1, 5, 6, -1, 7, 8, 9, 10]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [0, 1, 2, 3, 5, 7, 11]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 6
    target = 2
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [0, -1, 1, -1, 2, -1, 3, 4, 5, 6, 7, 8, 9, 10]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_6():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [0, 1, 2, 3, 5, 7, 11]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 6
    target = 1
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_rpad_axis1_64_7():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromoffsets = [0, 1, 2, 3, 4]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    fromlength = 4
    target = 0
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromoffsets, fromlength, target)
    pytest_toindex = [0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

