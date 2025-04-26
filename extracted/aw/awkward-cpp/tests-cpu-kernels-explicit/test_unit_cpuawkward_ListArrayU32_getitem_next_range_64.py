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

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_1():
    tooffsets = [123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 0
    start = 0
    stop = 0
    step = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_2():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 0
    stop = 3
    step = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 2, 2, 3, 5, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_3():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 7
    stop = 0
    step = -1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 1, 1, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [1, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_4():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 0
    stop = 2
    step = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_5():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 3, 3, 5, 7, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 7, 9, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 6
    start = 0
    stop = 6
    step = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 2, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [0, 2, 3, 5, 7, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_6():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 3, 3, 5, 7, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 7, 9, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 6
    start = 2
    stop = 6
    step = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 1, 1, 1, 1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_7():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 3, 3, 5, 7, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 7, 9, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 6
    start = 6
    stop = 2
    step = -2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 0, 0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_8():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 3, 3, 5, 7, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 7, 9, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 6
    start = 0
    stop = 6
    step = -2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 0, 0, 0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_range_64_9():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_uint32*len(tooffsets))(*tooffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 7
    stop = 0
    step = -2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_range_64')
    ret_pass = funcC(tooffsets, tocarry, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_tooffsets = [0, 1, 1, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [1, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

