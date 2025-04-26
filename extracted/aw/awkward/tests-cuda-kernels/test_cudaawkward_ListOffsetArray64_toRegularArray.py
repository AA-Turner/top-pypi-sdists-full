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

def test_cudaawkward_ListOffsetArray64_toRegularArray_1():
    size = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_ListOffsetArray_toRegularArray', cupy.int64, cupy.int64]
    funcC(size, fromoffsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [0]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

def test_cudaawkward_ListOffsetArray64_toRegularArray_2():
    size = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_ListOffsetArray_toRegularArray', cupy.int64, cupy.int64]

def test_cudaawkward_ListOffsetArray64_toRegularArray_3():
    size = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_ListOffsetArray_toRegularArray', cupy.int64, cupy.int64]

def test_cudaawkward_ListOffsetArray64_toRegularArray_4():
    size = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_ListOffsetArray_toRegularArray', cupy.int64, cupy.int64]

def test_cudaawkward_ListOffsetArray64_toRegularArray_5():
    size = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    offsetslength = 3
    funcC = cupy_backend['awkward_ListOffsetArray_toRegularArray', cupy.int64, cupy.int64]
    funcC(size, fromoffsets, offsetslength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_size = [0]
    cpt.assert_allclose(size[:len(pytest_size)], cupy.array(pytest_size))

