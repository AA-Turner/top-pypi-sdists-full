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

def test_cpuawkward_ListArray64_getitem_next_array_64_1():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    assert funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent).str

def test_cpuawkward_ListArray64_getitem_next_array_64_2():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [2, 2, 2, 1, 1, 1, 1, 1, 1]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_array_64_3():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [3, 4, 4, 2, 3, 3, 2, 3, 3]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_array_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [3, 2, 1, 2, 1, 0, 2, 1, 0]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_array_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [2, 1, 3, 1, 0, 2, 1, 0, 2]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_array_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [1, 1, 1, 0, 0, 0, 0, 0, 0]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_array_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = (ctypes.c_int64*len(toadvanced))(*toadvanced)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = (ctypes.c_int64*len(fromarray))(*fromarray)
    lenstarts = 3
    lenarray = 3
    lencontent = 6
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_array_64')
    ret_pass = funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)
    pytest_tocarry = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert not ret_pass.str

