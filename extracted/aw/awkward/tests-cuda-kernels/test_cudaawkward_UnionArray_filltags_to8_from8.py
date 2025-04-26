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

def test_cudaawkward_UnionArray_filltags_to8_from8_1():
    totags = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    totagsoffset = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_filltags', cupy.int8, cupy.int8]
    funcC(totags, totagsoffset, fromtags, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [123, 123, 123, 3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))

def test_cudaawkward_UnionArray_filltags_to8_from8_2():
    totags = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    totagsoffset = 3
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_filltags', cupy.int8, cupy.int8]
    funcC(totags, totagsoffset, fromtags, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [123, 123, 123, 4, 4, 4]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))

def test_cudaawkward_UnionArray_filltags_to8_from8_3():
    totags = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    totagsoffset = 3
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_filltags', cupy.int8, cupy.int8]
    funcC(totags, totagsoffset, fromtags, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [123, 123, 123, 4, 4, 4]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))

def test_cudaawkward_UnionArray_filltags_to8_from8_4():
    totags = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    totagsoffset = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_filltags', cupy.int8, cupy.int8]
    funcC(totags, totagsoffset, fromtags, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [123, 123, 123, 3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))

def test_cudaawkward_UnionArray_filltags_to8_from8_5():
    totags = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int8)
    totagsoffset = 3
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_UnionArray_filltags', cupy.int8, cupy.int8]
    funcC(totags, totagsoffset, fromtags, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_totags = [123, 123, 123, 3, 3, 3]
    cpt.assert_allclose(totags[:len(pytest_totags)], cupy.array(pytest_totags))

