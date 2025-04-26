import pytest
import numpy
import kernels

def test_awkward_UnionArray_fillindex_1():
	toindex = [123, 123, 123, 123]
	fromindex = [0, 0, 1, 1]
	length = 4
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex')
	funcPy(toindex = toindex,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 0, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_2():
	toindex = []
	fromindex = []
	length = 0
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex')
	funcPy(toindex = toindex,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillindex_3():
	toindex = [123, 123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, 0, 1, 2]
	length = 6
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillindex')
	funcPy(toindex = toindex,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2, 0, 1, 2]
	assert toindex == pytest_toindex


