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

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_1():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    sliceouterlen = 3
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    contentlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_2():
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    sliceouterlen = 3
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 3, 5]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [1, 0, 0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_3():
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    sliceouterlen = 3
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    contentlen = 6
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 3, 5]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [0, 0, 0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_4():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    sliceinnerlen = 2
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_5():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    sliceinnerlen = 1
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_6():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    sliceinnerlen = 1
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_7():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    sliceinnerlen = 2
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_8():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    contentlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_9():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    contentlen = 10
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [1, 0, 0, 0, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray64_getitem_jagged_apply_64_10():
    tooffsets = cupy.array([123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 6
    sliceindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    sliceinnerlen = 5
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    contentlen = 6
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_apply', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, tocarry, slicestarts, slicestops, sliceouterlen, sliceindex, sliceinnerlen, fromstarts, fromstops, contentlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))
    pytest_tocarry = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

