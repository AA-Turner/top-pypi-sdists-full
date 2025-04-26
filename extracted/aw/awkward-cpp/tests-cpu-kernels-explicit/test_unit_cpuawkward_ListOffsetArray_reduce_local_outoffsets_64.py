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

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_1():
    outoffsets = [123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 0
    outlength = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_2():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 10
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 10]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_3():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 1
    outlength = 1
    parents = [0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_4():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 3
    outlength = 3
    parents = [0, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 1, 1, 3]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_5():
    outoffsets = [123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 3
    outlength = 4
    parents = [0, 1, 3]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 1, 2, 2, 3]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_6():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 3
    outlength = 3
    parents = [0, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 1, 3, 3]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_7():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 4
    outlength = 3
    parents = [0, 1, 1, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 1, 3, 4]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_8():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 2
    outlength = 1
    parents = [0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_9():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 6
    outlength = 5
    parents = [0, 0, 2, 2, 3, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 2, 4, 5, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_10():
    outoffsets = [123, 123, 123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 7
    outlength = 5
    parents = [0, 0, 2, 2, 3, 4, 4]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 2, 4, 5, 7]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_11():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 3
    outlength = 2
    parents = [0, 0, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 3]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_12():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 4
    outlength = 2
    parents = [0, 0, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 2, 4]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_13():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 3
    outlength = 1
    parents = [0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 3]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_14():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 6
    outlength = 2
    parents = [0, 0, 0, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 3, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_15():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 4
    outlength = 1
    parents = [0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 4]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_16():
    outoffsets = [123, 123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 6
    outlength = 3
    parents = [0, 0, 0, 0, 2, 2]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 4, 4, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_17():
    outoffsets = [123, 123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 8
    outlength = 2
    parents = [0, 0, 0, 0, 1, 1, 1, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 4, 8]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_18():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 5
    outlength = 1
    parents = [0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 5]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_19():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 6
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 6]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_20():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 7
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 7]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_21():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 8
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 8]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListOffsetArray_reduce_local_outoffsets_64_22():
    outoffsets = [123, 123]
    outoffsets = (ctypes.c_int64*len(outoffsets))(*outoffsets)
    lenparents = 9
    outlength = 1
    parents = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    funcC = getattr(lib, 'awkward_ListOffsetArray_reduce_local_outoffsets_64')
    ret_pass = funcC(outoffsets, parents, lenparents, outlength)
    pytest_outoffsets = [0, 9]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)
    assert not ret_pass.str

