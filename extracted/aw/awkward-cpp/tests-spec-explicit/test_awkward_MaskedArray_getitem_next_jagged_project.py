import pytest
import numpy
import kernels

def test_awkward_MaskedArray_getitem_next_jagged_project_1():
	starts_out = []
	stops_out = []
	index = []
	length = 0
	starts_in = []
	stops_in = []
	funcPy = getattr(kernels, 'awkward_MaskedArray_getitem_next_jagged_project')
	funcPy(starts_out = starts_out,stops_out = stops_out,index = index,length = length,starts_in = starts_in,stops_in = stops_in)
	pytest_starts_out = []
	pytest_stops_out = []
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_MaskedArray_getitem_next_jagged_project_2():
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index = [0, 1, 2, 3]
	length = 4
	starts_in = [0, 2, 3, 3]
	stops_in = [2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_MaskedArray_getitem_next_jagged_project')
	funcPy(starts_out = starts_out,stops_out = stops_out,index = index,length = length,starts_in = starts_in,stops_in = stops_in)
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 3]
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_MaskedArray_getitem_next_jagged_project_3():
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index = [0, 1, 2, 3]
	length = 4
	starts_in = [0, 2, 3, 3]
	stops_in = [2, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_MaskedArray_getitem_next_jagged_project')
	funcPy(starts_out = starts_out,stops_out = stops_out,index = index,length = length,starts_in = starts_in,stops_in = stops_in)
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 5]
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_MaskedArray_getitem_next_jagged_project_4():
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index = [0, 1, 2, 3]
	length = 4
	starts_in = [0, 2, 3, 3]
	stops_in = [2, 3, 3, 6]
	funcPy = getattr(kernels, 'awkward_MaskedArray_getitem_next_jagged_project')
	funcPy(starts_out = starts_out,stops_out = stops_out,index = index,length = length,starts_in = starts_in,stops_in = stops_in)
	pytest_starts_out = [0, 2, 3, 3]
	pytest_stops_out = [2, 3, 3, 6]
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


def test_awkward_MaskedArray_getitem_next_jagged_project_5():
	starts_out = [123, 123, 123, 123]
	stops_out = [123, 123, 123, 123]
	index = [0, 1, 2, 3]
	length = 4
	starts_in = [0, 2, 3, 4]
	stops_in = [2, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_MaskedArray_getitem_next_jagged_project')
	funcPy(starts_out = starts_out,stops_out = stops_out,index = index,length = length,starts_in = starts_in,stops_in = stops_in)
	pytest_starts_out = [0, 2, 3, 4]
	pytest_stops_out = [2, 3, 4, 7]
	assert starts_out == pytest_starts_out
	assert stops_out == pytest_stops_out


