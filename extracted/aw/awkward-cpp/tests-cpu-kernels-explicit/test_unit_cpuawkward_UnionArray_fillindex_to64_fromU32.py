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

def test_unit_cpuawkward_UnionArray_fillindex_to64_fromU32_1():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 0, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 4
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [0, 0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillindex_to64_fromU32_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 0
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_fillindex_to64_fromU32_3():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = [0, 1, 2, 0, 1, 2]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    length = 6
    toindexoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_fillindex_to64_fromU32')
    ret_pass = funcC(toindex, toindexoffset, fromindex, length)
    pytest_toindex = [0, 1, 2, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

