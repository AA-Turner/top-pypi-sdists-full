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

def test_unit_cpuawkward_sorting_ranges_length_1():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 0
    funcC = getattr(lib, 'awkward_sorting_ranges_length')
    ret_pass = funcC(tolength, parents, parentslength)
    pytest_tolength = [2]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_length_2():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    parents = [0, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 2
    funcC = getattr(lib, 'awkward_sorting_ranges_length')
    ret_pass = funcC(tolength, parents, parentslength)
    pytest_tolength = [3]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_length_3():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    parents = [0, 3, 6, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 4
    funcC = getattr(lib, 'awkward_sorting_ranges_length')
    ret_pass = funcC(tolength, parents, parentslength)
    pytest_tolength = [5]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_length_4():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    parents = [3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 4
    funcC = getattr(lib, 'awkward_sorting_ranges_length')
    ret_pass = funcC(tolength, parents, parentslength)
    pytest_tolength = [2]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_length_5():
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    parents = [2, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 3
    funcC = getattr(lib, 'awkward_sorting_ranges_length')
    ret_pass = funcC(tolength, parents, parentslength)
    pytest_tolength = [3]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

