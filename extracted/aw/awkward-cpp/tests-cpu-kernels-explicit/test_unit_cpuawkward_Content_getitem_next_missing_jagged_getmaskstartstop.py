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

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_1():
    mask_out = [123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 2
    offsets_in = [0, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_2():
    mask_out = []
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = []
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = []
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = []
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 0
    offsets_in = []
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = []
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = []
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = []
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_3():
    mask_out = [123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 2
    offsets_in = [0, 4]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 4]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [4, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_4():
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, -1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 3
    offsets_in = [0, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, -1]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_5():
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 3
    offsets_in = [0, 1, 2]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 2]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_6():
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 3
    offsets_in = [0, 2, 4]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_7():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, -1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_8():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, -1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 1, 2]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1, 2]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_9():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, -1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, -1]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 2, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 2, 3, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_10():
    mask_out = [123, 123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 5
    offsets_in = [0, 2, 2, 4]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, -1, 4]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 2, 2, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 2, 2, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_11():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_12():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 0, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_13():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 1, 2, 3]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1, 1, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_14():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3, 3]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_15():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3, 4]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_16():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3, 5]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_17():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3, 5]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 2, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 2, 3, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_18():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 3, 6]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 3, 3, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_19():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 2, 4, 5]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 4, 4]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 4, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_20():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 3, 3, 4]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 3, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_21():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 3, 3, 5]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 3, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 3, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_22():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, 1, -1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 4, 5, 6]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, -1, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 4, 5, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [4, 5, 5, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_23():
    mask_out = [123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 4
    offsets_in = [0, 4, 5, 6]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 4, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [4, 4, 5, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_24():
    mask_out = [123, 123, 123, 123, 123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123, 123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123, 123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2, -1, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 8
    offsets_in = [0, 2, 4, 6, 8, 10, 12]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3, -1, 5, 6, 7]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 2, 2, 4, 6, 6, 8, 10]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [2, 2, 4, 6, 6, 8, 10, 12]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

def test_unit_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_25():
    mask_out = [123, 123, 123, 123, 123, 123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123, 123, 123, 123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123, 123, 123, 123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    index_in = [0, -1, 1, 2, 3, 4, 5, 6]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    length = 8
    offsets_in = [0, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, -1, 2, 3, 4, 5, 6, 7]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 1, 1, 1, 1, 1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1, 1, 1, 1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)
    assert not ret_pass.str

