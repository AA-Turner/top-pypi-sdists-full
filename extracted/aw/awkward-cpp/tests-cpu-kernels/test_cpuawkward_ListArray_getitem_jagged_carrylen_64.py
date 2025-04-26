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

def test_cpuawkward_ListArray_getitem_jagged_carrylen_64_1():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_carrylen_64_2():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [16]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_carrylen_64_3():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_carrylen_64_4():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [2]
    assert not ret_pass.str

def test_cpuawkward_ListArray_getitem_jagged_carrylen_64_5():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [3]
    assert not ret_pass.str

