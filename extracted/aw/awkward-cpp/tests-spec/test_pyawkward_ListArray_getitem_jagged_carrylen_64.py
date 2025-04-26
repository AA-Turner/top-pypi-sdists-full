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

def test_pyawkward_ListArray_getitem_jagged_carrylen_64_1():
    carrylen = [123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen_64')
    funcPy(carrylen=carrylen, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)

def test_pyawkward_ListArray_getitem_jagged_carrylen_64_2():
    carrylen = [123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen_64')
    funcPy(carrylen=carrylen, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen)
    pytest_carrylen = [16]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)

def test_pyawkward_ListArray_getitem_jagged_carrylen_64_3():
    carrylen = [123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen_64')
    funcPy(carrylen=carrylen, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)

def test_pyawkward_ListArray_getitem_jagged_carrylen_64_4():
    carrylen = [123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen_64')
    funcPy(carrylen=carrylen, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen)
    pytest_carrylen = [2]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)

def test_pyawkward_ListArray_getitem_jagged_carrylen_64_5():
    carrylen = [123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen_64')
    funcPy(carrylen=carrylen, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen)
    pytest_carrylen = [3]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)

