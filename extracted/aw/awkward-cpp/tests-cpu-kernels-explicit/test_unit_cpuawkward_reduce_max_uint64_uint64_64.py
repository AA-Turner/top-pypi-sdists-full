# AUTO GENERATED ON 2026-07-02 AT 19:33:43
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

def test_unit_cpuawkward_reduce_max_uint64_uint64_64_1():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 4
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [5, 4, 4, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_max_uint64_uint64_64_2():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_uint64*len(toptr))(*toptr)
    fromptr = [1, 3, 6, 4, 2, 2, 3, 1, 6]
    fromptr = (ctypes.c_uint64*len(fromptr))(*fromptr)
    identity = 4
    outlength = 4
    offsets = [0, 5, 5, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_max_uint64_uint64_64')
    ret_pass = funcC(toptr, fromptr, offsets, outlength, identity)
    pytest_toptr = [6, 4, 4, 6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

