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

def test_cudaawkward_UnionArray8_32_project_64_1():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_2():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_3():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 3, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_4():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 4, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_5():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_6():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    which = 1
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_7():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 1
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_8():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 1
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 3, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_9():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    which = 1
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 4, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_10():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    which = 1
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_11():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_12():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 2, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_13():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 3, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_14():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [1, 4, 2]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cudaawkward_UnionArray8_32_project_64_15():
    lenout = cupy.array([123], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromtags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    which = 0
    funcC = cupy_backend['awkward_UnionArray_project', cupy.int64, cupy.int64, cupy.int8, cupy.int32]
    funcC(lenout, tocarry, fromtags, fromindex, length, which)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_lenout = [3]
    cpt.assert_allclose(lenout[:len(pytest_lenout)], cupy.array(pytest_lenout))
    pytest_tocarry = [0, 0, 0]
    cpt.assert_allclose(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

