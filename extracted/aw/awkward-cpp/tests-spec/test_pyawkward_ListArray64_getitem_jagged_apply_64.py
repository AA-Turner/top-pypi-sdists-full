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

def test_pyawkward_ListArray64_getitem_jagged_apply_64_1():
    tooffsets = [123, 123, 123]
    tocarry = [123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    contentlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_2():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [1, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_3():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    contentlen = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_4():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    sliceinnerlen = 2
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_5():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    sliceinnerlen = 1
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_6():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    sliceinnerlen = 1
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_7():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    sliceinnerlen = 2
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [2, 1, 1, 1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_8():
    tooffsets = [123, 123, 123]
    tocarry = [123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    contentlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_9():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    contentlen = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [1, 0, 0, 0, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_apply_64_10():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tocarry = [123, 123, 123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 6
    sliceindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sliceinnerlen = 5
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    contentlen = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_apply_64')
    funcPy(tooffsets=tooffsets, tocarry=tocarry, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, sliceindex=sliceindex, sliceinnerlen=sliceinnerlen, fromstarts=fromstarts, fromstops=fromstops, contentlen=contentlen)
    pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    pytest_tocarry = [0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

