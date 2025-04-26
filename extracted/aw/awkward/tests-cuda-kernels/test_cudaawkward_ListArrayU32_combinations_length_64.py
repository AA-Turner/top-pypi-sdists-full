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

def test_cudaawkward_ListArrayU32_combinations_length_64_1():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    stops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [9]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 5, 9]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_2():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    stops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [139.0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_3():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_4():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [4]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 4, 4]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_5():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    stops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [3]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_6():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = False
    starts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    stops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_7():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = False
    starts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    stops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [49.0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 35.0, 39.0, 49.0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_8():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = False
    starts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_9():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = False
    starts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_10():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = False
    starts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    stops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_11():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    stops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [9]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 5, 9]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_12():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    stops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [139.0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_13():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_14():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [4]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 4, 4]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_15():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    stops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [3]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_16():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    stops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [9]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 5, 9]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_17():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    stops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [139.0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_18():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_19():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [4]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 4, 4]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_20():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    stops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [3]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_21():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    stops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [9]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 5, 9]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_22():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    stops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [139.0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_23():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [0]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 0, 0]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_24():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    stops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [4]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 0, 4, 4]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cudaawkward_ListArrayU32_combinations_length_64_25():
    totallen = cupy.array([123], dtype=cupy.int64)
    tooffsets = cupy.array([123, 123, 123, 123], dtype=cupy.int64)
    n = 3
    replacement = True
    starts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    stops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_ListArray_combinations_length', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(totallen, tooffsets, n, replacement, starts, stops, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totallen = [3]
    cpt.assert_allclose(totallen[:len(pytest_totallen)], cupy.array(pytest_totallen))
    pytest_tooffsets = [0, 1, 2, 3]
    cpt.assert_allclose(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

