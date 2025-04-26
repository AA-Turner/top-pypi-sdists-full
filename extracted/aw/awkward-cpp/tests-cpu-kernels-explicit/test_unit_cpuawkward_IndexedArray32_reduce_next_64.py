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

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = []
    index = (ctypes.c_int32*len(index))(*index)
    length = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_2():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 2
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [0, 1]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_3():
    nextcarry = [123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 3, 4, 5, 6]
    index = (ctypes.c_int32*len(index))(*index)
    length = 7
    parents = [0, 0, 2, 2, 3, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [0, 1, 2, 3, 4, 5, 6]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 2, 2, 3, 4, 4]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, 3, 4, 5, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_4():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2]
    index = (ctypes.c_int32*len(index))(*index)
    length = 2
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [1, 2]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_5():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2, 3]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [1, 2, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_6():
    nextcarry = [123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 2, 3, 4]
    index = (ctypes.c_int32*len(index))(*index)
    length = 4
    parents = [0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [1, 2, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_7():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [2, 3]
    index = (ctypes.c_int32*len(index))(*index)
    length = 2
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [2, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_8():
    nextcarry = [123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [2, 3, 4]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [2, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_9():
    nextcarry = [123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [3, 4]
    index = (ctypes.c_int32*len(index))(*index)
    length = 2
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_10():
    nextcarry = [123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [4, 3, 2, 1, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 5
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [4, 3, 2, 1, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 0, 0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, 3, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_11():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [5, 2, 4, 1, 3, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 6
    parents = [0, 0, 1, 1, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [5, 2, 4, 1, 3, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 1, 1, 2, 2]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_64_12():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [5, 4, 3, 2, 1, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 6
    parents = [0, 0, 0, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_64')
    ret_pass = funcC(nextcarry, nextparents, outindex, index, parents, length)
    pytest_nextcarry = [5, 4, 3, 2, 1, 0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 1, 1, 1]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_outindex = [0, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

