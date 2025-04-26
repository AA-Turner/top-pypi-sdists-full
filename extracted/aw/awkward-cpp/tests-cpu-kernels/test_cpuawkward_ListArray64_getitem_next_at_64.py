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

def test_cpuawkward_ListArray64_getitem_next_at_64_1():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 3
    at = 0
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_at_64')
    ret_pass = funcC(tocarry, fromstarts, fromstops, lenstarts, at)
    pytest_tocarry = [2, 0, 2]
    assert not ret_pass.str

def test_cpuawkward_ListArray64_getitem_next_at_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [8, 4, 5, 6, 5, 5, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    lenstarts = 3
    at = 5
    funcC = getattr(lib, 'awkward_ListArray64_getitem_next_at_64')
    assert funcC(tocarry, fromstarts, fromstops, lenstarts, at).str

