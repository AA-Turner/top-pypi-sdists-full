import pytest
import numpy
import kernels

def test_awkward_UnionArray_flatten_length_1():
	total_length = [123]
	fromtags = []
	fromindex = []
	length = 0
	offsetsraws = [[], []]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_length')
	funcPy(total_length = total_length,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_total_length = [0]
	assert total_length == pytest_total_length


def test_awkward_UnionArray_flatten_length_2():
	total_length = [123]
	fromtags = [0, 1, 0, 1]
	fromindex = [0, 0, 1, 1]
	length = 4
	offsetsraws = [[0, 2, 2, 3, 5], [2, 2, 3, 5, 6]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_length')
	funcPy(total_length = total_length,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_total_length = [3]
	assert total_length == pytest_total_length


def test_awkward_UnionArray_flatten_length_3():
	total_length = [123]
	fromtags = [0, 0, 0, 0]
	fromindex = [0, 1, 2, 3]
	length = 4
	offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_length')
	funcPy(total_length = total_length,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_total_length = [7]
	assert total_length == pytest_total_length


def test_awkward_UnionArray_flatten_length_4():
	total_length = [123]
	fromtags = [1, 1, 1, 1]
	fromindex = [0, 1, 2, 3]
	length = 4
	offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_length')
	funcPy(total_length = total_length,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_total_length = [8]
	assert total_length == pytest_total_length


