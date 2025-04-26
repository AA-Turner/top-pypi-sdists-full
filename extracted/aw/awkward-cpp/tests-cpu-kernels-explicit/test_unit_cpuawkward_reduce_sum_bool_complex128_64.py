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

def test_unit_cpuawkward_reduce_sum_bool_complex128_64_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_complex128_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_complex128_64_2():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    lenparents = 1
    outlength = 1
    parents = [0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_complex128_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_complex128_64_3():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_complex128_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_complex128_64_4():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_complex128_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_sum_bool_complex128_64_5():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_sum_bool_complex128_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

