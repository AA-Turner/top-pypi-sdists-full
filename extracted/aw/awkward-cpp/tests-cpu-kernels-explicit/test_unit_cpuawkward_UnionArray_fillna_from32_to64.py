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

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 0
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_2():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, -1, -1, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 5
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, -1, 0, -1, 1, 2, 3, 4, 5, -1, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 12
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_4():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [-1, 0, 1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 4
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, -1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_6():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, -1, 1, -1, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 5
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 1, 0, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_7():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, -1, 1, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 4
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_8():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_9():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 4
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 0, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_10():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, -1, 2, 3, -1, 4]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 7
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 0, 2, 3, 0, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_11():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, 2, -1, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 6
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 2, 0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_12():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, 2, -1, -1, 3, 4, 5, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 10
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 2, 0, 0, 3, 4, 5, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_13():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, 2, 3, 4, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 7
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [0, 1, 2, 3, 4, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillna_from32_to64_14():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [13, 9, 13, 4, 8, 3, 15, -1, 16, 2, 8]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 11
    funcC = getattr(lib, 'awkward_UnionArray_fillna_from32_to64')
    ret_pass = funcC(toindex, fromindex, length)
    pytest_toindex = [13, 9, 13, 4, 8, 3, 15, 0, 16, 2, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

