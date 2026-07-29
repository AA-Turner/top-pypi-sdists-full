# AUTO GENERATED ON 2026-07-28 AT 17:37:39
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

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = []
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 0
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_2():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [0, 1]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_3():
    nextcarry = [123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 3, 4, 5, 6]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2, 2, 4, 5, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [0, 1, 2, 3, 4, 5, 6]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2, 2, 4, 5, 7]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, 3, 4, 5, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_4():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [1, 2]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_5():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [1, 2, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 3]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_6():
    nextcarry = [123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2, 3, 4]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 4]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [1, 2, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 4]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_7():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [2, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_8():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [2, 3, 4]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [2, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 3]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_9():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [3, 4]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_10():
    nextcarry = [123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [4, 3, 2, 1, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [4, 3, 2, 1, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 5]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, 3, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_11():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [5, 2, 4, 1, 3, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 2, 4, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [5, 2, 4, 1, 3, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2, 4, 6]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_reduce_next_64_12():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [5, 4, 3, 2, 1, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    outlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextoffsets, outindex, index, offsets, outlength)
    pytest_nextcarry = [5, 4, 3, 2, 1, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 3, 6]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    pytest_outindex = [0, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

