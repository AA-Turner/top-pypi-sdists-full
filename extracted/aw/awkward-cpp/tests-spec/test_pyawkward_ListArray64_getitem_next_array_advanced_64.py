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

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_1():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_2():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_3():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_4():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_5():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_6():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_7():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_8():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_9():
    tocarry = [123, 123]
    toadvanced = [123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_10():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_11():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_12():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_13():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_14():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_15():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [4, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_16():
    tocarry = [123]
    toadvanced = [123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_17():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [4, 3, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_18():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [4, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_19():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [3, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_20():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_21():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_22():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_23():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 2, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_24():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [3, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_25():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_26():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [3, 3, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_27():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [3, 0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_28():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_29():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [2, 1, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_30():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_31():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_32():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_33():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_34():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 10
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_35():
    tocarry = [123]
    toadvanced = [123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_36():
    tocarry = [123]
    toadvanced = [123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_37():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_38():
    tocarry = [123]
    toadvanced = [123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_39():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_40():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_41():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_42():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

def test_pyawkward_ListArray64_getitem_next_array_advanced_64_43():
    tocarry = [123, 123, 123]
    toadvanced = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromarray = [0, 0, 0, 0, 0, 0, 0, 0]
    fromadvanced = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_next_array_advanced_64')
    funcPy(tocarry=tocarry, toadvanced=toadvanced, fromstarts=fromstarts, fromstops=fromstops, fromarray=fromarray, fromadvanced=fromadvanced, lenstarts=lenstarts, lencontent=lencontent)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_toadvanced = [0, 1, 2]
    assert toadvanced[:len(pytest_toadvanced)] == pytest.approx(pytest_toadvanced)

