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

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_1():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [1, 1, 1, 1]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_2():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [2, 2, 3, 4]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_3():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [2, 1, 0, -1]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_4():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [1, 3, 2, 1]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_5():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [0, 0, 0, 0]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_6():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_7():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_8():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_9():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_10():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_11():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_12():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_13():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_14():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_15():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_16():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_17():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_18():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_19():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_20():
    outoffsets = cupy.array([123, 123], dtype=cupy.int64)
    outindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_21():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [1, 1, 1, 1]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_22():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [2, 3, 4, 5]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_23():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [2, 1, 0, -1]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_24():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [1, 0, -1, -2]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

def test_cudaawkward_IndexedArrayU32_flatten_none2empty_64_25():
    outoffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outindexlength = 3
    offsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_IndexedArray_flatten_none2empty', cupy.int64, cupy.uint32, cupy.int64]
    funcC(outoffsets, outindex, outindexlength, offsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outoffsets = [0, 0, 0, 0]
    cpt.assert_allclose(outoffsets[:len(pytest_outoffsets)], cupy.array(pytest_outoffsets))

