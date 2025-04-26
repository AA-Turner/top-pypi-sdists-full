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

def test_pyawkward_ListOffsetArray32_toRegularArray_1():
    size = [123]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_toRegularArray')
    funcPy(size=size, fromoffsets=fromoffsets, offsetslength=offsetslength)
    pytest_size = [0]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

def test_pyawkward_ListOffsetArray32_toRegularArray_2():
    size = [123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_toRegularArray')
    with pytest.raises(Exception):
        funcPy(size=size, fromoffsets=fromoffsets, offsetslength=offsetslength)

def test_pyawkward_ListOffsetArray32_toRegularArray_3():
    size = [123]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_toRegularArray')
    with pytest.raises(Exception):
        funcPy(size=size, fromoffsets=fromoffsets, offsetslength=offsetslength)

def test_pyawkward_ListOffsetArray32_toRegularArray_4():
    size = [123]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_toRegularArray')
    with pytest.raises(Exception):
        funcPy(size=size, fromoffsets=fromoffsets, offsetslength=offsetslength)

def test_pyawkward_ListOffsetArray32_toRegularArray_5():
    size = [123]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_toRegularArray')
    funcPy(size=size, fromoffsets=fromoffsets, offsetslength=offsetslength)
    pytest_size = [0]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

