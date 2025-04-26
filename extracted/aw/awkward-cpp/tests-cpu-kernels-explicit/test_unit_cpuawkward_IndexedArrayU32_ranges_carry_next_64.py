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

def test_unit_cpuawkward_IndexedArrayU32_ranges_carry_next_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    index = []
    index = (ctypes.c_uint32*len(index))(*index)
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 0
    funcC = getattr(lib, 'awkward_IndexedArrayU32_ranges_carry_next_64')
    ret_pass = funcC(index, fromstarts, fromstops, length, tocarry)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_ranges_carry_next_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    index = [1]
    index = (ctypes.c_uint32*len(index))(*index)
    fromstarts = [0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 1
    funcC = getattr(lib, 'awkward_IndexedArrayU32_ranges_carry_next_64')
    ret_pass = funcC(index, fromstarts, fromstops, length, tocarry)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArrayU32_ranges_carry_next_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    index = [0, 1, 2]
    index = (ctypes.c_uint32*len(index))(*index)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_ranges_carry_next_64')
    ret_pass = funcC(index, fromstarts, fromstops, length, tocarry)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

