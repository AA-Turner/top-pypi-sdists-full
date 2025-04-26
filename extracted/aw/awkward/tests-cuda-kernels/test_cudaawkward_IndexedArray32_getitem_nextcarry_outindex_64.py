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

def test_cudaawkward_IndexedArray32_getitem_nextcarry_outindex_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    lenindex = 3
    lencontent = 2
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int32, cupy.int32]
    funcC(tocarry, toindex, fromindex, lenindex, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArray32_getitem_nextcarry_outindex_64_2():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toindex = cupy.array([123], dtype=cupy.int32)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    lenindex = 3
    lencontent = 2
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int32, cupy.int32]

def test_cudaawkward_IndexedArray32_getitem_nextcarry_outindex_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int32)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    lenindex = 3
    lencontent = 5
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int32, cupy.int32]
    funcC(tocarry, toindex, fromindex, lenindex, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toindex = [0, 1, 2]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

