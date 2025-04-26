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

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_1():
    tooffsets = []
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = []
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 0
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = []
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_2():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 2, 3]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 0, 0, 1, 3]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0, 1, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_3():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 2, 3, 4, 5, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 0, 1, 3, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 1, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_4():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 1, 5]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 0, 1, 3]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 1, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_5():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 1, 6, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 0, 1, 4]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 1, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_6():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 4, 8, 12, 14, 16]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 5]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 12, 12, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_7():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 2, 5, 5, 7, 7, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 1, 2, 2, 5, 7]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 6
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 1, 2, 2, 7, 11]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_8():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 1, 2, 3, 4, 5, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 1, 3, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 1, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_9():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 5, 10, 15, 20, 25, 30]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 15, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_10():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 2, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 1, 1, 1, 2]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 2, 2, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_11():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 0, 2, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 2, 2, 2, 3]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 2, 2, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_12():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 0, 0, 2, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 3, 4]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 2, 2, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_13():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 0, 0, 0, 2, 7, 7]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 4, 4, 4, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 2, 2, 2, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_14():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 5, 6, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 1, 2, 3, 4]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 3, 5, 6, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_15():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 5, 10, 15, 20, 25, 30]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 7
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 35, 70, 105, 140, 175, 210]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_16():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 2, 4, 6, 8, 10]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 6
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 4, 8, 12, 14, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_17():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 5, 6, 6, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 2, 2, 3, 5]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 5, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_18():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 3, 5, 6, 6, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 4, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 5, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_19():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 3, 3, 5, 6, 6, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 4, 4, 5, 7]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 5, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_20():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 3, 5, 5, 8]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 5]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 5, 5, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_21():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 6, 9, 12, 14, 16]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 2, 4, 5, 6, 6, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 7
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 6, 12, 14, 16, 16, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_22():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 2, 4, 6, 8, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 5]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 6, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_23():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 3, 5, 8, 8, 10]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 7
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 6, 6, 10, 16, 16, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_24():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 4, 4, 4, 4, 6, 7, 7, 12, 12]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 5, 5, 6, 9]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 5
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 6, 6, 7, 12]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_25():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 6, 9, 11, 13, 14]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [0, 3, 5, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 9, 13, 14]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_26():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 5, 6, 6]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [1, 2, 3, 4]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [3, 5, 6, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_27():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 3, 5, 6, 6, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [3, 3, 4, 6]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [5, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArrayU32_flatten_offsets_64_28():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    inneroffsets = [0, 3, 3, 3, 5, 6, 6, 10]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    outeroffsets = [4, 4, 5, 7]
    outeroffsets = (ctypes.c_uint32*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 4
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [5, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

