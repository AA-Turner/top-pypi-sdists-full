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

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_1():
    nextshifts = []
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 0
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = []
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_2():
    nextshifts = [123, 123, 123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 7
    mask = [0, 0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = [0, 0, 0, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_3():
    nextshifts = [123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 1
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = [0]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_4():
    nextshifts = [123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 1
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = [123]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_5():
    nextshifts = [123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 7
    mask = [0, 0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = [3, 3]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_6():
    nextshifts = [123, 123, 123]
    nextshifts = (ctypes.c_int64*len(nextshifts))(*nextshifts)
    length = 5
    mask = [0, 1, 0, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    valid_when = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
    ret_pass = funcC(nextshifts, mask, length, valid_when)
    pytest_nextshifts = [1, 2, 2]
    assert nextshifts[:len(pytest_nextshifts)] == pytest.approx(pytest_nextshifts)
    assert not ret_pass.str

