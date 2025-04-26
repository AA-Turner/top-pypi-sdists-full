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

def test_unit_cpuawkward_ListArray32_getitem_jagged_expand_64_1():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 2
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_ListArray32_getitem_jagged_expand_64')
    assert funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length).str.decode('utf-8') == "cannot fit jagged slice into nested list"

def test_unit_cpuawkward_ListArray32_getitem_jagged_expand_64_2():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [5]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [4]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    jaggedsize = 2
    length = 1
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_ListArray32_getitem_jagged_expand_64')
    assert funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length).str.decode('utf-8') == "stops[i] < starts[i]"

def test_unit_cpuawkward_ListArray32_getitem_jagged_expand_64_3():
    multistarts = [123, 123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    tocarry = [123, 123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    jaggedsize = 2
    length = 2
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_ListArray32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [0, 3, 0, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 4, 3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 1, 2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_getitem_jagged_expand_64_4():
    multistarts = []
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = []
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    tocarry = []
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = []
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    jaggedsize = 0
    length = 0
    singleoffsets = []
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_ListArray32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = []
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = []
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = []
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray32_getitem_jagged_expand_64_5():
    multistarts = [123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    tocarry = [123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [2]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [4]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    jaggedsize = 2
    length = 1
    singleoffsets = [0, 3, 4]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    funcC = getattr(lib, 'awkward_ListArray32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [0, 3]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 4]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [2, 3]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

