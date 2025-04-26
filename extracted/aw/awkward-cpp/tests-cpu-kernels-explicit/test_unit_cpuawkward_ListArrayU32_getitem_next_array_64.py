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

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_1():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [-3, 0, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 4
    lencontent = 3
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_2():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [5, 4, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 8, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 2
    lencontent = 13
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent).str.decode('utf-8') == "stops[i] < starts[i]"

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_3():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [4, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 14]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 2
    lencontent = 13
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent).str.decode('utf-8') == "stops[i] > len(content)"

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_4():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 0, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 4
    lencontent = 3
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 0, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_5():
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0, 4, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 8, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 2
    lencontent = 13
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = [0, 1, 0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [0, 3, 4, 7, 8, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_6():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [1, 1, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 4
    lencontent = 3
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [1, 1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_7():
    toadvanced = []
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = []
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 0
    lencontent = 0
    lenstarts = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = []
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_8():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [0, 3]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [4, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [8, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 2
    lencontent = 13
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = [0, 1, 0, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [4, 7, 8, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_array_64_9():
    toadvanced = [123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromarray = [2, 1, 1, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    fromstarts = [6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenarray = 4
    lencontent = 10
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_toadvanced = [0, 1, 2, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)
    pytest_tocarry = [8, 7, 7, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

