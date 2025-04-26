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

def test_unit_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_1():
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 0
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_2():
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 1
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_outindex = [-1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    pytest_tocarry = [123]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_3():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    length = 4
    mask = [0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_outindex = [-1, -1, -1, -1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    pytest_tocarry = [123, 123, 123, 123]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

