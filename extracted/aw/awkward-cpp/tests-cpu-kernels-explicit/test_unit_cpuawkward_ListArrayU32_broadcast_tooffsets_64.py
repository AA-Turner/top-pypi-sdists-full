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

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = []
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 0
    offsetslength = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 1
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_3():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 1
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    assert funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent).str.decode('utf-8') == "stops[i] > len(content)"

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_4():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [2, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 1
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    assert funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent).str.decode('utf-8') == "broadcast's offsets must be monotonically increasing"

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_5():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 1
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    assert funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent).str.decode('utf-8') == "cannot broadcast nested list"

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_6():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 0, 0, 0, 4, 4, 4, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 2, 2, 2, 5, 5, 5, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 11
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 4, 4, 4, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_7():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4, 6, 8, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 5, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_8():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 3, 3, 5, 5, 5, 8, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 5, 5, 7, 7, 7, 10, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 11
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4, 5, 6, 5, 6, 5, 6, 8, 9, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_9():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 15, 18, 21]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    offsetslength = 8
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_10():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 15, 18]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_11():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 15]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_12():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_13():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 3
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_14():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_15():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 8, 13, 18, 23, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 13, 3, 18, 8, 23]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 18, 8, 23, 13, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 13, 14, 15, 16, 17, 3, 4, 5, 6, 7, 18, 19, 20, 21, 22, 8, 9, 10, 11, 12, 23, 24, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_16():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 4
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_17():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 9, 13, 18, 23, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 13, 4, 18, 8, 23]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 18, 8, 23, 13, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 13, 14, 15, 16, 17, 4, 5, 6, 7, 18, 19, 20, 21, 22, 8, 9, 10, 11, 12, 23, 24, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_18():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 9, 14, 19, 24, 29]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 14, 4, 19, 9, 24]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 19, 9, 24, 14, 29]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 29
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 14, 15, 16, 17, 18, 4, 5, 6, 7, 8, 19, 20, 21, 22, 23, 9, 10, 11, 12, 13, 24, 25, 26, 27, 28]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_19():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 18, 21, 24, 29]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 0, 0, 8, 11, 11, 14]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 5, 11, 14, 14, 19]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 19
    offsetslength = 8
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 11, 12, 13, 14, 15, 16, 17, 18]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_20():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 4, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 4, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_21():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_22():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_23():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 5, 8]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 10, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 10, 13]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 13
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_24():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 10, 15, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 15, 20, 30]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_25():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 11, 12, 17, 22]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 11, 5, 16, 6, 17]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 16, 6, 17, 11, 22]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 22
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 5, 16, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_26():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 14, 18, 23, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 14, 5, 19, 9, 23]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 19, 9, 23, 14, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 14, 15, 16, 17, 18, 5, 6, 7, 8, 19, 20, 21, 22, 9, 10, 11, 12, 13, 23, 24, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_27():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 24, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 14, 5, 19, 10, 24]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 19, 10, 24, 14, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 14, 15, 16, 17, 18, 5, 6, 7, 8, 9, 19, 20, 21, 22, 23, 10, 11, 12, 13, 24, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_28():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 6, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 15, 16]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 16, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_29():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 15, 10, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 15, 30]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_30():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 19, 24, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 15, 5, 20, 10, 24]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 24, 15, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 10, 11, 12, 13, 14, 24, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_31():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 28]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 28]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_32():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 29]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 29]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 29
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_33():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 30]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_34():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 45, 5, 50, 10, 55]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 50, 10, 55, 15, 60]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 60
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 45, 46, 47, 48, 49, 5, 6, 7, 8, 9, 50, 51, 52, 53, 54, 10, 11, 12, 13, 14, 55, 56, 57, 58, 59]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_35():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 25
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_36():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_37():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 10, 14, 17]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 10, 14, 18]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 14, 18, 21]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 21
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_38():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 15]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 11, 14, 17]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 14, 17, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_39():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 15]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 11, 14, 17]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 14, 17, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 25
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_40():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 10, 14, 17]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 11, 15, 19]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 15, 19, 22]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 22
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_41():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 4, 6, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 4, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 4, 6, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 7
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_42():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 7
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_43():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 7
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_44():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 6, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_45():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 8, 8, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 5, 8, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 8, 8, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_46():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_47():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 7, 7, 9, 9, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 4, 7, 7, 9, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 7, 7, 9, 9, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 11
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_48():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 8, 12, 16, 19]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 8, 12, 16]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 8, 12, 16, 19]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 19
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_49():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 11, 15, 19, 22]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 6, 11, 15, 19]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 11, 15, 19, 22]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 22
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_50():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 5, 10, 15, 20, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 20, 25, 30]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_51():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 210
    offsetslength = 31
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_52():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 5, 10, 45, 50, 55]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 50, 55, 60]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 60
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_53():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 11, 15, 19, 22]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 8, 13, 17, 21]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 13, 17, 21, 24]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 24
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_54():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 8, 11, 14, 19]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 8, 11, 11, 14]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 11, 14, 14, 19]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 19
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 11, 12, 13, 14, 15, 16, 17, 18]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_55():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 8, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 4, 5, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_56():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 5, 6, 7, 7, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 4, 6, 3, 6, 7]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 7, 4, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 4, 5, 6, 3, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_57():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 5, 6, 7, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 4, 6, 3, 7]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 7, 4, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 4, 5, 6, 3, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_58():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 3, 4, 5, 6, 8]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 2, 4, 5, 6, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5, 6, 7, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 11
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 4, 5, 6, 9, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_59():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5, 6, 8]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 4, 4, 6, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 4, 6, 7, 11]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 11
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 4, 5, 6, 9, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_60():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 7
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_61():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_62():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_63():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 5, 7, 8, 9, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 6, 3, 8, 5, 9]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 8, 5, 9, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 6, 7, 3, 4, 8, 5, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_64():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 5, 5, 6, 8, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 6, 3, 8, 3, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 8, 3, 9, 5, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 6, 7, 8, 3, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_65():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 2, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_66():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4, 5, 6, 6, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 2, 5, 3, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 5, 3, 6, 3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 3, 4, 2, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_67():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 2, 4, 5, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [0, 3, 3, 5, 8]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [0, 1, 3, 4, 5, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_68():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [11, 14, 17]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [14, 17, 20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 25
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_69():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [1, 16, 6, 21, 11, 26]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 21, 11, 26, 16, 31]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 31
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 11, 12, 13, 14, 15, 26, 27, 28, 29, 30]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_70():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 3, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [1, 99, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 99, 7]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 7
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [1, 2, 3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_71():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [15, 10, 5, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 15, 10, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_72():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [15, 5, 10, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20, 10, 15, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_73():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [16]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [16, 17, 18, 19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_74():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 0, 1, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [2, 2, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_75():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [2, 4, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [2, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_76():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [25, 10, 20, 5, 15, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [30, 15, 25, 10, 20, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_77():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 10, 15, 20, 25, 30]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [25, 20, 15, 10, 5, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [30, 25, 20, 15, 10, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 30
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [25, 26, 27, 28, 29, 20, 21, 22, 23, 24, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_78():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 2, 2, 5, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 3, 3, 0, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 4, 3, 3, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 3, 0, 1, 2, 4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_79():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 2, 5, 6, 7, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 3, 0, 5, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 3, 3, 6, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 0, 1, 2, 5, 5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_80():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 3]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 16]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 20
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 15]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_81():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 4, 4, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 3, 3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 5
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 3, 4, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_82():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 7, 7, 9, 9, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 0, 999, 2, 6, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [7, 3, 999, 4, 6, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 12
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 5, 6, 0, 1, 2, 2, 3, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_83():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 2, 2, 2, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 5, 5, 5, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 5, 5, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_84():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 6, 9, 12, 14, 16]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 6, 17, 20, 11, 25]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 9, 20, 23, 13, 27]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 28
    offsetslength = 7
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 11, 12, 25, 26]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_85():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 8, 12, 16, 19]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 6, 11, 15, 19]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 11, 15, 19, 22]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 22
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_86():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 0, 2, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 3, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_87():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 2, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [3, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [3, 4, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_88():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 0, 2]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [4, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 6
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [4, 5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_89():
    tocarry = [123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 0, 2, 7]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [4, 4, 7]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4, 6, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 12
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [4, 5, 7, 8, 9, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_90():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 2, 5, 5, 7, 7, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [5, 5, 0, 3, 3, 6, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 3, 3, 5, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 8
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [5, 5, 0, 1, 2, 3, 4, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_91():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 0, 1, 4]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [5, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [5, 6, 7, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_92():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 1, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [5, 6, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_93():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 5]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [5, 6, 7, 8, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_94():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 4, 6, 6, 9]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [9, 6, 5, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 5, 3, 4, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_95():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 3, 4, 7, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 5, 6, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [9, 6, 9, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 9
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 5, 6, 7, 8, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_96():
    tocarry = [123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 1, 1, 6]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 7, 7]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [7, 7, 12]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 12
    offsetslength = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 9, 10, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_97():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 5, 8, 11, 14, 19]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 11, 14, 17, 20]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [11, 14, 17, 20, 25]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 25
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_98():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 5, 7, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_broadcast_tooffsets_64_99():
    tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [0, 4, 5, 7, 7, 10]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lencontent = 10
    offsetslength = 6
    funcC = getattr(lib, 'awkward_ListArrayU32_broadcast_tooffsets_64')
    ret_pass = funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent)
    pytest_tocarry = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

