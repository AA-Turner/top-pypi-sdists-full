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

def test_unit_cpuawkward_ListArray_fill_to64_from32_1():
    tostarts = []
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = []
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = []
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 0
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = []
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = []
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_2():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 0, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [0, 1, 3]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 0, 1]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [0, 1, 3]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_3():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 2, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 4]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 2, 2]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 2, 4]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_4():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 2, 4]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4, 6]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 2, 4]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [2, 4, 6]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_5():
    tostarts = [123, 123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 3, 3, 5, 6]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 6, 10]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 5
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 3, 3, 5, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 3, 5, 6, 10]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_6():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 3, 3]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 3, 5]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_7():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 3, 6]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 11]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 11]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_8():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 5, 10]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 3
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 5, 10]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [5, 10, 15]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_9():
    tostarts = [123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [0, 7]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [7, 14]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 2
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [0, 7]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [7, 14]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_10():
    tostarts = [123, 123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [1, 3, 3, 3]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 5]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 4
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [1, 3, 3, 3]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 3, 3, 5]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_fill_to64_from32_11():
    tostarts = [123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    base = 0
    fromstarts = [3, 5]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [5, 5]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    length = 2
    tostartsoffset = 0
    tostopsoffset = 0
    funcC = getattr(lib, 'awkward_ListArray_fill_to64_from32')
    ret_pass = funcC(tostarts, tostartsoffset, tostops, tostopsoffset, fromstarts, fromstops, length, base)
    pytest_tostarts = [3, 5]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [5, 5]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

