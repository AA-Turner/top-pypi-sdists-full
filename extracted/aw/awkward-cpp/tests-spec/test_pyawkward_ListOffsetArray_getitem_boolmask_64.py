# AUTO GENERATED ON 2026-11-12 AT 19:21:42
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

def test_pyawkward_ListOffsetArray_getitem_boolmask_64_1():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123, 123]
    mask = [1, 1, 1, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    carrylength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_getitem_boolmask_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, mask=mask, fromoffsets=fromoffsets, length=length, carrylength=carrylength)

def test_pyawkward_ListOffsetArray_getitem_boolmask_64_2():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123]
    mask = [0, 0, 0, 0, 0]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    carrylength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_getitem_boolmask_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, mask=mask, fromoffsets=fromoffsets, length=length, carrylength=carrylength)

def test_pyawkward_ListOffsetArray_getitem_boolmask_64_3():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123, 123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    carrylength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_getitem_boolmask_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, mask=mask, fromoffsets=fromoffsets, length=length, carrylength=carrylength)

def test_pyawkward_ListOffsetArray_getitem_boolmask_64_4():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123, 123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    carrylength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_getitem_boolmask_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, mask=mask, fromoffsets=fromoffsets, length=length, carrylength=carrylength)

def test_pyawkward_ListOffsetArray_getitem_boolmask_64_5():
    tooffsets = [123, 123, 123, 123]
    tocarry = [123]
    mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    carrylength = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray_getitem_boolmask_64')
    with pytest.raises(Exception):
        funcPy(tooffsets=tooffsets, tocarry=tocarry, mask=mask, fromoffsets=fromoffsets, length=length, carrylength=carrylength)

