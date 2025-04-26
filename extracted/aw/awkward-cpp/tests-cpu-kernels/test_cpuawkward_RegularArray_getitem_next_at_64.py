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

def test_cpuawkward_RegularArray_getitem_next_at_64_1():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0, 3, 6]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_at_64_2():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    length = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [0, 3, 6]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_at_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 2
    length = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [2, 5, 8]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_next_at_64_4():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    length = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_next_at_64')
    ret_pass = funcC(tocarry, at, length, size)
    pytest_tocarry = [1, 4, 7]
    assert not ret_pass.str

