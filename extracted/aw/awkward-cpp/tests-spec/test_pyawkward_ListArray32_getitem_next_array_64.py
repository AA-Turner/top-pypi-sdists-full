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

def test_pyawkward_ListArray32_getitem_next_array_64_1():
    tocarry = [123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lenarray = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)

def test_pyawkward_ListArray32_getitem_next_array_64_2():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [2, 2, 2, 1, 1, 1, 1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray32_getitem_next_array_64_3():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [3, 4, 4, 2, 3, 3, 2, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray32_getitem_next_array_64_4():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [3, 2, 1, 2, 1, 0, 2, 1, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray32_getitem_next_array_64_5():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [2, 1, 3, 1, 0, 2, 1, 0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray32_getitem_next_array_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lenarray = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [1, 1, 1, 0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray32_getitem_next_array_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lenarray = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_array_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, lenstarts=lenstarts, lenarray=lenarray, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

