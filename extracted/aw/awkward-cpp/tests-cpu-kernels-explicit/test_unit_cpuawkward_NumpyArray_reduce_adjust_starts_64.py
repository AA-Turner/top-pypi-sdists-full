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

def test_unit_cpuawkward_NumpyArray_reduce_adjust_starts_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
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
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14]
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
    offsets = [0, 5, 8, 9, 14, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
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
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
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
    offsets = [0, 5, 8, 9, 9, 14, 18, 21, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [-8, -7, -6, -4, -4, -3, -2, -1]
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
    offsets = [0, 3, 5, 5, 5, 5, 5, 7, 8]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [1, 2, 3, 5, 6, 7, 7, 8]
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
    offsets = [0, 3, 5, 5, 5, 5, 5, 7, 8]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [1, 2, 3, -1, -1, -1, 7, 8]
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
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [1, 0, 0, 5, -2, -3]
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
    offsets = [0, 2, 2, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [1, 1, -1]
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
    offsets = [0, 3, 3, 5, 6, 6, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
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
    offsets = [0, 3, 3, 5, 6, 6, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_adjust_starts_64')
    ret_pass = funcC(toptr, outlength, offsets, starts)
    pytest_toptr = [0, 0, 0, -2, 0, 1, -3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

