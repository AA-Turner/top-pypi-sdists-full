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

def test_pyawkward_IndexedArray64_simplify32_to64_1():
    toindex = [123, 123, 123]
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [0, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_2():
    toindex = [123, 123, 123]
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [2, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_3():
    toindex = [123, 123, 123]
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [3, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_4():
    toindex = [123, 123, 123]
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [4, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_5():
    toindex = [123, 123, 123]
    outerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_6():
    toindex = [123]
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    with pytest.raises(Exception):
        funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)

def test_pyawkward_IndexedArray64_simplify32_to64_7():
    toindex = [123]
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    with pytest.raises(Exception):
        funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)

def test_pyawkward_IndexedArray64_simplify32_to64_8():
    toindex = [123]
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    with pytest.raises(Exception):
        funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)

def test_pyawkward_IndexedArray64_simplify32_to64_9():
    toindex = [123]
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    with pytest.raises(Exception):
        funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)

def test_pyawkward_IndexedArray64_simplify32_to64_10():
    toindex = [123]
    outerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerlength = 2
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    with pytest.raises(Exception):
        funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)

def test_pyawkward_IndexedArray64_simplify32_to64_11():
    toindex = [123, 123, 123]
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerlength = 3
    innerindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    innerlength = 5
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_12():
    toindex = [123, 123, 123]
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerlength = 3
    innerindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    innerlength = 5
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_13():
    toindex = [123, 123, 123]
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerlength = 3
    innerindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    innerlength = 5
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_14():
    toindex = [123, 123, 123]
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerlength = 3
    innerindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    innerlength = 5
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [1, 1, 1]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

def test_pyawkward_IndexedArray64_simplify32_to64_15():
    toindex = [123, 123, 123]
    outerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outerlength = 3
    innerindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    innerlength = 5
    funcPy = getattr(kernels, 'awkward_IndexedArray64_simplify32_to64')
    funcPy(toindex=toindex, outerindex=outerindex, outerlength=outerlength, innerindex=innerindex, innerlength=innerlength)
    pytest_toindex = [0, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

