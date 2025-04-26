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

def test_cudaawkward_IndexedArray32_validity_1():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_2():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = False
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_3():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_4():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_5():
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_6():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_7():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = False
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_8():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_9():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_10():
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_11():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_12():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = False
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_13():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_14():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_15():
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int32)
    length = 3
    lencontent = 1
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_16():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_17():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = False
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_18():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_19():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_20():
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int32)
    length = 3
    lencontent = 2
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]

def test_cudaawkward_IndexedArray32_validity_21():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    lencontent = 5
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_22():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    lencontent = 5
    isoption = False
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_23():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    lencontent = 5
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_24():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    lencontent = 5
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_IndexedArray32_validity_25():
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    length = 3
    lencontent = 5
    isoption = True
    funcC = cupy_backend['awkward_IndexedArray_validity', cupy.int32]
    funcC(index, length, lencontent, isoption)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

