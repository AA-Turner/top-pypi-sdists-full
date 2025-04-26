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

def test_cudaawkward_IndexedArray64_numnull_1():
    numnull = cupy.array([123], dtype=cupy.int64)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    lenindex = 3
    funcC = cupy_backend['awkward_IndexedArray_numnull', cupy.int64, cupy.int64]
    funcC(numnull, fromindex, lenindex)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_numnull = [0]
    cpt.assert_allclose(numnull[:len(pytest_numnull)], cupy.array(pytest_numnull))

def test_cudaawkward_IndexedArray64_numnull_2():
    numnull = cupy.array([123], dtype=cupy.int64)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    lenindex = 3
    funcC = cupy_backend['awkward_IndexedArray_numnull', cupy.int64, cupy.int64]
    funcC(numnull, fromindex, lenindex)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_numnull = [0]
    cpt.assert_allclose(numnull[:len(pytest_numnull)], cupy.array(pytest_numnull))

def test_cudaawkward_IndexedArray64_numnull_3():
    numnull = cupy.array([123], dtype=cupy.int64)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    lenindex = 3
    funcC = cupy_backend['awkward_IndexedArray_numnull', cupy.int64, cupy.int64]
    funcC(numnull, fromindex, lenindex)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_numnull = [0]
    cpt.assert_allclose(numnull[:len(pytest_numnull)], cupy.array(pytest_numnull))

def test_cudaawkward_IndexedArray64_numnull_4():
    numnull = cupy.array([123], dtype=cupy.int64)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    lenindex = 3
    funcC = cupy_backend['awkward_IndexedArray_numnull', cupy.int64, cupy.int64]
    funcC(numnull, fromindex, lenindex)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_numnull = [0]
    cpt.assert_allclose(numnull[:len(pytest_numnull)], cupy.array(pytest_numnull))

def test_cudaawkward_IndexedArray64_numnull_5():
    numnull = cupy.array([123], dtype=cupy.int64)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lenindex = 3
    funcC = cupy_backend['awkward_IndexedArray_numnull', cupy.int64, cupy.int64]
    funcC(numnull, fromindex, lenindex)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_numnull = [0]
    cpt.assert_allclose(numnull[:len(pytest_numnull)], cupy.array(pytest_numnull))

