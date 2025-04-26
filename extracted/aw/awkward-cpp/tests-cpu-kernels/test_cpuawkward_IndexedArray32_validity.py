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

def test_cpuawkward_IndexedArray32_validity_1():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_2():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_3():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_4():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_5():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_6():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_7():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_8():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_9():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_10():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_11():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_12():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_13():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_14():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_15():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 1
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_16():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_17():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_18():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_19():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_20():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 2
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    assert funcC(index, length, lencontent, isoption).str

def test_cpuawkward_IndexedArray32_validity_21():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_22():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = False
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_23():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_24():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_cpuawkward_IndexedArray32_validity_25():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = (ctypes.c_int32*len(index))(*index)
    length = 3
    lencontent = 5
    isoption = True
    funcC = getattr(lib, 'awkward_IndexedArray32_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

