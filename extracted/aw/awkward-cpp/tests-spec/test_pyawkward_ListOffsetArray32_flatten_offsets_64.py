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

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_1():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_2():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [3, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_3():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_4():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_5():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_6():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_7():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [3, 4, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_8():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_9():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [2, 3, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_10():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_11():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_12():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [3, 3, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_13():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_14():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [2, 0, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_15():
    tooffsets = [123, 123, 123]
    outeroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_16():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_17():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [3, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_18():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 2, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_19():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_20():
    tooffsets = [123, 123, 123]
    outeroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_21():
    tooffsets = [123, 123, 123]
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_22():
    tooffsets = [123, 123, 123]
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [2, 2, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_23():
    tooffsets = [123, 123, 123]
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [2, 2, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_24():
    tooffsets = [123, 123, 123]
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [1, 1, 1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray32_flatten_offsets_64_25():
    tooffsets = [123, 123, 123]
    outeroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    outeroffsetslen = 3
    inneroffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    funcPy = getattr(kernels, 'awkward_ListOffsetArray32_flatten_offsets_64')
    funcPy(tooffsets=tooffsets, outeroffsets=outeroffsets, outeroffsetslen=outeroffsetslen, inneroffsets=inneroffsets)
    pytest_tooffsets = [0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

