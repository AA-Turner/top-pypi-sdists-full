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

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_1():
    toptr = []
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_2():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [0, 4, 1, 1, 5, 6]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 1, 1, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [0, 1, 9223372036854775807, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_3():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [0, 1, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 6
    outlength = 4
    parents = [0, 0, 1, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [0, 3, 9223372036854775807, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_4():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 2, 5, 3, 7, 3, 1, 5, 8, 1, 9, 4, 2, 7, 10, 2, 4, 7, 2]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 20
    outlength = 5
    parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 1, 1, 2, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_5():
    toptr = [123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_6():
    toptr = [123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_7():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 6, 4, 2, 2, 3, 1, 6]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 4
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 4, 1, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_8():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 3, 7, 8, 2, 4, 2, 3, 1, 7, 7, 5, 1, 9, 10, 2]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 20
    outlength = 4
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 2, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_9():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 4, 4, 2, 2, 5, 3, 3, 3, 6, 2, 4]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 12
    outlength = 9
    parents = [0, 0, 6, 6, 1, 1, 7, 7, 2, 2, 8, 8]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 2, 3, 9223372036854775807, 9223372036854775807, 9223372036854775807, 2, 3, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_10():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 2, 5, 3, 3, 5, 1, 4, 2]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 9
    outlength = 5
    parents = [0, 0, 0, 1, 1, 2, 2, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 3, 1, 4, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_11():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 4
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 4, 1, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_12():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 9
    outlength = 4
    parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [1, 9223372036854775807, 1, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_13():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 9
    outlength = 8
    parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [2, 3, 5, 9223372036854775807, 9223372036854775807, 9223372036854775807, 17, 19]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_min_uint64_uint64_64_14():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 9223372036854775807
    lenparents = 9
    outlength = 6
    parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_reduce_min_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, parents, lenparents, outlength, identity)
    pytest_toptr = [2, 9223372036854775807, 7, 13, 17, 23]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

