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

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_1():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_2():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_3():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 1, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 0, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_4():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_5():
    index_in = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_6():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_7():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_8():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 1, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 0, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_9():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_10():
    index_in = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_11():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_12():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_13():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 1, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 0, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_14():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_15():
    index_in = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_16():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_17():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_18():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 1, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 0, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_19():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_20():
    index_in = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_21():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 1, 1]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 1, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_22():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 3, 3]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [3, 3, 4]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_23():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [2, 1, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [1, 0, 1]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_24():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [1, 0, 2]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 2, 3]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

def test_pyawkward_Content_getitem_next_missing_jagged_getmaskstartstop_25():
    index_in = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    offsets_in = [0, 0, 0, 0, 0, 0, 0, 0]
    mask_out = [123, 123, 123]
    starts_out = [123, 123, 123]
    stops_out = [123, 123, 123]
    length = 3
    funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
    funcPy(index_in=index_in, offsets_in=offsets_in, mask_out=mask_out, starts_out=starts_out, stops_out=stops_out, length=length)
    pytest_mask_out = [0, 1, 2]
    assert mask_out[:len(pytest_mask_out)] == pytest.approx(pytest_mask_out)
    pytest_starts_out = [0, 0, 0]
    assert starts_out[:len(pytest_starts_out)] == pytest.approx(pytest_starts_out)
    pytest_stops_out = [0, 0, 0]
    assert stops_out[:len(pytest_stops_out)] == pytest.approx(pytest_stops_out)

