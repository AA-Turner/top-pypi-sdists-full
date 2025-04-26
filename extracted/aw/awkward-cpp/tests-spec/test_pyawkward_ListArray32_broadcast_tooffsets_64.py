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

def test_pyawkward_ListArray32_broadcast_tooffsets_64_1():
    tocarry = [123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    lencontent = 3
    funcPy = getattr(kernels, 'awkward_ListArray32_broadcast_tooffsets_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, fromoffsets=fromoffsets, offsetslength=offsetslength, fromstarts=fromstarts, fromstops=fromstops, lencontent=lencontent)

def test_pyawkward_ListArray32_broadcast_tooffsets_64_2():
    tocarry = [123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    lencontent = 6
    funcPy = getattr(kernels, 'awkward_ListArray32_broadcast_tooffsets_64')
    with pytest.raises(Exception):
        funcPy(tocarry=tocarry, fromoffsets=fromoffsets, offsetslength=offsetslength, fromstarts=fromstarts, fromstops=fromstops, lencontent=lencontent)

