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

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_1():
    outoffsets = [123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 6
    starts = [0, 1, 2, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 4
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 1, 2, 5, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_2():
    outoffsets = [123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 0
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 0
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_3():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 2
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 1
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 2]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_4():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 9
    starts = [0, 3, 3, 5, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 5
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 3, 3, 5, 6, 9]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_5():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 6
    starts = [0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 2
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 3, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_6():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 4
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 1
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 4]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_7():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 5
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 1
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 5]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray_reduce_next_fix_offsets_64_8():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    outindexlength = 8
    starts = [0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    startslength = 1
    funcC = getattr(lib, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
    ret_pass = funcC(outoffsets, starts, startslength, outindexlength)
    pytest_outoffsets = [0, 8]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

