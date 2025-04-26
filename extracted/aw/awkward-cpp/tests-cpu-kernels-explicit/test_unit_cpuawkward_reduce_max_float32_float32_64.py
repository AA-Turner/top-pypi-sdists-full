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

def test_unit_cpuawkward_reduce_max_float32_float32_64_1():
    toptr = []
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_2():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [13, 11, 5, -9223372036854775808, -9223372036854775808, -9223372036854775808, 23, 19]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_3():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 1, 3, 4, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 3, -9223372036854775808, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_4():
    toptr = [123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_5():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [0, 4, 1, 3, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 1, 1, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [4, 5, -9223372036854775808, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_6():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 5, 3, 3, 5, 1, 4, 2]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 1, 1, 2, 2, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, 3, 5, 4, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_7():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = 4
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, 4, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_8():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 3, 6, 4, 2, 2, 3, 1, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = 4
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [6, 4, 4, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_9():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 3, 2, 5, 3, 7, 3, 1, 5, 8, 1, 9, 4, 2, 7, 10, 2, 4, 7, 2]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 20
    outlength = 5
    parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, 7, 9, 10, 7]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_10():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 3, 7, 8, 2, 4, 2, 3, 1, 7, 7, 5, 1, 9, 10, 2]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 20
    outlength = 4
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, 8, 7, 10]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_11():
    toptr = [123.0, 123.0, 123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, -9223372036854775808, 11, 13, 19, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_12():
    toptr = [123.0, 123.0, 123.0, 123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [5, -9223372036854775808, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_float32_float32_64_13():
    toptr = [123.0]
    toptr = (ctypes.c_float*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_float*len(fromptr))(*fromptr)
    identity = -9223372036854775808
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_max_float32_float32_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

