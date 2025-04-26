import pytest
import numpy
import kernels

def test_awkward_UnionArray_regular_index_1():
	current = []
	toindex = []
	fromtags = []
	length = 0
	size = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index')
	funcPy(current = current,toindex = toindex,fromtags = fromtags,length = length,size = size)
	pytest_current = []
	pytest_toindex = []
	assert current == pytest_current
	assert toindex == pytest_toindex


def test_awkward_UnionArray_regular_index_2():
	current = [123, 123]
	toindex = [123, 123, 123, 123, 123, 123]
	fromtags = [0, 1, 0, 1, 0, 1]
	length = 6
	size = 2
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index')
	funcPy(current = current,toindex = toindex,fromtags = fromtags,length = length,size = size)
	pytest_current = [3, 3]
	pytest_toindex = [0, 0, 1, 1, 2, 2]
	assert current == pytest_current
	assert toindex == pytest_toindex


def test_awkward_UnionArray_regular_index_3():
	current = [123, 123]
	toindex = [123, 123, 123, 123]
	fromtags = [1, 0, 1, 1]
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index')
	funcPy(current = current,toindex = toindex,fromtags = fromtags,length = length,size = size)
	pytest_current = [1, 3]
	pytest_toindex = [0, 0, 1, 2]
	assert current == pytest_current
	assert toindex == pytest_toindex


def test_awkward_UnionArray_regular_index_4():
	current = [123, 123]
	toindex = [123, 123, 123, 123, 123, 123, 123, 123]
	fromtags = [1, 1, 0, 0, 1, 0, 1, 1]
	length = 8
	size = 2
	funcPy = getattr(kernels, 'awkward_UnionArray_regular_index')
	funcPy(current = current,toindex = toindex,fromtags = fromtags,length = length,size = size)
	pytest_current = [3, 5]
	pytest_toindex = [0, 1, 0, 1, 2, 2, 3, 4]
	assert current == pytest_current
	assert toindex == pytest_toindex


