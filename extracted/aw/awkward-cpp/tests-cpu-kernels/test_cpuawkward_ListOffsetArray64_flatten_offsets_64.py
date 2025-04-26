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

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_1():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_2():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_3():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_4():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_5():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_6():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_7():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [3, 4, 4]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_8():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_9():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [2, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_10():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_11():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_12():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [3, 3, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_13():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_14():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [2, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_15():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_16():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_17():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [3, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_18():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 2, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_19():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 1, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_20():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_21():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_22():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [2, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_23():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [2, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_24():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArray64_flatten_offsets_64_25():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsets = (ctypes.c_int64*len(outeroffsets))(*outeroffsets)
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    inneroffsets = (ctypes.c_int64*len(inneroffsets))(*inneroffsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray64_flatten_offsets_64')
    ret_pass = funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert not ret_pass.str

