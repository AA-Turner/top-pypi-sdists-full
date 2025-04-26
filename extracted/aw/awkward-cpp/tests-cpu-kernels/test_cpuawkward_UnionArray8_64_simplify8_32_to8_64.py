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

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_1():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_2():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_3():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_4():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_5():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_6():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_7():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_8():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_9():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_10():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_11():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_12():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_13():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_14():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_15():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_16():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_17():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_18():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_19():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_20():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_21():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_22():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_23():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_24():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_25():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_26():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_27():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_28():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_29():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_30():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_31():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_32():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_33():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_34():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_35():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_36():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_37():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_38():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_39():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_40():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_41():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_42():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_43():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_44():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_45():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_46():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_47():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_48():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_49():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_50():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_51():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_52():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_53():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_54():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_55():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_56():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_57():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_58():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_59():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_60():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_61():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_62():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_63():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_64():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_65():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_66():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_67():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_68():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_69():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_70():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_71():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_72():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_73():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_74():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_75():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_76():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_77():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_78():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_79():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_80():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_81():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_82():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_83():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_84():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_85():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_86():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_87():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_88():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_89():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_90():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_91():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_92():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_93():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_94():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_95():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_96():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_97():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_98():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_99():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_100():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_101():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_102():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_103():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_104():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_105():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_106():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_107():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_108():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_109():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_110():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_111():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_112():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_113():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_114():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_115():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_116():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_117():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_118():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_119():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_120():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_121():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_122():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_123():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_124():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_125():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_126():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_127():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_128():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_129():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_130():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_131():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_132():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_133():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_134():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_135():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_136():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_137():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_138():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_139():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_140():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_141():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_142():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_143():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_144():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_145():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_146():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_147():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_148():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_149():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_150():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_151():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_152():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_153():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_154():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_155():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_156():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_157():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_158():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_159():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_160():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_161():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_162():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_163():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_164():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_165():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_166():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_167():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_168():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_169():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_170():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_171():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_172():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_173():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_174():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_175():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_176():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_177():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_178():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_179():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_180():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_181():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_182():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_183():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_184():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_185():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_186():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_187():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_188():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_189():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_190():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_191():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_192():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_193():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_194():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_195():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_196():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_197():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_198():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_199():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_200():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_201():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_202():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_203():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_204():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_205():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_206():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_207():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_208():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_209():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_210():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_211():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_212():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_213():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_214():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_215():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_216():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_217():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_218():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_219():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_220():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_221():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_222():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_223():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_224():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_225():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_226():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_227():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_228():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_229():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_230():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_231():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_232():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_233():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_234():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_235():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_236():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_237():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_238():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_239():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_240():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_241():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_242():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_243():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_244():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_245():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_246():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_247():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_248():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_249():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_250():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_251():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_252():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_253():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_254():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_255():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_256():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_257():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_258():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_259():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_260():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_261():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_262():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_263():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_264():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_265():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_266():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_267():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_268():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_269():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_270():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_271():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_272():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_273():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_274():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_275():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_276():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_277():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_278():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_279():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_280():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_281():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_282():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_283():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_284():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_285():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_286():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_287():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_288():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_289():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_290():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_291():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_292():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_293():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_294():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_295():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_296():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_297():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_298():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_299():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_300():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_301():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_302():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_303():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_304():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_305():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_306():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_307():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_308():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_309():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_310():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_311():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_312():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_313():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_314():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_315():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_316():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_317():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_318():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_319():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_320():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_321():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_322():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_323():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_324():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_325():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_326():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_327():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_328():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_329():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_330():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_331():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_332():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_333():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_334():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_335():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_336():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_337():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_338():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_339():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_340():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_341():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_342():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_343():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_344():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_345():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_346():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_347():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_348():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_349():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_350():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_351():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_352():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_353():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_354():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_355():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_356():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_357():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_358():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_359():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_360():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_361():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_362():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_363():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_364():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_365():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_366():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_367():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_368():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_369():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_370():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_371():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_372():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_373():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_374():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_375():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_376():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_377():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_378():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_379():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_380():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_381():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_382():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_383():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_384():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_385():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_386():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_387():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_388():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_389():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_390():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_391():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_392():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_393():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_394():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_395():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_396():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_397():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_398():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_399():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_400():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_401():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_402():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_403():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_404():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_405():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_406():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_407():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_408():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_409():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_410():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_411():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_412():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_413():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_414():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_415():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_416():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_417():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_418():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_419():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_420():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_421():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_422():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_423():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_424():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_425():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_426():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_427():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_428():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_429():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_430():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_431():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_432():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_433():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_434():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_435():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_436():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_437():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_438():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 5, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_439():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_440():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_441():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_442():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_443():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_444():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_445():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_446():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_447():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_448():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_449():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_450():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_451():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_452():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_453():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_454():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_455():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_456():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_457():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_458():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 6, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_459():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_460():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_461():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_462():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_463():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_464():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_465():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_466():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_467():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_468():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_469():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_470():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_471():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_472():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 4, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_473():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_474():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [5, 3, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_475():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_476():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [6, 8, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_477():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_478():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [7, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_479():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_480():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_481():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_482():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_483():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_484():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_485():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_486():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_487():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_488():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_489():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_490():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_491():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_492():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_493():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_494():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_495():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_496():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_497():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_498():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [4, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_499():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_64_simplify8_32_to8_64_500():
    totags = [123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    innertags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_totags = [3, 3, 3]
    pytest_toindex = [3, 3, 3]
    assert not ret_pass.str

