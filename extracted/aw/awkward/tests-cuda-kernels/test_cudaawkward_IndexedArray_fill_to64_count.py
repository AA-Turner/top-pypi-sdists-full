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

def test_cudaawkward_IndexedArray_fill_to64_count_1():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_IndexedArray_fill_count', cupy.int64]
    funcC(toindex, toindexoffset, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [3, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArray_fill_to64_count_2():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_IndexedArray_fill_count', cupy.int64]
    funcC(toindex, toindexoffset, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [3, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArray_fill_to64_count_3():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_IndexedArray_fill_count', cupy.int64]
    funcC(toindex, toindexoffset, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [3, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArray_fill_to64_count_4():
    toindex = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    toindexoffset = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_IndexedArray_fill_count', cupy.int64]
    funcC(toindex, toindexoffset, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [123, 3, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArray_fill_to64_count_5():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindexoffset = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_IndexedArray_fill_count', cupy.int64]
    funcC(toindex, toindexoffset, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [3, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

