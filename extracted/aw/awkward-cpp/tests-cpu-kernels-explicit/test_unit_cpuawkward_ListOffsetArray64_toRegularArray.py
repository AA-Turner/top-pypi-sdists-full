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

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_1():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = []
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [0]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_2():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [0]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_3():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, -1, -2]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    assert funcC(size, fromoffsets, offsetslength).str.decode('utf-8') == "offsets must be monotonically increasing"

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_4():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 2, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    assert funcC(size, fromoffsets, offsetslength).str.decode('utf-8') == "cannot convert to RegularArray because subarray lengths are not regular"

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_5():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [0]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_6():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 1, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [1]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_7():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 2, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [2]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_8():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 2, 4, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [2]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_9():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [4]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_toRegularArray_10():
    size = [123]
    size = (ctypes.c_int64*len(size))(*size)
    fromoffsets = [0, 5, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_toRegularArray')
    ret_pass = funcC(size, fromoffsets, offsetslength)
    pytest_size = [5]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)
    assert not ret_pass.str

