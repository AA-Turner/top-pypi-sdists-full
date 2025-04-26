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

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_1():
    nextshifts = []
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = []
    index = (ctypes.c_int64*len(index))(*index)
    length = 0
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = []
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_2():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, 2, -1, 3, -1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 0, 1, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_3():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, 2, -1, -1, -1, -1, 7, 8]
    index = (ctypes.c_int64*len(index))(*index)
    length = 9
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 0, 4, 4]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_4():
    nextshifts = [123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, -1, 2, 3, -1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 1, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_5():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, -1, 2, 3, 4]
    index = (ctypes.c_int64*len(index))(*index)
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 1, 1, 1]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_6():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, -1, 2, 3, -1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 1, 1, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_7():
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, -1, 2, 3, -1, 4, 5, -1, 6, 7, -1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 12
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 1, 1, 2, 2, 3, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_8():
    nextshifts = [123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [0, 1, -1, -1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_9():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [4, 2, -1, -1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [0, 0, 2, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_10():
    nextshifts = [123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [-1, -1, 0, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [2, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64_11():
    nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    index = [-1, -1, 0, 1, 2, -1, -1, -1, 3, -1, 4, 5, -1, -1, 6, 7, 8]
    index = (ctypes.c_int64*len(index))(*index)
    length = 17
    funcC = getattr(lib, 'awkward_IndexedArray64_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, index, length)
    pytest_nextshifts = [2, 2, 2, 5, 6, 6, 8, 8, 8]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

