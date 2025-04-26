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

def test_cpuawkward_ByteMaskedArray_overlay_mask8_1():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_2():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_3():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_4():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_5():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_6():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_7():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_8():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_9():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_10():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_11():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_12():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_13():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_14():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_15():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_16():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_17():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_18():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_19():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_20():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_21():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_22():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_23():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_24():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_overlay_mask8_25():
    tomask = [123, 123, 123]
    tomask = (ctypes.c_int8*len(tomask))(*tomask)
    theirmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    theirmask = (ctypes.c_int8*len(theirmask))(*theirmask)
    mymask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mymask = (ctypes.c_int8*len(mymask))(*mymask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_overlay_mask8')
    ret_pass = funcC(tomask, theirmask, mymask, length, validwhen)
    pytest_tomask = [1, 1, 1]
    assert not ret_pass.str

