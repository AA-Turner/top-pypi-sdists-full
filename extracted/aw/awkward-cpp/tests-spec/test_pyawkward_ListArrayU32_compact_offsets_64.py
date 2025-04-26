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

def test_pyawkward_ListArrayU32_compact_offsets_64_1():
    tooffsets = [123, 123, 123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromstarts=fromstarts, fromstops=fromstops, length=length)
    pytest_tooffsets = [0, 1, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_compact_offsets_64_2():
    tooffsets = [123, 123, 123, 123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromstarts=fromstarts, fromstops=fromstops, length=length)
    pytest_tooffsets = [0, 7, 11, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_compact_offsets_64_3():
    tooffsets = [123, 123, 123, 123]
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromstarts=fromstarts, fromstops=fromstops, length=length)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_compact_offsets_64_4():
    tooffsets = [123, 123, 123, 123]
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromstarts=fromstarts, fromstops=fromstops, length=length)
    pytest_tooffsets = [0, 0, 2, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_compact_offsets_64_5():
    tooffsets = [123, 123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromstarts=fromstarts, fromstops=fromstops, length=length)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

