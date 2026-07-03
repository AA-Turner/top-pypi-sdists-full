# AUTO GENERATED ON 2026-07-02 AT 19:33:43
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

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 3
    length = 0
    outlength = 0
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_2():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 1, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 0
    length = 2
    outlength = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_3():
    nextcarry = [123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 1, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 2
    length = 2
    outlength = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = [0, 1, 2, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 1, 2, 3, 4]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_4():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 3
    length = 2
    outlength = 1
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = [0, 3, 1, 4, 2, 5]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2, 4, 6]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_5():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 2, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 2
    length = 3
    outlength = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = [0, 2, 1, 3, 4, 5]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 2, 4, 5, 6]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_6():
    nextcarry = [123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123, 123, 123, 123, 123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 0, 2, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 2
    length = 2
    outlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = [0, 2, 1, 3]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 0, 0, 2, 4, 4, 4]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_7():
    nextcarry = [123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextoffsets = [123, 123]
    nextoffsets = (ctypes.c_int64*len(nextoffsets))(*nextoffsets)
    offsets = [0, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    size = 1
    length = 1
    outlength = 1
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextoffsets, offsets, size, length, outlength)
    pytest_nextcarry = [0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextoffsets = [0, 1]
    assert nextoffsets[:len(pytest_nextoffsets)] == pytest.approx(pytest_nextoffsets)
    assert not ret_pass.str

