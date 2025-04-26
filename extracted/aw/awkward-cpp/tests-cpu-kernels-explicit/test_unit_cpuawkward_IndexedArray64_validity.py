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

def test_unit_cpuawkward_IndexedArray64_validity_1():
    index = []
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 0
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_2():
    index = []
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 0
    length = 0
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_3():
    index = [0, 1, 1, 1, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 0
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str.decode('utf-8') == "index[i] >= len(content)"

def test_unit_cpuawkward_IndexedArray64_validity_4():
    index = [0, 1, 1, 1, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str.decode('utf-8') == "index[i] >= len(content)"

def test_unit_cpuawkward_IndexedArray64_validity_5():
    index = [2, -4, 4, 0, 8]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = False
    lencontent = 10
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    assert funcC(index, length, lencontent, isoption).str.decode('utf-8') == "index[i] < 0"

def test_unit_cpuawkward_IndexedArray64_validity_6():
    index = [0, 1, 1, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_7():
    index = [0, 1, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_8():
    index = [0, 1, 1, 1, 2, 3, 4]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 5
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_9():
    index = [0, 1, 1, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_10():
    index = [0, 1, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_11():
    index = [0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_12():
    index = [0, 1, 1, 2, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_13():
    index = [0, 1, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_14():
    index = [0, 1, 1, 2, 3, 1, 4, 5, 6]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 7
    length = 9
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_15():
    index = [0, 1, 1, 2, 3, 4, 1, 5]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 6
    length = 8
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_16():
    index = [0, 1, 1, 2, 3, 4, 5, 6, 7]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 8
    length = 9
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_17():
    index = [0, 1, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 6
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_18():
    index = [0, 1, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_19():
    index = [0, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_20():
    index = [0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 3
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_21():
    index = [0, 1, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_22():
    index = [0, 1, 2, 1, 3, 1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 5
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_23():
    index = [0, 1, 2, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_24():
    index = [0, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_25():
    index = [0, 1, 2, 3, 1, 4, 5, 6, 7, 8, 1, 9]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 10
    length = 12
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_26():
    index = [0, 1, 2, 3, 1, 4, 5, 6]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 7
    length = 8
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_27():
    index = [0, 1, 2, 3, 1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 5
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_28():
    index = [0, 1, 2, 3, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_29():
    index = [1, 0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_30():
    index = [1, 0, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_31():
    index = [1, 0, 1, 2, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 6
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_32():
    index = [1, 0, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_33():
    index = [1, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 4
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_34():
    index = [1, 0, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 4
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_35():
    index = [1, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_36():
    index = [1, 1, 0, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 3
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_37():
    index = [1, 1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 2
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_38():
    index = [1, 4, 4, 1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 10
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_39():
    index = [2, 1, 4, 0, 8]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 10
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_40():
    index = [2, 2, 0, 1, 4]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = True
    lencontent = 5
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_41():
    index = [2, 4, 4, 0, 8]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = False
    lencontent = 10
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_42():
    index = [6, 4, 4, 8, 0]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = False
    lencontent = 10
    length = 5
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

def test_unit_cpuawkward_IndexedArray64_validity_43():
    index = [6, 5, 4, 3, 2, 1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    isoption = False
    lencontent = 7
    length = 7
    funcC = getattr(lib, 'awkward_IndexedArray64_validity')
    ret_pass = funcC(index, length, lencontent, isoption)
    assert not ret_pass.str

