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

def test_pyawkward_IndexedArrayU32_numnull_1():
    numnull = [123]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    lenindex = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_numnull')
    funcPy(numnull=numnull, fromindex=fromindex, lenindex=lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_IndexedArrayU32_numnull_2():
    numnull = [123]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    lenindex = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_numnull')
    funcPy(numnull=numnull, fromindex=fromindex, lenindex=lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_IndexedArrayU32_numnull_3():
    numnull = [123]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    lenindex = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_numnull')
    funcPy(numnull=numnull, fromindex=fromindex, lenindex=lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_IndexedArrayU32_numnull_4():
    numnull = [123]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    lenindex = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_numnull')
    funcPy(numnull=numnull, fromindex=fromindex, lenindex=lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

def test_pyawkward_IndexedArrayU32_numnull_5():
    numnull = [123]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lenindex = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_numnull')
    funcPy(numnull=numnull, fromindex=fromindex, lenindex=lenindex)
    pytest_numnull = [0]
    assert numnull[:len(pytest_numnull)] == pytest.approx(pytest_numnull)

