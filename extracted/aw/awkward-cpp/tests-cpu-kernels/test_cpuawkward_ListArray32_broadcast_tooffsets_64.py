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

def test_cpuawkward_ListArray32_broadcast_tooffsets_64_1():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    fromstarts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lencontent = 3
    funcC = getattr(lib, 'awkward_ListArray32_broadcast_tooffsets_64')
    assert funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent).str

def test_cpuawkward_ListArray32_broadcast_tooffsets_64_2():
    tocarry = [123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_int32*len(fromstops))(*fromstops)
    lencontent = 6
    funcC = getattr(lib, 'awkward_ListArray32_broadcast_tooffsets_64')
    assert funcC(tocarry, fromoffsets, offsetslength, fromstarts, fromstops, lencontent).str

