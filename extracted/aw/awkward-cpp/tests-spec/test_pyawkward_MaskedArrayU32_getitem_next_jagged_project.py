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

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_1():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [2, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_2():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [8, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_3():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_4():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 7, 6]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 9, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_5():
    index = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_6():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [2, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_7():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [8, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_8():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_9():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 7, 6]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 9, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_10():
    index = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_11():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [2, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_12():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [8, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_13():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_14():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 7, 6]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 9, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_15():
    index = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_16():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [2, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_17():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [8, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_18():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_19():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 7, 6]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 9, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_20():
    index = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_21():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops_in = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [2, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 2, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_22():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops_in = [8, 4, 5, 6, 5, 5, 7]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [8, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_23():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops_in = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 4, 5]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 4, 5]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_24():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops_in = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [1, 7, 6]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 9, 6]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_MaskedArrayU32_getitem_next_jagged_project_25():
    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    starts_in = [0, 0, 0, 0, 0, 0, 0, 0]
    stops_in = [1, 1, 1, 1, 1, 1, 1, 1]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_MaskedArrayU32_getitem_next_jagged_project')
    funcPy(index=index, starts_in=starts_in, stops_in=stops_in, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

