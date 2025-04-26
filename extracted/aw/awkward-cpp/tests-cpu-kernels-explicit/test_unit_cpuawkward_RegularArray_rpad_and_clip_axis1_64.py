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

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 0
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [-1, -1, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    size = 0
    target = 0
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_3():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    size = 0
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_4():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    size = 2
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_5():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 2
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 2, 3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_6():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 2
    size = 3
    target = 3
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 2, 3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_7():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 3
    target = 3
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_8():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 3
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 3, 4, 6, 7]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_9():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    size = 5
    target = 2
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_10():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 2
    target = 1
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 2, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_rpad_and_clip_axis1_64_11():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    size = 3
    target = 1
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 3, 6]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

