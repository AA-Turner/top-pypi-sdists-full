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

def test_pyawkward_RegularArray_getitem_carry_64_1():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_2():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_3():
    tocarry = [123, 123, 123]
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_4():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lencarry = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [6, 7, 8, 9, 10, 11, 9, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_6():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_7():
    tocarry = [123, 123, 123]
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lencarry = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_8():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lencarry = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_10():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_11():
    tocarry = [123, 123, 123]
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lencarry = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_12():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_13():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [3, 4, 5, 0, 1, 2, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_14():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_15():
    tocarry = [123, 123, 123]
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [1, 0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_16():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    lencarry = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_18():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_19():
    tocarry = [123, 123, 123]
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    lencarry = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_RegularArray_getitem_carry_64_20():
    tocarry = [123, 123, 123, 123, 123, 123]
    fromcarry = [0, 0, 0, 0, 0, 0, 0, 0]
    lencarry = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry_64')
    funcPy(tocarry=tocarry, fromcarry=fromcarry, lencarry=lencarry, size=size)
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

