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

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_1():
    nextshifts = []
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = []
    index = (ctypes.c_int32*len(index))(*index)
    length = 0
    shifts = []
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = []
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_2():
    nextshifts = [123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 3, 4, 1, -1, 5, 2]
    index = (ctypes.c_int32*len(index))(*index)
    length = 7
    shifts = [0, 0, 1, 0, 0, 1, 0]
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = [0, 0, 1, 0, 2, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_3():
    nextshifts = [123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 3, 4, 1, -1, 5, 2]
    index = (ctypes.c_int32*len(index))(*index)
    length = 7
    shifts = [0, 1, 1, 0, 1, 1, 0]
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = [0, 1, 1, 0, 2, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_4():
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, -1, 3, 5, 6, 1, -1, 4, -1, 7, 2, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 25
    shifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = [0, 1, 1, 1, 1, 2, 3, 3, 6]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_5():
    nextshifts = [123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, -1, 4, 1, 3, 5, 2]
    index = (ctypes.c_int32*len(index))(*index)
    length = 7
    shifts = [0, 1, 1, 0, 1, 1, 0]
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = [0, 2, 1, 2, 2, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64_6():
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [-1, -1, 3, 5, 6, -1, -1, -1, -1, 7, 0, -1, 4, -1, 8, 1, 2]
    index = (ctypes.c_int32*len(index))(*index)
    length = 17
    shifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    shifts = (ctypes.c_int64*len(shifts))(*shifts)
    funcC = getattr(lib, 'awkward_IndexedArray32_reduce_next_nonlocal_nextshifts_fromshifts_64')
    ret_pass = funcC(nextshifts, index, length, shifts)
    pytest_nextshifts = [2, 2, 2, 6, 6, 7, 8, 8, 8]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

