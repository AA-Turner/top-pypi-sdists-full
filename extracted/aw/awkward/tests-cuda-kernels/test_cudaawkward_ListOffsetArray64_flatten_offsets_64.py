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

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_1():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_2():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_3():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_4():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_5():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_6():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_7():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 4, 4]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_8():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_9():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_10():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_11():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_12():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 3, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_13():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_14():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 0, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_15():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_16():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_17():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 2, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_18():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 2, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_19():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_20():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_21():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_22():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 2, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_23():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 2, 2]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_24():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListOffsetArray64_flatten_offsets_64_25():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

