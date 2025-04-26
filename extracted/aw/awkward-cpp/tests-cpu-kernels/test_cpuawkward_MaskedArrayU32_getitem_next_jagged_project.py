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

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_1():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [2, 0, 2]
    pytest_stops_out = [3, 2, 4]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_2():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 0, 0]
    pytest_stops_out = [8, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_3():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 4, 5]
    pytest_stops_out = [1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_4():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 7, 6]
    pytest_stops_out = [1, 9, 6]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_5():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_6():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [2, 0, 2]
    pytest_stops_out = [3, 2, 4]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_7():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 0, 0]
    pytest_stops_out = [8, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_8():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 4, 5]
    pytest_stops_out = [1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_9():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 7, 6]
    pytest_stops_out = [1, 9, 6]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_10():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_11():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [2, 0, 2]
    pytest_stops_out = [3, 2, 4]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_12():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 0, 0]
    pytest_stops_out = [8, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_13():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 4, 5]
    pytest_stops_out = [1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_14():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 7, 6]
    pytest_stops_out = [1, 9, 6]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_15():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_16():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [2, 0, 2]
    pytest_stops_out = [3, 2, 4]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_17():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 0, 0]
    pytest_stops_out = [8, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_18():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 4, 5]
    pytest_stops_out = [1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_19():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 7, 6]
    pytest_stops_out = [1, 9, 6]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_20():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_21():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [2, 0, 2]
    pytest_stops_out = [3, 2, 4]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_22():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 0, 0]
    pytest_stops_out = [8, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_23():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 4, 5]
    pytest_stops_out = [1, 4, 5]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_24():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [1, 7, 6]
    pytest_stops_out = [1, 9, 6]
    assert not ret_pass.str

def test_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_25():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_uint32*len(index))(*index)
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

