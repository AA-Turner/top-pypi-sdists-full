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

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = []
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 0
    maxcount = 0
    distinctslen = 0
    nextlen = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = []
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = []
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [0]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = []
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_2():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = []
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 3
    maxcount = 5
    distinctslen = 0
    nextlen = 15
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 5, 10, 15]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [4]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = []
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_3():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = [123, 123]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 3
    maxcount = 5
    distinctslen = 2
    nextlen = 15
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 5, 10, 15]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [4]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = [0, 0]
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_4():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = [123, 123]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 2
    maxcount = 3
    distinctslen = 2
    nextlen = 6
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 3, 6]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 3, 1, 4, 2, 5]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 1, 1, 2, 2]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [2]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = [0, 0]
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_5():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = [123, 123, 123, 123, 123, 123]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 5
    maxcount = 5
    distinctslen = 6
    nextlen = 17
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 5, 8, 11, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 5, 8, 11, 14, 17]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [4]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = [0, 0, 0, 0, 0, -1]
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_6():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = [123, 123, 123, 123, 123, 123]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 10
    maxcount = 3
    distinctslen = 6
    nextlen = 18
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [5]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = [0, 0, 0, 1, 1, 1]
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_preparenext_64_7():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    maxnextparents = [123]
    maxnextparents = (ctypes.c_int64*len(maxnextparents))(*maxnextparents)
    distincts = [123, 123, 123, 123, 123, 123]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    length = 10
    maxcount = 4
    distinctslen = 6
    nextlen = 18
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, nextlen, maxnextparents, distincts, distinctslen, offsetscopy, offsets, length, parents, maxcount)
    pytest_nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 2, 6]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    pytest_maxnextparents = [6]
    assert maxnextparents[:len(pytest_maxnextparents)] == pytest.approx(pytest_maxnextparents)
    pytest_distincts = [0, 0, 0, -1, 1, 1]
    assert distincts[:len(pytest_distincts)] == pytest.approx(pytest_distincts)
    assert not ret_pass.str

