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

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_1():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [5]
    cpt.assert_allclose(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_2():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [16]
    cpt.assert_allclose(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_3():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [0]
    cpt.assert_allclose(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_4():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [2]
    cpt.assert_allclose(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_5():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [3]
    cpt.assert_allclose(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

