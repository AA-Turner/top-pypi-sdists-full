import pytest
import numpy
import kernels

def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_1():
	mask_out = [123, 123]
	starts_out = [123, 123]
	stops_out = [123, 123]
	index_in = [0, -1]
	length = 2
	offsets_in = [0, 1]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1]
	pytest_starts_out = [0, 1]
	pytest_stops_out = [1, 1]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_2():
	mask_out = []
	starts_out = []
	stops_out = []
	index_in = []
	length = 0
	offsets_in = []
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = []
	pytest_starts_out = []
	pytest_stops_out = []
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_3():
	mask_out = [123, 123]
	starts_out = [123, 123]
	stops_out = [123, 123]
	index_in = [0, -1]
	length = 2
	offsets_in = [0, 4]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1]
	pytest_starts_out = [0, 4]
	pytest_stops_out = [4, 4]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_4():
	mask_out = [123, 123, 123]
	starts_out = [123, 123, 123]
	stops_out = [123, 123, 123]
	index_in = [0, -1, -1]
	length = 3
	offsets_in = [0, 1]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, -1]
	pytest_starts_out = [0, 1, 1]
	pytest_stops_out = [1, 1, 1]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_5():
	mask_out = [123, 123, 123]
	starts_out = [123, 123, 123]
	stops_out = [123, 123, 123]
	index_in = [0, -1, 1]
	length = 3
	offsets_in = [0, 1, 2]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2]
	pytest_starts_out = [0, 1, 1]
	pytest_stops_out = [1, 1, 2]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_6():
	mask_out = [123, 123, 123]
	starts_out = [123, 123, 123]
	stops_out = [123, 123, 123]
	index_in = [0, -1, 1]
	length = 3
	offsets_in = [0, 2, 4]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2]
	pytest_starts_out = [0, 2, 2]
	pytest_stops_out = [2, 2, 4]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_7():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, -1, 1]
	length = 4
	offsets_in = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, -1, 3]
	pytest_starts_out = [0, 0, 0, 0]
	pytest_stops_out = [0, 0, 0, 0]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_8():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, -1, 1]
	length = 4
	offsets_in = [0, 1, 2]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, -1, 3]
	pytest_starts_out = [0, 1, 1, 1]
	pytest_stops_out = [1, 1, 1, 2]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_9():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, 1, -1]
	length = 4
	offsets_in = [0, 2, 3]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, -1]
	pytest_starts_out = [0, 2, 2, 3]
	pytest_stops_out = [2, 2, 3, 3]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_10():
	mask_out = [123, 123, 123, 123, 123]
	starts_out = [123, 123, 123, 123, 123]
	stops_out = [123, 123, 123, 123, 123]
	index_in = [0, -1, 1, -1, 2]
	length = 5
	offsets_in = [0, 2, 2, 4]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, -1, 4]
	pytest_starts_out = [0, 2, 2, 2, 2]
	pytest_stops_out = [2, 2, 2, 2, 4]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_11():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 0, 0, 0]
	pytest_stops_out = [0, 0, 0, 0]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_12():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 0, 1, 1]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 0, 1, 1]
	pytest_stops_out = [0, 1, 1, 1]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_13():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, 1, 2]
	length = 4
	offsets_in = [0, 1, 2, 3]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3]
	pytest_starts_out = [0, 1, 1, 2]
	pytest_stops_out = [1, 1, 2, 3]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_14():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 2, 3, 3]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 3]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_15():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 4]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_16():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 5]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_17():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, 1, 2]
	length = 4
	offsets_in = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3]
	pytest_starts_out = [0, 2, 2, 3]
	pytest_stops_out = [2, 2, 3, 5]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_18():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 2, 3, 6]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 6]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_19():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 2, 4, 5]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 2, 4, 4]
	pytest_stops_out = [2, 4, 4, 5]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_20():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, 1, 2]
	length = 4
	offsets_in = [0, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3]
	pytest_starts_out = [0, 3, 3, 3]
	pytest_stops_out = [3, 3, 3, 4]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_21():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 3, 3, 3]
	pytest_stops_out = [3, 3, 3, 5]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_22():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, 1, -1, 2]
	length = 4
	offsets_in = [0, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, 1, -1, 3]
	pytest_starts_out = [0, 4, 5, 5]
	pytest_stops_out = [4, 5, 5, 6]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_23():
	mask_out = [123, 123, 123, 123]
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index_in = [0, -1, 1, 2]
	length = 4
	offsets_in = [0, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3]
	pytest_starts_out = [0, 4, 4, 5]
	pytest_stops_out = [4, 4, 5, 6]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_24():
	mask_out = [123, 123, 123, 123, 123, 123, 123, 123]
	starts_out = [123, 123, 123, 123, 123, 123, 123, 123]
	stops_out = [123, 123, 123, 123, 123, 123, 123, 123]
	index_in = [0, -1, 1, 2, -1, 3, 4, 5]
	length = 8
	offsets_in = [0, 2, 4, 6, 8, 10, 12]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3, -1, 5, 6, 7]
	pytest_starts_out = [0, 2, 2, 4, 6, 6, 8, 10]
	pytest_stops_out = [2, 2, 4, 6, 6, 8, 10, 12]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_Content_getitem_next_missing_jagged_getmaskstartstop_25():
	mask_out = [123, 123, 123, 123, 123, 123, 123, 123]
	starts_out = [123, 123, 123, 123, 123, 123, 123, 123]
	stops_out = [123, 123, 123, 123, 123, 123, 123, 123]
	index_in = [0, -1, 1, 2, 3, 4, 5, 6]
	length = 8
	offsets_in = [0, 1, 1, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_Content_getitem_next_missing_jagged_getmaskstartstop')
	funcPy(mask_out = mask_out,starts_out = starts_out,stops_out = stops_out,index_in = index_in,length = length,offsets_in = offsets_in)
	pytest_mask_out = [0, -1, 2, 3, 4, 5, 6, 7]
	pytest_starts_out = [0, 1, 1, 1, 1, 1, 1, 1]
	pytest_stops_out = [1, 1, 1, 1, 1, 1, 1, 1]
	assert mask_out == pytest_mask_out
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


