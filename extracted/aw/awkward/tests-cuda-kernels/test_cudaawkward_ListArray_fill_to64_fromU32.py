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

def test_cudaawkward_ListArray_fill_to64_fromU32_1():
    tostarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostartsoffset = 3
    tostops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostopsoffset = 3
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.uint32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.uint32)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_ListArray_fill', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [123, 123, 123, 5, 3, 5]
    cpt.assert_allclose(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [123, 123, 123, 6, 5, 7]
    cpt.assert_allclose(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

def test_cudaawkward_ListArray_fill_to64_fromU32_2():
    tostarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostartsoffset = 3
    tostops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostopsoffset = 3
    fromstarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.uint32)
    fromstops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.uint32)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_ListArray_fill', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [123, 123, 123, 4, 3, 3]
    cpt.assert_allclose(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [123, 123, 123, 11, 7, 8]
    cpt.assert_allclose(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

def test_cudaawkward_ListArray_fill_to64_fromU32_3():
    tostarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostartsoffset = 3
    tostops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostopsoffset = 3
    fromstarts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    fromstops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.uint32)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_ListArray_fill', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [123, 123, 123, 4, 7, 8]
    cpt.assert_allclose(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [123, 123, 123, 4, 7, 8]
    cpt.assert_allclose(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

def test_cudaawkward_ListArray_fill_to64_fromU32_4():
    tostarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostartsoffset = 3
    tostops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostopsoffset = 3
    fromstarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.uint32)
    fromstops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.uint32)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_ListArray_fill', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [123, 123, 123, 4, 10, 9]
    cpt.assert_allclose(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [123, 123, 123, 4, 12, 9]
    cpt.assert_allclose(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

def test_cudaawkward_ListArray_fill_to64_fromU32_5():
    tostarts = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostartsoffset = 3
    tostops = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    tostopsoffset = 3
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.uint32)
    length = 3
    base = 3
    funcC = cupy_backend['awkward_ListArray_fill', cupy.int64, cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [123, 123, 123, 3, 3, 3]
    cpt.assert_allclose(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [123, 123, 123, 4, 4, 4]
    cpt.assert_allclose(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

