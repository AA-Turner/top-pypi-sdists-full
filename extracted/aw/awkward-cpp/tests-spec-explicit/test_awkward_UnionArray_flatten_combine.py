import pytest
import numpy
import kernels

def test_awkward_UnionArray_flatten_combine_1():
	totags = []
	toindex = []
	tooffsets = [123]
	fromtags = []
	fromindex = []
	length = 0
	offsetsraws = [[], []]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_combine')
	funcPy(totags = totags,toindex = toindex,tooffsets = tooffsets,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_totags = []
	pytest_toindex = []
	pytest_tooffsets = [0]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tooffsets == pytest_tooffsets


def test_awkward_UnionArray_flatten_combine_2():
	totags = [123, 123, 123]
	toindex = [123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123]
	fromtags = [0, 1, 0, 1]
	fromindex = [0, 0, 1, 1]
	length = 4
	offsetsraws = [[0, 2, 2, 3, 5], [2, 2, 3, 5, 6]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_combine')
	funcPy(totags = totags,toindex = toindex,tooffsets = tooffsets,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_totags = [0, 0, 1]
	pytest_toindex = [0, 1, 2]
	pytest_tooffsets = [0, 2, 2, 2, 3]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tooffsets == pytest_tooffsets


def test_awkward_UnionArray_flatten_combine_3():
	totags = [123, 123, 123, 123, 123, 123, 123]
	toindex = [123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123]
	fromtags = [0, 0, 0, 0]
	fromindex = [0, 1, 2, 3]
	length = 4
	offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_combine')
	funcPy(totags = totags,toindex = toindex,tooffsets = tooffsets,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_totags = [0, 0, 0, 0, 0, 0, 0]
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6]
	pytest_tooffsets = [0, 1, 3, 5, 7]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tooffsets == pytest_tooffsets


