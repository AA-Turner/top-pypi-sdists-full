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

def test_unit_cpuawkward_UnionArray64_flatten_combine_64_1():
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 0
    offsetsraws = [[], []]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(offsetsraws)
    dim1 = len(offsetsraws[0])
    offsetsraws_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            offsetsraws_np_arr_2d[i][j] = offsetsraws[i][j]
    offsetsraws_ct_arr = np.ctypeslib.as_ctypes(offsetsraws_np_arr_2d)
    int64PtrArr = int64Ptr * offsetsraws_ct_arr._length_
    offsetsraws_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in offsetsraws_ct_arr)), int64PtrPtr)
    offsetsraws = offsetsraws_ct_ptr
    funcC = getattr(lib, 'awkward_UnionArray64_flatten_combine_64')
    ret_pass = funcC(totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_flatten_combine_64_2():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromtags = [0, 1, 0, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 1, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 4
    offsetsraws = [[0, 2, 2, 3, 5], [2, 2, 3, 5, 6]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(offsetsraws)
    dim1 = len(offsetsraws[0])
    offsetsraws_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            offsetsraws_np_arr_2d[i][j] = offsetsraws[i][j]
    offsetsraws_ct_arr = np.ctypeslib.as_ctypes(offsetsraws_np_arr_2d)
    int64PtrArr = int64Ptr * offsetsraws_ct_arr._length_
    offsetsraws_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in offsetsraws_ct_arr)), int64PtrPtr)
    offsetsraws = offsetsraws_ct_ptr
    funcC = getattr(lib, 'awkward_UnionArray64_flatten_combine_64')
    ret_pass = funcC(totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws)
    pytest_totags = [0, 0, 1]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tooffsets = [0, 2, 2, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_flatten_combine_64_3():
    totags = [123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromtags = [0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 1, 2, 3]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 4
    offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(offsetsraws)
    dim1 = len(offsetsraws[0])
    offsetsraws_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            offsetsraws_np_arr_2d[i][j] = offsetsraws[i][j]
    offsetsraws_ct_arr = np.ctypeslib.as_ctypes(offsetsraws_np_arr_2d)
    int64PtrArr = int64Ptr * offsetsraws_ct_arr._length_
    offsetsraws_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in offsetsraws_ct_arr)), int64PtrPtr)
    offsetsraws = offsetsraws_ct_ptr
    funcC = getattr(lib, 'awkward_UnionArray64_flatten_combine_64')
    ret_pass = funcC(totags, toindex, tooffsets, fromtags, fromindex, length, offsetsraws)
    pytest_totags = [0, 0, 0, 0, 0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tooffsets = [0, 1, 3, 5, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

