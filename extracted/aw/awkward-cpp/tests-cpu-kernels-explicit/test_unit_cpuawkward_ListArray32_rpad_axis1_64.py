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

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = []
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = []
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = []
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 0
    target = 4
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = []
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = []
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = []
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = []
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = []
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 0
    target = 0
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = []
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = []
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 0
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, 4, 5, 5, 6, 7, 8, 123, 123]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 3, 5, 8]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 3, 5, 8, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 4
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, -1, -1, -1, -1, -1, 4, 5, -1, -1, 5, 6, 7, -1, 8, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 8, 12, 16]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 8, 12, 16, 20]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, -1, -1, -1, 4, 5, -1, 5, 6, 7, 8, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6, 9, 12]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9, 12, 15]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_6():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 7]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    target = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, -1, -1, -1, 5, 6, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_7():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 2
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, -1, -1, 4, 5, 5, 6, 7, 8, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 5, 7, 10]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 5, 7, 10, 12]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_8():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 1
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, 1, 2, -1, 4, 5, 5, 6, 7, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 4, 6, 9]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 4, 6, 9, 10]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_9():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 4
    target = 4
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, -1, -1, -1, 3, 4, -1, -1, 0, 1, 2, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 8, 12]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 8, 12, 16]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_10():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 4
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, -1, -1, -1, 3, 4, -1, -1, -1, -1, -1, -1, 0, 1, 2, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 8, 12, 16]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 8, 12, 16, 20]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_11():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 4
    target = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, -1, -1, 3, 4, -1, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 7, 10]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 7, 10, 13]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_12():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, -1, -1, 3, 4, -1, -1, -1, -1, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 7, 10, 13]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 7, 10, 13, 16]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_13():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    target = 2
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, -1, 3, 4, -1, -1, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 6, 8, 10]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 6, 8, 10, 13]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_rpad_axis1_64_14():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tostarts = [123, 123, 123, 123]
    tostarts = (ctypes.c_int32*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123]
    tostops = (ctypes.c_int32*len(tostops))(*tostops)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 4
    target = 1
    funcC = getattr(lib, 'awkward_ListArray32_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 4, 5, 7]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [4, 5, 7, 10]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

