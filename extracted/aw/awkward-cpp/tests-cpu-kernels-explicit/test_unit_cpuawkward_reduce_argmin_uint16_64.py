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

def test_unit_cpuawkward_reduce_argmin_uint16_64_1():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 0, 4, 4, 6]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_2():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_3():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_4():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_5():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 6]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_6():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 1, 3, 2, 1]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 3
    parents = [0, 0, 1, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 2, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_7():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 2, 1, 0, 1, 0]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 1, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_8():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 0, 2, 1, 1, 0]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [1, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_9():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 4, 2, 2, 2, 1, 6, 1, 4, 1, 3, 3, 4, 6, 6]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 15
    outlength = 5
    parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [2, 5, 7, 9, 12]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_10():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [6, 3, 2, 1, 2]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_11():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 15
    outlength = 3
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [3, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_12():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 2, 2, 2, 3, 3]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 18
    outlength = 6
    parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 10, 16, 5, 13, 17]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_13():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3, 999]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 22
    outlength = 8
    parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 10, 17, -1, 5, 14, 20, 21]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_uint16_64_14():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3]
    fromptr = (ctypes.c_uint16*len(fromptr))(*fromptr)
    lenparents = 21
    outlength = 6
    parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 4, 2, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_argmin_uint16_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength)
    pytest_toptr = [0, 10, 17, 5, 14, 20]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

