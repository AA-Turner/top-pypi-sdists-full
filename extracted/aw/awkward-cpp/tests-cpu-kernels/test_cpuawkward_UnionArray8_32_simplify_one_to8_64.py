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

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_1():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_2():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_3():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 6, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_4():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 7, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_5():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_6():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_7():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_8():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 6, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_9():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 7, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_10():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_11():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_12():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_13():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 6, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_14():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 7, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_simplify_one_to8_64_15():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_32_simplify_one_to8_64')
    ret_pass = funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

