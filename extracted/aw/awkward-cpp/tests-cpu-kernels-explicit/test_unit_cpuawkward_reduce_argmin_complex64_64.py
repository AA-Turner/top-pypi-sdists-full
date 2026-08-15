# AUTO GENERATED ON 2026-08-14 AT 14:44:29
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

def test_unit_cpuawkward_reduce_argmin_complex64_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_complex64_64_2():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_complex64_64_3():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_complex64_64_4():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [0, -1, 3, 5, 6, 8]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmin_complex64_64_5():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmin_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength)
    pytest_toptr = [2, -1, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

