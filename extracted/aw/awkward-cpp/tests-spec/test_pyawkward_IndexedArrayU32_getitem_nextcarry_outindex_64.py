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

def test_pyawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_1():
    tocarry = [123, 123, 123]
    toindex = [123, 123, 123]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    lenindex = 3
    lencontent = 2
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, toindex=toindex, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_2():
    tocarry = [123]
    toindex = [123]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    lenindex = 3
    lencontent = 2
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toindex=toindex, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)

def test_pyawkward_IndexedArrayU32_getitem_nextcarry_outindex_64_3():
    tocarry = [123, 123, 123]
    toindex = [123, 123, 123]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lenindex = 3
    lencontent = 5
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, toindex=toindex, fromindex=fromindex, lenindex=lenindex, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

