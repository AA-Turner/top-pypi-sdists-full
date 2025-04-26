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

def test_pyawkward_ListArray_getitem_jagged_shrink_64_1():
    tocarry = [123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [2, 3, 5, 7]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_2():
    tocarry = [123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [2, 3, 5, 7]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_3():
    tocarry = [123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [2, 3, 5, 7]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_4():
    tocarry = [123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [2, 3, 5, 7]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_5():
    tocarry = [123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [2, 0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [2, 3, 5, 7]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [2, 3, 5, 7]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 8, 12, 17]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 8, 12, 17]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 8, 12, 17]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 8, 12, 17]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 8, 12, 17]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 8, 12, 17]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_11():
    tocarry = [123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 1, 3, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_12():
    tocarry = [123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 1, 3, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_13():
    tocarry = [123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 1, 3, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_14():
    tocarry = [123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 1, 3, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_15():
    tocarry = [123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [1, 1, 3, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [1, 1, 3, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_16():
    tocarry = [123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    missing = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [0, 1, 2, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_17():
    tocarry = [123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    missing = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [0, 1, 2, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_18():
    tocarry = [123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    missing = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [0, 1, 2, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_19():
    tocarry = [123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    missing = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [0, 1, 2, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

def test_pyawkward_ListArray_getitem_jagged_shrink_64_20():
    tocarry = [123, 123, 123]
    tosmalloffsets = [123, 123, 123, 123]
    tolargeoffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink_64')
    funcPy(tocarry=tocarry, tosmalloffsets=tosmalloffsets, tolargeoffsets=tolargeoffsets, slicestarts=slicestarts, slicestops=slicestops, length=length, missing=missing)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_tosmalloffsets = [0, 1, 2, 3]
    assert tosmalloffsets[:len(pytest_tosmalloffsets)] == pytest.approx(pytest_tosmalloffsets)
    pytest_tolargeoffsets = [0, 1, 2, 3]
    assert tolargeoffsets[:len(pytest_tolargeoffsets)] == pytest.approx(pytest_tolargeoffsets)

