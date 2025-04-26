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

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_1():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    assert funcC(tocarry, fromstarts, fromstops, lenstarts, at).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [3, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    assert funcC(tocarry, fromstarts, fromstops, lenstarts, at).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_4():
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = []
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 0
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_5():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_6():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_7():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_8():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -5
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_9():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0, 1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0, 1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_10():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0, 1, 2, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 2, 3, 4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_11():
    tocarry = [123, 123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0, 1, 2, 3, 4]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 2, 3, 4, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 5
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0, 1, 2, 3, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_12():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0, 2, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_13():
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [0, 3, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 6, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 4
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [0, 3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_14():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_15():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_16():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_17():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_18():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_19():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_20():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [2]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_21():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_22():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [13]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_23():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3, 5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1, 4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_24():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [1, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_25():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [16]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_26():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [18]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_27():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [15]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [20]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [19]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_28():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_29():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_30():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [1]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [4]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_31():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [3]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_32():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [2]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_33():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_34():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_35():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [3, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [3, 5, 6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_36():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_37():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 4
    fromstarts = [0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_38():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_39():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_40():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_41():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [3, 5, 6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 6, 9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4, 5, 8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_42():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [0, 5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [5, 10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [4, 9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_43():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [5, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [5, 10]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_44():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [3]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [6]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_45():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 0
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_46():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -5
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [5]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_47():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [5, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [6, 11]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_48():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [6]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_49():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_50():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 1
    fromstarts = [6]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [9]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [7]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_51():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -2
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [8]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_52():
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [5, 10]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10, 15]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 2
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [9, 14]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_53():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = -1
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArrayU32_getitem_next_at_64_54():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    at = 4
    fromstarts = [5]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [10]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    lenstarts = 1
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [9]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

