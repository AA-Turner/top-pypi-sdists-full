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

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_1():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_2():
    toptr = []
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_3():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0, 1, 12, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_4():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 31, 101, 3, 59, 37, 103, 5, 61, 41, 107, 7, 67, 43, 109, 11, 71, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 12, 14, 16, 18, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 3131, 177, 3811, 305, 1, 1, 1, 1, 1, 4387, 469, 4687, 781, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_5():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 18, 20, 22, 24, 26, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 1, 469, 2047, 4687, 781, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_6():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 11, 71, 29, 97, 47]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 27, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 473, 2059, 97, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_7():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 14
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_8():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 29]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_9():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_10():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 47]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 7, 1541, 3827, 1199, 2059, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_11():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 0, 0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_12():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 7, 17, 29, 3, 11, 19, 31, 5, 13, 23, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 2, 4, 6, 8, 10, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [14, 493, 33, 589, 65, 851]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_13():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [159, 949, 3131, 5, 59, 1343, 3811, 427, 1577, 4387, 1541, 3827, 7739, 2813, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_14():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [159, 949, 3131, 295, 17, 2923, 721, 1159, 3403, 1177, 1541, 3827, 7739, 2813, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_15():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 97, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [159, 949, 3131, 295, 17, 2923, 721, 1159, 3403, 107, 737, 2047, 4687, 6887, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_16():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [182, 391, 3, 1, 1, 1, 209, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_17():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 4, 8, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [210, 46189, 765049]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_18():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 7, 3, 11, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 1, 2, 3, 3, 3, 3, 4, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [2, 7, 3, 1, 1, 1, 11, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_19():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [5, 53, 13, 73, 31, 101, 7, 59, 17, 79, 37, 103, 11, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [265, 949, 3131, 7, 59, 1343, 3811, 671, 1577, 4387, 1541, 3827, 7739, 2813, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_20():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 8
    offsets = [0, 3, 3, 3, 6, 9, 9, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 1, 1001, 7429, 1, 1, 33263]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_21():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 77, 13]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_22():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 77, 13, 323, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_23():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 3, 5, 6, 8]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 77, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_24():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [6, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 2, 2, 4, 5, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 77, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_25():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 1, 77]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_26():
    toptr = [123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_27():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 4, 5, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 7, 11, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_28():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 3
    offsets = [0, 3, 4, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [30, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_29():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [101, 31, 53, 2, 103, 37, 59, 3, 107, 41, 61, 5, 109, 43, 67, 7, 113, 47, 71, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 12, 14, 16, 18, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [3131, 106, 3811, 177, 4387, 1, 1, 1, 1, 1, 305, 4687, 469, 5311, 781]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_30():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [101, 31, 73, 13, 53, 2, 103, 37, 79, 17, 59, 3, 107, 41, 83, 19, 61, 5, 109, 43, 89, 23, 67, 7, 113, 47, 97, 29, 71, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [3131, 949, 106, 3811, 1343, 177, 4387, 1577, 305, 4687, 2047, 469, 5311, 2813, 781]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_31():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 12
    offsets = [0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 6, 8, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [34, 203, 1, 1, 1, 1, 1, 1, 1, 57, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_32():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 17, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 12
    offsets = [0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [34, 87, 1, 1, 1, 1, 1, 1, 1, 19, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_33():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 5, 23, 13, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 12
    offsets = [0, 2, 4, 6, 6, 6, 6, 6, 6, 6, 8, 10, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [34, 203, 57, 1, 1, 1, 1, 1, 1, 341, 115, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_34():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 23, 13, 29, 3, 19, 11, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 7
    offsets = [0, 2, 4, 5, 7, 8, 8, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [34, 161, 13, 87, 19, 1, 55]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_35():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 17, 23, 7, 13, 3, 19, 11, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 2, 4, 5, 6, 6, 6, 7, 8, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [34, 161, 13, 3, 1, 1, 19, 11, 1, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_36():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 11, 17, 7, 19, 3, 13, 23, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 5
    offsets = [0, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [374, 133, 3, 299, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_37():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [101, 73, 53, 31, 13, 2, 103, 79, 59, 37, 17, 3, 107, 83, 61, 41, 19, 5, 109, 89, 67, 43, 23, 7, 113, 97, 71, 47, 29, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [390769, 806, 480083, 1887, 541741, 3895, 649967, 6923, 778231, 14993]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_38():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 11, 23, 3, 13, 29, 5, 17, 31, 7, 19, 37]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [506, 1131, 2635, 4921]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_39():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [101, 53, 31, 2, 103, 59, 37, 3, 107, 61, 41, 5, 109, 67, 43, 7, 113, 71, 47, 11]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [5353, 62, 6077, 111, 6527, 205, 7303, 301, 8023, 517]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_40():
    toptr = [123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_41():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 31, 53, 101, 3, 37, 59, 103, 5, 41, 61, 107, 7, 43, 67, 109, 11, 47, 71, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [62, 5353, 111, 6077, 205, 6527, 301, 7303, 517, 8023]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_42():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 7
    offsets = [0, 2, 3, 4, 5, 6, 7, 8]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [6, 5, 7, 11, 13, 17, 19]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_43():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 2, 3, 4, 5, 6, 8]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [6, 5, 7, 11, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_44():
    toptr = [123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [720]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_uint32_uint8_64_45():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint32*len(toptr))(*toptr)
    fromptr = [2, 13, 31, 53, 73, 101, 3, 17, 37, 59, 79, 103, 5, 19, 41, 61, 83, 107, 7, 23, 43, 67, 89, 109, 11, 29, 47, 71, 97, 113]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    outlength = 10
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_prod_uint32_uint8_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [806, 390769, 1887, 480083, 3895, 541741, 6923, 649967, 14993, 778231]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

