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

def test_unit_cpuawkward_reduce_min_complex64_complex64_64_1():
    toptr = []
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = 9223372036854775807
    fromptr = []
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_complex64_complex64_64_2():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = 9223372036854775807
    fromptr = [0, 0]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    lenparents = 1
    outlength = 1
    parents = [0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_complex64_complex64_64_3():
    toptr = [123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = 9223372036854775807
    fromptr = [1, 0, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    lenparents = 2
    outlength = 1
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_complex64_complex64_64_4():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = 9223372036854775807
    fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [2, 2, 9223372036854775807, 0, 7, 7, 13, 13, 17, 17, 23, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_complex64_complex64_64_5():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    identity = 9223372036854775807
    fromptr = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 4
    parents = [0, 0, 0, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_complex64_complex64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [0, 0, 9223372036854775807, 0, 0, 1, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

