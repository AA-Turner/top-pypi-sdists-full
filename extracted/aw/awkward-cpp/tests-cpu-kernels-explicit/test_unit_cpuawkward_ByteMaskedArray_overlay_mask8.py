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

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_1():
    tomask = []
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 0
    mymask = []
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = []
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = []
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_2():
    tomask = [123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 2
    mymask = [0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = [0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_3():
    tomask = [123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 2
    mymask = [0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = [0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_4():
    tomask = [123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 2
    mymask = [1, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = [0, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_5():
    tomask = [123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 2
    mymask = [0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = [0, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 1]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_overlay_mask8_6():
    tomask = [123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    length = 2
    mymask = [1, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    theirmask = [0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 0]
    assert tomask[:len(pytest_tomask)] == pytest.approx(pytest_tomask)
    assert not ret_pass.str

