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

def test_unit_cpuawkward_unique_ranges_bool_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromoffsets = [0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 1
    funcC = getattr(lib, 'awkward_unique_ranges_bool')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_bool_2():
    toptr = [True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [1, 1]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromoffsets = [0, 2]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 2
    funcC = getattr(lib, 'awkward_unique_ranges_bool')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_bool_3():
    toptr = [True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [0, 1, 1, 1, 1, 1]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromoffsets = [0, 3, 5, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_unique_ranges_bool')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [0, 1, 1, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 2, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_unique_ranges_bool_4():
    toptr = [True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    toptr = [1, 1, 1, 0]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromoffsets = [0, 0, 3, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    funcC = getattr(lib, 'awkward_unique_ranges_bool')
    ret_pass = funcC(toptr, fromoffsets, offsetslength, tooffsets)
    pytest_toptr = [1, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

