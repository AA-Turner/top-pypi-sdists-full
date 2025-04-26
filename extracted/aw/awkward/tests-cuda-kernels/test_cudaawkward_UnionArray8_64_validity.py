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

def test_cudaawkward_UnionArray8_64_validity_1():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_2():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_3():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_4():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_5():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_6():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_7():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_8():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_9():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_10():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_11():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_12():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_13():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_14():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_15():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_16():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_17():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_18():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_19():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_20():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_21():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_22():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_23():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_24():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_25():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_26():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_27():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_28():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_29():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_30():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_31():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_32():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_33():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_34():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_35():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_36():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_37():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_38():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_39():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_40():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_41():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_42():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_43():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_44():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_45():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_46():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_47():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_48():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_49():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_50():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 2
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_51():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_52():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_53():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_54():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_55():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_56():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_57():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_58():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_59():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_60():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_61():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_62():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_63():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_64():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_65():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_66():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_67():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_68():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_69():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_70():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_71():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_72():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_73():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_74():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_75():
    tags = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_76():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_77():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_78():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_79():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_80():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_81():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_82():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_83():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_84():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_85():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_86():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_87():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_88():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_89():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_90():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_91():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_92():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_93():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_94():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_95():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_96():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_97():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_98():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_99():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_100():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 3
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_101():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_102():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_103():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_104():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_105():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_106():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_107():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_108():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_109():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_110():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_111():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_112():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_113():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_114():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_115():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_116():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_117():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_118():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_119():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_120():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

def test_cudaawkward_UnionArray8_64_validity_121():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_122():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_123():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_124():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]
    funcC(tags, index, length, numcontents, lencontents)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")

def test_cudaawkward_UnionArray8_64_validity_125():
    tags = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    index = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    length = 3
    numcontents = 10
    lencontents = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    funcC = cupy_backend['awkward_UnionArray_validity', cupy.int8, cupy.int64, cupy.int64]

