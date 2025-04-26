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

def test_cudaawkward_RegularArray_getitem_carry_64_1():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_2():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_4():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_5():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [6, 7, 8, 9, 10, 11, 9, 10, 11]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_6():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_7():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_8():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_9():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_10():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_11():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_12():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_13():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 5, 0, 1, 2, 6, 7, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_14():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_15():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_16():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_17():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_18():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_19():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_RegularArray_getitem_carry_64_20():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

