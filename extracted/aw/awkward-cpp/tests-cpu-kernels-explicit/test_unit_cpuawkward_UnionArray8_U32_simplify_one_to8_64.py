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

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 0
    length = 0
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_2():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = [0, 0, 0, 0, 0]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = [1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 5
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = [0, 0, 0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [0, 0, 0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 9
    fromindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 9
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = [9, 10, 11, 12, 13, 14, 15, 16, 17]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_4():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = [0, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = [1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 2
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_5():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = [0]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = [1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 1
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_6():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 0
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_U32_simplify_one_to8_64_7():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromwhich = 1
    length = 0
    towhich = 1
    funcC = getattr(lib, 'awkward_UnionArray8_U32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

