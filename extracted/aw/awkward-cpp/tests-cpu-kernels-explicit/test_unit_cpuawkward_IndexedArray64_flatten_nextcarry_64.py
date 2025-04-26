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

def test_unit_cpuawkward_IndexedArray64_flatten_nextcarry_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = []
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 0
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_flatten_nextcarry_64_2():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lencontent = 0
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray64_flatten_nextcarry_64_3():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 2]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lencontent = 2
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_nextcarry_64')
    assert funcC(tocarry, fromindex, lenindex, lencontent).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray64_flatten_nextcarry_64_4():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromindex = [0, 1]
    fromindex = (ctypes.c_int64*len(fromindex))(*fromindex)
    lencontent = 2
    lenindex = 2
    funcC = getattr(lib, 'awkward_IndexedArray64_flatten_nextcarry_64')
    ret_pass = funcC(tocarry, fromindex, lenindex, lencontent)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

