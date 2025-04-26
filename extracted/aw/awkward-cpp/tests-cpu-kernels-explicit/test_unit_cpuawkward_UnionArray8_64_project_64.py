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

def test_unit_cpuawkward_UnionArray8_64_project_64_1():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 0
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [0]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_2():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 0
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [0]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_3():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 1
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [1]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_4():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 2
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [2]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_5():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 2
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [2]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_6():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 2
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [2]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_7():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 3]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 2
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [2]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_8():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 3]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 2
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [2]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_9():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_10():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_11():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2, 3, 4]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 5
    which = 0
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [5]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_project_64_12():
    lenout = [123]
    lenout = (ctypes.c_int64*len(lenout))(*lenout)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2, 3, 4]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    fromtags = [1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 5
    which = 1
    funcC = getattr(lib, 'awkward_UnionArray8_64_project_64')
    ret_pass = funcC(lenout, tocarry, fromtags, fromindex, length, which)
    pytest_lenout = [5]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

