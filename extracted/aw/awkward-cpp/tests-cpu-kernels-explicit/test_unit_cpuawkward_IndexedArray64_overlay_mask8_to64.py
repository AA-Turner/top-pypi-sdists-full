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

def test_unit_cpuawkward_IndexedArray64_overlay_mask8_to64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 0
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    funcC = getattr(lib, 'awkward_IndexedArray64_overlay_mask8_to64')
    ret_pass = funcC(toindex, mask, fromindex, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_overlay_mask8_to64_2():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [5, 4, 3, 2, 1, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 6
    mask = [0, 0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    funcC = getattr(lib, 'awkward_IndexedArray64_overlay_mask8_to64')
    ret_pass = funcC(toindex, mask, fromindex, length)
    pytest_toindex = [5, 4, 3, 2, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

