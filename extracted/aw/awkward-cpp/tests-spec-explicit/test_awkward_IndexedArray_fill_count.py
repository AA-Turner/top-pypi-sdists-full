import pytest
import numpy
import kernels

def test_awkward_IndexedArray_fill_count_1():
	toindex = []
	base = 0
	length = 0
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill_count')
	funcPy(toindex = toindex,base = base,length = length,toindexoffset = toindexoffset)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_count_2():
	toindex = [123, 123, 123, 123, 123]
	base = 0
	length = 5
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill_count')
	funcPy(toindex = toindex,base = base,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_count_3():
	toindex = [123, 123, 123, 123, 123, 123]
	base = 0
	length = 3
	toindexoffset = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill_count')
	funcPy(toindex = toindex,base = base,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 123, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_count_4():
	toindex = [123, 123, 123, 123]
	base = 3
	length = 4
	toindexoffset = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill_count')
	funcPy(toindex = toindex,base = base,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [3, 4, 5, 6]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_fill_count_5():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	base = 3
	length = 5
	toindexoffset = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_fill_count')
	funcPy(toindex = toindex,base = base,length = length,toindexoffset = toindexoffset)
	pytest_toindex = [123, 123, 3, 4, 5, 6, 7]
	assert toindex == pytest_toindex


