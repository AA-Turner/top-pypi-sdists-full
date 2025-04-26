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

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = []
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 0
    outerindex = [0, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_2():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = []
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 0
    outerindex = []
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 0
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_3():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 2
    outerindex = []
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 0
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [123, 123]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_4():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 2
    outerindex = [0, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str.decode('utf-8') == "index out of range"

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_5():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 2
    outerindex = [0, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_6():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_7():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 4]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_8():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 3
    outerindex = [0, 1, 1, 1, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 6
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_9():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 1, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_10():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2, 3, 4, 1, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 1, 2, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_11():
    toindex = [123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 4]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2, 3, 4, 1, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 7
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 1, 4, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_12():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_13():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 1, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_14():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 2, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_15():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 3]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 1, 2, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 2, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_16():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 3]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 1, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_17():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 3
    outerindex = [0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_18():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 3]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 2, 1, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 2, 1, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_19():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 1, 4]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2, 3, 4]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 2, 1, 4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_20():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 2, 3, 4, 5, 6, 7, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 10
    outerindex = [0, 1, 2, 3, 4, 1, 1, 1, 5, 6, 1, 1, 7, 8, 9, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 16
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 2, 3, 4, 1, 1, 1, 5, 6, 1, 1, 7, 1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_21():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 2, 1, 1, 3, 4]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 8
    outerindex = [2, 2, 1, 6, 5]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [1, 1, 1, 3, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_22():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 11
    outerindex = [0, 3, 6]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [13, 4, 15]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_23():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 11
    outerindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 9
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [13, 9, 13, 4, 8, 3, 15, 1, 16]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_24():
    toindex = [123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 11
    outerindex = [0, 1, 3, 4, 6, 7]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 6
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [13, 9, 4, 8, 15, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_25():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [2, 1, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 2, 1, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [2, 1, 1, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_26():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [3, 1, 1, 7]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 1, 2, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [3, 1, 1, 1, 7]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_27():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [3, 1, 2, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 4
    outerindex = [0, 1, 2, 1, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [3, 1, 2, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_28():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 1
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_29():
    toindex = [123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 3]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_30():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 5, 6, 7, 3, 1, 2, 0, 1, 1]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 10
    outerindex = [0, 4, 5, 7]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 3, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_31():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 3
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 3, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_32():
    toindex = [123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2, 3, 4]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 3, 2, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_33():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 5
    outerindex = [0, 1, 2, 3]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 3, 2, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_34():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 10
    outerindex = [6, 7, 8, 9, 5, 1, 1, 1, 3, 4, 1, 1, 0, 1, 2, 1]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 16
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 5, 6, 7, 3, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_35():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 10
    outerindex = [6, 7, 8, 9, 5, 1, 1, 3, 4, 1, 0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 13
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 5, 6, 7, 3, 1, 1, 1, 2, 1, 0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_36():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 10
    outerindex = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 10
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 5, 6, 7, 3, 1, 2, 0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_37():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [6, 5, 1, 3, 1, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 7
    outerindex = [0, 2, 4, 6]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [6, 1, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray32_simplify32_to64_38():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    innerindex = [6, 5, 4, 3, 2, 1, 0]
    innerindex = (ctypes.c_int32*len(innerindex))(*innerindex)
    innerlength = 7
    outerindex = [0, 2, 4, 6]
    outerindex = (ctypes.c_int32*len(outerindex))(*outerindex)
    outerlength = 4
    funcC = getattr(lib, 'awkward_IndexedArray32_simplify32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [6, 4, 2, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

