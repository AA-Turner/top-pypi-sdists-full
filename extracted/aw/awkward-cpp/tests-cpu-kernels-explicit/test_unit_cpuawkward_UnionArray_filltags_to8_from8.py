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

def test_unit_cpuawkward_UnionArray_filltags_to8_from8_1():
    totags = []
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromtags = []
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 0
    totagsoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = []
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray_filltags_to8_from8_2():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    base = 0
    fromtags = [0, 0, 0, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 6
    totagsoffset = 0
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [0, 0, 0, 1, 1, 1]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

