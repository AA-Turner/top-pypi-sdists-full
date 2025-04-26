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

def test_pyawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_1():
    tocarry = [123, 123, 123]
    outindex = [123, 123, 123]
    mask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, outindex=outindex, mask=mask, length=length, validwhen=validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_2():
    tocarry = [123, 123, 123]
    outindex = [123, 123, 123]
    mask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, outindex=outindex, mask=mask, length=length, validwhen=validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_3():
    tocarry = [123, 123, 123]
    outindex = [123, 123, 123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, outindex=outindex, mask=mask, length=length, validwhen=validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_4():
    tocarry = [123, 123, 123]
    outindex = [123, 123, 123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    funcPy(tocarry=tocarry, outindex=outindex, mask=mask, length=length, validwhen=validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

