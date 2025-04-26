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

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_1():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [2, 3, 5, 7]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_2():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_3():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_4():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_5():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_6():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_7():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [1, 8, 12, 17]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_8():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_9():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_10():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [8, 4, 5, 6, 5, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_11():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_12():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_13():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [1, 1, 1, 1]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_14():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_15():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_16():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_17():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_18():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_19():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [1, 1, 3, 3]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_20():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_21():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_22():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_23():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_24():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    assert funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops).str

def test_cpuawkward_ListArray64_getitem_jagged_descend_64_25():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    slicestarts = [0, 0, 0, 0, 0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 1, 1, 1, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    funcC = getattr(lib, 'awkward_ListArray64_getitem_jagged_descend_64')
    ret_pass = funcC(tooffsets, slicestarts, slicestops, sliceouterlen, fromstarts, fromstops)
    pytest_tooffsets = [0, 1, 2, 3]
    assert not ret_pass.str

