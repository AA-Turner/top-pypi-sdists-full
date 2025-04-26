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

def test_pyawkward_ListArrayU32_rpad_and_clip_length_axis1_1():
    tomin = [123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    target = 3
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_and_clip_length_axis1')
    funcPy(tomin=tomin, fromstarts=fromstarts, fromstops=fromstops, target=target, lenstarts=lenstarts)
    pytest_tomin = [9]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)

def test_pyawkward_ListArrayU32_rpad_and_clip_length_axis1_2():
    tomin = [123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    target = 3
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_and_clip_length_axis1')
    funcPy(tomin=tomin, fromstarts=fromstarts, fromstops=fromstops, target=target, lenstarts=lenstarts)
    pytest_tomin = [16]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)

def test_pyawkward_ListArrayU32_rpad_and_clip_length_axis1_3():
    tomin = [123]
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    target = 3
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_and_clip_length_axis1')
    funcPy(tomin=tomin, fromstarts=fromstarts, fromstops=fromstops, target=target, lenstarts=lenstarts)
    pytest_tomin = [9]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)

def test_pyawkward_ListArrayU32_rpad_and_clip_length_axis1_4():
    tomin = [123]
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    target = 3
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_and_clip_length_axis1')
    funcPy(tomin=tomin, fromstarts=fromstarts, fromstops=fromstops, target=target, lenstarts=lenstarts)
    pytest_tomin = [9]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)

def test_pyawkward_ListArrayU32_rpad_and_clip_length_axis1_5():
    tomin = [123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    target = 3
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_rpad_and_clip_length_axis1')
    funcPy(tomin=tomin, fromstarts=fromstarts, fromstops=fromstops, target=target, lenstarts=lenstarts)
    pytest_tomin = [9]
    assert tomin[:len(pytest_tomin)] == pytest.approx(pytest_tomin)

