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

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_1():
    outoffsets = [123, 123, 123, 123]
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [1, 1, 1, 1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_2():
    outoffsets = [123, 123, 123, 123]
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [2, 2, 3, 4]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_3():
    outoffsets = [123, 123, 123, 123]
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [2, 1, 0, -1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_4():
    outoffsets = [123, 123, 123, 123]
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [1, 3, 2, 1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_5():
    outoffsets = [123, 123, 123, 123]
    outindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [0, 0, 0, 0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_6():
    outoffsets = [123, 123]
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_7():
    outoffsets = [123, 123]
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_8():
    outoffsets = [123, 123]
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_9():
    outoffsets = [123, 123]
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_10():
    outoffsets = [123, 123]
    outindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_11():
    outoffsets = [123, 123]
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_12():
    outoffsets = [123, 123]
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_13():
    outoffsets = [123, 123]
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_14():
    outoffsets = [123, 123]
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_15():
    outoffsets = [123, 123]
    outindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_16():
    outoffsets = [123, 123]
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_17():
    outoffsets = [123, 123]
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_18():
    outoffsets = [123, 123]
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_19():
    outoffsets = [123, 123]
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_20():
    outoffsets = [123, 123]
    outindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    with pytest.raises(Exception):
        funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_21():
    outoffsets = [123, 123, 123, 123]
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindexlength = 3
    offsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [1, 1, 1, 1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_22():
    outoffsets = [123, 123, 123, 123]
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindexlength = 3
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [2, 3, 4, 5]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_23():
    outoffsets = [123, 123, 123, 123]
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindexlength = 3
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [2, 1, 0, -1]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_24():
    outoffsets = [123, 123, 123, 123]
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindexlength = 3
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [1, 0, -1, -2]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

def test_pyawkward_IndexedArrayU32_flatten_none2empty_64_25():
    outoffsets = [123, 123, 123, 123]
    outindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outindexlength = 3
    offsets = [0, 0, 0, 0, 0, 0, 0, 0]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_IndexedArrayU32_flatten_none2empty_64')
    funcPy(outoffsets=outoffsets, outindex=outindex, outindexlength=outindexlength, offsets=offsets, offsetslength=offsetslength)
    pytest_outoffsets = [0, 0, 0, 0]
    assert outoffsets[:len(pytest_outoffsets)] == pytest.approx(pytest_outoffsets)

