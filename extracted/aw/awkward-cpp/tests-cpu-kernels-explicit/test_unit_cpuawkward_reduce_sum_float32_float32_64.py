# AUTO GENERATED ON 2026-07-02 AT 19:33:43
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

def test_unit_cpuawkward_reduce_sum_float32_float32_64_1():
    toptr = []
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_2():
    toptr = [123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_3():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0, 5, 20, 1, 6, 23, 29, 11, 27, 33]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_4():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [10, 0, 18, 13, 36, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_5():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 0, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_6():
    toptr = [123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [10, 35, 110]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_7():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 5, 10, 15, 20, 25, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [10, 35, 60, 85, 110, 135]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_8():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 3, 4, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 2, 3, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 3, 0, 15]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_9():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 5, 10, 15, 25, 1, 11, 16, 26, 2, 12, 17, 27, 8, 18, 28, 4, 9, 14, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 3, 5, 7, 8, 11, 13, 15, 17, 19, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 40, 12, 16, 40, 44, 26, 32, 23, 29]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_10():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_11():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 15, 5, 10, 25, 1, 16, 11, 26, 2, 17, 12, 27, 18, 8, 28, 4, 9, 14, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 7, 8, 9, 9, 9, 10, 11, 13, 15, 17, 18, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 15, 26, 16, 11, 26, 0, 0, 2, 17, 39, 26, 32, 9, 43]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_12():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 15, 5, 20, 10, 25, 1, 16, 6, 21, 11, 26, 2, 17, 7, 22, 12, 27, 3, 18, 8, 23, 13, 28, 4, 19, 9, 24, 14, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 25, 35, 17, 27, 37, 19, 29, 39, 21, 31, 41, 23, 33, 43]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_13():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 5, 10, 15, 20, 25, 1, 6, 11, 16, 21, 26, 2, 7, 12, 17, 22, 27, 3, 8, 13, 18, 23, 28, 4, 9, 14, 19, 24, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 60, 18, 63, 21, 66, 24, 69, 27, 72]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_14():
    toptr = [123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 4, 8, 16, 32, 64, 128, 0, 0, 0, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 4, 8, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 240, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_15():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [15, 15]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_16():
    toptr = [123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [21]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_17():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [22, 40, 3, 0, 0, 0, 30, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_18():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 16, 0, 2, 32, 0, 4, 64, 0, 8, 128, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [17, 34, 68, 136]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_19():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [3, 0, 7, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_20():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 4, 1, 3, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 2, 5, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [4, 9, 0, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_21():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 4, 9, 16, 25, 1, 4, 9, 16, 25]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [55, 55]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_22():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 4, 9, 16, 26, 1, 4, 10, 16, 24]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [56, 55]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_23():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 2, 4, 6, 8, 10, 11, 12, 13, 14, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [5, 21, 27, 9, 25, 8, 23, 4, 9, 24]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_24():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 6, 9, 12, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [60, 63, 66, 69, 72]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_25():
    toptr = [123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_26():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 25, 26, 27, 28, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 4, 7, 11, 15, 15, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [7, 22, 47, 66, 0, 135]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_27():
    toptr = [123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [2, 2, 4, 5, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [8, 0, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_28():
    toptr = [123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [85, 110, 135]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_29():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [4, 1, 0, 1, 4, 5, 1, 0, 1, 3]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [10, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_float32_float32_64_30():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [4, 1, 0, 1, 4, 4, 1, 0, 1, 4]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [10, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

