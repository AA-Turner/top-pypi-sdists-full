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

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    length = 0
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, mask, parents, length, validwhen)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_2():
    nextcarry = [123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0, 0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    parents = [0, 0, 1, 1, 2, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    length = 7
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, mask, parents, length, validwhen)
    pytest_nextcarry = [0, 1, 2, 5, 6]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 1, 2, 2]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, -1, -1, 3, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_3():
    nextcarry = [123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    parents = [2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    length = 1
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, mask, parents, length, validwhen)
    pytest_nextcarry = [0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [2]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_4():
    nextcarry = [123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    parents = [1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    length = 1
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, mask, parents, length, validwhen)
    pytest_nextcarry = [123]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [123]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [-1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_64_5():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0, 1, 0, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    parents = [0, 0, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    length = 5
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, mask, parents, length, validwhen)
    pytest_nextcarry = [1, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 1, 1]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [-1, 0, -1, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

