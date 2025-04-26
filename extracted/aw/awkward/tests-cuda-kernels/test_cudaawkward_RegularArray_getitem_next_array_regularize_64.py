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

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_1():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [1, 1, 1]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_2():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [1, 1, 1]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_3():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_4():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [1, 1, 1]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_5():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_6():
    toarray = cupy.array([123, 123], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenarray = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_7():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_8():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenarray = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_9():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_10():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lenarray = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_11():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [2, 1, 0]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_12():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_13():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_14():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_15():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_16():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [1, 0, 2]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_17():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_18():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_19():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_20():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lenarray = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_21():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [0, 0, 0]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_22():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [0, 0, 0]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_23():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [0, 0, 0]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_24():
    toarray = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]
    funcC(toarray, fromarray, lenarray, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toarray = [0, 0, 0]
    cpt.assert_allclose(toarray[:len(pytest_toarray)], cupy.array(pytest_toarray))

def test_cudaawkward_RegularArray_getitem_next_array_regularize_64_25():
    toarray = cupy.array([123], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenarray = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_regularize', cupy.int64, cupy.int64]

