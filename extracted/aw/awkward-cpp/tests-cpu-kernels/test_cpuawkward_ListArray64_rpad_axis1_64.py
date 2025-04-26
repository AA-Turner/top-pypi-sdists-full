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

def test_cpuawkward_ListArray64_rpad_axis1_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [2, -1, -1, 0, 1, -1, 2, 3, -1]
    pytest_tostarts = [0, 3, 6]
    pytest_tostops = [3, 6, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_rpad_axis1_64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    pytest_tostarts = [0, 7, 11]
    pytest_tostops = [7, 11, 16]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_rpad_axis1_64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    pytest_tostarts = [0, 3, 6]
    pytest_tostops = [3, 6, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_rpad_axis1_64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [-1, -1, -1, 7, 8, -1, -1, -1, -1]
    pytest_tostarts = [0, 3, 6]
    pytest_tostops = [3, 6, 9]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_rpad_axis1_64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_rpad_axis1_64')
    ret_pass = funcC(toindex, fromstarts, fromstops, tostarts, tostops, target, length)
    pytest_toindex = [0, -1, -1, 0, -1, -1, 0, -1, -1]
    pytest_tostarts = [0, 3, 6]
    pytest_tostops = [3, 6, 9]
    assert not ret_pass.str

