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

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_1():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 0
    start = 0
    stop = 0
    step = 0
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [0]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_2():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 0
    stop = 3
    step = 1
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [7]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_3():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 7
    stop = 0
    step = -1
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [3]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_4():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 0
    stop = 2
    step = 0
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [0]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_5():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 0
    stop = 6
    step = 2
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [4]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_getitem_next_range_carrylength_6():
    carrylength = [123]
    carrylength = (ctypes.c_int64*len(carrylength))(*carrylength)
    fromstarts = [0, 2, 2, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 3, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 5
    start = 7
    stop = 0
    step = -2
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_range_carrylength')
    ret_pass = funcC(carrylength, fromstarts, fromstops, lenstarts, start, stop, step)
    pytest_carrylength = [3]
    assert carrylength[:len(pytest_carrylength)] == pytest.approx(pytest_carrylength)
    assert not ret_pass.str

