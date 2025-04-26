# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import cupy
import cupy.testing as cpt
import numpy as np
import pytest

import awkward as ak
import awkward._connect.cuda as ak_cu
from awkward._backends.cupy import CupyBackend

cupy_backend = CupyBackend.instance()

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_1():
    index_in = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 1, 1]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_2():
    index_in = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 3, 3]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 3, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_3():
    index_in = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 1, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 0, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_4():
    index_in = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 2, 3]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_5():
    index_in = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 0, 0]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_6():
    index_in = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 1, 1]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_7():
    index_in = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 3, 3]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 3, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_8():
    index_in = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 1, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 0, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_9():
    index_in = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 2, 3]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_10():
    index_in = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 0, 0]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_11():
    index_in = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 1, 1]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_12():
    index_in = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 3, 3]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 3, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_13():
    index_in = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 1, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 0, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_14():
    index_in = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 2, 3]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_15():
    index_in = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    offsets_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 0, 0]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_16():
    index_in = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    offsets_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 1, 1]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_17():
    index_in = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    offsets_in = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 3, 3]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 3, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_18():
    index_in = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    offsets_in = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 1, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 0, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_19():
    index_in = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    offsets_in = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 2, 3]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_20():
    index_in = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    offsets_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 0, 0]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_21():
    index_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsets_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 1, 1]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_22():
    index_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsets_in = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 3, 3]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 3, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_23():
    index_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsets_in = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [2, 1, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 0, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_24():
    index_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsets_in = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [1, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 2, 3]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_Content_getitem_next_missing_jagged_getmaskstartstop_25():
    index_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsets_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    mask_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_Content_getitem_next_missing_jagged_getmaskstartstop', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index_in, offsets_in, mask_out, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_mask_out = [0, 1, 2]
    cpt.assert_allclose(mask_out[:len(pytest_mask_out)], cupy.array(pytest_mask_out))
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [0, 0, 0]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

