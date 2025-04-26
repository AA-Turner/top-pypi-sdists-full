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

def test_unit_cpuawkward_NumpyArray_rearrange_shifted_toint64_fromint64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromshifts = []
    fromshifts = (ctypes.c_int64*len(fromshifts))(*fromshifts)
    length = 0
    fromoffsets = []
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 0
    fromparents = []
    fromparents = (ctypes.c_int64*len(fromparents))(*fromparents)
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    funcC = getattr(lib, 'awkward_NumpyArray_rearrange_shifted_toint64_fromint64')
    ret_pass = funcC(toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_rearrange_shifted_toint64_fromint64_2():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromshifts = [0, 1, 2, 3, 4, 5, 6]
    fromshifts = (ctypes.c_int64*len(fromshifts))(*fromshifts)
    length = 4
    fromoffsets = [0, 1, 3, 3, 5, 7, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 7
    fromparents = [0, 1, 3, 6]
    fromparents = (ctypes.c_int64*len(fromparents))(*fromparents)
    fromstarts = [0, 1, 2, 3, 4, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    funcC = getattr(lib, 'awkward_NumpyArray_rearrange_shifted_toint64_fromint64')
    ret_pass = funcC(toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts)
    pytest_toptr = [0, 3, 3, 6, 7, 10, 11, 14, 15]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_rearrange_shifted_toint64_fromint64_3():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [0, 0, 0, 0, 0, 0, 0, 0]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromshifts = [0, 1, 2, 3, 4, 5, 6]
    fromshifts = (ctypes.c_int64*len(fromshifts))(*fromshifts)
    length = 4
    fromoffsets = [0, 2, 5, 8]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 4
    fromparents = [0, 1, 3, 6]
    fromparents = (ctypes.c_int64*len(fromparents))(*fromparents)
    fromstarts = [0, 1, 2, 3, 4, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    funcC = getattr(lib, 'awkward_NumpyArray_rearrange_shifted_toint64_fromint64')
    ret_pass = funcC(toptr, fromshifts, length, fromoffsets, offsetslength, fromparents, fromstarts)
    pytest_toptr = [0, -1, 1, -2, 2, 5, 5, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

