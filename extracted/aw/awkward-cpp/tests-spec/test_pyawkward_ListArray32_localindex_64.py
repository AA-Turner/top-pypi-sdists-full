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

def test_pyawkward_ListArray32_localindex_64_1():
    toindex = [123, 123, 123, 123]
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_localindex_64')
    funcPy(toindex=toindex, offsets=offsets, length=length)
    pytest_toindex = [123, 123, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_ListArray32_localindex_64_2():
    toindex = [123]
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_localindex_64')
    funcPy(toindex=toindex, offsets=offsets, length=length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_ListArray32_localindex_64_3():
    toindex = [123, 123, 123]
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_localindex_64')
    funcPy(toindex=toindex, offsets=offsets, length=length)
    pytest_toindex = [0, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

