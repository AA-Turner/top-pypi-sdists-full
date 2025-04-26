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

def test_cudaawkward_UnionArray8_32_regular_index_1():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    current = cupy.array([123, 123, 123], dtype=cupy.int32)
    size = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index', cupy.int32, cupy.int32, cupy.int8]
    funcC(toindex, current, size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))
    pytest_current = [3, 0, 0]
    cpt.assert_allclose(current[:len(pytest_current)], cupy.array(pytest_current))

def test_cudaawkward_UnionArray8_32_regular_index_2():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    current = cupy.array([123, 123, 123], dtype=cupy.int32)
    size = 3
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index', cupy.int32, cupy.int32, cupy.int8]
    funcC(toindex, current, size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))
    pytest_current = [0, 3, 0]
    cpt.assert_allclose(current[:len(pytest_current)], cupy.array(pytest_current))

def test_cudaawkward_UnionArray8_32_regular_index_3():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    current = cupy.array([123, 123, 123], dtype=cupy.int32)
    size = 3
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index', cupy.int32, cupy.int32, cupy.int8]
    funcC(toindex, current, size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))
    pytest_current = [0, 3, 0]
    cpt.assert_allclose(current[:len(pytest_current)], cupy.array(pytest_current))

def test_cudaawkward_UnionArray8_32_regular_index_4():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    current = cupy.array([123, 123, 123], dtype=cupy.int32)
    size = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index', cupy.int32, cupy.int32, cupy.int8]
    funcC(toindex, current, size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))
    pytest_current = [3, 0, 0]
    cpt.assert_allclose(current[:len(pytest_current)], cupy.array(pytest_current))

def test_cudaawkward_UnionArray8_32_regular_index_5():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    current = cupy.array([123, 123, 123], dtype=cupy.int32)
    size = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_regular_index', cupy.int32, cupy.int32, cupy.int8]
    funcC(toindex, current, size, fromtags, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))
    pytest_current = [3, 0, 0]
    cpt.assert_allclose(current[:len(pytest_current)], cupy.array(pytest_current))

