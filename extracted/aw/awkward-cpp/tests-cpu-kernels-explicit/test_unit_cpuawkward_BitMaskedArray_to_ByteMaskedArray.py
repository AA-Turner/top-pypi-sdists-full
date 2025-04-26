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

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_1():
    tobytemask = []
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 0
    frombitmask = []
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = []
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_2():
    tobytemask = []
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 0
    frombitmask = []
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = []
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_3():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 1
    frombitmask = [66]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 1, 0, 0, 0, 0, 1, 0]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_4():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 2
    frombitmask = [58, 59]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_5():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 1
    frombitmask = [27]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 0, 0, 1, 1, 0, 1, 1]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_6():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 3
    frombitmask = [1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_7():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 3
    frombitmask = [1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_8():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 4
    frombitmask = [0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = False
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_9():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 4
    frombitmask = [0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

def test_unit_cpuawkward_BitMaskedArray_to_ByteMaskedArray_10():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    bitmasklength = 2
    frombitmask = [58, 59]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    lsb_order = True
    validwhen = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)
    assert not ret_pass.str

