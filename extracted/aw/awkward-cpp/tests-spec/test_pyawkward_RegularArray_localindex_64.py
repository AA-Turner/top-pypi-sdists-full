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

def test_pyawkward_RegularArray_localindex_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    size = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_localindex_64')
    funcPy(toindex=toindex, size=size, length=length)
    pytest_toindex = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_RegularArray_localindex_64_2():
    toindex = [123, 123, 123, 123, 123, 123]
    size = 2
    length = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_localindex_64')
    funcPy(toindex=toindex, size=size, length=length)
    pytest_toindex = [0, 1, 0, 1, 0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_RegularArray_localindex_64_3():
    toindex = [123, 123, 123]
    size = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_localindex_64')
    funcPy(toindex=toindex, size=size, length=length)
    pytest_toindex = [0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_RegularArray_localindex_64_4():
    toindex = [123, 123, 123, 123, 123, 123]
    size = 2
    length = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_localindex_64')
    funcPy(toindex=toindex, size=size, length=length)
    pytest_toindex = [0, 1, 0, 1, 0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

