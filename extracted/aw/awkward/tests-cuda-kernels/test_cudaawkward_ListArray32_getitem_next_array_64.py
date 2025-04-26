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

def test_cudaawkward_ListArray32_getitem_next_array_64_1():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_64_2():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 2, 1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_64_3():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 4, 2, 3, 3, 2, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_64_4():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 2, 1, 2, 1, 0, 2, 1, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_64_5():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 3, 1, 0, 2, 1, 0, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_64_6():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_64_7():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lenarray = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, lenstarts, lenarray, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

