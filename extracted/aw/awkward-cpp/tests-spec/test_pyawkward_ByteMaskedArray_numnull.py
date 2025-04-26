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

def test_pyawkward_ByteMaskedArray_numnull_1():
    numnull = [123]
    mask = [1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
    funcPy(numnull=numnull, mask=mask, length=length, validwhen=validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_ByteMaskedArray_numnull_2():
    numnull = [123]
    mask = [0, 0, 0, 0, 0]
    length = 3
    validwhen = False
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
    funcPy(numnull=numnull, mask=mask, length=length, validwhen=validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_ByteMaskedArray_numnull_3():
    numnull = [123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
    funcPy(numnull=numnull, mask=mask, length=length, validwhen=validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_ByteMaskedArray_numnull_4():
    numnull = [123]
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
    funcPy(numnull=numnull, mask=mask, length=length, validwhen=validwhen)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_ByteMaskedArray_numnull_5():
    numnull = [123]
    mask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    validwhen = True
    funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
    funcPy(numnull=numnull, mask=mask, length=length, validwhen=validwhen)
    pytest_numnull = [3]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

