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

def test_unit_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_1():
    starts_out = []
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = []
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index = []
    index = (ctypes.c_uint32*len(index))(*index)
    length = 0
    starts_in = []
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = []
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = []
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = []
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_2():
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index = [0, 1, 2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    length = 4
    starts_in = [0, 2, 3, 3]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [2, 3, 3, 3]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_3():
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index = [0, 1, 2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    length = 4
    starts_in = [0, 2, 3, 3]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [2, 3, 3, 5]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_4():
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index = [0, 1, 2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    length = 4
    starts_in = [0, 2, 3, 3]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [2, 3, 3, 6]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_MaskedArrayU32_getitem_next_jagged_project_5():
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index = [0, 1, 2, 3]
    index = (ctypes.c_uint32*len(index))(*index)
    length = 4
    starts_in = [0, 2, 3, 4]
    starts_in = (ctypes.c_int64*len(starts_in))(*starts_in)
    stops_in = [2, 3, 4, 7]
    stops_in = (ctypes.c_int64*len(stops_in))(*stops_in)
    funcC = getattr(lib, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    ret_pass = funcC(index, starts_in, stops_in, starts_out, stops_out, length)
    pytest_starts_out = [0, 2, 3, 4]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 4, 7]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

