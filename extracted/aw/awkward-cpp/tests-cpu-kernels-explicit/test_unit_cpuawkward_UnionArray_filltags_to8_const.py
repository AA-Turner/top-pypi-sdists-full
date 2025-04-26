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

def test_unit_cpuawkward_UnionArray_filltags_to8_const_1():
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    length = 0
    totagsoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_filltags_to8_const_2():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    length = 6
    totagsoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = [0, 0, 0, 0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_filltags_to8_const_3():
    totags = [123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 3
    length = 5
    totagsoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = [3, 3, 3, 3, 3]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_filltags_to8_const_4():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    length = 3
    totagsoffset = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = [123, 123, 123, 0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_filltags_to8_const_5():
    totags = [123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 2
    length = 2
    totagsoffset = 2
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_const')
    ret_pass = funcC(totags, totagsoffset, length, base)
    pytest_totags = [123, 123, 2, 2]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

