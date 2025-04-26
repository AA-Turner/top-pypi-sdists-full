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

def test_unit_cpuawkward_RegularArray_getitem_next_range_spreadadvanced_64_1():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromadvanced = []
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    length = 0
    nextsize = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    ret_pass = funcC(toadvanced, fromadvanced, length, nextsize)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_spreadadvanced_64_2():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromadvanced = []
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    length = 1
    nextsize = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    ret_pass = funcC(toadvanced, fromadvanced, length, nextsize)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_spreadadvanced_64_3():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromadvanced = []
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    length = 0
    nextsize = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    ret_pass = funcC(toadvanced, fromadvanced, length, nextsize)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_spreadadvanced_64_4():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromadvanced = [0]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    length = 1
    nextsize = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    ret_pass = funcC(toadvanced, fromadvanced, length, nextsize)
    pytest_toadvanced = [0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_spreadadvanced_64_5():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    length = 2
    nextsize = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    ret_pass = funcC(toadvanced, fromadvanced, length, nextsize)
    pytest_toadvanced = [0, 0, 1, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    assert not ret_pass.str

