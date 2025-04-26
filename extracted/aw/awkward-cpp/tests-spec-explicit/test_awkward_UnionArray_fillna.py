import pytest
import numpy
import kernels

def test_awkward_UnionArray_fillna_1():
	toindex = []
	fromindex = []
	length = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_2():
	toindex = [123, 123, 123, 123, 123]
	fromindex = [-1, -1, -1, -1, -1]
	length = 5
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 0, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [-1, -1, 0, -1, 1, 2, 3, 4, 5, -1, -1, -1]
	length = 12
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_4():
	toindex = [123, 123, 123, 123]
	fromindex = [-1, 0, 1, -1]
	length = 4
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_5():
	toindex = [123, 123, 123]
	fromindex = [0, -1, 1]
	length = 3
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 1]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_6():
	toindex = [123, 123, 123, 123, 123]
	fromindex = [0, -1, 1, -1, 2]
	length = 5
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 1, 0, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_7():
	toindex = [123, 123, 123, 123]
	fromindex = [0, -1, 1, 2]
	length = 4
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_8():
	toindex = [123, 123, 123]
	fromindex = [0, 1, -1]
	length = 3
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_9():
	toindex = [123, 123, 123, 123]
	fromindex = [0, 1, -1, 2]
	length = 4
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 0, 2]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_10():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 1, -1, 2, 3, -1, 4]
	length = 7
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 0, 2, 3, 0, 4]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_11():
	toindex = [123, 123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, -1, -1, -1]
	length = 6
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 2, 0, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_12():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, -1, -1, 3, 4, 5, -1, -1]
	length = 10
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 2, 0, 0, 3, 4, 5, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_13():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, 3, 4, -1, -1]
	length = 7
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [0, 1, 2, 3, 4, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_UnionArray_fillna_14():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [13, 9, 13, 4, 8, 3, 15, -1, 16, 2, 8]
	length = 11
	funcPy = getattr(kernels, 'awkward_UnionArray_fillna')
	funcPy(toindex = toindex,fromindex = fromindex,length = length)
	pytest_toindex = [13, 9, 13, 4, 8, 3, 15, 0, 16, 2, 8]
	assert toindex == pytest_toindex


