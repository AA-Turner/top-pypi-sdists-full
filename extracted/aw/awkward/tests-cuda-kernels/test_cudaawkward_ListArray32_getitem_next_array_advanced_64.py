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

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_1():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_2():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_3():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_4():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_5():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_6():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_7():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_8():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_9():
    tocarry = cupy.array([123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_10():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_11():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_12():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_13():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_14():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_15():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_16():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toadvanced = cupy.array([123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_17():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 3, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_18():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_19():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_20():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_21():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_22():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_23():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_24():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_25():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_26():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_27():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_28():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_29():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_30():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_31():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_32():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_33():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_34():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 10
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_35():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toadvanced = cupy.array([123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_36():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toadvanced = cupy.array([123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_37():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_38():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toadvanced = cupy.array([123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_39():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_40():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_41():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_42():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_ListArray32_getitem_next_array_advanced_64_43():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenstarts = 3
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int32, cupy.int32, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromstarts, fromstops, fromarray, fromadvanced, lenstarts, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

