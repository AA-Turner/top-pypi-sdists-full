# AUTO GENERATED ON 2026-08-14 AT 14:44:29
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

def test_unit_cpuawkward_reduce_sum_bool_int8_64_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_2():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_3():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False, False, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_4():
    toptr = [True, True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, False, False, False, False, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_5():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_6():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 0, 2, 0, 0, 0, 0, 0]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_7():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 2, 2, 0, 3, 0, 0, 0]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_8():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_int8_64_9():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_int8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_int8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

