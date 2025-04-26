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

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_1():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_2():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [2, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_3():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [3, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_4():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [4, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_5():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 0, 0]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_6():
    toindex = cupy.array([123], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_7():
    toindex = cupy.array([123], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_8():
    toindex = cupy.array([123], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_9():
    toindex = cupy.array([123], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_10():
    toindex = cupy.array([123], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    innerlength = 2
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_11():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    innerlength = 5
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_12():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 5
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_13():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    innerlength = 5
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_14():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    innerlength = 5
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 1, 1]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_IndexedArrayU32_simplifyU32_to64_15():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    outerlength = 3
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    innerlength = 5
    funcC = cupy_backend['awkward_IndexedArray_simplify', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(toindex, outerindex, outerlength, innerindex, innerlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 0, 0]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

