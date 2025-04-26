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

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_1():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_2():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_3():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 1, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_4():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 0, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_5():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_6():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_7():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_8():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 1, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_9():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 0, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_10():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_11():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_12():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_13():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 1, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_14():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 0, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_15():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_16():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_17():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_18():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 1, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_19():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 0, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_20():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_21():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_22():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_23():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 1, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_24():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 0, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray_drop_none_indexes_64_25():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    noneindexes = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length_offsets = 3
    length_indexes = 3
    funcC = cupy_backend['awkward_ListOffsetArray_drop_none_indexes', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, noneindexes, fromoffsets, length_offsets, length_indexes)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

