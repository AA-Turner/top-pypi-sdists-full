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

def test_pyawkward_ListArrayU32_rpad_axis1_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_axis1_64')
    funcPy(toindex=toindex, fromstarts=fromstarts, fromstops=fromstops, tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_toindex = [2, -1, -1, 0, 1, -1, 2, 3, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArrayU32_rpad_axis1_64_2():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_axis1_64')
    funcPy(toindex=toindex, fromstarts=fromstarts, fromstops=fromstops, tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_toindex = [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 7, 11]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [7, 11, 16]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArrayU32_rpad_axis1_64_3():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_axis1_64')
    funcPy(toindex=toindex, fromstarts=fromstarts, fromstops=fromstops, tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArrayU32_rpad_axis1_64_4():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_axis1_64')
    funcPy(toindex=toindex, fromstarts=fromstarts, fromstops=fromstops, tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_toindex = [-1, -1, -1, 7, 8, -1, -1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

def test_pyawkward_ListArrayU32_rpad_axis1_64_5():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_axis1_64')
    funcPy(toindex=toindex, fromstarts=fromstarts, fromstops=fromstops, tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_toindex = [0, -1, -1, 0, -1, -1, 0, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

