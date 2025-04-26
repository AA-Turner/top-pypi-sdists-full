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

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 0
    target = 0
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_2():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 2
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_3():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    target = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_5():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    target = 4
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_6():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    target = 5
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_7():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    target = 6
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2, 3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_8():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    target = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_9():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    target = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_10():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_11():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 3
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_12():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 5
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis0_64_13():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    length = 6
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis0_64')
    ret_pass = funcC(toindex, target, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

