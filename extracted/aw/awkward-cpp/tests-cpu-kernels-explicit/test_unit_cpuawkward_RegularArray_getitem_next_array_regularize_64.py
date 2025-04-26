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

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_1():
    toarray = []
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = []
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 0
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = []
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_2():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_3():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_4():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_5():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_6():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_7():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_8():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_9():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_10():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_11():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_12():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 1, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_13():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_14():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_15():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 1, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_16():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 2, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_17():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 2, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_18():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_19():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_20():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3, 4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3, 4, 5]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_21():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3, 4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 7
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3, 4, 5]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_22():
    toarray = [123, 123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_23():
    toarray = [123, 123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 3, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_24():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_25():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_26():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 1, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 1, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_27():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_28():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_29():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2, 1, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_30():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_31():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_32():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 2, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_33():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_34():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_35():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_36():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_37():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_38():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_39():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_40():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 1, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_41():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_42():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_43():
    toarray = [123, 123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 1, 1, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 6
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 1, 1, 1, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_44():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 1, 1, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_45():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_46():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_47():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_48():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_49():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 2, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_50():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 2, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_51():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 2, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_52():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_53():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_54():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 3, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_55():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 3, 4, 6, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 9
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 3, 4, 6, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_56():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_57():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 0, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_58():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 0, 0, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_59():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_60():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_61():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_62():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 2, 2, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_63():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 2, 2, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_64():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_65():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_66():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_67():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_68():
    toarray = [123, 123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 4, 5, 6]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 5
    size = 7
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 3, 4, 5, 6]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_69():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_70():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3, 1, 1, 7]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 10
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3, 1, 1, 7]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_71():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3, 2, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3, 2, 1, 0]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_72():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3, 2, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 4
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3, 2, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_73():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_74():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3, 3, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3, 3, 3]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_75():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [3, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [3, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_76():
    toarray = [123, 123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [4, 3, 2, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 4
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [4, 3, 2, 1]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_77():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [4, 3, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 8
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [4, 3, 2]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_78():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 1
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_79():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [4, 4]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 5
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [4, 4]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_next_array_regularize_64_80():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [4, 5]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 2
    size = 6
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [4, 5]
    assert toarray[:len(pytest_toarray)] == pytest.approx(pytest_toarray)
    assert not ret_pass.str

