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

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_1():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 1, 1]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_2():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 3, 3]
    pytest_stops_out = [3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_3():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 1, 0]
    pytest_stops_out = [1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_4():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 0, 2]
    pytest_stops_out = [0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_5():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_6():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 1, 1]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_7():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 3, 3]
    pytest_stops_out = [3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_8():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 1, 0]
    pytest_stops_out = [1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_9():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 0, 2]
    pytest_stops_out = [0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_10():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_11():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 1, 1]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_12():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 3, 3]
    pytest_stops_out = [3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_13():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 1, 0]
    pytest_stops_out = [1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_14():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 0, 2]
    pytest_stops_out = [0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_15():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_16():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 1, 1]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_17():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 3, 3]
    pytest_stops_out = [3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_18():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 1, 0]
    pytest_stops_out = [1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_19():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 0, 2]
    pytest_stops_out = [0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_20():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_21():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 1, 1]
    pytest_stops_out = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_22():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 3, 3]
    pytest_stops_out = [3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_23():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [2, 1, 0]
    pytest_stops_out = [1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_24():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [1, 0, 2]
    pytest_stops_out = [0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_Content_getitem_next_missing_jagged_getmaskstartstop_25():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_in = (ctypes.c_int64*len(index_in))(*index_in)
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = (ctypes.c_int64*len(offsets_in))(*offsets_in)
    mask_out = [123, 123, 123]
    mask_out = (ctypes.c_int64*len(mask_out))(*mask_out)
    starts_out = [123, 123, 123]
    starts_out = (ctypes.c_int64*len(starts_out))(*starts_out)
    stops_out = [123, 123, 123]
    stops_out = (ctypes.c_int64*len(stops_out))(*stops_out)
    length = 3
    funcC = getattr(lib, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    ret_pass = funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)
    pytest_mask_out = [0, 1, 2]
    pytest_starts_out = [0, 0, 0]
    pytest_stops_out = [0, 0, 0]
    assert not ret_pass.str

