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

def test_unit_cpuawkward_RegularArray_getitem_carry_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_2():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = []
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 0
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_3():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = []
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 0
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_4():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_5():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 6
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 0, 0, 1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_6():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 2, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 5
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 0, 0, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 10
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 10
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 0, 1, 2, 3, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_11():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 1, 1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_12():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_13():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 6
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_14():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 2, 3, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_15():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 2, 4]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_16():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 3, 6, 9]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 3, 1, 4, 2, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 6
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_18():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 4, 8, 10]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 50, 51, 52, 53, 54]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_19():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_20():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 12
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_21():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 12
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_22():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 0, 0, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_23():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 2, 2, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 10, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_24():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [10, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_25():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 5, 8, 11]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [10, 11, 12, 13, 14, 25, 26, 27, 28, 29, 40, 41, 42, 43, 44, 55, 56, 57, 58, 59]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_26():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_27():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [3, 4, 5, 0, 1, 2, 0, 1, 2, 3, 4, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 12
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_28():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 12
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_29():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [3, 4, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_30():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [4, 4, 4, 4]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_31():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [4]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [20, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_32():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_33():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_34():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_35():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 2, 3, 0, 1, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_36():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_37():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0, 0, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [3, 4, 5, 0, 1, 2, 0, 1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_38():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_39():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_40():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_41():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5, 6, 7, 8, 9, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_42():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_43():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 2, 3, 4, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 5
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_44():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_45():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 3, 6, 10]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 50, 51, 52, 53, 54]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_46():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 4, 0, 5]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_carry_64_47():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 1, 1, 2]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 4
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [8, 9, 10, 11, 4, 5, 6, 7, 4, 5, 6, 7, 8, 9, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

