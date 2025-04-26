import pytest
import numpy
import kernels

def test_awkward_UnionArray_fillindex_count_1():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	length = 3
	toindexoffset = 4
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 123, 123, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_2():
	toindex = []
	length = 0
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_3():
	toindex = [123, 123, 123, 123]
	length = 2
	toindexoffset = 2
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 0, 1]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_4():
	toindex = [123, 123]
	length = 2
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_5():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	toindexoffset = 6
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 123, 123, 123, 123, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_6():
	toindex = [123, 123, 123]
	length = 3
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_7():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	toindexoffset = 9
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_8():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 4
	toindexoffset = 5
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 123, 123, 123, 0, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_count_9():
	toindex = [123, 123, 123, 123, 123]
	length = 5
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_count')
	funcPy(toindex = toindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


