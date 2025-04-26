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

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 0
    frombitmask = []
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 0
    frombitmask = []
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 1
    frombitmask = [66]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, -1, 2, 3, 4, 5, -1, 7]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 2
    frombitmask = [58, 59]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, -1, 2, -1, -1, -1, 6, 7, -1, -1, 10, -1, -1, -1, 14, 15]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 2
    frombitmask = [58, 59]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, -1, -1, -1, 5, -1, 7, 8, 9, -1, -1, -1, 13, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_6():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 1
    frombitmask = [27]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, -1, -1, 5, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_7():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 3
    frombitmask = [1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, -1, 8, 9, 10, 11, 12, 13, 14, -1, 16, 17, 18, 19, 20, 21, 22, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_8():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 3
    frombitmask = [1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, 23]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_9():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 4
    frombitmask = [0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_IndexedOptionArray64_10():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    bitmasklength = 4
    frombitmask = [0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    ret_pass = funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

