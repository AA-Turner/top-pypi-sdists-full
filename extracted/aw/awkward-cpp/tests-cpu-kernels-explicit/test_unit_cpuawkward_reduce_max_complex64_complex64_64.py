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

def test_unit_cpuawkward_reduce_max_complex64_complex64_64_1():
    toptr = []
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = -9223372036854775808
    fromptr = []
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_complex64_complex64_64_2():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = -9223372036854775808
    fromptr = [0, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_complex64_complex64_64_3():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = -9223372036854775808
    fromptr = [1, 0, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 1
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_complex64_complex64_64_4():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = -9223372036854775808
    fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 5, -9223372036854775808, 0, 11, 11, 13, 13, 19, 19, 23, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_complex64_complex64_64_5():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = -9223372036854775808
    fromptr = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    outlength = 4
    offsets = [0, 3, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [1, 1, -9223372036854775808, 0, 1, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

