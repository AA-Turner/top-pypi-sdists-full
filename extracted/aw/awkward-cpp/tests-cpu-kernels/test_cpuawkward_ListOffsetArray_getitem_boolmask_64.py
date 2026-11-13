# AUTO GENERATED ON 2026-11-12 AT 19:21:42
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import numpy as np
import pytest

from awkward_cpp.cpu_kernels import lib

def test_cpuawkward_ListOffsetArray_getitem_boolmask_64_1():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    mask = [1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    length = 3
    carrylength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_getitem_boolmask_64')
    assert funcC(tooffsets, tocarry, mask, fromoffsets, length, carrylength).str

def test_cpuawkward_ListOffsetArray_getitem_boolmask_64_2():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    mask = [0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    length = 3
    carrylength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_getitem_boolmask_64')
    assert funcC(tooffsets, tocarry, mask, fromoffsets, length, carrylength).str

def test_cpuawkward_ListOffsetArray_getitem_boolmask_64_3():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    length = 3
    carrylength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_getitem_boolmask_64')
    assert funcC(tooffsets, tocarry, mask, fromoffsets, length, carrylength).str

def test_cpuawkward_ListOffsetArray_getitem_boolmask_64_4():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    length = 3
    carrylength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_getitem_boolmask_64')
    assert funcC(tooffsets, tocarry, mask, fromoffsets, length, carrylength).str

def test_cpuawkward_ListOffsetArray_getitem_boolmask_64_5():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    length = 3
    carrylength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_getitem_boolmask_64')
    assert funcC(tooffsets, tocarry, mask, fromoffsets, length, carrylength).str

