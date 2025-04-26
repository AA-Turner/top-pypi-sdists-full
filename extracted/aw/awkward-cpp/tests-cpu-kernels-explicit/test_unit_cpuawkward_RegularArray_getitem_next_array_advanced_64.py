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

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_1():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = []
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = []
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 0
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_2():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_3():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 6, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_4():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, 2, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 4, 8, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_5():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 5, 10, 15]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_6():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, 4, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 6, 14, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_7():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_8():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3, 6, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_9():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 5, 10, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_10():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 3, 0, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 8, 10, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_11():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 5, 10, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_12():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 5, 8, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_13():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 7, 12, 17]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_14():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [3, 3, 3, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 8, 13, 18]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_advanced_64_15():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [4, 4, 4, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    length = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 9, 14, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

