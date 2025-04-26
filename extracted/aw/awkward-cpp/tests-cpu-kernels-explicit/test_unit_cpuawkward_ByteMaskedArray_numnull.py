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

def test_unit_cpuawkward_ByteMaskedArray_numnull_1():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 0
    mask = []
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_2():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 4
    mask = [0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_3():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 2
    mask = [0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_4():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 1
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_5():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 30
    mask = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [10]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_6():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 30
    mask = [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [10]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_7():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 30
    mask = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [10]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_8():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 4
    mask = [0, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_9():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 1
    mask = [0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_10():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 3
    mask = [0, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [1]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_11():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 6
    mask = [0, 0, 1, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_12():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 5
    mask = [0, 0, 1, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_13():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 9
    mask = [0, 1, 0, 0, 0, 0, 1, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_14():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 6
    mask = [0, 1, 0, 0, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_15():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 3
    mask = [0, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_16():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 3
    mask = [1, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [2]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_17():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 8
    mask = [0, 1, 0, 0, 1, 0, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [3]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

def test_unit_cpuawkward_ByteMaskedArray_numnull_18():
    numnull = [123]
    numnull = (ctypes.c_int64*len(numnull))(*numnull)
    length = 10
    mask = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_numnull')
    ret_pass = funcC(numnull, mask, length, validwhen)
    pytest_numnull = [5]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)
    assert not ret_pass.str

