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

def test_cpuawkward_UnionArray8_32_project_64_1():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_2():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_3():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 3, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_4():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 4, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_5():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_6():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_7():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_8():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 3, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_9():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 4, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_10():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_11():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_12():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_13():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 3, 0]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_14():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [1, 4, 2]
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_32_project_64_15():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_32_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

