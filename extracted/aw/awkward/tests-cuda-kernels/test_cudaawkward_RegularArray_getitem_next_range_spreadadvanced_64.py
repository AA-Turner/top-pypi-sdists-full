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

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_1():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_2():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_3():
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 1]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_4():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_5():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    nextsize = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 2, 3, 3, 3, 3, 3, 3]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_6():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 3, 3, 3, 3]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_7():
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    nextsize = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 3, 3]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_8():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 3, 3, 3, 3]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_9():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 2, 1, 1, 1, 0, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_10():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 1, 1, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_11():
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 1, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_12():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [2, 2, 1, 1, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_13():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 1, 0, 0, 0, 2, 2, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_14():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 0, 0, 2, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_15():
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 0, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_16():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [1, 1, 0, 0, 2, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_17():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_18():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_19():
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [0, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_range_spreadadvanced_64_20():
    toadvanced = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    nextsize = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_range_spreadadvanced', cupy.int64, cupy.int64]
    funcC(toadvanced, fromadvanced, length, nextsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toadvanced = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

