import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_toRegularArray_1():
	size = [123]
	fromoffsets = []
	offsetslength = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [0]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_2():
	size = [123]
	fromoffsets = [0]
	offsetslength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [0]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_3():
	size = [123]
	fromoffsets = [0, -1, -2]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	with pytest.raises(Exception):
		funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)


def test_awkward_ListOffsetArray_toRegularArray_4():
	size = [123]
	fromoffsets = [0, 2, 5]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	with pytest.raises(Exception):
		funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)


def test_awkward_ListOffsetArray_toRegularArray_5():
	size = [123]
	fromoffsets = [0, 0, 0, 0]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [0]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_6():
	size = [123]
	fromoffsets = [0, 1, 2, 3]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [1]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_7():
	size = [123]
	fromoffsets = [0, 2, 4]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [2]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_8():
	size = [123]
	fromoffsets = [0, 2, 4, 6]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [2]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_9():
	size = [123]
	fromoffsets = [0, 4]
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [4]
	assert size == pytest_size


def test_awkward_ListOffsetArray_toRegularArray_10():
	size = [123]
	fromoffsets = [0, 5, 10]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_toRegularArray')
	funcPy(size = size,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_size = [5]
	assert size == pytest_size


