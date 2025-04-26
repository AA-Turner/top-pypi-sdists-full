import pytest
import numpy
import kernels

def test_awkward_IndexedArray_fill_1():
	toindex = []
	base = 0
	fromindex = []
	length = 0
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_2():
	toindex = [123, 123, 123, 123, 123]
	base = 0
	fromindex = [0, 1, -1, -1, 4]
	length = 5
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, -1, -1, 4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_3():
	toindex = [123, 123, 123, 123, 123]
	base = 0
	fromindex = [0, 1, 2, 3, -1]
	length = 5
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2, 3, -1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_4():
	toindex = [123, 123, 123]
	base = 0
	fromindex = [0, 1, 2]
	length = 3
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_5():
	toindex = [123, 123, 123, 123, 123, 123]
	base = 0
	fromindex = [-1, -1, 0, -1, 1, 2]
	length = 6
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [-1, -1, 0, -1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_6():
	toindex = [123, 123, 123, 123, 123, 123]
	base = 0
	fromindex = [2, 0, -1, 0, 1, 2]
	length = 6
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill')
	funcPy(toindex = toindex,base = base,fromindex = fromindex,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [2, 0, -1, 0, 1, 2]
	assert toindex == pytest_toindex


