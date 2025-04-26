import pytest
import numpy
import kernels

def test_awkward_ListArray_localindex_1():
	toindex = []
	length = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_2():
	toindex = [123]
	length = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_3():
	toindex = [123, 123, 123, 123, 123]
	length = 3
	offsets = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 0, 0, 1]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_4():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 4
	offsets = [0, 2, 3, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 0, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_5():
	toindex = [123, 123, 123]
	length = 2
	offsets = [0, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_6():
	toindex = [123, 123]
	length = 1
	offsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_7():
	toindex = [123, 123, 123, 123, 123]
	length = 4
	offsets = [0, 3, 3, 4, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 0, 0]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_8():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 7
	offsets = [0, 3, 3, 5, 6, 10, 10, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_9():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 3, 3, 5, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_10():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 3, 5, 6, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 0, 1, 0, 0, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_11():
	toindex = [123, 123, 123, 123, 123]
	length = 3
	offsets = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 0, 1]
	assert toindex == pytest_toindex


def test_awkward_ListArray_localindex_12():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_localindex')
	funcPy(toindex = toindex,length = length,offsets = offsets)
	pytest_toindex = [0, 1, 2, 3, 0, 1, 2, 0, 0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


