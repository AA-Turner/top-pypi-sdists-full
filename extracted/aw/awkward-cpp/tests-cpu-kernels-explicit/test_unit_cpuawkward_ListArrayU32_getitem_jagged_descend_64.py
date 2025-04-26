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

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_1():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 0
    slicestarts = []
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = []
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_2():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 1
    slicestarts = [0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_3():
    tooffsets = []
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 2
    slicestarts = [0, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str.decode('utf-8') == "jagged slice inner length differs from array inner length"

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_4():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 2
    slicestarts = [0, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 2, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_5():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 4, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 4
    slicestarts = [0, 3, 3, 4]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 4, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 3, 3, 4, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_6():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 3
    slicestarts = [0, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_jagged_descend_64_7():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    sliceouterlen = 2
    slicestarts = [0, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

