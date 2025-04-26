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

def test_cpuawkward_BitMaskedArray_to_ByteMaskedArray_1():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    frombitmask = [1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_ByteMaskedArray_2():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    frombitmask = [0, 0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_ByteMaskedArray_3():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    frombitmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_ByteMaskedArray_4():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    assert not ret_pass.str

def test_cpuawkward_BitMaskedArray_to_ByteMaskedArray_5():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tobytemask = (ctypes.c_int8*len(tobytemask))(*tobytemask)
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    frombitmask = (ctypes.c_uint8*len(frombitmask))(*frombitmask)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = getattr(lib, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    ret_pass = funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)
    pytest_tobytemask = [np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_]
    assert not ret_pass.str

