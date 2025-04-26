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

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_1():
    tostarts = []
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = []
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 0
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = []
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = []
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_2():
    tostarts = [123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 4
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 1, 2, 3]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [1, 2, 3, 4]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_3():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 5
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 1, 2, 3, 4]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [1, 2, 3, 4, 5]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_4():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 6
    target = 1
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 1, 2, 3, 4, 5]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [1, 2, 3, 4, 5, 6]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_5():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 3
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 2, 4]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 4, 6]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_6():
    tostarts = [123, 123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 7
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 2, 4, 6, 8, 10, 12]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 4, 6, 8, 10, 12, 14]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_7():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 6
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 2, 4, 6, 8, 10]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 4, 6, 8, 10, 12]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_8():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 5
    target = 2
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 2, 4, 6, 8]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 4, 6, 8, 10]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_9():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 6
    target = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 3, 6, 9, 12, 15]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9, 12, 15, 18]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_10():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 5
    target = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 3, 6, 9, 12]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9, 12, 15]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_11():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 6
    target = 4
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 4, 8, 12, 16, 20]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 8, 12, 16, 20, 24]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_12():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 5
    target = 4
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 4, 8, 12, 16]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 8, 12, 16, 20]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_13():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 6
    target = 5
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 5, 10, 15, 20, 25]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [5, 10, 15, 20, 25, 30]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_index_rpad_and_clip_axis1_64_14():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    length = 5
    target = 5
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 5, 10, 15, 20]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [5, 10, 15, 20, 25]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

