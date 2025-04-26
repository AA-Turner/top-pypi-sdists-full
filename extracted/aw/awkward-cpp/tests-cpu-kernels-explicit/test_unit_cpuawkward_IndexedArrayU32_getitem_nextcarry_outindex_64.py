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

def test_unit_cpuawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = []
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 0
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, toindex, fromindex, lenindex, lencontent)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_2():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = []
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    fromindex = [0, 1, 2, 4]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    assert funcC(tocarry, toindex, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_3():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    fromindex = [0, 1, 2, 4]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    assert funcC(tocarry, toindex, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_4():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    fromindex = [0, 1, 2, 3]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, toindex, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_5():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    fromindex = [3, 2, 1, 0]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, toindex, fromindex, lenindex, lencontent)
    pytest_tocarry = [3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

