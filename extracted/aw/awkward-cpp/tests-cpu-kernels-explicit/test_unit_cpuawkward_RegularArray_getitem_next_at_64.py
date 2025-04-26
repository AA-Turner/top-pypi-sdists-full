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

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_1():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    length = 1
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    assert funcC(tocarry, at, length, size).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_2():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 6
    length = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    assert funcC(tocarry, at, length, size).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_3():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 1
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_4():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 0
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_5():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_6():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_7():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_8():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_9():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_10():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_11():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_12():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_13():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_14():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_15():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_16():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_17():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_18():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_19():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_20():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 5
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2, 7, 12, 17, 22]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_21():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 3
    length = 1
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_22():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 3
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_23():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 4
    length = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_at_64_24():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 4
    length = 1
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

