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

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_1():
    outstarts = []
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = []
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = []
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 0
    outlength = 0
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = []
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = []
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_2():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = []
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 0
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [0]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_3():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 5, 15]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_4():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 5, 15]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_5():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 2
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [2]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_6():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 3
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_7():
    outstarts = [123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 1, 1, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 6
    outlength = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 5]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_8():
    outstarts = [123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 6
    outlength = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 6]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_9():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 1, 1, -1, 2, -1, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 9
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 5, 7]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_10():
    outstarts = [123, 123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 1, -1, -1, 2, 1, -1, 3, -1, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 12
    outlength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6, 9]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 4, 8, 10]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_11():
    outstarts = [123, 123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, -1, 1, -1, -1, -1, -1, -1, 2, 1, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 12
    outlength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6, 9]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [2, 4, 6, 12]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_12():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 4
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [4]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_13():
    outstarts = [123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, -1, 1, 1, 1, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 8
    outlength = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 4]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 8]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_14():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 5
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_15():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 10, 14]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_16():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 10, 15]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_17():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, -1, -1, -1, -1, 2, 1, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 6, 15]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_18():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, -1, 2, 2, 2, 2, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 9, 15]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_19():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 15
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5, 10]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 10, 10]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_20():
    outstarts = [123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 10
    outlength = 2
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 5]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [5, 10]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_21():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, -1, -1, -1, 1, 1, -1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 9
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 3, 8]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_22():
    outstarts = [123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, -1, -1, -1, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 9
    outlength = 3
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 3, 9]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_23():
    outstarts = [123, 123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, -1, -1, -1, -1, 1, -1, -1, 2, 1, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 12
    outlength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6, 9]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [2, 3, 7, 12]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_24():
    outstarts = [123, 123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 0]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 12
    outlength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6, 9]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [2, 3, 6, 12]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_25():
    outstarts = [123, 123, 123, 123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123, 123, 123, 123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = [0, 0, 0, -1, -1, -1, -1, -1, -1, 1, 1, 1]
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 12
    outlength = 4
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0, 3, 6, 9]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [3, 3, 6, 12]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_26():
    outstarts = [123]
    outstarts = (ctypes.c_int64*len(outstarts))(*outstarts)
    outstops = [123]
    outstops = (ctypes.c_int64*len(outstops))(*outstops)
    distincts = []
    distincts = (ctypes.c_int64*len(distincts))(*distincts)
    lendistincts = 0
    outlength = 1
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
    ret_pass = funcC(outstarts, outstops, distincts, lendistincts, outlength)
    pytest_outstarts = [0]
    assert outstarts[:len(pytest_outstarts)] == pytest.approx(pytest_outstarts)
    pytest_outstops = [0]
    assert outstops[:len(pytest_outstops)] == pytest.approx(pytest_outstops)
    assert not ret_pass.str

