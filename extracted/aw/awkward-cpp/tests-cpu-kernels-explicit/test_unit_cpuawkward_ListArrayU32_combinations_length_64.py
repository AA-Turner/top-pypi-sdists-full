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

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_1():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 0
    n = 0
    replacement = False
    starts = []
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = []
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_2():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 5
    n = 3
    replacement = False
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 4, 4, 5, 5, 15]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [15]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_3():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 1
    n = 2
    replacement = False
    starts = [0]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [1]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_4():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 1
    n = 2
    replacement = False
    starts = [0]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [2]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [1]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_5():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 5
    n = 2
    replacement = False
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 6, 6, 9, 9, 19]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [19]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_6():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 5
    n = 2
    replacement = True
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 10, 10, 16, 17, 32]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [32]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_7():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 3
    n = 2
    replacement = False
    starts = [0, 3, 3]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [3, 3, 5]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 3, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_8():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 3
    n = 2
    replacement = False
    starts = [0, 3, 5]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [3, 3, 7]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 3, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_9():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 5
    n = 3
    replacement = True
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 20, 20, 30, 31, 66]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [66]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_combinations_length_64_10():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    length = 5
    n = 2
    replacement = False
    starts = [0, 3, 3, 10, 10]
    starts = (ctypes.c_uint32*len(starts))(*starts)
    stops = [3, 3, 5, 10, 13]
    stops = (ctypes.c_uint32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArrayU32_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_tooffsets = [0, 3, 3, 4, 4, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_totallen = [7]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    assert not ret_pass.str

