import pytest
import numpy
import kernels

def test_awkward_ListArray_combinations_length_1():
	tooffsets = [123]
	totallen = [123]
	length = 0
	n = 0
	replacement = False
	starts = []
	stops = []
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0]
	pytest_totallen = [0]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_2():
	tooffsets = [123, 123, 123, 123, 123, 123]
	totallen = [123]
	length = 5
	n = 3
	replacement = False
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 4, 4, 5, 5, 15]
	pytest_totallen = [15]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_3():
	tooffsets = [123, 123]
	totallen = [123]
	length = 1
	n = 2
	replacement = False
	starts = [0]
	stops = [1]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 0]
	pytest_totallen = [0]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_4():
	tooffsets = [123, 123]
	totallen = [123]
	length = 1
	n = 2
	replacement = False
	starts = [0]
	stops = [2]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 1]
	pytest_totallen = [1]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_5():
	tooffsets = [123, 123, 123, 123, 123, 123]
	totallen = [123]
	length = 5
	n = 2
	replacement = False
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 6, 6, 9, 9, 19]
	pytest_totallen = [19]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_6():
	tooffsets = [123, 123, 123, 123, 123, 123]
	totallen = [123]
	length = 5
	n = 2
	replacement = True
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 10, 10, 16, 17, 32]
	pytest_totallen = [32]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_7():
	tooffsets = [123, 123, 123, 123]
	totallen = [123]
	length = 3
	n = 2
	replacement = False
	starts = [0, 3, 3]
	stops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 3, 3, 4]
	pytest_totallen = [4]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_8():
	tooffsets = [123, 123, 123, 123]
	totallen = [123]
	length = 3
	n = 2
	replacement = False
	starts = [0, 3, 5]
	stops = [3, 3, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 3, 3, 4]
	pytest_totallen = [4]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_9():
	tooffsets = [123, 123, 123, 123, 123, 123]
	totallen = [123]
	length = 5
	n = 3
	replacement = True
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 20, 20, 30, 31, 66]
	pytest_totallen = [66]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


def test_awkward_ListArray_combinations_length_10():
	tooffsets = [123, 123, 123, 123, 123, 123]
	totallen = [123]
	length = 5
	n = 2
	replacement = False
	starts = [0, 3, 3, 10, 10]
	stops = [3, 3, 5, 10, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations_length')
	funcPy(tooffsets = tooffsets,totallen = totallen,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tooffsets = [0, 3, 3, 4, 4, 7]
	pytest_totallen = [7]
	assert tooffsets == pytest_tooffsets
	assert totallen == pytest_totallen


