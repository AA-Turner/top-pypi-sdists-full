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

def test_cpuawkward_index_rpad_and_clip_axis1_64_1():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 3, 6]
    pytest_tostops = [3, 6, 9]
    assert not ret_pass.str

