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

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_1():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    pytest_tosmalloffsets = [2, 3, 5, 7]
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_2():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    pytest_tosmalloffsets = [2, 3, 5, 7]
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_3():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    pytest_tosmalloffsets = [2, 3, 5, 7]
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_4():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    pytest_tosmalloffsets = [2, 3, 5, 7]
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_5():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    pytest_tosmalloffsets = [2, 3, 5, 7]
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tosmalloffsets = [1, 8, 12, 17]
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tosmalloffsets = [1, 8, 12, 17]
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tosmalloffsets = [1, 8, 12, 17]
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tosmalloffsets = [1, 8, 12, 17]
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tosmalloffsets = [1, 8, 12, 17]
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_11():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [7, 8]
    pytest_tosmalloffsets = [1, 1, 3, 3]
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_12():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [7, 8]
    pytest_tosmalloffsets = [1, 1, 3, 3]
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_13():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [7, 8]
    pytest_tosmalloffsets = [1, 1, 3, 3]
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_14():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [7, 8]
    pytest_tosmalloffsets = [1, 1, 3, 3]
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_15():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [7, 8]
    pytest_tosmalloffsets = [1, 1, 3, 3]
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_16():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 0, 0]
    pytest_tosmalloffsets = [0, 1, 2, 3]
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_17():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 0, 0]
    pytest_tosmalloffsets = [0, 1, 2, 3]
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_18():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 0, 0]
    pytest_tosmalloffsets = [0, 1, 2, 3]
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_19():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 0, 0]
    pytest_tosmalloffsets = [0, 1, 2, 3]
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_shrink_64_20():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    tosmalloffsets = [123, 123, 123, 123]
    tosmalloffsets = (ctypes.c_int64*len(tosmalloffsets))(*tosmalloffsets)
    tolargeoffsets = [123, 123, 123, 123]
    tolargeoffsets = (ctypes.c_int64*len(tolargeoffsets))(*tolargeoffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    missing = (ctypes.c_int64*len(missing))(*missing)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_shrink_64')
    ret_pass = funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)
    pytest_tocarry = [0, 0, 0]
    pytest_tosmalloffsets = [0, 1, 2, 3]
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert not ret_pass.str

