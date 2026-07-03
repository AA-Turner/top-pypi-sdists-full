import pytest
import numpy
import kernels

def test_awkward_IndexedArray_index_of_nulls_1():
	toindex = []
	fromindex = []
	starts = []
	offsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_2():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [-1, -1, 0, 1, 2, -1, -1, -1, 3, -1, 4, 5, -1, -1, 6, 7, 8]
	starts = [0, 5, 8, 11, 14]
	offsets = [0, 5, 8, 11, 14, 17]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [0, 1, 0, 1, 2, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [-1, -1, 3, 5, 6, -1, -1, -1, -1, 7, 0, -1, 4, -1, 8, 1, 2]
	starts = [0, 5, 10, 15, 16]
	offsets = [0, 5, 10, 15, 16, 17]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [0, 1, 0, 1, 2, 3, 1, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_4():
	toindex = [123, 123]
	fromindex = [-1, -1, 0, 1, 2]
	starts = [0]
	offsets = [0, 5]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_5():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, -1, 3, 5, 6, 1, -1, 4, -1, 7, 2, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
	starts = [0, 5, 10, 15, 20]
	offsets = [0, 5, 10, 15, 20, 25]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [1, 1, 3, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_6():
	toindex = [123, 123]
	fromindex = [0, -1, 1, 2, -1, 3, 4, 5]
	starts = [0]
	offsets = [0, 8]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [1, 4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_7():
	toindex = [123]
	fromindex = [0, 1, -1, 2]
	starts = [0]
	offsets = [0, 4]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_8():
	toindex = [123, 123]
	fromindex = [0, 1, -1, -1, 4]
	starts = [0]
	offsets = [0, 5]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [2, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_9():
	toindex = [123, 123]
	fromindex = [0, 1, -1, 2, 3, -1]
	starts = [0]
	offsets = [0, 6]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [2, 5]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_10():
	toindex = [123, 123, 123, 123]
	fromindex = [0, 1, -1, 2, 3, -1, 4, 5, -1, 6, 7, -1]
	starts = [0, 6]
	offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [2, 5, 2, 5]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_index_of_nulls_11():
	toindex = [123, 123, 123, 123]
	fromindex = [0, 1, 2, -1, -1, -1, -1, 7, 8]
	starts = [0, 4]
	offsets = [0, 4, 9]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_index_of_nulls')
	funcPy(toindex = toindex,fromindex = fromindex,starts = starts,offsets = offsets,outlength = outlength)
	pytest_toindex = [3, 0, 1, 2]
	assert toindex == pytest_toindex


