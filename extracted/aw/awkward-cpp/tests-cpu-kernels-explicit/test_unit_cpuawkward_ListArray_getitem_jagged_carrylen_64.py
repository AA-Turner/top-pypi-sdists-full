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

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_1():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = []
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = []
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 0
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_2():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [0, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 2
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_3():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 1
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [2]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_4():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    slicestarts = [1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    sliceouterlen = 1
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_5():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 0, 0]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_6():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 0]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [0]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_7():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 0, 1, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 1, 1, 1]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [1]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_8():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 6
    slicestarts = [0, 1, 3, 5, 6, 8]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 3, 5, 6, 8, 10]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [10]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_9():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 5, 5, 6, 8]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [5, 5, 6, 8, 10]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [10]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_10():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 3, 4, 7]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 4, 7, 11]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [11]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_11():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 6
    slicestarts = [0, 1, 3, 6, 7, 9]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 3, 6, 7, 9, 12]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [12]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_12():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 0, 0]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [0, 0, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [2]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_13():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [2]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_14():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 1, 1]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [3]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_15():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 1, 1, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 2, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [3]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_16():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [3]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_17():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 3]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [3]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_18():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2, 2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [4]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_19():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [4]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_20():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 2
    slicestarts = [0, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [4]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_21():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 1, 1, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 1, 3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_22():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 2, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_23():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 2, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_24():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 3, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_25():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 4, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [5]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_26():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 1, 3, 4]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 3, 4, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [6]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_27():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 2, 2]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 2, 2, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [6]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_28():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 2
    slicestarts = [0, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [6]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_29():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 5, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [6]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_30():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 4, 6]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [4, 6, 6]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [6]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_31():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 3
    slicestarts = [0, 2, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 5, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [7]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_32():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 3, 4]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 3, 4, 7]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [7]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_33():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 1, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [1, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [8]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_34():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 7
    slicestarts = [0, 2, 2, 4, 4, 5, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4, 4, 5, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [8]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_35():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [8]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_36():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 4
    slicestarts = [0, 3, 0, 3]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 4, 3, 4]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [8]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_37():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 4, 5, 8]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [8]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_38():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 2, 2, 4, 5]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [2, 2, 4, 5, 9]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [9]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

def test_unit_cpuawkward_ListArray_getitem_jagged_carrylen_64_39():
    carrylen = [123]
    carrylen = (ctypes.c_int64*len(carrylen))(*carrylen)
    sliceouterlen = 5
    slicestarts = [0, 3, 3, 5, 6]
    slicestarts = (ctypes.c_int64*len(slicestarts))(*slicestarts)
    slicestops = [3, 3, 5, 6, 9]
    slicestops = (ctypes.c_int64*len(slicestops))(*slicestops)
    funcC = getattr(lib, 'awkward_ListArray_getitem_jagged_carrylen_64')
    ret_pass = funcC(carrylen, slicestarts, slicestops, sliceouterlen)
    pytest_carrylen = [9]
    assert carrylen[:len(pytest_carrylen)] == pytest.approx(pytest_carrylen)
    assert not ret_pass.str

