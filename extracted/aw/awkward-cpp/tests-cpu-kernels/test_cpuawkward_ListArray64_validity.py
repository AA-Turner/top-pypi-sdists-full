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

def test_cpuawkward_ListArray64_validity_1():
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str

def test_cpuawkward_ListArray64_validity_2():
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [8, 4, 5, 6, 5, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str

def test_cpuawkward_ListArray64_validity_3():
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_cpuawkward_ListArray64_validity_4():
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str

def test_cpuawkward_ListArray64_validity_5():
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    length = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

