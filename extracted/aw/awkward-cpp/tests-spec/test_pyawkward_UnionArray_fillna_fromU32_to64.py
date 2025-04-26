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

def test_pyawkward_UnionArray_fillna_fromU32_to64_1():
    toindex = [123, 123, 123]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillna_fromU32_to64')
    funcPy(toindex=toindex, fromindex=fromindex, length=length)
    pytest_toindex = [1, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_UnionArray_fillna_fromU32_to64_2():
    toindex = [123, 123, 123]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillna_fromU32_to64')
    funcPy(toindex=toindex, fromindex=fromindex, length=length)
    pytest_toindex = [1, 2, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_UnionArray_fillna_fromU32_to64_3():
    toindex = [123, 123, 123]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillna_fromU32_to64')
    funcPy(toindex=toindex, fromindex=fromindex, length=length)
    pytest_toindex = [1, 3, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_UnionArray_fillna_fromU32_to64_4():
    toindex = [123, 123, 123]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillna_fromU32_to64')
    funcPy(toindex=toindex, fromindex=fromindex, length=length)
    pytest_toindex = [1, 4, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_UnionArray_fillna_fromU32_to64_5():
    toindex = [123, 123, 123]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillna_fromU32_to64')
    funcPy(toindex=toindex, fromindex=fromindex, length=length)
    pytest_toindex = [0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

