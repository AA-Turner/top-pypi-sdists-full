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

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_1():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = []
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 0
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [0]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_2():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 1, 2, 3, 4, 5, 6, 7]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 1, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [0]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_3():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 2, 2, 3, 5]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [0]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_4():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 2, 2, 0, 2]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_5():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 0, 0, 0, 0]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_6():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 4, 6, 8, 10]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 4, 6, 8, 10, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_7():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 4, 6, 8, 10]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 4, 6, 8, 10, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_8():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [0, 2, 4, 6, 8, 10]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 4, 6, 8, 10, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_9():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [1, 1, 1, 1, 1, 1]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [2, 2, 2, 2, 2, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 4, 4, 4, 4, 4]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_subrange_equal_uint64_10():
    toequal = [True]
    toequal = (ctypes.c_bool*len(toequal))(*toequal)
    tmpptr = [1, 2, 3, 4, 5, 6]
    tmpptr = (ctypes.c_uint64*len(tmpptr))(*tmpptr)
    fromstarts = [2, 2, 2, 2, 2, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 4, 4, 4, 4, 4]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_NumpyArray_subrange_equal_uint64')
    ret_pass = funcC(tmpptr, fromstarts, fromstops, length, toequal)
    pytest_toequal = [1]
    assert toequal[:len(pytest_toequal)] == pytest.approx(pytest_toequal)
    assert not ret_pass.str

