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

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_1():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 3
    length = 0
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_2():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 0
    length = 0
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_3():
    nextcarry = []
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = [0, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 0
    length = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = []
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_4():
    nextcarry = [123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = [0, 1]
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 3
    length = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = [0, 3, 1, 4, 2, 5]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0, 3, 1, 4, 2, 5]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_5():
    nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = [2, 4, 6]
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 3
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [6, 12, 18, 7, 13, 19, 8, 14, 20]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_nonlocal_preparenext_64_6():
    nextcarry = [123]
    nextcarry = (ctypes.c_int64*len(nextcarry))(*nextcarry)
    nextparents = [123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    parents = [0]
    parents = (ctypes.c_int64*len(parents))(*parents)
    size = 1
    length = 1
    funcC = getattr(lib, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
    ret_pass = funcC(nextcarry, nextparents, parents, size, length)
    pytest_nextcarry = [0]
    assert nextcarry[:len(pytest_nextcarry)] == pytest.approx(pytest_nextcarry)
    pytest_nextparents = [0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

