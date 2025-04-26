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

def test_pyawkward_BitMaskedArray_to_IndexedOptionArray64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    funcPy(toindex=toindex, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_BitMaskedArray_to_IndexedOptionArray64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [0, 0, 0, 0, 0]
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    funcPy(toindex=toindex, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_BitMaskedArray_to_IndexedOptionArray64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    funcPy(toindex=toindex, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_BitMaskedArray_to_IndexedOptionArray64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    funcPy(toindex=toindex, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_toindex = [0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_BitMaskedArray_to_IndexedOptionArray64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray64')
    funcPy(toindex=toindex, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, -1, 8, 9, 10, 11, 12, 13, 14, -1, 16, 17, 18, 19, 20, 21, 22, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

