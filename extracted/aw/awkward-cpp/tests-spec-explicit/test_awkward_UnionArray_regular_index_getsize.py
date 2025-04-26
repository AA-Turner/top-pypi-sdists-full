import pytest
import numpy
import kernels

def test_awkward_UnionArray_regular_index_getsize_1():
	size = [123]
	fromtags = []
	length = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [1]
	assert size == pytest_size


def test_awkward_UnionArray_regular_index_getsize_2():
	size = [123]
	fromtags = [0]
	length = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [1]
	assert size == pytest_size


def test_awkward_UnionArray_regular_index_getsize_3():
	size = [123]
	fromtags = [-1]
	length = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [1]
	assert size == pytest_size


def test_awkward_UnionArray_regular_index_getsize_4():
	size = [123]
	fromtags = [0, 1, 0, 1, 0, 1]
	length = 6
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [2]
	assert size == pytest_size


def test_awkward_UnionArray_regular_index_getsize_5():
	size = [123]
	fromtags = [1, 0, 1, 1]
	length = 4
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [2]
	assert size == pytest_size


def test_awkward_UnionArray_regular_index_getsize_6():
	size = [123]
	fromtags = [1, 1, 0, 0, 1, 0, 1, 1]
	length = 8
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index_getsize')
	funcPy(size = size,fromtags = fromtags,length = length)
	pytest_size = [2]
	assert size == pytest_size


