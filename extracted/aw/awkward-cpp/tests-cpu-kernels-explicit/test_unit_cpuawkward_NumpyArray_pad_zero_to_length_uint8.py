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

def test_unit_cpuawkward_NumpyArray_pad_zero_to_length_uint8_1():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint8*len(toptr))(*toptr)
    fromoffsets = [0, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromptr = [0, 1, 3]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    offsetslength = 3
    target = 2
    funcC = getattr(lib, 'awkward_NumpyArray_pad_zero_to_length_uint8')
    ret_pass = funcC(fromptr, fromoffsets, offsetslength, target, toptr)
    pytest_toptr = [0, 1, 3, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_pad_zero_to_length_uint8_2():
    toptr = []
    toptr = (ctypes.c_uint8*len(toptr))(*toptr)
    fromoffsets = []
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromptr = []
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    offsetslength = 0
    target = 0
    funcC = getattr(lib, 'awkward_NumpyArray_pad_zero_to_length_uint8')
    ret_pass = funcC(fromptr, fromoffsets, offsetslength, target, toptr)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_pad_zero_to_length_uint8_3():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint8*len(toptr))(*toptr)
    fromoffsets = [0, 2, 2, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromptr = [1, 3, 3, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    offsetslength = 4
    target = 4
    funcC = getattr(lib, 'awkward_NumpyArray_pad_zero_to_length_uint8')
    ret_pass = funcC(fromptr, fromoffsets, offsetslength, target, toptr)
    pytest_toptr = [1, 3, 0, 0, 0, 0, 0, 0, 3, 5, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_pad_zero_to_length_uint8_4():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint8*len(toptr))(*toptr)
    fromoffsets = [0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromptr = [3, 5]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    offsetslength = 2
    target = 4
    funcC = getattr(lib, 'awkward_NumpyArray_pad_zero_to_length_uint8')
    ret_pass = funcC(fromptr, fromoffsets, offsetslength, target, toptr)
    pytest_toptr = [0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_pad_zero_to_length_uint8_5():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_uint8*len(toptr))(*toptr)
    fromoffsets = [0, 1, 2, 3, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromptr = [0, 3, 3, 5, 6]
    fromptr = (ctypes.c_uint8*len(fromptr))(*fromptr)
    offsetslength = 5
    target = 4
    funcC = getattr(lib, 'awkward_NumpyArray_pad_zero_to_length_uint8')
    ret_pass = funcC(fromptr, fromoffsets, offsetslength, target, toptr)
    pytest_toptr = [0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 5, 6, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

