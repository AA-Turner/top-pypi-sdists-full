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

def test_unit_cpuawkward_ListArray32_combinations_64_1():
    tocarry = [[], []]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 0
    n = 0
    replacement = False
    starts = []
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = []
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[], []]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_2():
    tocarry = [[123], [123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 1
    n = 2
    replacement = False
    starts = [0]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [2]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0], [1]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_3():
    tocarry = [[123], [123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 2
    n = 2
    replacement = False
    starts = [0, 2]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [2, 3]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0], [1]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_4():
    tocarry = [[123, 123, 123, 123], [123, 123, 123, 123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 2
    n = 2
    replacement = True
    starts = [0, 2]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [2, 3]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0, 0, 1, 2], [0, 1, 1, 2]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [4, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_5():
    tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    n = 2
    replacement = False
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0, 0, 0, 1, 1, 2, 4, 4, 5, 8, 8, 8, 8, 9, 9, 9, 10, 10, 11], [1, 2, 3, 2, 3, 3, 5, 6, 6, 9, 10, 11, 12, 10, 11, 12, 11, 12, 12]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [19, 19]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_6():
    tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    n = 2
    replacement = True
    starts = [0, 4, 4, 7, 8]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [4, 4, 7, 8, 13]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 4, 5, 5, 6, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12], [0, 1, 2, 3, 1, 2, 3, 2, 3, 3, 4, 5, 6, 5, 6, 6, 7, 8, 9, 10, 11, 12, 9, 10, 11, 12, 10, 11, 12, 11, 12, 12]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [32, 32]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_combinations_64_7():
    tocarry = [[123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123]]
    int64Ptr = ctypes.POINTER(ctypes.c_int64)
    int64PtrPtr = ctypes.POINTER(int64Ptr)
    dim0 = len(tocarry)
    dim1 = len(tocarry[0])
    tocarry_np_arr_2d = np.empty([dim0, dim1], dtype=np.int64)
    for i in range(dim0):
        for j in range(dim1):
            tocarry_np_arr_2d[i][j] = tocarry[i][j]
    tocarry_ct_arr = np.ctypeslib.as_ctypes(tocarry_np_arr_2d)
    int64PtrArr = int64Ptr * tocarry_ct_arr._length_
    tocarry_ct_ptr = ctypes.cast(int64PtrArr(*(ctypes.cast(row, int64Ptr) for row in tocarry_ct_arr)), int64PtrPtr)
    tocarry = tocarry_ct_ptr
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    length = 5
    n = 2
    replacement = False
    starts = [0, 3, 3, 10, 10]
    starts = (ctypes.c_int32*len(starts))(*starts)
    stops = [3, 3, 5, 10, 13]
    stops = (ctypes.c_int32*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray32_combinations_64')
    ret_pass = funcC(tocarry, toindex, fromindex, n, replacement, starts, stops, length)
    pytest_tocarry = [[0, 0, 1, 3, 10, 10, 11], [1, 2, 2, 4, 11, 12, 12]]
    for row1, row2 in zip(pytest_tocarry, tocarry_np_arr_2d[:len(pytest_tocarry)]):
        assert row1 == pytest.approx(row2)
    pytest_toindex = [7, 7]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

