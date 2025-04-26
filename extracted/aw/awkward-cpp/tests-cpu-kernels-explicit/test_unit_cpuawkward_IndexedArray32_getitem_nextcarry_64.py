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

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = []
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 0
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_2():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_3():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 1, 0, 2, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_5():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 6
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_6():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_7():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_8():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 1
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 3
    lenindex = 9
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 2, 3, 3, 4]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0, 2, 3, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_11():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 2
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_12():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 3
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_13():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2, 3]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_14():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1, 2, 3, 4]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_15():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 1, 1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 6
    lenindex = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_16():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_17():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 6
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_18():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 3
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_19():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 3]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 6
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_20():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 1, 0, 3, 3, 4]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 6
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2, 1, 0, 3, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_21():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 2, 1, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 3
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_22():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 2, 1, 0, 3]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2, 2, 1, 0, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_23():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 3
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_24():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_25():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [2, 4, 4, 0, 8]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 10
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [2, 4, 4, 0, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_26():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [3, 2, 1, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 4
    lenindex = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_27():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [4, 3, 2, 1, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [4, 3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_28():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [4]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 5
    lenindex = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_29():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [6, 4, 4, 8, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 10
    lenindex = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [6, 4, 4, 8, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_getitem_nextcarry_64_30():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [6, 5, 4, 3, 2, 1, 0]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    lencontent = 7
    lenindex = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [6, 5, 4, 3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

