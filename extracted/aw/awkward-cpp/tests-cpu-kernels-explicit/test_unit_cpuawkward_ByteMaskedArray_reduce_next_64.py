# AUTO GENERATED ON 2026-08-14 AT 14:44:29
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

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 0
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, mask, offsets, outlength, validwhen)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_2():
    nextcarry = [123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0, 0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    offsets = [0, 2, 4, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 3
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, mask, offsets, outlength, validwhen)
    pytest_nextcarry = [0, 1, 2, 5, 6]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2, 3, 5]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, -1, -1, 3, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_3():
    nextcarry = [123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    offsets = [0, 0, 0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 3
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, mask, offsets, outlength, validwhen)
    pytest_nextcarry = [0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 0, 0, 1]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_4():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    offsets = [0, 0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 2
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, mask, offsets, outlength, validwhen)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 0, 0]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [-1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_5():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0, 1, 0, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    offsets = [0, 2, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 2
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, mask, offsets, outlength, validwhen)
    pytest_nextcarry = [1, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 1, 3]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [-1, 0, -1, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

