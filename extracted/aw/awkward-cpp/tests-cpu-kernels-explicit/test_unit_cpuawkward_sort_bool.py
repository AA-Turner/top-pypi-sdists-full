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

def test_unit_cpuawkward_sort_bool_1():
    toptr = []
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = []
    fromptr = (ctypes.c_bool*len(fromptr))(*fromptr)
    offsets = []
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 0
    parentslength = 0
    length = 1
    ascending = True
    stable = True
    funcC = getattr(lib, 'awkward_sort_bool')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, parentslength, ascending, stable)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_sort_bool_2():
    toptr = [True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [8, 6, 7, 5, 3, 0, 9]
    fromptr = (ctypes.c_bool*len(fromptr))(*fromptr)
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    parentslength = 7
    length = 7
    ascending = True
    stable = True
    funcC = getattr(lib, 'awkward_sort_bool')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, parentslength, ascending, stable)
    pytest_toptr = [1, 1, 1, 0, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_sort_bool_3():
    toptr = [True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [8, 6, 7, 5, 3, 0, 9]
    fromptr = (ctypes.c_bool*len(fromptr))(*fromptr)
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    parentslength = 7
    length = 7
    ascending = False
    stable = True
    funcC = getattr(lib, 'awkward_sort_bool')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, parentslength, ascending, stable)
    pytest_toptr = [1, 1, 1, 1, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_sort_bool_4():
    toptr = [True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [8, 6, 7, 5, 3, 0, 9]
    fromptr = (ctypes.c_bool*len(fromptr))(*fromptr)
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    parentslength = 7
    length = 7
    ascending = True
    stable = False
    funcC = getattr(lib, 'awkward_sort_bool')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, parentslength, ascending, stable)
    pytest_toptr = [1, 1, 1, 0, 1, 1, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_sort_bool_5():
    toptr = [True, True, True, True, True, True, True]
    toptr = (ctypes.c_bool*len(toptr))(*toptr)
    fromptr = [8, 6, 7, 5, 3, 0, 9]
    fromptr = (ctypes.c_bool*len(fromptr))(*fromptr)
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetslength = 4
    parentslength = 7
    length = 7
    ascending = False
    stable = False
    funcC = getattr(lib, 'awkward_sort_bool')
    ret_pass = funcC(toptr, fromptr, length, offsets, offsetslength, parentslength, ascending, stable)
    pytest_toptr = [1, 1, 1, 1, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

