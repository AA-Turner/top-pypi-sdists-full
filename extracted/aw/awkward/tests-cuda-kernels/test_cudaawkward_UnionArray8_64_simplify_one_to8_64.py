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

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_1():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_2():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_3():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 6, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_4():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 7, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_5():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_6():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_7():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_8():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 6, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_9():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 7, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_10():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    fromwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_11():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_12():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_13():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 6, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_14():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 7, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray8_64_simplify_one_to8_64_15():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    fromwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify_one', cupy.int8, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, fromtags, fromindex, towhich, fromwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

