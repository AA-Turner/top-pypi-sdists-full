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

def test_pyawkward_RegularArray_getitem_next_at_64_1():
    tocarry = [123, 123, 123]
    at = 0
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at_64')
    funcPy(tocarry=tocarry, at=at, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_next_at_64_2():
    tocarry = [123, 123, 123]
    at = 0
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at_64')
    funcPy(tocarry=tocarry, at=at, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_next_at_64_3():
    tocarry = [123, 123, 123]
    at = 2
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at_64')
    funcPy(tocarry=tocarry, at=at, length=length, size=size)
    pytest_tocarry = [2, 5, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_next_at_64_4():
    tocarry = [123, 123, 123]
    at = 1
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at_64')
    funcPy(tocarry=tocarry, at=at, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

