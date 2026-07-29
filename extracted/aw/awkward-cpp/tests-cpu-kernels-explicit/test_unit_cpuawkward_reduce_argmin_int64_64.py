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

def test_unit_cpuawkward_reduce_argmin_int64_64_1():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 0, 4, 4, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_2():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 0
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_3():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_4():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_5():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_6():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 4, 2, 6, 3, 0, -10]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 4
    starts = [0, 3, 5, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 5, 6, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 4, 5, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_7():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 1, 3, 4, 6, 6, -4, -6, -7]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, -1, 3, 5, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 3, 5, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, -1, 3, 5, 8]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_8():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 1, 3, -4, -6, -7]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, -1, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, -1, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_9():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 1, 3, 2, 1]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 2, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_10():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 2, 1, 0, 1, 0]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 2, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_11():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 0, 2, 1, 1, 0]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_12():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, -3, 4, 4, 2, 2, 2, 2, 2, -2, 1, 1, 6, -6, 1, 1, 4, 4, 1, 1, 3, -3, 3, 3, 4, 4, 6, 6, 6, -6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 15
    starts = [0, 6, 12, 18, 24, 2, 8, 14, 20, 26, 4, 10, 16, 22, 28]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 2, 4, 6, 9, 10, 13, 14, 16, 18, 21, 22, 24, 26, 29]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_13():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 5, 9]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [1, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_14():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [-4, -6, -7, 6, 4, 6, 2, 1, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, 3, 4, -1, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 4, 6, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 3, 4, -1, 7]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_15():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [-4, -6, -7, 6, -4, -6, -7, 2, 1, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 4
    starts = [0, 3, 4, 7]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 4, 7, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 3, 6, 8]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_16():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, 3, 6, 9, 11]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 6, 9, 11, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 3, 8, 9, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_17():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 4, 2, 2, 2, 1, 6, 1, 4, 1, 3, 3, 4, 6, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 5
    starts = [0, 3, 6, 9, 12]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 6, 9, 12, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 5, 7, 9, 12]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_18():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 4, 2, -3, 4, 2, 2, 2, 1, 2, -2, 1, 6, 1, 4, -6, 1, 4, 1, 3, 3, 1, -3, 3, 4, 6, 6, 4, 6, -6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 10
    starts = [0, 6, 12, 18, 24, 3, 9, 15, 21, 27]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [2, 3, 8, 10, 13, 15, 18, 22, 24, 29]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_19():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [6, 3, 2, 1, 2]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 1
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_20():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6, -3, 2, -6, 1, 4, 4, -2, 1, -3, 6, 2, 1, 4, 3, -6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 6
    starts = [0, 5, 10, 15, 20, 25]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 10, 15, 20, 25, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [3, 7, 11, 17, 23, 29]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_21():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 3
    starts = [0, 5, 10]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [3, 7, 11]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_22():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 2, 2, 2, 3, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 6
    starts = [0, 10, 16, 5, 13, 17]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 8, 9, 14, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 5, 8, 9, 14, 17]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_23():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3, 999]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 8
    starts = [0, 10, 17, -1, 5, 13, 18, 21]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 8, 9, 9, 14, 18, 21, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 5, 8, -1, 9, 14, 20, 21]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_int64_64_24():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3]
    fromptr = (ctypes.c_int64*len(fromptr))(*fromptr)
    outlength = 6
    starts = [0, 10, 17, 5, 13, 18]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5, 8, 9, 14, 18, 21]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_int64_64')
    ret_pass = funcC(toptr, fromptr, offsets, starts, outlength)
    pytest_toptr = [0, 5, 8, 9, 14, 20]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

