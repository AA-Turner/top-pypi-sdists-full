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

def test_pyawkward_ListArray32_getitem_next_range_counts_64_1():
    total = [123]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_range_counts_64')
    funcPy(total=total, fromoffsets=fromoffsets, lenstarts=lenstarts)
    pytest_total = [0]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)

def test_pyawkward_ListArray32_getitem_next_range_counts_64_2():
    total = [123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_range_counts_64')
    funcPy(total=total, fromoffsets=fromoffsets, lenstarts=lenstarts)
    pytest_total = [2]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)

def test_pyawkward_ListArray32_getitem_next_range_counts_64_3():
    total = [123]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_range_counts_64')
    funcPy(total=total, fromoffsets=fromoffsets, lenstarts=lenstarts)
    pytest_total = [-1]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)

def test_pyawkward_ListArray32_getitem_next_range_counts_64_4():
    total = [123]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_range_counts_64')
    funcPy(total=total, fromoffsets=fromoffsets, lenstarts=lenstarts)
    pytest_total = [2]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)

def test_pyawkward_ListArray32_getitem_next_range_counts_64_5():
    total = [123]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    lenstarts = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_range_counts_64')
    funcPy(total=total, fromoffsets=fromoffsets, lenstarts=lenstarts)
    pytest_total = [0]
    assert total[:len(pytest_total)] == pytest.approx(pytest_total)

