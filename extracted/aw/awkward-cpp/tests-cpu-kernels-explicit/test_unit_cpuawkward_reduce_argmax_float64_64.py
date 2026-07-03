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

def test_unit_cpuawkward_reduce_argmax_float64_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 0
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_2():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, -1, 1, -1, 1, 21]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 1, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 1, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 2, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_3():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6, 7]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 1, 3, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 1, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 2, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_4():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [6, 1, 10, 33, -1, 21, 2, 45, 4]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, 2, 4, 5, 7]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 4, 5, 7, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 3, 4, 5, 7]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_5():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 2, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 2, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_6():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, 3, 6, 9, 11]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 6, 9, 11, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 5, 6, 10, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_7():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_8():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_9():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 5, 9]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 8, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_10():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 0, 4, 4, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_11():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_float64_64_12():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_double*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_float64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

