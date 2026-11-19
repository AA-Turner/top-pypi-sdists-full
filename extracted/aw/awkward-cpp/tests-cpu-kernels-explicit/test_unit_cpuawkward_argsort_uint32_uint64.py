# AUTO GENERATED ON 2026-11-18 AT 19:13:59
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

def test_unit_cpuawkward_argsort_uint32_uint64_1():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [-1, -1, -1, -1, -1]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 1]
    fromptr = (ctypes.c_uint32*len(fromptr))(*fromptr)
    offsets = [0, 2]
    offsets = (ctypes.c_uint64*len(offsets))(*offsets)
    offsetslength = 2
    length = 5
    ascending = True
    stable = True
    funcC = getattr(lib, 'awkward_argsort_uint32_uint64')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, ascending, stable)
    pytest_toptr = [1, 0, 2, 3, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_argsort_uint32_uint64_2():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [-1, -1, -1, -1, -1]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 1]
    fromptr = (ctypes.c_uint32*len(fromptr))(*fromptr)
    offsets = [0, 0, 0]
    offsets = (ctypes.c_uint64*len(offsets))(*offsets)
    offsetslength = 3
    length = 5
    ascending = True
    stable = True
    funcC = getattr(lib, 'awkward_argsort_uint32_uint64')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, ascending, stable)
    pytest_toptr = [0, 1, 2, 3, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_argsort_uint32_uint64_3():
    toptr = [123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    toptr = [-1, -1, -1, -1, -1]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    fromptr = [1, 0, 0, 1, 1]
    fromptr = (ctypes.c_uint32*len(fromptr))(*fromptr)
    offsets = [0, 2, 5]
    offsets = (ctypes.c_uint64*len(offsets))(*offsets)
    offsetslength = 2
    length = 5
    ascending = True
    stable = True
    funcC = getattr(lib, 'awkward_argsort_uint32_uint64')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, ascending, stable)
    pytest_toptr = [1, 0, 2, 3, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

