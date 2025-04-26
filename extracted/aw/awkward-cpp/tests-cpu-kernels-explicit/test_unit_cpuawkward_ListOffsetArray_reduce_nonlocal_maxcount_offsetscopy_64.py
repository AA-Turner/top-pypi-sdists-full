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

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_1():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [0]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_2():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 1
    offsets = [0, 2]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [2]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 2]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_3():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 2, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [2]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 2, 3, 5]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_4():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 2, 4, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [2]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 2, 4, 6]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_5():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 3, 3, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 3, 5]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_6():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 3, 5, 6, 8, 9]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_7():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 5
    offsets = [0, 3, 3, 5, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 3, 5, 6, 9]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_8():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 3, 5, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 5, 5, 6, 8, 9]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_9():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 3, 5, 6, 7, 7, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 5, 6, 7, 7, 9]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_10():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 5
    offsets = [0, 3, 5, 6, 7, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 5, 6, 7, 9]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_11():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 3, 5, 7, 8, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 5, 7, 8, 9, 10]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_12():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 2
    offsets = [0, 3, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 6]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_13():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 5
    offsets = [0, 3, 6, 9, 12, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [3]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 6, 9, 12, 15]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_14():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 9
    offsets = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_15():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 3, 3, 7]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 3, 7]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_16():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 6, 10]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_17():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 4, 4, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 4, 4, 6]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_18():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 2
    offsets = [0, 4, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 4, 6]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_19():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 4, 8, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [4]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 4, 8, 12]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_20():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 3, 8, 13, 18, 23, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 3, 8, 13, 18, 23, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_21():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 4, 9, 13, 18, 23, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 4, 9, 13, 18, 23, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_22():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 4, 9, 14, 19, 24, 29]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 4, 9, 14, 19, 24, 29]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_23():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 11, 12, 17, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 11, 12, 17, 22]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_24():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 14, 18, 23, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 14, 18, 23, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_25():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 5, 10, 15]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_26():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 15, 19, 24, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 19, 24, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_27():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 4
    offsets = [0, 5, 10, 15, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_28():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 15, 20, 24, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20, 24, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_29():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 5
    offsets = [0, 5, 10, 15, 20, 25]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20, 25]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_30():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 15, 20, 25, 28]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 28]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_31():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 15, 20, 25, 29]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 29]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_32():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 10, 15, 20, 25, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 30]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_33():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 6
    offsets = [0, 5, 6, 11, 16, 17, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 6, 11, 16, 17, 22]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_34():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 5
    offsets = [0, 5, 8, 11, 14, 17]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 8, 11, 14, 17]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_35():
    maxcount = [123]
    maxcount = (ctypes.c_int64*len(maxcount))(*maxcount)
    offsetscopy = [123, 123, 123, 123]
    offsetscopy = (ctypes.c_int64*len(offsetscopy))(*offsetscopy)
    length = 3
    offsets = [0, 5, 9, 12]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
    ret_pass = funcC(maxcount, offsetscopy, offsets, length)
    pytest_maxcount = [5]
    assert maxcount[:len(pytest_maxcount)] == pytest.approx(pytest_maxcount)
    pytest_offsetscopy = [0, 5, 9, 12]
    assert offsetscopy[:len(pytest_offsetscopy)] == pytest.approx(pytest_offsetscopy)
    assert not ret_pass.str

