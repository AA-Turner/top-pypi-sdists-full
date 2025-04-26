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

def test_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_1():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [1, 1, 1, 1, 1]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 3
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [-1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [0, 0, 0, 0, 0]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 3
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 3
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [-1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 3
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [-1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 3
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

