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

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_1():
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 0
    offsets = [0]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_2():
    nextparents = [123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 1
    offsets = [0, 1]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = [0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_3():
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 18
    offsets = [0, 0, 1, 3, 3, 6, 8, 9, 9, 9, 10, 10, 12, 15, 15, 17, 18, 18, 18]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = [1, 2, 2, 4, 4, 4, 5, 5, 6, 9, 11, 11, 12, 12, 12, 14, 14, 15]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_4():
    nextparents = [123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 4
    offsets = [0, 1, 3, 5, 5]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = [0, 1, 1, 2, 2]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_5():
    nextparents = [123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 5
    offsets = [0, 1, 1, 3, 5, 7]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = [0, 2, 2, 3, 3, 4, 4]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_reduce_local_nextparents_64_6():
    nextparents = [123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    length = 5
    offsets = [0, 0, 1, 1, 2, 2]
    offsets = (ctypes.c_uint32*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, offsets, length)
    pytest_nextparents = [1, 3]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

