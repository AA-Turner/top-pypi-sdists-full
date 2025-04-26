# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_missing_repeat_64_1():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 0, 0, 4, 3, 3, 7, 6, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_2():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 0, 0, 3, 2, 2, 5, 4, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_3():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 0, 0, 2, 1, 1, 3, 2, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_4():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 0, 0, 3, 2, 2, 5, 4, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_5():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 0, 0, 1, 0, 0, 1, 0, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_6():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 2, 2, 4, 5, 5, 7, 8, 8]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_7():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 2, 2, 3, 4, 4, 5, 6, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_8():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 2, 2, 2, 3, 3, 3, 4, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_9():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 2, 2, 3, 4, 4, 5, 6, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_10():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 2, 2, 1, 2, 2, 1, 2, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_11():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 3, 0, 4, 6, 3, 7, 9, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_12():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 3, 0, 3, 5, 2, 5, 7, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_13():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 3, 0, 2, 4, 1, 3, 5, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_14():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 3, 0, 3, 5, 2, 5, 7, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_15():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 3, 0, 1, 3, 0, 1, 3, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_16():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 4, 2, 4, 7, 5, 7, 10, 8]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_17():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 4, 2, 3, 6, 4, 5, 8, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_18():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 4, 2, 2, 5, 3, 3, 6, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_19():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 4, 2, 3, 6, 4, 5, 8, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_20():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [1, 4, 2, 1, 4, 2, 1, 4, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_21():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexlength = 3
    repetitions = 3
    regularsize = 3
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [0, 0, 0, 3, 3, 3, 6, 6, 6]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_22():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_23():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexlength = 3
    repetitions = 3
    regularsize = 1
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_24():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexlength = 3
    repetitions = 3
    regularsize = 2
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [0, 0, 0, 2, 2, 2, 4, 4, 4]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

def test_pyawkward_missing_repeat_64_25():
    outindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexlength = 3
    repetitions = 3
    regularsize = 0
    funcPy = getattr(kernels, 'awkward_missing_repeat_64')
    funcPy(outindex=outindex, index=index, indexlength=indexlength, repetitions=repetitions, regularsize=regularsize)
    pytest_outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)

