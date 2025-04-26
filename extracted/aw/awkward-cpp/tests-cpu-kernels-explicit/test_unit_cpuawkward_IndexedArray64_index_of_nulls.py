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

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, -1, 0, 1, 2, -1, -1, -1, 3, -1, 4, 5, -1, -1, 6, 7, 8]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 17
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5, 8, 11, 14]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [0, 1, 0, 1, 2, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, -1, 3, 5, 6, -1, -1, -1, -1, 7, 0, -1, 4, -1, 8, 1, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 17
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5, 10, 15, 16]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [0, 1, 0, 1, 2, 3, 1, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_4():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, -1, 0, 1, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 5
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, -1, 3, 5, 6, 1, -1, 4, -1, 7, 2, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 25
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5, 10, 15, 20]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [1, 1, 3, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_6():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, -1, 1, 2, -1, 3, 4, 5]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 8
    parents = [0, 0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [1, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_7():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 4
    parents = [0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_8():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, -1, 4]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 5
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_9():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, 2, 3, -1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 6
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [2, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_10():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, 2, 3, -1, 4, 5, -1, 6, 7, -1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 12
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [2, 5, 2, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_index_of_nulls_11():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, 2, -1, -1, -1, -1, 7, 8]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lenindex = 9
    parents = [0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArray64_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = [3, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

