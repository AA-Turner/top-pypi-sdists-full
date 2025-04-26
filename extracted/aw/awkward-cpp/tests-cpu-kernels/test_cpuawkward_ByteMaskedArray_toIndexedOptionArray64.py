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

def test_cpuawkward_ByteMaskedArray_toIndexedOptionArray64_1():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    mask = [1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_toIndexedOptionArray64')
    ret_pass = funcC(toindex, mask, length, validwhen)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_toIndexedOptionArray64_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    mask = [0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_toIndexedOptionArray64')
    ret_pass = funcC(toindex, mask, length, validwhen)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_toIndexedOptionArray64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_toIndexedOptionArray64')
    ret_pass = funcC(toindex, mask, length, validwhen)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_toIndexedOptionArray64_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_toIndexedOptionArray64')
    ret_pass = funcC(toindex, mask, length, validwhen)
    pytest_toindex = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_toIndexedOptionArray64_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_toIndexedOptionArray64')
    ret_pass = funcC(toindex, mask, length, validwhen)
    pytest_toindex = [-1, -1, -1]
    assert not ret_pass.str

