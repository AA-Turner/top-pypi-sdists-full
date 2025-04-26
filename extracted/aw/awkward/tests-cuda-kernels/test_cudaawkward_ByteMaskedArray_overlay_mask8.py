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

def test_cudaawkward_ByteMaskedArray_overlay_mask8_1():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_2():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_3():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_4():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_5():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_6():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_7():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [0, 0, 0]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_8():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_9():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_10():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [0, 0, 0]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_11():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_12():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_13():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_14():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_15():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_16():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_17():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_18():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_19():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_20():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_21():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [0, 0, 0]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_22():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_23():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [0, 0, 0]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_24():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [0, 0, 0]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

def test_cudaawkward_ByteMaskedArray_overlay_mask8_25():
    tomask = cupy.array([123, 123, 123], dtype=cupy.int8)
    theirmask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    mymask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_overlay_mask', cupy.int8, cupy.int8, cupy.int8]
    funcC(tomask, theirmask, mymask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tomask = [1, 1, 1]
    cpt.assert_allclose(tomask[:len(pytest_tomask)], cupy.array(pytest_tomask))

