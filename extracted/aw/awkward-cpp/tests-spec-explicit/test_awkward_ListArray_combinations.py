import pytest
import numpy
import kernels

def test_awkward_ListArray_combinations_1():
	tocarry = [[], []]
	toindex = []
	fromindex = []
	length = 0
	n = 0
	replacement = False
	starts = []
	stops = []
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[], []]
	pytest_toindex = []
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_2():
	tocarry = [[123], [123]]
	toindex = [123, 123]
	fromindex = [0, 0]
	length = 1
	n = 2
	replacement = False
	starts = [0]
	stops = [2]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0], [1]]
	pytest_toindex = [1, 1]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_3():
	tocarry = [[123], [123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0]
	length = 2
	n = 2
	replacement = False
	starts = [0, 2]
	stops = [2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0], [1]]
	pytest_toindex = [1, 1]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_4():
	tocarry = [[123, 123, 123, 123], [123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0]
	length = 2
	n = 2
	replacement = True
	starts = [0, 2]
	stops = [2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0, 0, 1, 2], [0, 1, 1, 2]]
	pytest_toindex = [4, 4]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_5():
	tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = False
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0, 0, 0, 1, 1, 2, 4, 4, 5, 8, 8, 8, 8, 9, 9, 9, 10, 10, 11], [1, 2, 3, 2, 3, 3, 5, 6, 6, 9, 10, 11, 12, 10, 11, 12, 11, 12, 12]]
	pytest_toindex = [19, 19]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_6():
	tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = True
	starts = [0, 4, 4, 7, 8]
	stops = [4, 4, 7, 8, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 4, 5, 5, 6, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12], [0, 1, 2, 3, 1, 2, 3, 2, 3, 3, 4, 5, 6, 5, 6, 6, 7, 8, 9, 10, 11, 12, 9, 10, 11, 12, 10, 11, 12, 11, 12, 12]]
	pytest_toindex = [32, 32]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_ListArray_combinations_7():
	tocarry = [[123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = False
	starts = [0, 3, 3, 10, 10]
	stops = [3, 3, 5, 10, 13]
	funcPy = getattr(kernels, 'awkward_ListArray_combinations')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,starts = starts,stops = stops)
	pytest_tocarry = [[0, 0, 1, 3, 10, 10, 11], [1, 2, 2, 4, 11, 12, 12]]
	pytest_toindex = [7, 7]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


