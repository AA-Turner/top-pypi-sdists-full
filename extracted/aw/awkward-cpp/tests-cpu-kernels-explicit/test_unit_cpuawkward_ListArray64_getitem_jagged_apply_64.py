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

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 0
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = []
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 0
    sliceouterlen = 0
    slicestarts = []
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = []
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_2():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 0
    fromstarts = [0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [0, 0, 0, 0]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = []
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 0
    sliceouterlen = 4
    slicestarts = [0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 0, 0]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_3():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = []
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 0
    sliceouterlen = 3
    slicestarts = [0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 0]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_4():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 2
    sliceouterlen = 3
    slicestarts = [0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 0, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_5():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 3
    sliceouterlen = 3
    slicestarts = [0, 1, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 1, 1, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_6():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 3
    sliceouterlen = 3
    slicestarts = [0, 1, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 1, 1, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_7():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 10
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [1, 0, 1, 0, 3]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    sliceouterlen = 5
    slicestarts = [0, 1, 1, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [1, 3, 4, 6, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 1, 1, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_8():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 2
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_9():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 4
    fromstarts = [0, 1, 1, 1, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 4]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 0, 2, 1, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 6
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2, 2, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 0, 3, 2, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 2, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_10():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 3
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_11():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 3
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_12():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 3
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 0, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_13():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 2, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 4
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_14():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 9
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 2, 0, 1, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 8
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 2, 3, 4, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 4, 5, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_15():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 9
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [1, 2, 0, 1, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 8
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 2, 2, 4, 5, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_16():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 9
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 2, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 7
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 3, 4]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 3, 4, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 3, 3, 4, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 9
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 2, 1, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 8
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 2, 4, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 3, 4, 5, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_18():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 2, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    sliceouterlen = 3
    slicestarts = [0, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_19():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 5
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 1, 0, 0, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    sliceouterlen = 3
    slicestarts = [0, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 1, 0, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_20():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 9
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [0, 1, 2, 0, 1, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 9
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 5, 6]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5, 6, 9]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 3, 5, 6, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_21():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 6
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 1, 0, 2, 1, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 6
    sliceouterlen = 2
    slicestarts = [0, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 1, 0, 5, 4, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_22():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 6
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 1, 1, 0, 1, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 6
    sliceouterlen = 3
    slicestarts = [0, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 4, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 1, 1, 0, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 4, 4, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_23():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 6
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [2, 1, 1, 0, 1, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 6
    sliceouterlen = 3
    slicestarts = [0, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 5, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [2, 1, 1, 0, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_24():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 8
    fromstarts = [0, 4, 7]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 7, 8]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [3, 2, 2, 1, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 6
    sliceouterlen = 3
    slicestarts = [0, 4, 6]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 6, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [3, 2, 2, 1, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 4, 6, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_jagged_apply_64_25():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    contentlen = 13
    fromstarts = [0, 4, 4, 7, 8]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 4, 7, 8, 13]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    sliceindex = [3, 2, 1, 1, 0, 1, 0, 0, 1, 2]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 10
    sliceouterlen = 5
    slicestarts = [0, 5, 5, 6, 8]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [5, 5, 6, 8, 10]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tocarry = [3, 2, 1, 1, 0, 5, 7, 7, 9, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tooffsets = [0, 5, 5, 6, 8, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

