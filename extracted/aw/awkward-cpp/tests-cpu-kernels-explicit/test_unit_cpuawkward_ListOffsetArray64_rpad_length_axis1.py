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

def test_unit_cpuawkward_ListOffsetArray64_rpad_length_axis1_1():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = []
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromlength = 0
    target = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray64_rpad_length_axis1')
    ret_pass = funcC(tooffsets, fromoffsets, fromlength, target, tolength)
    pytest_tolength = [0]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_rpad_length_axis1_2():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromlength = 1
    target = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_rpad_length_axis1')
    ret_pass = funcC(tooffsets, fromoffsets, fromlength, target, tolength)
    pytest_tolength = [3]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    pytest_tooffsets = [0, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_rpad_length_axis1_3():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [1, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromlength = 1
    target = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_rpad_length_axis1')
    ret_pass = funcC(tooffsets, fromoffsets, fromlength, target, tolength)
    pytest_tolength = [3]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    pytest_tooffsets = [0, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_rpad_length_axis1_4():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 1, 2, 3, 5, 7, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromlength = 6
    target = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray64_rpad_length_axis1')
    ret_pass = funcC(tooffsets, fromoffsets, fromlength, target, tolength)
    pytest_tolength = [19]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    pytest_tooffsets = [0, 3, 6, 9, 12, 15, 19]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray64_rpad_length_axis1_5():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 1, 2, 3, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromlength = 4
    target = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray64_rpad_length_axis1')
    ret_pass = funcC(tooffsets, fromoffsets, fromlength, target, tolength)
    pytest_tolength = [4]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    pytest_tooffsets = [0, 1, 2, 3, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

