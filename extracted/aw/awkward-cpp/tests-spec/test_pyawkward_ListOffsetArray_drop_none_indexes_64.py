# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_1():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_2():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_3():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_4():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_5():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_6():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_7():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_8():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_9():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_10():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_11():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_12():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_13():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_14():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_15():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_16():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_17():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_18():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_19():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_20():
    tooffsets = [123, 123, 123]
    noneindexes = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_21():
    tooffsets = [123, 123, 123]
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_22():
    tooffsets = [123, 123, 123]
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_23():
    tooffsets = [123, 123, 123]
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [2, 1, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_24():
    tooffsets = [123, 123, 123]
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [1, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray_drop_none_indexes_64_25():
    tooffsets = [123, 123, 123]
    noneindexes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length_offsets = 3
    length_indexes = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes_64')
    funcPy(tooffsets=tooffsets, noneindexes=noneindexes, fromoffsets=fromoffsets, length_offsets=length_offsets, length_indexes=length_indexes)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

