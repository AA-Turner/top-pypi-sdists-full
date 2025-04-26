# AUTO GENERATED ON 2025-03-19 AT 21:19:36
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

def test_cpuawkward_IndexedArrayU32_getitem_nextcarry_64_1():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_getitem_nextcarry_64_2():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [1, 2, 2]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_getitem_nextcarry_64_3():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str

def test_cpuawkward_IndexedArrayU32_getitem_nextcarry_64_4():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str

def test_cpuawkward_IndexedArrayU32_getitem_nextcarry_64_5():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 3
    lencontent = 3
    funcC = getattr(lib, 'awkward_IndexedArrayU32_getitem_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 0, 0]
    assert not ret_pass.str

