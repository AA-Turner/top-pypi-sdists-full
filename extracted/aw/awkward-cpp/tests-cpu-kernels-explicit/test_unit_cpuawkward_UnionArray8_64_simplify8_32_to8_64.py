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

def test_unit_cpuawkward_UnionArray8_64_simplify8_32_to8_64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    innerindex = []
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innertags = []
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerwhich = 0
    length = 0
    outerindex = []
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    outertags = []
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerwhich = 1
    towhich = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_simplify8_32_to8_64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    innerindex = [0, 0, 1, 1, 2, 3, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innertags = [0, 1, 0, 1, 0, 0, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerwhich = 0
    length = 12
    outerindex = [0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    outertags = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerwhich = 1
    towhich = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_toindex = [123, 123, 0, 123, 1, 123, 123, 2, 3, 123, 123, 123]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [123, 123, 1, 123, 1, 123, 123, 1, 1, 123, 123, 123]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_simplify8_32_to8_64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    totags = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 5
    innerindex = [0, 0, 1, 1, 2, 3, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innertags = [0, 1, 0, 1, 0, 0, 1]
    innertags = (ctypes.c_int8*len(innertags))(*innertags)
    innerwhich = 1
    length = 12
    outerindex = [0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4]
    outerindex = (ctypes.c_int64*len(outerindex))(*outerindex)
    outertags = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    outertags = (ctypes.c_int8*len(outertags))(*outertags)
    outerwhich = 1
    towhich = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_simplify8_32_to8_64')
    ret_pass = funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)
    pytest_toindex = [123, 123, 123, 5, 123, 123, 6, 123, 123, 123, 7, 123]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_totags = [123, 123, 123, 0, 123, 123, 0, 123, 123, 123, 0, 123]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

