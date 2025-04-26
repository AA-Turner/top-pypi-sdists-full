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

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_1():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 0
    missing = []
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 0
    slicestarts = []
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = []
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [0]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_2():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [4]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_3():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, -1, 0, -1, 0, -1, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 7
    slicestarts = [0, 2, 3, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [4]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_4():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 0, 0]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [0]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_5():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, -1, 0, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 2, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [1]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_6():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, -1, 0, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 1, 2, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 2, 3, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [2]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_7():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [0, -1, 0, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 2, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [1]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_8():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [-1, -1, -1, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [0]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_9():
    numvalid = [123]
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 4
    missing = [-1, -1, -1, -1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 4
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    ret_pass = funcC(numvalid, slicestarts, slicestops, length, missing, missinglength)
    pytest_numvalid = [0]
    assert numvalid[:len(pytest_numvalid)] == pytest.approx(pytest_numvalid)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_10():
    numvalid = []
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 2
    missing = [0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 2
    slicestarts = [4, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    assert funcC(numvalid, slicestarts, slicestops, length, missing, missinglength).str.decode('utf-8') == "jagged slice's stops[i] < starts[i]"

def test_unit_cpuawkward_ListArray_getitem_jagged_numvalid_64_11():
    numvalid = []
    numvalid = (ctypes.c_int64*len(numvalid))(*numvalid)
    length = 2
    missing = [0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    missinglength = 1
    slicestarts = [0, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_numvalid_64')
    assert funcC(numvalid, slicestarts, slicestops, length, missing, missinglength).str.decode('utf-8') == "jagged slice's offsets extend beyond its content"

