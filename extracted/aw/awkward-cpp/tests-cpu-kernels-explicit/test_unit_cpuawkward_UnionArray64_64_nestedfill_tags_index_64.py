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

def test_unit_cpuawkward_UnionArray64_64_nestedfill_tags_index_64_1():
    totags = []
    totags = (ctypes.c_int64*len(totags))(*totags)
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tmpstarts = []
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    tmpstarts = []
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    fromcounts = []
    fromcounts = (ctypes.c_int64*len(fromcounts))(*fromcounts)
    length = 0
    tag = 0
    funcC = getattr(lib, 'awkward_UnionArray64_64_nestedfill_tags_index_64')
    ret_pass = funcC(totags, toindex, tmpstarts, tag, fromcounts, length)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tmpstarts = []
    assert tmpstarts[:len(pytest_tmpstarts)] == pytest.approx(pytest_tmpstarts)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_64_nestedfill_tags_index_64_2():
    totags = [123]
    totags = (ctypes.c_int64*len(totags))(*totags)
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tmpstarts = [123]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    tmpstarts = [0]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    fromcounts = [1]
    fromcounts = (ctypes.c_int64*len(fromcounts))(*fromcounts)
    length = 1
    tag = 1
    funcC = getattr(lib, 'awkward_UnionArray64_64_nestedfill_tags_index_64')
    ret_pass = funcC(totags, toindex, tmpstarts, tag, fromcounts, length)
    pytest_totags = [1]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tmpstarts = [1]
    assert tmpstarts[:len(pytest_tmpstarts)] == pytest.approx(pytest_tmpstarts)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_64_nestedfill_tags_index_64_3():
    totags = [123, 123, 123]
    totags = (ctypes.c_int64*len(totags))(*totags)
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tmpstarts = [123, 123]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    tmpstarts = [0, 1]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    fromcounts = [1, 2]
    fromcounts = (ctypes.c_int64*len(fromcounts))(*fromcounts)
    length = 2
    tag = 0
    funcC = getattr(lib, 'awkward_UnionArray64_64_nestedfill_tags_index_64')
    ret_pass = funcC(totags, toindex, tmpstarts, tag, fromcounts, length)
    pytest_totags = [0, 0, 0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tmpstarts = [1, 3]
    assert tmpstarts[:len(pytest_tmpstarts)] == pytest.approx(pytest_tmpstarts)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_64_nestedfill_tags_index_64_4():
    totags = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int64*len(totags))(*totags)
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tmpstarts = [123, 123, 123, 123, 123]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    tmpstarts = [0, 5, 5, 6, 8]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    fromcounts = [5, 0, 2, 3, 1]
    fromcounts = (ctypes.c_int64*len(fromcounts))(*fromcounts)
    length = 5
    tag = 1
    funcC = getattr(lib, 'awkward_UnionArray64_64_nestedfill_tags_index_64')
    ret_pass = funcC(totags, toindex, tmpstarts, tag, fromcounts, length)
    pytest_totags = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 7, 8, 10]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tmpstarts = [5, 5, 7, 9, 9]
    assert tmpstarts[:len(pytest_tmpstarts)] == pytest.approx(pytest_tmpstarts)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray64_64_nestedfill_tags_index_64_5():
    totags = [123, 123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int64*len(totags))(*totags)
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    tmpstarts = [123, 123, 123, 123, 123]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    tmpstarts = [0, 2, 4, 5, 7]
    tmpstarts = (ctypes.c_int64*len(tmpstarts))(*tmpstarts)
    fromcounts = [2, 3, 2, 2, 0]
    fromcounts = (ctypes.c_int64*len(fromcounts))(*fromcounts)
    length = 5
    tag = 1
    funcC = getattr(lib, 'awkward_UnionArray64_64_nestedfill_tags_index_64')
    ret_pass = funcC(totags, toindex, tmpstarts, tag, fromcounts, length)
    pytest_totags = [1, 1, 1, 1, 1, 1, 1]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    pytest_toindex = [0, 1, 2, 3, 5, 7, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tmpstarts = [2, 5, 6, 7, 7]
    assert tmpstarts[:len(pytest_tmpstarts)] == pytest.approx(pytest_tmpstarts)
    assert not ret_pass.str

