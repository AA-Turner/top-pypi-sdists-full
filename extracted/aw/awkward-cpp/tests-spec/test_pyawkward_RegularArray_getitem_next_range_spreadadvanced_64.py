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

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_1():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_2():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 1, 1, 1, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_3():
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_4():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 1, 1, 1, 1]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_5():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 2, 3, 3, 3, 3, 3, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_6():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 3, 3, 3, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_7():
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    nextsize = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 3, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_8():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 3, 3, 3, 3]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_9():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 2, 1, 1, 1, 0, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_10():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 1, 1, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_11():
    toadvanced = [123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    nextsize = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 1, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_12():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [2, 2, 1, 1, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_13():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 1, 0, 0, 0, 2, 2, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_14():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 0, 0, 2, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_15():
    toadvanced = [123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 0, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_16():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [1, 1, 0, 0, 2, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_17():
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    nextsize = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_18():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [0, 0, 0, 0, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_19():
    toadvanced = [123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    nextsize = 1
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [0, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_RegularArray_getitem_next_range_spreadadvanced_64_20():
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    nextsize = 2
    funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced_64')
    funcPy(toadvanced=toadvanced, fromadvanced=fromadvanced, length=length, nextsize=nextsize)
    pytest_toadvanced = [0, 0, 0, 0, 0, 0]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

