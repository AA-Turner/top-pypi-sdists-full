# AUTO GENERATED ON 2026-07-28 AT 17:37:39
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

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_1():
    toptr = []
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_2():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 15
    offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_3():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 10
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_4():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 5, 8, 11, 11, 16, 20, 21, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 0, 0, 1, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_5():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 0, 0, 1, 1, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_6():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 1, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_NumpyArray_reduce_mask_ByteMaskedArray_64_7():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int8*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 3, 3, 5, 6, 6, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 1, 0, 0, 1, 1, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

