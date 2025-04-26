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

def test_pyawkward_ListArray_fill_to64_fromU32_1():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostopsoffset = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_ListArray_fill_to64_fromU32')
    funcPy(tostarts=tostarts, tostartsoffset=tostartsoffset, tostops=tostops, tostopsoffset=tostopsoffset, fromstarts=fromstarts, fromstops=fromstops, length=length, base=base)
    pytest_tostarts = [123, 123, 123, 5, 3, 5]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 6, 5, 7]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArray_fill_to64_fromU32_2():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostopsoffset = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_ListArray_fill_to64_fromU32')
    funcPy(tostarts=tostarts, tostartsoffset=tostartsoffset, tostops=tostops, tostopsoffset=tostopsoffset, fromstarts=fromstarts, fromstops=fromstops, length=length, base=base)
    pytest_tostarts = [123, 123, 123, 4, 3, 3]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 11, 7, 8]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArray_fill_to64_fromU32_3():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostopsoffset = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_ListArray_fill_to64_fromU32')
    funcPy(tostarts=tostarts, tostartsoffset=tostartsoffset, tostops=tostops, tostopsoffset=tostopsoffset, fromstarts=fromstarts, fromstops=fromstops, length=length, base=base)
    pytest_tostarts = [123, 123, 123, 4, 7, 8]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4, 7, 8]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArray_fill_to64_fromU32_4():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostopsoffset = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_ListArray_fill_to64_fromU32')
    funcPy(tostarts=tostarts, tostartsoffset=tostartsoffset, tostops=tostops, tostopsoffset=tostopsoffset, fromstarts=fromstarts, fromstops=fromstops, length=length, base=base)
    pytest_tostarts = [123, 123, 123, 4, 10, 9]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4, 12, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArray_fill_to64_fromU32_5():
    tostarts = [123, 123, 123, 123, 123, 123]
    tostartsoffset = 3
    tostops = [123, 123, 123, 123, 123, 123]
    tostopsoffset = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_ListArray_fill_to64_fromU32')
    funcPy(tostarts=tostarts, tostartsoffset=tostartsoffset, tostops=tostops, tostopsoffset=tostopsoffset, fromstarts=fromstarts, fromstops=fromstops, length=length, base=base)
    pytest_tostarts = [123, 123, 123, 3, 3, 3]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [123, 123, 123, 4, 4, 4]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

