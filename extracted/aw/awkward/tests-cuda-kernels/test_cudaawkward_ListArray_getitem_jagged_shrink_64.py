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

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_1():
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_2():
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_3():
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_4():
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_5():
    tocarry = cupy.array([123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    length = 3
    missing = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [2, 3, 5, 7]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_6():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_7():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_8():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_9():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_10():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    length = 3
    missing = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 8, 12, 17]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_11():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_12():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_13():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_14():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_15():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    length = 3
    missing = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [1, 1, 3, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_16():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_17():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_18():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_19():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    missing = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

def test_cudaawkward_ListArray_getitem_jagged_shrink_64_20():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    tosmalloffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    tolargeoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    missing = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_shrink', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, tosmalloffsets, tolargeoffsets, slicestarts, slicestops, length, missing)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_tosmalloffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tosmalloffsets[:len(pytest_tosmalloffsets)], cupy.array(pytest_tosmalloffsets))
    pytest_tolargeoffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tolargeoffsets[:len(pytest_tolargeoffsets)], cupy.array(pytest_tolargeoffsets))

