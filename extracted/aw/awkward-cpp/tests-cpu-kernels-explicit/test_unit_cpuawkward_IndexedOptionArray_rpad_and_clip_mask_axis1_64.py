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

def test_unit_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = []
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 0
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_2():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frommask = [0, 0, 0, 0]
    frommask = (ctypes.c_int8*len(frommask))(*frommask)
    length = 4
    funcC = getattr(lib, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    ret_pass = funcC(toindex, frommask, length)
    pytest_toindex = [0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

