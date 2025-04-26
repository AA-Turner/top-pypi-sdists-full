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

def test_unit_cpuawkward_unique_offsets_int32_1():
    tooffsets = [123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    fromoffsets = [0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 0
    length = 1
    funcC = getattr(lib, 'awkward_unique_offsets_int32')
    ret_pass = funcC(tooffsets, length, fromoffsets, starts, startslength)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_offsets_int32_2():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 2, 2, 3, 4, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    starts = [0, 2, 4, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 4
    length = 6
    funcC = getattr(lib, 'awkward_unique_offsets_int32')
    ret_pass = funcC(tooffsets, length, fromoffsets, starts, startslength)
    pytest_tooffsets = [0, 2, 2, 3, 5, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_offsets_int32_3():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 1, 2, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    starts = [0, 1, 3, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 4
    length = 5
    funcC = getattr(lib, 'awkward_unique_offsets_int32')
    ret_pass = funcC(tooffsets, length, fromoffsets, starts, startslength)
    pytest_tooffsets = [0, 1, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_offsets_int32_4():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int32*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 1, 2, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    starts = [0, 1, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 4
    length = 5
    funcC = getattr(lib, 'awkward_unique_offsets_int32')
    ret_pass = funcC(tooffsets, length, fromoffsets, starts, startslength)
    pytest_tooffsets = [0, 1, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

