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

def test_pyawkward_ListArray32_getitem_next_at_64_1():
    tocarry = [123, 123, 123]
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    lenstarts = 3
    at = 0
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_at_64')
    funcPy(tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, lenstarts=lenstarts, at=at)
    pytest_tocarry = [2, 0, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray32_getitem_next_at_64_2():
    tocarry = [123]
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    lenstarts = 3
    at = 5
    funcPy = getattr(kernels, 'awkward_ListArray32_getitem_next_at_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, lenstarts=lenstarts, at=at)

