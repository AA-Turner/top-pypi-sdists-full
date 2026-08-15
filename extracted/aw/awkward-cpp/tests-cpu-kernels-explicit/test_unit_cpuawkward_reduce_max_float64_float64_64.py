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

def test_unit_cpuawkward_reduce_max_float64_float64_64_1():
    toptr = []
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_2():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [13, 23, 3, -9223372036854775808, -9223372036854775808, -9223372036854775808, 19, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_3():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [0, 1, 3, 4, 5, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 4
    offsets = [0, 2, 3, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [1, 3, -9223372036854775808, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_4():
    toptr = [123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_5():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [0, 4, 1, 3, 5, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 4
    offsets = [0, 2, 5, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [4, 5, -9223372036854775808, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_6():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 2, 5, 3, 3, 5, 1, 4, 2]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 5
    offsets = [0, 3, 5, 7, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 3, 5, 4, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_7():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = 4
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 4, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_8():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 3, 6, 4, 2, 2, 3, 1, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = 4
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [6, 4, 4, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_9():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 3, 2, 5, 3, 7, 3, 1, 5, 8, 1, 9, 4, 2, 7, 10, 2, 4, 7, 2]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 5
    offsets = [0, 4, 8, 12, 16, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 7, 9, 10, 7]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_10():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 3, 7, 8, 2, 4, 2, 3, 1, 7, 7, 5, 1, 9, 10, 2]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 4
    offsets = [0, 5, 10, 15, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 8, 7, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_11():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, -9223372036854775808, 11, 13, 19, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_12():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, -9223372036854775808, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float64_float64_64_13():
    toptr = [123.0]
    toptr = (ctypes.c_double*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_float64_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

