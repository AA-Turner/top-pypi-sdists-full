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

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_2():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 15
    parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_3():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, 0, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 6
    parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_4():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [-1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_5():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, 1, 0, 0, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [8, 7, 6, 5, 4, 3, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 8
    parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [-8, -8, -8, -7, -8, -8, -8, -8]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_6():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, 1, 1, 1, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [-1, -2, -3, -4, -5, -6, -7, -8]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [1, 1, 1, 2, 2, 2, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_7():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, -1, -1, -1, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [-1, -2, -3, -4, -5, -6, -7, -8]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [1, 1, 1, -1, -1, -1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_8():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 1, 0, 0, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [-1, 1, 0, -5, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [1, 2, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_9():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 1, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [-1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 3
    parents = [0, 0, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [1, 2, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_10():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [-1, -1, -1, -1, -1, -1, -1]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [0, 1, 0, 2, 1, 0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 7
    parents = [0, 0, 0, 2, 2, 3, 6, 6, 6]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [-1, -1, -1, -1, -1, -1, -1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_11():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 1, 0, 0, 1, 1, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = [0, 1, 0, 2, 1, 0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 7
    parents = [0, 0, 0, 2, 2, 3, 6, 6, 6]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, parents, starts)
    pytest_toptr = [0, 1, 0, 0, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

