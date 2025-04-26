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

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_1():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_2():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_3():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_4():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_5():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_6():
    toarray = [123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_7():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_8():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_9():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_10():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_11():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [2, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_12():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_13():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_14():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_15():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_16():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [1, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_17():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_18():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_19():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_20():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_21():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_22():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_23():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_24():
    toarray = [123, 123, 123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    ret_pass = funcC(toarray, fromarray, lenarray, size)
    pytest_toarray = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_array_regularize_64_25():
    toarray = [123]
    toarray = (ctypes.c_int64*len(toarray))(*toarray)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenarray = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_array_regularize_64')
    assert funcC(toarray, fromarray, lenarray, size).str

