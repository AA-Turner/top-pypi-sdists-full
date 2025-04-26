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

def test_cudaawkward_missing_repeat_64_1():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 0, 0, 4, 3, 3, 7, 6, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_2():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 0, 0, 3, 2, 2, 5, 4, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_3():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 0, 0, 2, 1, 1, 3, 2, 2]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_4():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 0, 0, 3, 2, 2, 5, 4, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_5():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 0, 0, 1, 0, 0, 1, 0, 0]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_6():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 2, 2, 4, 5, 5, 7, 8, 8]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_7():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 2, 2, 3, 4, 4, 5, 6, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_8():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 2, 2, 2, 3, 3, 3, 4, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_9():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 2, 2, 3, 4, 4, 5, 6, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_10():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 2, 2, 1, 2, 2, 1, 2, 2]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_11():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 3, 0, 4, 6, 3, 7, 9, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_12():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 3, 0, 3, 5, 2, 5, 7, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_13():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 3, 0, 2, 4, 1, 3, 5, 2]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_14():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 3, 0, 3, 5, 2, 5, 7, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_15():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 3, 0, 1, 3, 0, 1, 3, 0]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_16():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 4, 2, 4, 7, 5, 7, 10, 8]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_17():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 4, 2, 3, 6, 4, 5, 8, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_18():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 4, 2, 2, 5, 3, 3, 6, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_19():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 4, 2, 3, 6, 4, 5, 8, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_20():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [1, 4, 2, 1, 4, 2, 1, 4, 2]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_21():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [0, 0, 0, 3, 3, 3, 6, 6, 6]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_22():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_23():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_24():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cudaawkward_missing_repeat_64_25():
    outindex = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcC = cupy_backend['awkward_missing_repeat', cupy.int64, cupy.int64]
    funcC(outindex, index, indexlength, repetitions, regularsize)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cpt.assert_allclose(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

