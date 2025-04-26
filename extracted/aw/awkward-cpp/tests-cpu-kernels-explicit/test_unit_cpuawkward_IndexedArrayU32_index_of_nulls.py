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

def test_unit_cpuawkward_IndexedArrayU32_index_of_nulls_1():
    toindex = []
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    fromindex = []
    fromindex = (ctypes.c_uint32*len(fromindex))(*fromindex)
    lenindex = 0
    parents = []
    parents = (ctypes.c_int64*len(parents))(*parents)
    starts = []
    starts = (ctypes.c_int64*len(starts))(*starts)
    funcC = getattr(lib, 'awkward_IndexedArrayU32_index_of_nulls')
    ret_pass = funcC(toindex, fromindex, lenindex, parents, starts)
    pytest_toindex = []
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

