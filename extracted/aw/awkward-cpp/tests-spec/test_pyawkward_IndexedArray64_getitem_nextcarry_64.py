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

def test_pyawkward_IndexedArray64_getitem_nextcarry_64_1():
    tocarry = [123, 123, 123]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    lenindex = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray64_getitem_nextcarry_64')
    funcPy(tocarry=tocarry, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_IndexedArray64_getitem_nextcarry_64_2():
    tocarry = [123, 123, 123]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    lenindex = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray64_getitem_nextcarry_64')
    funcPy(tocarry=tocarry, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)
    pytest_tocarry = [1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_IndexedArray64_getitem_nextcarry_64_3():
    tocarry = [123]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    lenindex = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray64_getitem_nextcarry_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)

def test_pyawkward_IndexedArray64_getitem_nextcarry_64_4():
    tocarry = [123]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    lenindex = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray64_getitem_nextcarry_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)

def test_pyawkward_IndexedArray64_getitem_nextcarry_64_5():
    tocarry = [123, 123, 123]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lenindex = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray64_getitem_nextcarry_64')
    funcPy(tocarry=tocarry, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

