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

def test_pyawkward_IndexedArray_fill_to64_count_1():
    toindex = [123, 123, 123]
    toindexoffset = 0
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length, base=base)
    pytest_toindex = [3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_count_2():
    toindex = [123, 123, 123]
    toindexoffset = 0
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length, base=base)
    pytest_toindex = [3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_count_3():
    toindex = [123, 123, 123]
    toindexoffset = 0
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length, base=base)
    pytest_toindex = [3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_count_4():
    toindex = [123, 123, 123, 123]
    toindexoffset = 1
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length, base=base)
    pytest_toindex = [123, 3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray_fill_to64_count_5():
    toindex = [123, 123, 123]
    toindexoffset = 0
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_IndexedArray_fill_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length, base=base)
    pytest_toindex = [3, 4, 5]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

