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

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_1():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 4
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent).str.decode('utf-8') == "stops[i] > len(content)"

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_2():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -4, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_3():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_4():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 4
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_5():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = []
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = []
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 0
    lenstarts = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_6():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 1, 2, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_7():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_8():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_9():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_10():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [1, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_11():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 10, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 15, 15, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [10, 11, 14, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_12():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_13():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 10, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 15, 15, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [11, 10, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_14():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, -2, 0, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 10, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 15, 15, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [11, 13, 10, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_15():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, -2, 0, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 0, 0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 5, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [11, 3, 0, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_16():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 15, 15, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 20, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 15, 15, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_17():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_18():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 10, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 15, 15, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [12, 10, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_19():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 2, 2, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 0, 0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 5, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [12, 2, 2, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_20():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-2, -2, -2, -2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 10, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 15, 15, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [13, 13, 13, 13]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_21():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-2, -2, -2, -2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [10, 0, 0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15, 5, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [13, 3, 3, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_22():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 3, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_23():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 5, 10, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 5, 10, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_24():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [15, 0, 0, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 5, 5, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [15, 1, 4, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_25():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [15, 15, 15, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 20, 20, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [15, 16, 19, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_26():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [15, 15, 15, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 20, 20, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [16, 15, 15, 16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_27():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [15, 0, 0, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 5, 5, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [19, 4, 4, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_28():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_29():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_30():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 2]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [1, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 4
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_31():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [2, 5, 5, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_32():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 3, 3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 0, 0, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_33():
    toadvanced = [123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_34():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [1, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 4
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_35():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 3, 3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 1, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_36():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_37():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [3, 4, 5, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_38():
    toadvanced = [123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_39():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 1, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 0, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 3, 3, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 1, 0, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_40():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 15, 15, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 20, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 19, 19, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_41():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, -1, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 3, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 2, 0, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_42():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 0, 0, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 3, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 6, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 3, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_43():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 5, 10, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 9, 14, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_44():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3, 4, 5]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [2, 0, 1, 1, 2, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 3, 3, 3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 3, 6, 6, 6, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3, 4, 5]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [5, 0, 4, 4, 5, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_45():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [0, 1, -1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [5, 0, 0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 5, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [5, 1, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_46():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [3, 0, 0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 3, 3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [5, 2, 2, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_47():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [1, 1, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [6, 0, 0, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [9, 3, 3, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [7, 1, 0, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_advanced_64_48():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromadvanced = [0, 1, 2, 3]
    fromadvanced = (ctypes.c_int64*len(fromadvanced))(*fromadvanced)
    fromarray = [-1, -1, -1, -1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [5, 0, 0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 5, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_advanced_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [9, 4, 4, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

