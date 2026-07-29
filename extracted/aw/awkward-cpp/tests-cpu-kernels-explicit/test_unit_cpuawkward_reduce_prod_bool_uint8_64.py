# AUTO GENERATED ON 2026-07-28 AT 17:37:39
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

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_2():
    toptr = [True, True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, False, False, 1, 1, 1, False, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_3():
    toptr = [True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_4():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, False, 1, False, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_5():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, False, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_6():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 2, 2, 2, 3, 0, 0, 4]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, False, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_7():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_8():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 6, 10, 15, 21, 25]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, 1, False, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_9():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 6, 9, 12, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [False, 1, 1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_10():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 6, 11, 15, 19, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False, False, 1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_11():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_12():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 5, 8, 11, 14, 19]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False, False, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_13():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 0, 2, 0, 0, 2, 0, 4]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_14():
    toptr = [True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_15():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, False]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_16():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 6, 9, 12, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, False, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_17():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 6, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_18():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 6, 10, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_19():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 8, 12, 16, 19]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_20():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 6, 11, 15, 19, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_21():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_uint8_64_22():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

