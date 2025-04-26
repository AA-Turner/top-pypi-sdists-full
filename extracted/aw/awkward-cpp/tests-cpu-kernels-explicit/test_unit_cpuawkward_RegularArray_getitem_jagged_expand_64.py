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

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_1():
    multistarts = []
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = []
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 0
    regularsize = 0
    singleoffsets = [0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = []
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = []
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_2():
    multistarts = []
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = []
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 0
    singleoffsets = [1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = []
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = []
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_3():
    multistarts = []
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = []
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 0
    regularsize = 0
    singleoffsets = [0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = []
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = []
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_4():
    multistarts = [123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 1
    singleoffsets = [0, 2]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_5():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 2
    regularsize = 1
    singleoffsets = [0, 2]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_6():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 4
    singleoffsets = [0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0, 0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_7():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_8():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 4
    singleoffsets = [0, 0, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 1, 1, 1]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_9():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 1, 1, 3]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 3]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_10():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 1, 1, 3, 3, 5]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 1, 1, 3, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 3, 3, 5]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_11():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 2, 2, 2, 2, 6]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 2, 2, 6]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_12():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 2, 2, 3]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 3]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_13():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 2, 2, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_14():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 2
    singleoffsets = [0, 2, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_15():
    multistarts = [123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 7
    singleoffsets = [0, 2, 2, 4, 4, 5, 5, 8]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2, 4, 4, 5, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 4, 4, 5, 5, 8]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_16():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 2, 2, 4, 5, 6]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2, 4, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 4, 5, 6]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_17():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 2, 2, 4, 5, 8]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2, 4, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 4, 5, 8]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_18():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 2, 2, 4, 5, 9]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 2, 4, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 2, 4, 5, 9]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_19():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 2, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_20():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 4
    singleoffsets = [0, 2, 3, 3, 5]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 3, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 3, 3, 5]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_21():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 4
    singleoffsets = [0, 2, 3, 4, 7]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 3, 4]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 3, 4, 7]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_22():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 2, 5, 7]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 5, 7]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_23():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 2, 6, 8]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 2, 6]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [2, 6, 8]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_24():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 2
    regularsize = 2
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 0, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 4, 3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_25():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 3, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_26():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 3, 3, 5]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 5]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_27():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 3, 3, 3, 4, 7]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3, 3, 4]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 3, 4, 7]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_28():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 2
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_29():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 4
    singleoffsets = [0, 3, 3, 4, 5]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3, 4]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 4, 5]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_30():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 3, 3, 4, 5, 8]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3, 4, 5]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 4, 5, 8]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_31():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 3, 3, 5, 6, 9]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3, 3, 5, 6]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 5, 6, 9]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_32():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 2
    singleoffsets = [0, 3, 6]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 6]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_33():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 3
    singleoffsets = [0, 4, 6, 6]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 4, 6]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [4, 6, 6]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

def test_unit_cpuawkward_RegularArray_getitem_jagged_expand_64_34():
    multistarts = [123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    regularlength = 1
    regularsize = 5
    singleoffsets = [0, 5, 5, 6, 8, 10]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 5, 5, 6, 8]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [5, 5, 6, 8, 10]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    assert not ret_pass.str

