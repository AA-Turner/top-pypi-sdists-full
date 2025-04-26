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

def test_cpuawkward_ByteMaskedArray_numnull_1():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    mask = [1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_numnull_2():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    mask = [0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_numnull_3():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_numnull_4():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_numnull_5():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [3]
    assert not ret_pass.str

