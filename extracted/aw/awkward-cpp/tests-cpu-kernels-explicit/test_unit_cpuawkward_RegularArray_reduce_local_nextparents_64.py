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

def test_unit_cpuawkward_RegularArray_reduce_local_nextparents_64_1():
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    size = 3
    length = 0
    funcC = getattr(lib, 'awkward_RegularArray_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, size, length)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_local_nextparents_64_2():
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    size = 0
    length = 0
    funcC = getattr(lib, 'awkward_RegularArray_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, size, length)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_local_nextparents_64_3():
    nextparents = []
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    size = 0
    length = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, size, length)
    pytest_nextparents = []
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_local_nextparents_64_4():
    nextparents = [123, 123, 123, 123, 123, 123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    size = 3
    length = 2
    funcC = getattr(lib, 'awkward_RegularArray_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, size, length)
    pytest_nextparents = [0, 0, 0, 1, 1, 1]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_reduce_local_nextparents_64_5():
    nextparents = [123]
    nextparents = (ctypes.c_int64*len(nextparents))(*nextparents)
    size = 1
    length = 1
    funcC = getattr(lib, 'awkward_RegularArray_reduce_local_nextparents_64')
    ret_pass = funcC(nextparents, size, length)
    pytest_nextparents = [0]
    assert nextparents[:len(pytest_nextparents)] == pytest.approx(pytest_nextparents)
    assert not ret_pass.str

