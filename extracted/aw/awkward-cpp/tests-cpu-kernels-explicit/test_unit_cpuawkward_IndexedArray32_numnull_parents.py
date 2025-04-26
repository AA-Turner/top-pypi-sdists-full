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

def test_unit_cpuawkward_IndexedArray32_numnull_parents_1():
    numnull = []
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = []
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 0
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = []
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [0]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_2():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [0]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_3():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [-1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [1]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_4():
    numnull = [123, 123, 123, 123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [-1, -1, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [1, 1, 1, 1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [4]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_5():
    numnull = [123, 123, 123, 123, 123, 123, 123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [0, -1, 2, -1, -1, -1, -1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [0, 1, 0, 1, 1, 1, 1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [5]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_6():
    numnull = [123, 123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [0, 0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [0]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_7():
    numnull = [123, 123, 123, 123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [0, 1, 2, 3]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [0, 0, 0, 0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [0]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_numnull_parents_8():
    numnull = [123, 123, 123, 123, 123, 123, 123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    tolength = [123]
    tolength = (ctypes.c_int64*len(tolength))(*tolength)
    fromindex = [0, 1, -2, 3, -4, 5, -6]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_numnull_parents')
    ret_pass = funcC(numnull, tolength, fromindex, lenindex)
    pytest_numnull = [0, 0, 1, 0, 1, 0, 1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    pytest_tolength = [3]
    assert tolength[:len(pytest_tolength)] == pytest.approx(pytest_tolength)
    assert not ret_pass.str

