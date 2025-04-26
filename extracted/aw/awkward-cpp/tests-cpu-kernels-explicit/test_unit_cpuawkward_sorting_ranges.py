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

def test_unit_cpuawkward_sorting_ranges_1():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 0
    tolength = 2
    funcC = getattr(lib, 'awkward_sorting_ranges')
    ret_pass = funcC(toindex, tolength, parents, parentslength)
    pytest_toindex = [0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    parents = [0, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 2
    tolength = 3
    funcC = getattr(lib, 'awkward_sorting_ranges')
    ret_pass = funcC(toindex, tolength, parents, parentslength)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_3():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    parents = [0, 3, 6, 9]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 4
    tolength = 5
    funcC = getattr(lib, 'awkward_sorting_ranges')
    ret_pass = funcC(toindex, tolength, parents, parentslength)
    pytest_toindex = [0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_4():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    parents = [3, 3, 3, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 4
    tolength = 2
    funcC = getattr(lib, 'awkward_sorting_ranges')
    ret_pass = funcC(toindex, tolength, parents, parentslength)
    pytest_toindex = [0, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_sorting_ranges_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    parents = [2, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    parentslength = 3
    tolength = 3
    funcC = getattr(lib, 'awkward_sorting_ranges')
    ret_pass = funcC(toindex, tolength, parents, parentslength)
    pytest_toindex = [0, 1, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

