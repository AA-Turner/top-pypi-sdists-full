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

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_1():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    assert funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen).str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_2():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 3, 5]
    pytest_tocarry = [1, 0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_3():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 3, 5]
    pytest_tocarry = [0, 0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_4():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 2
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_5():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 1
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_6():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 1
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_7():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 2
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_8():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    assert funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen).str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_9():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 10
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [1, 0, 0, 0, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_apply_64_10():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceindex = (ctypes.c_int64*len(sliceindex))(*sliceindex)
    sliceinnerlen = 5
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    contentlen = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_apply_64')
    ret_pass = funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    pytest_tocarry = [0, 0, 0, 0, 0, 0]
    assert not ret_pass.str

