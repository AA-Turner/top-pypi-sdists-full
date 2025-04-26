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

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_1():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [2, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [3, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [4, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_6():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_7():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_8():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_9():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_10():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 2
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    assert funcC(toindex, outerindex, outerlength, innerindex, innerlength).str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_11():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_12():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_13():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_14():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_IndexedArrayU32_simplifyU32_to64_15():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerindex = (ctypes.c_uint32*len(outerindex))(*outerindex)
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerindex = (ctypes.c_uint32*len(innerindex))(*innerindex)
    innerlength = 5
    funcC = getattr(lib, 'awkward_IndexedArrayU32_simplifyU32_to64')
    ret_pass = funcC(toindex, outerindex, outerlength, innerindex, innerlength)
    pytest_toindex = [0, 0, 0]
    assert not ret_pass.str

