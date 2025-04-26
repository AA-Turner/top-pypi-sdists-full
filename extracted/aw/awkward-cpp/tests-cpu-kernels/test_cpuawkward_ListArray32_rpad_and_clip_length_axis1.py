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

def test_cpuawkward_ListArray32_rpad_and_clip_length_axis1_1():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    target = 3
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_and_clip_length_axis1')
    ret_pass = funcC(tomin, fromstarts, fromstops, target, lenstarts)
    pytest_tomin = [9]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_rpad_and_clip_length_axis1_2():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    target = 3
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_and_clip_length_axis1')
    ret_pass = funcC(tomin, fromstarts, fromstops, target, lenstarts)
    pytest_tomin = [16]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_rpad_and_clip_length_axis1_3():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    target = 3
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_and_clip_length_axis1')
    ret_pass = funcC(tomin, fromstarts, fromstops, target, lenstarts)
    pytest_tomin = [9]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_rpad_and_clip_length_axis1_4():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    target = 3
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_and_clip_length_axis1')
    ret_pass = funcC(tomin, fromstarts, fromstops, target, lenstarts)
    pytest_tomin = [9]
    assert not ret_pass.str

def test_cpuawkward_ListArray32_rpad_and_clip_length_axis1_5():
    tomin = [123]
    tomin = (ctypes.c_int64*len(tomin))(*tomin)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    target = 3
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArray32_rpad_and_clip_length_axis1')
    ret_pass = funcC(tomin, fromstarts, fromstops, target, lenstarts)
    pytest_tomin = [9]
    assert not ret_pass.str

