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

def test_pyawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_1():
    toindex = [123, 123, 123]
    frommask = [1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    funcPy(toindex=toindex, frommask=frommask, length=length)
    pytest_toindex = [-1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_2():
    toindex = [123, 123, 123]
    frommask = [0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    funcPy(toindex=toindex, frommask=frommask, length=length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_3():
    toindex = [123, 123, 123]
    frommask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    funcPy(toindex=toindex, frommask=frommask, length=length)
    pytest_toindex = [-1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_4():
    toindex = [123, 123, 123]
    frommask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    funcPy(toindex=toindex, frommask=frommask, length=length)
    pytest_toindex = [-1, -1, -1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64_5():
    toindex = [123, 123, 123]
    frommask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_64')
    funcPy(toindex=toindex, frommask=frommask, length=length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

