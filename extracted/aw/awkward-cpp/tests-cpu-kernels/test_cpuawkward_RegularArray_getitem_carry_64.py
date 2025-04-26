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

def test_cpuawkward_RegularArray_getitem_carry_64_1():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_2():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_4():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [6, 7, 8, 9, 10, 11, 9, 10, 11]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_6():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_7():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_8():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_10():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_11():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_12():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_13():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [3, 4, 5, 0, 1, 2, 6, 7, 8]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_14():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_15():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_16():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_18():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_19():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_carry_64_20():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    fromcarry = (ctypes.c_int64*len(fromcarry))(*fromcarry)
    lencarry = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_carry_64')
    ret_pass = funcC(tocarry, fromcarry, lencarry, size)
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert not ret_pass.str

