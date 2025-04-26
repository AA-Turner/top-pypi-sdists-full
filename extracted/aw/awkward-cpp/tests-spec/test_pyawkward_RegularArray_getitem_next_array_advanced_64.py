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

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_1():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_2():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_3():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_4():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_5():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_6():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 6, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_7():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_8():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_9():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_10():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_11():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_12():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_13():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_14():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_15():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_16():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_17():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_18():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_19():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_20():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_21():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_22():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_23():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_24():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_25():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_26():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_27():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_28():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_29():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_30():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_31():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 7, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_32():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 6, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_33():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_34():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 6, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_35():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_36():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_37():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_38():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_39():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_40():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_41():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 6, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_42():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_43():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_44():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 5, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_45():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_46():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_47():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_48():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_49():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_50():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_51():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_52():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_53():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_54():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_55():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_56():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 6, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_57():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_58():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_59():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_60():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_61():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 4, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_62():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_63():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_64():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_65():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_66():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 3, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_67():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 2, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_68():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 1, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_69():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 2, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_70():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_71():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_72():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_73():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_74():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_75():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_76():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_77():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_78():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_79():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_80():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_81():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 5, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_82():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_83():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_84():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_85():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [3, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_86():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_87():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_88():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_89():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_90():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_91():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 4, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_92():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_93():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_94():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_95():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_96():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_97():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_98():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_99():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_100():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_101():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_102():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_103():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_104():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_105():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_106():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 5, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_107():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_108():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_109():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_110():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_111():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 5, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_112():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_113():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_114():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 4, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_115():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [2, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_116():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 4, 7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_117():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_118():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_119():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 3, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_120():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_121():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 3, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_122():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_123():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_124():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 2, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_array_advanced_64_125():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    size = 0
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromadvanced=fromadvanced, fromarray=fromarray, length=length, size=size)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

