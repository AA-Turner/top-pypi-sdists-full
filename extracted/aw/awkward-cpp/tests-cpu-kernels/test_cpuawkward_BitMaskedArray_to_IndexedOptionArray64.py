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

def test_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frombitmask = [1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frombitmask = [0, 0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frombitmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, -1, 8, 9, 10, 11, 12, 13, 14, -1, 16, 17, 18, 19, 20, 21, 22, -1]
    assert not ret_pass.str

