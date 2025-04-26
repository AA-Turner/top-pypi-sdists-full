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

def test_cudaawkward_UnionArray64_regular_index_getsize_1():
    size = cupy.array([123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index_getsize', cupy.int64, cupy.int64]
    funcC(size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [1]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

def test_cudaawkward_UnionArray64_regular_index_getsize_2():
    size = cupy.array([123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index_getsize', cupy.int64, cupy.int64]
    funcC(size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [2]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

def test_cudaawkward_UnionArray64_regular_index_getsize_3():
    size = cupy.array([123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index_getsize', cupy.int64, cupy.int64]
    funcC(size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [2]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

def test_cudaawkward_UnionArray64_regular_index_getsize_4():
    size = cupy.array([123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index_getsize', cupy.int64, cupy.int64]
    funcC(size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [1]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

def test_cudaawkward_UnionArray64_regular_index_getsize_5():
    size = cupy.array([123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index_getsize', cupy.int64, cupy.int64]
    funcC(size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [1]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

