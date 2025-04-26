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

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_1():
    outoffsets = [123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = []
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 0
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = []
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_2():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 1
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 2
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_3():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 2
    parents = [1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 2
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 2]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [1, 0]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_4():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123, 123, 123, 123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 6
    parents = [0, 0, 0, 1, 1, 1, 2, 3, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 11
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 3, 6, 7, 8, 11, 11]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0, 1, 2, 3, 5, 4]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_5():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123, 123, 123, 123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 6
    parents = [0, 0, 0, 1, 1, 1, 3, 3, 5, 5, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 11
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 3, 6, 8, 11, 11, 11]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0, 1, 4, 2, 5, 3]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_6():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123, 123, 123, 123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 6
    parents = [0, 0, 3, 3, 1, 1, 4, 4, 2, 2, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 11
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 4, 6, 8, 10, 11]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0, 2, 4, 1, 3, 5]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_7():
    outoffsets = [123, 123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123, 123, 123, 123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 6
    parents = [0, 0, 0, 3, 1, 1, 4, 4, 2, 2, 5]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 11
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 3, 4, 6, 8, 10, 11]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0, 2, 4, 1, 3, 5]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

def test_unit_cpuawkward_RecordArray_reduce_nonlocal_outoffsets_64_8():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outcarry = [123, 123, 123, 123, 123]
    outcarry = (ctypes.c_int64*len(outcarry))(*outcarry)
    outlength = 5
    parents = [0, 0, 1, 1, 1, 2, 3, 3, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    lenparents = 10
    funcC = getattr(lib, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
    ret_pass = funcC(outoffsets, outcarry, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 5, 6, 8, 10]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    pytest_outcarry = [0, 1, 2, 3, 4]
    assert outcarry[:len(pytest_outcarry)] == pytest.approx(pytest_outcarry)
    assert not ret_pass.str

