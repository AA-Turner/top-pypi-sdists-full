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

def test_pyawkward_RegularArray_getitem_next_array_64_1():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 1, 1, 4, 4, 4, 7, 7, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_2():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 1, 1, 3, 3, 3, 5, 5, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_3():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 1, 1, 2, 2, 2, 3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 1, 1, 3, 3, 3, 5, 5, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    lenarray = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 3, 3, 5, 6, 6, 8, 9, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 3, 3, 4, 5, 5, 6, 7, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    lenarray = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 3, 3, 3, 4, 4, 4, 5, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 3, 3, 4, 5, 5, 6, 7, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    lenarray = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 3, 3, 2, 3, 3, 2, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_11():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 1, 0, 5, 4, 3, 8, 7, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_12():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 1, 0, 4, 3, 2, 6, 5, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_13():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 1, 0, 3, 2, 1, 4, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_14():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 1, 0, 4, 3, 2, 6, 5, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_15():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [2, 1, 0, 2, 1, 0, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_16():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 0, 2, 4, 3, 5, 7, 6, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 0, 2, 3, 2, 4, 5, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_18():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 0, 2, 2, 1, 3, 3, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_19():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 0, 2, 3, 2, 4, 5, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_20():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lenarray = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [1, 0, 2, 1, 0, 2, 1, 0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_21():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [0, 0, 0, 3, 3, 3, 6, 6, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_22():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_23():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_24():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_64_25():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    lenarray = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromarray=fromarray, length=length, lenarray=lenarray, size=size)
    pytest_tocarry = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

