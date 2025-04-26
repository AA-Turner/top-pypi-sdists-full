import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_drop_none_indexes_1():
	tooffsets = []
	noneindexes = []
	length_indexes = 0
	fromoffsets = []
	length_offsets = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = []
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_2():
	tooffsets = []
	noneindexes = [0]
	length_indexes = 1
	fromoffsets = []
	length_offsets = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = []
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_3():
	tooffsets = [123]
	noneindexes = []
	length_indexes = 0
	fromoffsets = [0]
	length_offsets = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_4():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [-1, -1, -1, -1, -1, -1, -1]
	length_indexes = 7
	fromoffsets = [0, 2, 3, 5, 7]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 0, 0, 0, 0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_5():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [-1, 0, -1, 0, 0, -1, 0]
	length_indexes = 7
	fromoffsets = [0, 2, 3, 5, 7]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 1, 1, 3, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_6():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [0, 0, 0, 0, 0, 0]
	length_indexes = 6
	fromoffsets = [0, 2, 3, 5, 6]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 2, 3, 5, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_7():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [0, 0, 0, 0, 0, 0]
	length_indexes = 6
	fromoffsets = [0, 0, 0, 0, 0]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 0, 0, 0, 0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_8():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [0, 0, 0, 0, 0, 0]
	length_indexes = 6
	fromoffsets = [0, 2, 3, 3, 6]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 2, 3, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_drop_none_indexes_9():
	tooffsets = [123, 123, 123, 123, 123]
	noneindexes = [-1, -1, -1, -1, -1, -1]
	length_indexes = 6
	fromoffsets = [0, 2, 3, 3, 6]
	length_offsets = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_drop_none_indexes')
	funcPy(tooffsets = tooffsets,noneindexes = noneindexes,length_indexes = length_indexes,fromoffsets = fromoffsets,length_offsets = length_offsets)
	pytest_tooffsets = [0, 0, 0, 0, 0]
	assert tooffsets == pytest_tooffsets


