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

def test_unit_cpuawkward_ListArray64_compact_offsets_64_1():
    tooffsets = [123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = []
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = []
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 0
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_2():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [1]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [1]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 1
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_3():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [2, 2, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    assert funcC(tooffsets, fromstarts, fromstops, length).str.decode('utf-8') == "stops[i] < starts[i]"

def test_unit_cpuawkward_ListArray64_compact_offsets_64_4():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [2, 2, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0, 1, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_5():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [5, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0, 1, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_6():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [4, 4]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_7():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 3, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_8():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [4, 4, 7]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 6, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 0, 2, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_9():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [5, 6, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 1, 1, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_10():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 7, 7]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [7, 7, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 1, 1, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_11():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 3, 3, 0, 4]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 4, 3, 3, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 1, 2, 2, 5, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_12():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [2, 4, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 5, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_13():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [5, 5, 0, 3, 3, 6, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [6, 6, 3, 3, 5, 6, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 7
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 1, 2, 5, 5, 7, 7, 11]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_14():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 5, 5, 5, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 5, 5, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 2, 2, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_15():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3, 5, 8]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 2, 4, 5, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_16():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 3, 0, 5, 5, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 3, 3, 6, 6, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 2, 5, 6, 7, 11]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_17():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 15]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 16]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_18():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 2, 4, 5, 6, 9]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 3, 5, 6, 7, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 3, 4, 5, 6, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_19():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 2]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 4]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_20():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 3, 3, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4, 4, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_21():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 2, 5, 3, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 5, 3, 6, 3, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4, 5, 6, 6, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_22():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 5, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4, 6, 8, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_23():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 0, 0, 0, 4, 4, 4, 4]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 2, 2, 2, 5, 5, 5, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 10
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_24():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 3, 3, 5, 5, 5, 8, 8]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [2, 2, 2, 5, 5, 7, 7, 7, 10, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 10
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_25():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 2, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_26():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_27():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3, 4]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 4, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 4, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_28():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_29():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_30():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [1, 99, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 99, 7]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_31():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3, 10, 10]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 10, 13]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5, 5, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_32():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 3, 15, 16]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 5, 16, 20]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5, 6, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_33():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 4, 4, 6, 9]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 4, 6, 7, 11]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5, 6, 8]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_34():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 4, 5, 8]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 6, 8, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 5, 8, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_35():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_36():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 6]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 3, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_37():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [9, 6, 5, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 4, 6, 6, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_38():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 5, 6, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [9, 6, 9, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 4, 7, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_39():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 6, 3, 8, 3, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 8, 3, 9, 5, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 5, 5, 6, 8, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_40():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 4, 6, 3, 6, 7]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 7, 4, 6, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 5, 6, 7, 7, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_41():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 4, 6, 3, 7]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 7, 4, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 5, 6, 7, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_42():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 6, 3, 8, 5, 9]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 8, 5, 9, 6, 10]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 5, 7, 8, 9, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_43():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_44():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_45():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 10, 14, 18]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 14, 18, 21]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 10, 14, 17]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_46():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 6, 11, 15, 19]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 11, 15, 19, 22]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 11, 15, 19, 22]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_47():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_48():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 6, 17, 20, 11, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [6, 9, 20, 23, 13, 27]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9, 12, 14, 16]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_49():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9, 12, 15]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_50():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 3, 11, 14, 17]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 6, 14, 17, 20]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9, 12, 15]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_51():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9, 12, 15, 18]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_52():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 3, 3, 3, 3, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 7
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 6, 9, 12, 15, 18, 21]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_53():
    tooffsets = [123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 5]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 9]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 2
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 7]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_54():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 6, 11, 15, 19]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [6, 11, 15, 19, 22]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 8, 12, 16, 19]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_55():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 13, 3, 18, 8, 23]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [3, 18, 8, 23, 13, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 3, 8, 13, 18, 23, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_56():
    tooffsets = [123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [16]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [20]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 1
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_57():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 5, 3, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4, 5, 7, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_58():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 5, 3, 3, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [10, 6, 5, 3, 3]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4, 5, 7, 7, 10]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_59():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [3, 0, 999, 2, 6, 10]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [7, 3, 999, 4, 6, 12]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4, 7, 7, 9, 9, 11]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_60():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 13, 4, 18, 8, 23]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 18, 8, 23, 13, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4, 9, 13, 18, 23, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_61():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 14, 4, 19, 9, 24]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [4, 19, 9, 24, 14, 29]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 4, 9, 14, 19, 24, 29]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_62():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 11, 5, 16, 6, 17]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 16, 6, 17, 11, 22]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 11, 12, 17, 22]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_63():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 14, 5, 19, 9, 23]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 19, 9, 23, 14, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 14, 18, 23, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_64():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 0, 0, 8, 11, 11, 14]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 5, 5, 11, 14, 14, 19]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 7
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 18, 21, 24, 29]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_65():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 15, 5, 20, 10, 24]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 24, 15, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 19, 24, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_66():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 10, 15, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 15, 20, 30]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_67():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 15, 10, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 15, 30]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_68():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [15, 10, 5, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [20, 15, 10, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_69():
    tooffsets = [123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [15, 5, 10, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [20, 10, 15, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 4
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_70():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 14, 5, 19, 10, 24]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 19, 10, 24, 14, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 24, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_71():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 28]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 28]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_72():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 29]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 29]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_73():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 15, 5, 20, 10, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 20, 10, 25, 15, 30]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_74():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 45, 5, 50, 10, 55]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 50, 10, 55, 15, 60]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_75():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 5, 10, 15, 20, 25]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 20, 25, 30]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_76():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 5, 10, 45, 50, 55]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 10, 15, 50, 55, 60]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_77():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [1, 16, 6, 21, 11, 26]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [6, 21, 11, 26, 16, 31]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_78():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [25, 10, 20, 5, 15, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [30, 15, 25, 10, 20, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_79():
    tooffsets = [123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [25, 20, 15, 10, 5, 0]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [30, 25, 20, 15, 10, 5]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 6
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_80():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 8, 11, 11, 14]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [5, 11, 14, 14, 19]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 8, 11, 14, 19]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_81():
    tooffsets = [123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [6, 11, 14, 17, 20]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [11, 14, 17, 20, 25]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 5
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 5, 8, 11, 14, 19]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray64_compact_offsets_64_82():
    tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromstarts = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203]
    fromstarts = (ctypes.c_int64*len(fromstarts))(*fromstarts)
    fromstops = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
    fromstops = (ctypes.c_int64*len(fromstops))(*fromstops)
    length = 30
    funcC = getattr(lib, 'awkward_ListArray64_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromstarts, fromstops, length)
    pytest_tooffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

