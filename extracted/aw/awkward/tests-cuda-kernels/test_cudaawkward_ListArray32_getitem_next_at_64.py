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

def test_cudaawkward_ListArray32_getitem_next_at_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    lenstarts = 3
    at = 0
    funcC = cupy_backend['awkward_ListArray_getitem_next_at', cupy.int64, cupy.int32, cupy.int32]
    funcC(tocarry, fromstarts, fromstops, lenstarts, at)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_ListArray32_getitem_next_at_64_2():
    tocarry = cupy.array([123], dtype=cupy.int64)
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int32)
    lenstarts = 3
    at = 5
    funcC = cupy_backend['awkward_ListArray_getitem_next_at', cupy.int64, cupy.int32, cupy.int32]

