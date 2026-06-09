# AUTO GENERATED ON 2026-06-08 AT 11:28:09
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

def test_unit_cpuawkward_reduce_argmax_uint8_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = []
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_2():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6, 7]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 3
    parents = [0, 1, 1, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 1, 3, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 1, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [0, 2, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_3():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 3
    parents = [0, 0, 1, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 2, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 2, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [1, 2, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_4():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_5():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 1, 2, 3, 4, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 3, 5, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [2, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_6():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [0, 0, 4, 4, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_7():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_argmax_uint8_64_8():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 2, 3, 4, 5, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_argmax_uint8_64')
    ret_pass = funcC(toptr, fromptr, parents, offsets, lenparents, starts, outlength)
    pytest_toptr = [5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

