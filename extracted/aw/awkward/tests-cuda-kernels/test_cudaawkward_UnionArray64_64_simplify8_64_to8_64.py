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

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_1():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_2():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_3():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_4():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_5():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_6():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_7():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_8():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_9():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_10():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_11():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_12():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_13():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_14():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_15():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_16():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_17():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_18():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_19():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_20():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_21():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_22():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_23():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_24():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_25():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_26():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_27():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_28():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_29():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_30():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_31():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_32():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_33():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_34():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_35():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_36():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_37():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_38():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_39():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_40():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_41():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_42():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_43():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_44():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_45():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_46():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_47():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_48():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_49():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_50():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_51():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_52():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_53():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_54():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_55():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_56():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_57():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_58():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_59():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_60():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_61():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_62():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_63():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_64():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_65():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_66():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_67():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_68():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_69():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_70():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_71():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_72():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_73():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_74():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_75():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_76():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_77():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_78():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_79():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_80():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_81():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_82():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_83():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_84():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_85():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_86():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_87():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_88():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_89():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_90():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_91():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_92():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_93():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_94():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_95():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_96():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_97():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_98():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_99():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_100():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_101():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_102():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_103():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_104():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_105():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_106():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_107():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_108():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_109():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_110():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_111():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_112():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_113():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_114():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_115():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_116():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_117():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_118():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_119():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_120():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_121():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_122():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_123():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_124():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_125():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_126():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_127():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_128():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_129():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_130():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_131():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_132():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_133():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_134():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_135():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_136():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_137():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_138():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_139():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_140():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_141():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_142():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_143():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_144():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_145():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_146():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_147():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_148():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_149():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_150():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_151():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_152():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_153():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_154():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_155():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_156():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_157():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_158():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_159():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_160():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_161():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_162():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_163():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_164():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_165():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_166():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_167():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_168():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_169():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_170():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_171():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_172():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_173():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_174():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_175():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_176():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_177():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_178():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_179():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_180():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_181():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_182():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_183():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_184():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_185():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_186():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_187():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_188():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_189():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_190():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_191():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_192():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_193():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_194():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_195():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_196():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_197():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_198():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_199():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_200():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_201():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_202():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_203():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_204():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_205():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_206():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_207():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_208():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_209():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_210():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_211():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_212():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_213():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_214():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_215():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_216():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_217():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_218():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_219():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_220():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_221():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_222():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_223():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_224():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_225():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_226():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_227():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_228():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_229():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_230():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_231():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_232():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_233():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_234():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_235():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_236():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_237():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_238():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_239():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_240():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_241():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_242():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_243():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_244():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_245():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_246():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_247():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_248():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_249():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_250():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_251():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_252():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_253():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_254():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_255():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_256():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_257():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_258():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_259():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_260():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_261():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_262():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_263():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_264():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_265():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_266():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_267():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_268():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_269():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_270():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_271():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_272():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_273():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_274():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_275():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_276():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_277():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_278():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_279():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_280():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_281():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_282():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_283():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_284():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_285():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_286():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_287():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_288():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_289():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_290():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 1
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_291():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_292():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_293():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_294():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_295():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_296():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_297():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_298():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_299():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_300():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 1
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_301():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_302():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_303():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_304():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_305():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_306():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_307():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_308():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_309():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_310():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_311():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_312():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_313():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_314():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_315():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_316():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_317():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_318():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_319():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_320():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_321():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_322():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_323():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_324():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_325():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_326():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_327():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_328():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_329():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_330():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_331():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_332():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_333():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_334():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_335():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_336():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_337():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_338():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_339():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_340():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_341():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_342():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_343():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_344():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_345():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_346():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_347():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_348():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_349():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_350():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_351():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_352():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_353():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_354():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_355():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_356():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_357():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_358():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_359():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_360():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_361():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_362():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_363():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_364():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_365():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_366():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_367():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_368():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_369():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_370():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_371():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_372():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_373():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_374():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_375():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_376():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_377():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_378():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_379():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_380():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_381():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_382():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_383():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_384():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_385():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_386():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_387():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_388():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_389():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_390():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_391():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_392():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_393():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_394():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_395():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_396():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_397():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_398():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_399():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_400():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_401():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_402():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_403():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_404():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_405():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_406():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_407():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_408():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_409():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_410():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_411():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_412():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_413():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_414():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_415():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_416():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_417():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_418():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_419():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_420():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_421():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_422():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_423():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_424():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_425():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_426():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_427():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_428():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_429():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_430():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_431():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_432():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_433():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_434():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_435():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_436():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_437():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_438():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 5, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_439():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_440():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_441():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_442():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_443():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_444():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_445():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_446():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_447():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_448():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_449():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_450():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_451():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_452():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_453():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_454():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_455():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_456():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_457():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_458():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 6, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_459():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_460():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_461():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_462():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_463():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_464():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_465():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_466():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_467():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_468():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_469():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_470():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_471():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_472():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 4, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_473():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_474():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [5, 3, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_475():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_476():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [6, 8, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_477():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_478():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [7, 4, 5]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_479():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_480():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_481():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_482():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_483():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_484():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_485():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_486():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_487():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_488():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_489():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_490():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_491():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_492():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_493():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_494():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_495():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_496():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_497():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_498():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [4, 4, 4]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_499():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cudaawkward_UnionArray64_64_simplify8_64_to8_64_500():
    totags = cupy.array([123, 123, 123], dtype=cupy.int8)
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    outertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    innertags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    innerindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    towhich = 3
    innerwhich = 0
    outerwhich = 0
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_simplify', cupy.int8, cupy.int64, cupy.int64, cupy.int64, cupy.int8, cupy.int64]
    funcC(totags, toindex, outertags, outerindex, innertags, innerindex, towhich, innerwhich, outerwhich, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))
    pytest_toindex = [3, 3, 3]
    cpt.assert_allclose(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

