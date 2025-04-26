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

def test_unit_cpuawkward_ListArray32_min_range_1():
    tomin = []
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = []
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lenstarts = 0
    funcC = getattr(lib, 'awkward_ListArray32_min_range')
    ret_pass = funcC(tomin, fromstarts, fromstops, lenstarts)
    pytest_tomin = []
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_min_range_2():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lenstarts = 5
    funcC = getattr(lib, 'awkward_ListArray32_min_range')
    ret_pass = funcC(tomin, fromstarts, fromstops, lenstarts)
    pytest_tomin = [0]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_min_range_3():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 7]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_min_range')
    ret_pass = funcC(tomin, fromstarts, fromstops, lenstarts)
    pytest_tomin = [0]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_min_range_4():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lenstarts = 5
    funcC = getattr(lib, 'awkward_ListArray32_min_range')
    ret_pass = funcC(tomin, fromstarts, fromstops, lenstarts)
    pytest_tomin = [0]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_min_range_5():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArray32_min_range')
    ret_pass = funcC(tomin, fromstarts, fromstops, lenstarts)
    pytest_tomin = [1]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)
    assert not ret_pass.str

