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

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_1():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    stops_in = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [2, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 2, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_2():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    stops_in = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [8, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_3():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 4, 5]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_4():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 7, 6]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 9, 6]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_5():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    stops_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_6():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    stops_in = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [2, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 2, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_7():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    stops_in = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [8, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_8():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 4, 5]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_9():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 7, 6]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 9, 6]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_10():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    stops_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_11():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    stops_in = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [2, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 2, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_12():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    stops_in = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [8, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_13():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 4, 5]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_14():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 7, 6]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 9, 6]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_15():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    starts_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    stops_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_16():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    starts_in = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    stops_in = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [2, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 2, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_17():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    starts_in = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    stops_in = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [8, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_18():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    starts_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 4, 5]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_19():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    starts_in = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 7, 6]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 9, 6]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_20():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    starts_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    stops_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_21():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    starts_in = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    stops_in = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [2, 0, 2]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [3, 2, 4]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_22():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    starts_in = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    stops_in = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [8, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_23():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    starts_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 4, 5]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 4, 5]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_24():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    starts_in = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    stops_in = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [1, 7, 6]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 9, 6]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

def test_cudaawkward_MaskedArrayU32_getitem_next_jagged_project_25():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    starts_in = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    stops_in = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    starts_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    stops_out = cupy.array([123, 123, 123], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_MaskedArray_getitem_next_jagged_project', cupy.uint32, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(index, starts_in, stops_in, starts_out, stops_out, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_starts_out = [0, 0, 0]
    cpt.assert_allclose(starts_out[:len(pytest_starts_out)], cupy.array(pytest_starts_out))
    pytest_stops_out = [1, 1, 1]
    cpt.assert_allclose(stops_out[:len(pytest_stops_out)], cupy.array(pytest_stops_out))

