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

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 0
    missing = []
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = []
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = []
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_2():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 1
    missing = [0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 4]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 4]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_3():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 2
    missing = [0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 2]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 2, 2]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_4():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 3
    missing = [0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 2, 4]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 2, 2, 4]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_5():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 3
    missing = [-1, 0, -1, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 2, 4]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 1, 1, 2]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_6():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 4
    missing = [-1, -1, -1, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 3, 3, 4]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 0, 0, 0, 0]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_7():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 4
    missing = [0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 3, 3, 4]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 2, 3, 3, 4]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_shrink_64_8():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tolargeoffsets = [123, 123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    tosmalloffsets = [123, 123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    length = 4
    missing = [0, 0, 0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tolargeoffsets = [0, 2, 3, 3, 6]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)
    pytest_tosmalloffsets = [0, 2, 3, 3, 6]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    assert not ret_pass.str

