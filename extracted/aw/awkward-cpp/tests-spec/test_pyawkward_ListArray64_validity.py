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

def test_pyawkward_ListArray64_validity_1():
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_validity')
    with pytest.raises(Exception):
        funcPy(starts=starts, stops=stops, length=length, lencontent=lencontent)

def test_pyawkward_ListArray64_validity_2():
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_validity')
    with pytest.raises(Exception):
        funcPy(starts=starts, stops=stops, length=length, lencontent=lencontent)

def test_pyawkward_ListArray64_validity_3():
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_validity')
    funcPy(starts=starts, stops=stops, length=length, lencontent=lencontent)

def test_pyawkward_ListArray64_validity_4():
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_validity')
    with pytest.raises(Exception):
        funcPy(starts=starts, stops=stops, length=length, lencontent=lencontent)

def test_pyawkward_ListArray64_validity_5():
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_validity')
    funcPy(starts=starts, stops=stops, length=length, lencontent=lencontent)

