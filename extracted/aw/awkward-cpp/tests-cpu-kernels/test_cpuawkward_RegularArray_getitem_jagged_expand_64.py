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

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_1():
    multistarts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 3
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    pytest_multistops = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_2():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 1, 1, 1, 1, 1]
    pytest_multistops = [1, 1, 1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_3():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 1
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 1, 1]
    pytest_multistops = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_4():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 1, 1, 1, 1, 1]
    pytest_multistops = [1, 1, 1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_5():
    multistarts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 3
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 3, 3, 2, 3, 3, 2, 3, 3]
    pytest_multistops = [3, 3, 4, 3, 3, 4, 3, 3, 4]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_6():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 3, 2, 3, 2, 3]
    pytest_multistops = [3, 3, 3, 3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_7():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 1
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 2, 2]
    pytest_multistops = [3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_8():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 3, 2, 3, 2, 3]
    pytest_multistops = [3, 3, 3, 3, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_9():
    multistarts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 3
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 1, 0, 2, 1, 0, 2, 1, 0]
    pytest_multistops = [1, 0, 1, 1, 0, 1, 1, 0, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_10():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 1, 2, 1, 2, 1]
    pytest_multistops = [1, 0, 1, 0, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_11():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 1
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 2, 2]
    pytest_multistops = [1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_12():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [2, 1, 2, 1, 2, 1]
    pytest_multistops = [1, 0, 1, 0, 1, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_13():
    multistarts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 3
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 0, 2, 1, 0, 2, 1, 0, 2]
    pytest_multistops = [0, 2, 3, 0, 2, 3, 0, 2, 3]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_14():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 0, 1, 0, 1, 0]
    pytest_multistops = [0, 2, 0, 2, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_15():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 1
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 1, 1]
    pytest_multistops = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_16():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [1, 0, 1, 0, 1, 0]
    pytest_multistops = [0, 2, 0, 2, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_17():
    multistarts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 3
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    pytest_multistops = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_18():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0, 0, 0, 0]
    pytest_multistops = [0, 0, 0, 0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_19():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 1
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0]
    pytest_multistops = [0, 0, 0]
    assert not ret_pass.str

def test_cpuawkward_RegularArray_getitem_jagged_expand_64_20():
    multistarts = [123, 123, 123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    regularsize = 2
    regularlength = 3
    funcC = getattr(lib, 'awkward_RegularArray_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, regularsize, regularlength)
    pytest_multistarts = [0, 0, 0, 0, 0, 0]
    pytest_multistops = [0, 0, 0, 0, 0, 0]
    assert not ret_pass.str

