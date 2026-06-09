# AUTO GENERATED ON 2026-06-08 AT 11:28:09
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

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = []
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_2():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [0, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_3():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1, 0, 0, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_4():
    toptr = [True, True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1, 0, 1, 0, 0, 0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_5():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_6():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 0, 2, 0, 0, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_7():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 2, 2, 0, 3, 0, 0, 0]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_8():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_uint8_64_9():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

