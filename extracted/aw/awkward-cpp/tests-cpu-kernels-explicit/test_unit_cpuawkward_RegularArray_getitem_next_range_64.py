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

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 0
    nextsize = 0
    regular_start = 0
    size = 0
    step = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 0
    size = 1
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_3():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 0
    size = 2
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_4():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_5():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 0
    size = 3
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_6():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 0
    size = 5
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_7():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 0
    size = 2
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_8():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 0
    size = 3
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_9():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 3
    regular_start = 0
    size = 3
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_10():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 4
    regular_start = 0
    size = 4
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_11():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 4
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_12():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 2
    nextsize = 2
    regular_start = 0
    size = 2
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_13():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 5
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_14():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 5
    regular_start = 0
    size = 6
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_15():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 6
    regular_start = 0
    size = 6
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_16():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 8
    regular_start = 0
    size = 8
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 10
    regular_start = 0
    size = 10
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_18():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 3
    nextsize = 5
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_19():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 5
    nextsize = 5
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_20():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 2
    nextsize = 4
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_21():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 3
    nextsize = 4
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_22():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 5
    nextsize = 4
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_23():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 6
    nextsize = 4
    regular_start = 0
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 28]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_24():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 0
    size = 3
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_25():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 0
    size = 5
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_26():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 3
    regular_start = 0
    size = 5
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_27():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 3
    regular_start = 0
    size = 6
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_28():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 5
    nextsize = 3
    regular_start = 0
    size = 5
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_29():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 6
    nextsize = 3
    regular_start = 0
    size = 5
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, 27, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_30():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 4
    regular_start = 0
    size = 8
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 2, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_31():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 0
    size = 5
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [0, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_32():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 1
    size = 2
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_33():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 1
    size = 3
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_34():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 1
    size = 3
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_35():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 1
    size = 5
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_36():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 1
    size = 3
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_37():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 1
    size = 4
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_38():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 3
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_39():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 4
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_40():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 5
    regular_start = 1
    size = 6
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_41():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 3
    nextsize = 4
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_42():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 5
    nextsize = 4
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_43():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 6
    nextsize = 4
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_44():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 2
    nextsize = 4
    regular_start = 1
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_45():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 1
    size = 5
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_46():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 1
    size = 5
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_47():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 2
    size = 3
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_48():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 2
    size = 3
    step = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_49():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 2
    size = 3
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_50():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 1
    regular_start = 2
    size = 5
    step = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_51():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 3
    regular_start = 2
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_range_64_52():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    nextsize = 2
    regular_start = 3
    size = 5
    step = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_range_64')
    ret_pass = funcC(tocarry, regular_start, step, length, size, nextsize)
    pytest_tocarry = [3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

