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

def test_unit_cpuawkward_ListArray64_validity_1():
    lencontent = 0
    length = 0
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = []
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_2():
    lencontent = 2
    length = 0
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = []
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_3():
    lencontent = 0
    length = 3
    starts = [0, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 5]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str.decode('utf-8') == "stop[i] > len(content)"

def test_unit_cpuawkward_ListArray64_validity_4():
    lencontent = 1
    length = 3
    starts = [1, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str.decode('utf-8') == "start[i] > stop[i]"

def test_unit_cpuawkward_ListArray64_validity_5():
    lencontent = 4
    length = 3
    starts = [0, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 5]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str.decode('utf-8') == "stop[i] > len(content)"

def test_unit_cpuawkward_ListArray64_validity_6():
    lencontent = 1
    length = 4
    starts = [-1, 0, 1, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    assert funcC(starts, stops, length, lencontent).str.decode('utf-8') == "start[i] < 0"

def test_unit_cpuawkward_ListArray64_validity_7():
    lencontent = 0
    length = 5
    starts = [0, 0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 0, 0, 0, 0]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_8():
    lencontent = 0
    length = 4
    starts = [0, 0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 0, 0, 0]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_9():
    lencontent = 0
    length = 3
    starts = [0, 0, 0]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 0, 0]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_10():
    lencontent = 1
    length = 3
    starts = [0, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_11():
    lencontent = 4
    length = 3
    starts = [0, 0, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 4]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_12():
    lencontent = 1
    length = 4
    starts = [0, 0, 1, 1]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 1, 1]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_13():
    lencontent = 6
    length = 4
    starts = [0, 0, 1, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 3, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_14():
    lencontent = 10
    length = 5
    starts = [0, 0, 1, 3, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 1, 3, 6, 10]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_15():
    lencontent = 19
    length = 8
    starts = [0, 0, 3, 3, 8, 12, 12, 16]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 3, 3, 8, 12, 12, 16, 19]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_16():
    lencontent = 19
    length = 9
    starts = [0, 0, 3, 3, 8, 12, 12, 16, 19]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [0, 3, 3, 8, 12, 12, 16, 19, 19]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_17():
    lencontent = 6
    length = 3
    starts = [0, 1, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 3, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_18():
    lencontent = 15
    length = 5
    starts = [0, 1, 3, 6, 10]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 3, 6, 10, 15]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_19():
    lencontent = 12
    length = 6
    starts = [0, 1, 3, 6, 7, 9]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 3, 6, 7, 9, 12]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_20():
    lencontent = 8
    length = 4
    starts = [0, 1, 4, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [1, 4, 5, 8]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_21():
    lencontent = 3
    length = 3
    starts = [0, 2, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_22():
    lencontent = 4
    length = 3
    starts = [0, 2, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 2, 4]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_23():
    lencontent = 3
    length = 2
    starts = [0, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_24():
    lencontent = 4
    length = 2
    starts = [0, 2]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 4]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_25():
    lencontent = 8
    length = 7
    starts = [0, 2, 2, 4, 4, 5, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 2, 4, 4, 5, 5, 8]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_26():
    lencontent = 6
    length = 5
    starts = [0, 2, 2, 4, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 2, 4, 5, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_27():
    lencontent = 9
    length = 5
    starts = [0, 2, 2, 4, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 2, 4, 5, 9]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_28():
    lencontent = 3
    length = 3
    starts = [0, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 3]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_29():
    lencontent = 4
    length = 3
    starts = [0, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 4]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_30():
    lencontent = 5
    length = 3
    starts = [0, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 5]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_31():
    lencontent = 6
    length = 3
    starts = [0, 2, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_32():
    lencontent = 5
    length = 4
    starts = [0, 2, 3, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 3, 5]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_33():
    lencontent = 7
    length = 4
    starts = [0, 2, 3, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 3, 4, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_34():
    lencontent = 6
    length = 3
    starts = [0, 2, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 4, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_35():
    lencontent = 7
    length = 3
    starts = [0, 2, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 5, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_36():
    lencontent = 8
    length = 3
    starts = [0, 2, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [2, 6, 8]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_37():
    lencontent = 5
    length = 3
    starts = [0, 3, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 5]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_38():
    lencontent = 7
    length = 3
    starts = [0, 3, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_39():
    lencontent = 8
    length = 3
    starts = [0, 3, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 8]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_40():
    lencontent = 4
    length = 2
    starts = [0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 4]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_41():
    lencontent = 9
    length = 4
    starts = [0, 3, 3, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 5, 9]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_42():
    lencontent = 11
    length = 6
    starts = [0, 3, 3, 5, 6, 10]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 5, 6, 10, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_43():
    lencontent = 9
    length = 5
    starts = [0, 3, 3, 5, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 5, 6, 9]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_44():
    lencontent = 9
    length = 6
    starts = [0, 3, 3, 5, 6, 8]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 3, 5, 6, 8, 9]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_45():
    lencontent = 6
    length = 2
    starts = [0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_46():
    lencontent = 7
    length = 2
    starts = [0, 3]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 7]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_47():
    lencontent = 11
    length = 4
    starts = [0, 3, 4, 7]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 4, 7, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_48():
    lencontent = 25
    length = 7
    starts = [0, 3, 6, 11, 14, 17, 20]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 11, 14, 17, 20, 25]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_49():
    lencontent = 20
    length = 6
    starts = [0, 3, 6, 11, 14, 17]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 11, 14, 17, 20]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_50():
    lencontent = 19
    length = 5
    starts = [0, 3, 6, 11, 15]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 11, 15, 19]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_51():
    lencontent = 10
    length = 3
    starts = [0, 3, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 10]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_52():
    lencontent = 11
    length = 3
    starts = [0, 3, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_53():
    lencontent = 21
    length = 9
    starts = [0, 3, 6, 6, 10, 14, 14, 18, 21]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 6, 10, 14, 14, 18, 21, 21]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_54():
    lencontent = 21
    length = 8
    starts = [0, 3, 6, 6, 10, 14, 14, 18]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 6, 10, 14, 14, 18, 21]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_55():
    lencontent = 22
    length = 9
    starts = [0, 3, 6, 6, 11, 15, 15, 19, 22]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 6, 11, 15, 15, 19, 22, 22]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_56():
    lencontent = 22
    length = 8
    starts = [0, 3, 6, 6, 11, 15, 15, 19]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 6, 11, 15, 15, 19, 22]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_57():
    lencontent = 24
    length = 9
    starts = [0, 3, 6, 8, 13, 17, 17, 21, 24]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 8, 13, 17, 17, 21, 24, 24]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_58():
    lencontent = 24
    length = 8
    starts = [0, 3, 6, 8, 13, 17, 17, 21]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 6, 8, 13, 17, 17, 21, 24]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_59():
    lencontent = 9
    length = 3
    starts = [0, 3, 7]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [3, 7, 9]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_60():
    lencontent = 10
    length = 2
    starts = [0, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 10]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_61():
    lencontent = 6
    length = 3
    starts = [0, 4, 4]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 4, 6]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_62():
    lencontent = 10
    length = 3
    starts = [0, 4, 6]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 6, 10]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_63():
    lencontent = 14
    length = 4
    starts = [0, 4, 6, 9]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 6, 9, 14]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_64():
    lencontent = 11
    length = 6
    starts = [0, 4, 7, 7, 9, 9]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 7, 7, 9, 9, 11]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_65():
    lencontent = 12
    length = 3
    starts = [0, 4, 8]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [4, 8, 12]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_66():
    lencontent = 30
    length = 6
    starts = [0, 5, 10, 15, 20, 25]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [5, 10, 15, 20, 25, 30]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_67():
    lencontent = 10
    length = 2
    starts = [0, 5]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [5, 10]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_validity_68():
    lencontent = 12
    length = 6
    starts = [3, 0, 999, 2, 6, 10]
    starts = (ctypes.c_int64*len(starts))(*starts)
    stops = [7, 3, 999, 4, 6, 12]
    stops = (ctypes.c_int64*len(stops))(*stops)
    funcC = getattr(lib, 'awkward_ListArray64_validity')
    ret_pass = funcC(starts, stops, length, lencontent)
    assert not ret_pass.str

