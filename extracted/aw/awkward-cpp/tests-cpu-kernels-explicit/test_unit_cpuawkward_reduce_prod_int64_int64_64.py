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

def test_unit_cpuawkward_reduce_prod_int64_int64_64_1():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 0, 0]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_2():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_3():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 12, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_4():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 31, 101, 3, 59, 37, 103, 5, 61, 41, 107, 7, 67, 43, 109, 11, 71, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 15
    parents = [0, 0, 10, 10, 1, 1, 11, 11, 2, 2, 12, 12, 3, 3, 13, 13, 4, 4, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 1, 1, 1, 1, 1, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_5():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 1, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_6():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 11, 71, 29, 97, 47]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 4, 4, 9, 9, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 43, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_7():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 14
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_8():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 29
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_9():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_10():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 47]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 29, 3131, 3811, 4387, 4687, 47]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_11():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 1
    outlength = 3
    parents = [2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_12():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 6
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [13710311357, 1, 907383479, 95041567, 1, 2310]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_13():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 103, 107, 109, 113, 73, 79, 83, 89, 97, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 13, 17, 19, 23, 29, 2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 6
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [13710311357, 4132280413, 907383479, 95041567, 2800733, 2310]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_14():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 4
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [13710311357, 907383479, 95041567, 2310]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_15():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 7, 17, 29, 3, 11, 19, 31, 5, 13, 23, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 6
    parents = [0, 0, 3, 3, 1, 1, 4, 4, 2, 2, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [14, 33, 65, 493, 589, 851]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_16():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [159, 295, 427, 67, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_17():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 29
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [159, 295, 427, 737, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_18():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 97, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [159, 295, 427, 737, 71, 949, 1343, 1577, 2047, 97, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_19():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [182, 33, 5, 1, 1, 1, 391, 19]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_20():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 3
    parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [210, 46189, 765049]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_21():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 6
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [2310, 1, 95041567, 907383479, 1, 13710311357]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_22():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 6
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [2310, 2800733, 95041567, 907383479, 4132280413, 13710311357]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_23():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 4
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [2310, 95041567, 907383479, 13710311357]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_24():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 7, 3, 11, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 8
    parents = [0, 6, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [2, 3, 5, 1, 1, 1, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_25():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [5, 53, 13, 73, 31, 101, 7, 59, 17, 79, 37, 103, 11, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 28
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [265, 413, 671, 67, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_26():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 8
    parents = [0, 0, 0, 3, 3, 3, 4, 4, 4, 7, 7, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 1, 1001, 7429, 1, 1, 33263]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_27():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 77, 13]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_28():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 77, 13, 323, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_29():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 8
    outlength = 5
    parents = [0, 0, 0, 2, 2, 3, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 77, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_30():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [6, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 7
    outlength = 5
    parents = [0, 0, 2, 2, 3, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 77, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_31():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 3
    parents = [0, 0, 0, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 1, 77]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_32():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_33():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 4
    parents = [0, 0, 0, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 7, 11, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_34():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 3
    parents = [0, 0, 0, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [30, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_35():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 31, 53, 2, 103, 37, 59, 3, 107, 41, 61, 5, 109, 43, 67, 7, 113, 47, 71, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 15
    parents = [0, 0, 10, 10, 1, 1, 11, 11, 2, 2, 12, 12, 3, 3, 13, 13, 4, 4, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [3131, 3811, 4387, 4687, 5311, 1, 1, 1, 1, 1, 106, 177, 305, 469, 781]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_36():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 31, 73, 13, 53, 2, 103, 37, 79, 17, 59, 3, 107, 41, 83, 19, 61, 5, 109, 43, 89, 23, 67, 7, 113, 47, 97, 29, 71, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [3131, 3811, 4387, 4687, 5311, 949, 1343, 1577, 2047, 2813, 106, 177, 305, 469, 781]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_37():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 11
    outlength = 12
    parents = [0, 0, 3, 9, 9, 1, 1, 10, 10, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, -1, 1, 1, 1, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_38():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 11
    outlength = 12
    parents = [0, 0, 6, 9, 9, 1, 1, 10, 10, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, -1, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_39():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 12
    parents = [0, 0, 9, 9, 1, 1, 10, 10, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, 1, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_40():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 8
    outlength = 12
    parents = [0, 0, 3, 9, 1, 1, 10, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, -1, 1, 1, 1, 1, 1, 29, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_41():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 8
    outlength = 12
    parents = [0, 0, 6, 9, 1, 1, 10, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, -1, 1, 1, 29, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_42():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 7
    outlength = 12
    parents = [0, 0, 9, 1, 1, 10, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, 1, 1, 1, 29, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_43():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 12
    parents = [0, 0, 6, 6, 9, 9, 1, 1, 10, 10, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, -39, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_44():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 12
    parents = [0, 0, 6, 6, 9, 1, 1, 10, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, 1, 1, 1, -39, 1, 1, 29, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_45():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 5, 23, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 12
    parents = [0, 0, 9, 9, 1, 1, 10, 10, 2, 2, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 115, 1, 1, 1, 1, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_46():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 12
    parents = [0, 0, 3, 3, 9, 9, 1, 1, 10, 10, 11, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, -39, 1, 1, 1, 1, 1, 203, 341, 481]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_47():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 12
    parents = [0, 0, 3, 3, 9, 1, 1, 10, 11]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 1, -39, 1, 1, 1, 1, 1, 29, 31, 37]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_48():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, 7, 23, 13, 29, 3, 19, 11, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 7
    parents = [0, 0, 3, 3, 6, 6, 1, 1, 4, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 5, 161, 11, 1, 377]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_49():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 17, 23, 7, 13, 3, 19, 11, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 10
    parents = [0, 0, 3, 6, 9, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [34, 57, 5, 23, 1, 1, 7, 11, 1, 13]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_50():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 11, 17, 7, 19, 3, 13, 23, 5]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 3, 3, 1, 1, 4, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [374, 39, 5, 133, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_51():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 73, 53, 31, 13, 2, 103, 79, 59, 37, 17, 3, 107, 83, 61, 41, 19, 5, 109, 89, 67, 43, 23, 7, 113, 97, 71, 47, 29, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 10
    parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [390769, 480083, 541741, 649967, 778231, 806, 1887, 3895, 6923, 14993]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_52():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 11, 23, 3, 13, 29, 5, 17, 31, 7, 19, 37]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 12
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [506, 1131, 2635, 4921]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_53():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [101, 53, 31, 2, 103, 59, 37, 3, 107, 61, 41, 5, 109, 67, 43, 7, 113, 71, 47, 11]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 10
    parents = [0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [5353, 6077, 6527, 7303, 8023, 62, 111, 205, 301, 517]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_54():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_55():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 31, 53, 101, 3, 37, 59, 103, 5, 41, 61, 107, 7, 43, 67, 109, 11, 47, 71, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 20
    outlength = 10
    parents = [0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [62, 111, 205, 301, 517, 5353, 6077, 6527, 7303, 8023]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_56():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 8
    outlength = 7
    parents = [0, 0, 1, 2, 3, 4, 5, 6]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [6, 5, 7, 11, 13, 17, 19]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_57():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 8
    outlength = 6
    parents = [0, 0, 1, 2, 3, 4, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [6, 5, 7, 11, 13, 323]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_58():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [720]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_int64_int64_64_59():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 13, 31, 53, 73, 101, 3, 17, 37, 59, 79, 103, 5, 19, 41, 61, 83, 107, 7, 23, 43, 67, 89, 109, 11, 29, 47, 71, 97, 113]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    lenparents = 30
    outlength = 10
    parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_int64_int64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [806, 1887, 3895, 6923, 14993, 390769, 480083, 541741, 649967, 778231]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

