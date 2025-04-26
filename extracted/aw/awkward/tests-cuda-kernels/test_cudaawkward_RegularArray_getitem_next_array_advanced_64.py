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

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_2():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_4():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_5():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_6():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 6, 9]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_7():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_8():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_9():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_10():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_11():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_12():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_13():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_14():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_15():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_16():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_17():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_18():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_19():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_20():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_21():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_22():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_23():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_24():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_25():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_26():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_27():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_28():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_29():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_30():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_31():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 7, 10]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_32():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 6, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_33():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_34():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 6, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_35():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_36():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_37():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_38():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_39():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_40():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_41():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 6, 9]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_42():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 5, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_43():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 4, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_44():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 5, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_45():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_46():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_47():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_48():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_49():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_50():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_51():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_52():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_53():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_54():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_55():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_56():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 6, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_57():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_58():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_59():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_60():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 3, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_61():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 4, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_62():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_63():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_64():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_65():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_66():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_67():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_68():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_69():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_70():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 0, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_71():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_72():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_73():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_74():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_75():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_76():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_77():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_78():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_79():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_80():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_81():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 5, 9]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_82():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_83():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_84():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_85():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_86():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 5, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_87():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_88():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_89():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_90():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_91():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 4, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_92():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_93():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_94():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_95():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_96():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_97():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_98():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_99():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_100():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_101():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_102():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_103():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_104():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_105():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_106():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 5, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_107():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 4, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_108():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_109():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 4, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_110():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_111():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 5, 8]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_112():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 4, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_113():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_114():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 4, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_115():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_116():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_117():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_118():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 2, 3]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_119():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 3, 5]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_120():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_121():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_122():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_123():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_124():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 2, 4]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

def test_cudaawkward_RegularArray_getitem_next_array_advanced_64_125():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toadvanced = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromadvanced = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    fromarray = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    size = 0
    funcC = cupy_backend['awkward_RegularArray_getitem_next_array_advanced', cupy.int64, cupy.int64, cupy.int64, cupy.int64]
    funcC(tocarry, toadvanced, fromadvanced, fromarray, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toadvanced = [0, 1, 2]
    cpt.assert_allclose(toadvanced[:len(pytest_toadvanced)], cupy.array(pytest_toadvanced))

