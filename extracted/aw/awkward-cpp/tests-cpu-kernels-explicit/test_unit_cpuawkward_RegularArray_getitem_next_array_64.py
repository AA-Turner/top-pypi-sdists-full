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

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_1():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = []
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 0
    length = 0
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_2():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_3():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_4():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_5():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 0, 1, 1, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 0, 1, 1, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_6():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_7():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_8():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_9():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_10():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_11():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_12():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_13():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 0, 1, 0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_14():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_15():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_16():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_17():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3, 4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_18():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3, 4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 7
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_19():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_20():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 3, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_21():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_22():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_23():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 1, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_24():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_25():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_26():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_27():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_28():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_29():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_30():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_31():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_32():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 2
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_33():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 3
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 4, 7, 8, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_34():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_35():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_36():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_37():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 0, 1, 1, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0, 1, 1, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_38():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_39():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_40():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0, 1, 3, 2, 3, 5, 4, 5, 7, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_41():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 0, 1, 0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0, 3, 2, 5, 4, 7, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_42():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_43():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_44():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_45():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_46():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_47():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_48():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_49():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_50():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_51():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3, 4, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_52():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_53():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 4, 0, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 4, 0, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_54():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_55():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_56():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 0, 0, 1, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0, 0, 1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_57():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 0, 0, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0, 0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_58():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 0, 0, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0, 0, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_59():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_60():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_61():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 1, 1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 1, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_62():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 1, 1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 2
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 1, 1, 3, 6, 5, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_63():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 1, 1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 3
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 1, 1, 3, 6, 5, 5, 7, 10, 9, 9, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_64():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_65():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_66():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_67():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_68():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_69():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_70():
    toadvanced = [123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 3, 4, 5, 6]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    length = 1
    size = 7
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 3, 4, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_71():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_72():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_73():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 1, 1, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 10
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 1, 1, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_74():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 2, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_75():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 2, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 2, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_76():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 3, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_77():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_78():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [3, 6, 8, 6]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 10
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 6, 8, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_79():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_80():
    toadvanced = [123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4, 3, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_81():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4, 3, 2, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 3, 2, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_82():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_83():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4, 4, 4, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 4, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_84():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_85():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [7, 3, 0, 2, 3, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [7, 3, 0, 2, 3, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_86():
    toadvanced = [123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [7, 3, 2, 0, 2, 3, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 7
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5, 6]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [7, 3, 2, 0, 2, 3, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_64_87():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [7, 3, 2, 0, 3, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    length = 1
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromarray, length, lenarray, size)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [7, 3, 2, 0, 3, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

