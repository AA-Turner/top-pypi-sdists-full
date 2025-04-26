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

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_1():
    missing = []
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = []
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = []
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 0
    maxcount = 0
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 0
    offsets = []
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = []
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = []
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = []
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_2():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 3
    maxcount = 5
    nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 15
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 0, 0, 0, 0]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_3():
    missing = [123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 2
    maxcount = 3
    nextcarry = [0, 3, 1, 4, 2, 5]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 6
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 0, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 0, 0]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_4():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 3
    maxcount = 5
    nextcarry = [0, 5, 9, 1, 6, 10, 2, 7, 11, 3, 8, 4]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 12
    offsets = [0, 5, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 0, 0, 1, 2]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_5():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 5
    maxcount = 5
    nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 17
    offsets = [0, 5, 8, 11, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 0, 0, 4, 4]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_6():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 4
    maxcount = 3
    nextcarry = [0, 2, 5, 7, 1, 3, 6, 8, 4]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 9
    offsets = [0, 2, 5, 7, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 0, 2]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_7():
    missing = [123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 3
    maxcount = 4
    nextcarry = [0, 2, 3, 1, 4, 5, 6]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 7
    offsets = [0, 2, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 1, 2, 2]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 1, 2, 2]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_8():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 10
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 2, 4]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_9():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 2, 4]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_10():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [0, 2, 4]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_11():
    missing = [123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 3
    maxcount = 4
    nextcarry = [0, 3, 1, 4, 2, 5, 6]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 7
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 1, 1, 1, 2]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 1, 0, 1, 0, 1, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 1, 1, 2]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_12():
    missing = [123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 4
    maxcount = 3
    nextcarry = [0, 3, 5, 1, 4, 6, 2]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 7
    offsets = [0, 3, 5, 5, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 0, 0, 1, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 1, 0, 0, 1, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 1, 3]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_13():
    missing = [123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 4
    maxcount = 3
    nextcarry = [0, 3, 5, 1, 4, 6, 2]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 7
    offsets = [0, 3, 3, 5, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 0, 1, 1, 1, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 1, 1, 0, 1, 1, 0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 1, 3]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_14():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_15():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_16():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_17():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_18():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 11
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_19():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_20():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_21():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_22():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_23():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_24():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_25():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1, 3, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_26():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 2, 3, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_27():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2, 1, 2, 2, 3, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_28():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [1, 3, 5]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_29():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 12
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 2, 2, 3, 2, 3, 4, 2, 3, 2]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 3, 3, 3, 2, 4]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [2, 4, 6]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_30():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 13
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 1, 3, 6, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 3, 3, 3, 2, 4]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [2, 4, 6]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_31():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 13
    maxcount = 3
    nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 18
    offsets = [0, 0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [2, 4, 6]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_32():
    missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    missing = (ctypes.c_int64*len(missing))(*missing)
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    nummissing = [123, 123, 123, 123]
    nummissing = (ctypes.c_int64*len(nummissing))(*nummissing)
    length = 9
    maxcount = 4
    nextcarry = [0, 1, 3, 6, 10, 13, 15, 2, 4, 7, 11, 14, 5, 8, 12, 9]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextlen = 16
    offsets = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    parents = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
    ret_pass = funcC(nummissing, missing, nextshifts, offsets, length, starts, parents, maxcount, nextlen, nextcarry)
    pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1]
    assert missing[:len(pytest_missing)] == pytest.approx(pytest_missing)
    pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    pytest_nummissing = [2, 4, 6, 8]
    assert nummissing[:len(pytest_nummissing)] == pytest.approx(pytest_nummissing)
    assert not ret_pass.str

