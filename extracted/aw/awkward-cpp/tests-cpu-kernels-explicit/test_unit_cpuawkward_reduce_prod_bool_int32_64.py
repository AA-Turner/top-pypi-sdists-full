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

def test_unit_cpuawkward_reduce_prod_bool_int32_64_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_2():
    toptr = [True, True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 0, 1, 1, 1, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_3():
    toptr = [True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 2
    parents = [0, 0, 0, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_4():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_5():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_6():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 2, 2, 2, 3, 0, 0, 4]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 4
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_7():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_8():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 25
    outlength = 6
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 1, 0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_9():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 15
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 1, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_10():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 22
    outlength = 6
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 0, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_11():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_12():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 19
    outlength = 5
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_13():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 0, 2, 0, 0, 2, 0, 4]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 10
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_14():
    toptr = [True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 2
    parents = [0, 0, 0, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_15():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_16():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 15
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 0, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_17():
    toptr = [True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 11
    outlength = 3
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_18():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 17
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_19():
    toptr = [True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 19
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_20():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 22
    outlength = 6
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_21():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_prod_bool_int32_64_22():
    toptr = [True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_int32*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_prod_bool_int32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

