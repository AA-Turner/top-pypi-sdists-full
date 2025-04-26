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

def test_cudaawkward_BitMaskedArray_to_ByteMaskedArray_1():
    tobytemask = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    frombitmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = cupy_backend['awkward_BitMaskedArray_to_ByteMaskedArray', cupy.int8, cupy.uint8]
    funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tobytemask = [np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    cpt.assert_allclose(tobytemask[:len(pytest_tobytemask)], cupy.array(pytest_tobytemask))

def test_cudaawkward_BitMaskedArray_to_ByteMaskedArray_2():
    tobytemask = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    frombitmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_ByteMaskedArray', cupy.int8, cupy.uint8]
    funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tobytemask = [np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_]
    cpt.assert_allclose(tobytemask[:len(pytest_tobytemask)], cupy.array(pytest_tobytemask))

def test_cudaawkward_BitMaskedArray_to_ByteMaskedArray_3():
    tobytemask = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    frombitmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_ByteMaskedArray', cupy.int8, cupy.uint8]
    funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tobytemask = [np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    cpt.assert_allclose(tobytemask[:len(pytest_tobytemask)], cupy.array(pytest_tobytemask))

def test_cudaawkward_BitMaskedArray_to_ByteMaskedArray_4():
    tobytemask = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    frombitmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcC = cupy_backend['awkward_BitMaskedArray_to_ByteMaskedArray', cupy.int8, cupy.uint8]
    funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tobytemask = [np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.False_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_, np.True_]
    cpt.assert_allclose(tobytemask[:len(pytest_tobytemask)], cupy.array(pytest_tobytemask))

def test_cudaawkward_BitMaskedArray_to_ByteMaskedArray_5():
    tobytemask = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    frombitmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint8)
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcC = cupy_backend['awkward_BitMaskedArray_to_ByteMaskedArray', cupy.int8, cupy.uint8]
    funcC(tobytemask, frombitmask, bitmasklength, validwhen, lsb_order)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tobytemask = [np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.False_, np.True_]
    cpt.assert_allclose(tobytemask[:len(pytest_tobytemask)], cupy.array(pytest_tobytemask))

