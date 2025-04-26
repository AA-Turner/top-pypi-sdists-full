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

def test_unit_cpuawkward_unique_ranges_int64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromoffsets = [0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 1
    funcC = getattr(lib, 'awkward_unique_ranges_int64')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_int64_2():
    toptr = [123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [1, 2]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromoffsets = [0, 2]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 2
    funcC = getattr(lib, 'awkward_unique_ranges_int64')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [1, 2]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_int64_3():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [0, 1, 2, 3, 4, 5]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromoffsets = [0, 3, 5, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_unique_ranges_int64')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [0, 1, 2, 3, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 3, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_int64_4():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [3, 2, 1, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromoffsets = [0, 0, 3, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_unique_ranges_int64')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [3, 3, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 1, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

