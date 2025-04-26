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

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_1():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 3
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_2():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_3():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 1
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_4():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1, 1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_5():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    regularsize = 3
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 3, 3, 2, 3, 3, 2, 3, 3]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 4, 3, 3, 4, 3, 3, 4]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_6():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 3, 2, 3, 2, 3]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 3, 3, 3, 3]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_7():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    regularsize = 1
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 3]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_8():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 3, 2, 3, 2, 3]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 3, 3, 3, 3]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_9():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 3
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 1, 0, 2, 1, 0, 2, 1, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 0, 1, 1, 0, 1, 1, 0, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_10():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 1, 2, 1, 2, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 0, 1, 0, 1, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_11():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 1
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_12():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 1, 2, 1, 2, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 0, 1, 0, 1, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_13():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 3
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 0, 2, 1, 0, 2, 1, 0, 2]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 2, 3, 0, 2, 3, 0, 2, 3]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_14():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 0, 1, 0, 1, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 2, 0, 2, 0, 2]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_15():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 1
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_16():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 0, 1, 0, 1, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 2, 0, 2, 0, 2]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_17():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 3
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_18():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_19():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 1
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

def test_cudaawkward_RegularArray_getitem_jagged_expand_64_20():
    multistarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    regularsize = 2
    regularlength = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64]
    funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))

