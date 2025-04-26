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

def test_unit_cpuawkward_missing_repeat_64_1():
    outindex = []
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = []
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 0
    regularsize = 0
    repetitions = 0
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = []
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_2():
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 1
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_3():
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 2
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_4():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_5():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_6():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_7():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_8():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_9():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_10():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_11():
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 6
    regularsize = 4
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 1, 2, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_12():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_13():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 2, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_14():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 4
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 2, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_15():
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 7
    regularsize = 6
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_16():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_17():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_18():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 1, 3]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 4
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 1, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_19():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 3, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 4
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 3, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_20():
    outindex = [123, 123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 3, 1, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 7
    regularsize = 6
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 3, 1, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_21():
    outindex = [123, 123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [0, 1, 2, 3, 4, 5]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 6
    regularsize = 6
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [0, 1, 2, 3, 4, 5]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_22():
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 2
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_23():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_24():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_25():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_26():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_27():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_28():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_29():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_30():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_31():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 2, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 2, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_32():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 4
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 0, 1, 2, 3]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_33():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_34():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_35():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_36():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_37():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_38():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 0, 1, 2]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 3
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 0, 1, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_39():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_40():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_41():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 2
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 0, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_42():
    outindex = [123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 1
    regularsize = 0
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_43():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 1, 0]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 1
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 1, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_44():
    outindex = [123, 123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 5
    regularsize = 0
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_45():
    outindex = [123, 123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 4
    regularsize = 0
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_46():
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 3
    regularsize = 0
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_unit_cpuawkward_missing_repeat_64_47():
    outindex = [123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    index = [1, 1]
    index = (ctypes.c_int64*len(index))(*index)
    indexlength = 2
    regularsize = 0
    repetitions = 1
    funcC = getattr(lib, 'awkward_missing_repeat_64')
    ret_pass = funcC(outindex, index, indexlength, repetitions, regularsize)
    pytest_outindex = [1, 1]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

