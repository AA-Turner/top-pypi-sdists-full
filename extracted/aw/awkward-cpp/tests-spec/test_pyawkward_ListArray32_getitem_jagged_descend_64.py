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

def test_pyawkward_ListArray32_getitem_jagged_descend_64_1():
    tooffsets = [123, 123, 123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)
    pytest_tooffsets = [2, 3, 5, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_2():
    tooffsets = [123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_3():
    tooffsets = [123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_4():
    tooffsets = [123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_5():
    tooffsets = [123, 123]
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_6():
    tooffsets = [123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_7():
    tooffsets = [123, 123, 123, 123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)
    pytest_tooffsets = [1, 8, 12, 17]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_8():
    tooffsets = [123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_9():
    tooffsets = [123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_10():
    tooffsets = [123]
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_11():
    tooffsets = [123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_12():
    tooffsets = [123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_13():
    tooffsets = [123, 123, 123, 123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)
    pytest_tooffsets = [1, 1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_14():
    tooffsets = [123, 123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_15():
    tooffsets = [123]
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_16():
    tooffsets = [123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_17():
    tooffsets = [123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_18():
    tooffsets = [123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_19():
    tooffsets = [123, 123, 123, 123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)
    pytest_tooffsets = [1, 1, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_20():
    tooffsets = [123]
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_21():
    tooffsets = [123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_22():
    tooffsets = [123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_23():
    tooffsets = [123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_24():
    tooffsets = [123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)

def test_pyawkward_ListArray32_getitem_jagged_descend_64_25():
    tooffsets = [123, 123, 123, 123]
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_jagged_descend_64')
    funcPy(tooffsets=tooffsets, slicestarts=slicestarts, slicestops=slicestops, sliceouterlen=sliceouterlen, fromstarts=fromstarts, fromstops=fromstops)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

