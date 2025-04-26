import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_local_preparenext_64_1():
	tocarry = []
	fromindex = []
	length = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_2():
	tocarry = [123]
	fromindex = [0]
	length = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_3():
	tocarry = [123, 123]
	fromindex = [2, 0]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [1, 0]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_4():
	tocarry = [123, 123]
	fromindex = [0, 2]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_5():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 2, 3, 5, 7]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_6():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [7, 5, 3, 2, 0]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [4, 3, 2, 1, 0]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_7():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 2, 7, 5, 3]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [0, 1, 4, 3, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListOffsetArray_local_preparenext_64_8():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [1, 0, 2, 4, 3, 6, 5, 7]
	length = 8
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_local_preparenext_64')
	funcPy(tocarry = tocarry,fromindex = fromindex,length = length)
	pytest_tocarry = [1, 0, 2, 4, 3, 6, 5, 7]
	assert tocarry == pytest_tocarry


