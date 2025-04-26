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

def test_cpuawkward_ListArray64_combinations_length_64_1():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [9]
    pytest_tooffsets = [0, 1, 5, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_2():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [139.0]
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_3():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_4():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [4]
    pytest_tooffsets = [0, 0, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_5():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [3]
    pytest_tooffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_6():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = False
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_7():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = False
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [49.0]
    pytest_tooffsets = [0, 35.0, 39.0, 49.0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_8():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = False
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_9():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = False
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_10():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = False
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_11():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [9]
    pytest_tooffsets = [0, 1, 5, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_12():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [139.0]
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_13():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_14():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [4]
    pytest_tooffsets = [0, 0, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_15():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [3]
    pytest_tooffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_16():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [9]
    pytest_tooffsets = [0, 1, 5, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_17():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [139.0]
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_18():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_19():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [4]
    pytest_tooffsets = [0, 0, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_20():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [3]
    pytest_tooffsets = [0, 1, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_21():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [9]
    pytest_tooffsets = [0, 1, 5, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_22():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [139.0]
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_23():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [0]
    pytest_tooffsets = [0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_24():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [4]
    pytest_tooffsets = [0, 0, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_combinations_length_64_25():
    totallen = [123]
    totallen = (ctypes.c_int64*len(totallen))(*totallen)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_combinations_length_64')
    ret_pass = funcC(totallen, tooffsets, n, replacement, starts, stops, length)
    pytest_totallen = [3]
    pytest_tooffsets = [0, 1, 2, 3]
    assert not ret_pass.str

