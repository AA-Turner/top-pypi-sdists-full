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

def test_cudaawkward_BitMaskedArray_to_IndexedOptionArray64_1():
    toindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    frombitmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = cupy_backend['awkward_BitMaskedArray_to_IndexedOptionArray', cupy.int64, cupy.uint8]
    funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_BitMaskedArray_to_IndexedOptionArray64_2():
    toindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    frombitmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_IndexedOptionArray', cupy.int64, cupy.uint8]
    funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_BitMaskedArray_to_IndexedOptionArray64_3():
    toindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    frombitmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_IndexedOptionArray', cupy.int64, cupy.uint8]
    funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_BitMaskedArray_to_IndexedOptionArray64_4():
    toindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    frombitmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = cupy_backend['awkward_BitMaskedArray_to_IndexedOptionArray', cupy.int64, cupy.uint8]
    funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_BitMaskedArray_to_IndexedOptionArray64_5():
    toindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    frombitmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_IndexedOptionArray', cupy.int64, cupy.uint8]
    funcC(toindex, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, -1, 8, 9, 10, 11, 12, 13, 14, -1, 16, 17, 18, 19, 20, 21, 22, -1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

