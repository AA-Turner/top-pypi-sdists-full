import pytest
import numpy
import kernels

def test_awkward_RegularArray_combinations_64_1():
	tocarry = [[], []]
	toindex = []
	fromindex = []
	length = 0
	n = 0
	replacement = False
	size = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[], []]
	pytest_toindex = []
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_2():
	tocarry = [[123], [123]]
	toindex = [123, 123]
	fromindex = [0, 0]
	length = 1
	n = 2
	replacement = False
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0], [1]]
	pytest_toindex = [1, 1]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_3():
	tocarry = [[123, 123, 123], [123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0]
	length = 1
	n = 2
	replacement = True
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0, 0, 1], [0, 1, 1]]
	pytest_toindex = [3, 3]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_4():
	tocarry = [[123, 123, 123], [123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0]
	length = 3
	n = 2
	replacement = False
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0, 2, 4], [1, 3, 5]]
	pytest_toindex = [3, 3]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_5():
	tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = True
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0, 0, 0, 1, 1, 2, 3, 3, 3, 4, 4, 5, 6, 6, 6, 7, 7, 8, 9, 9, 9, 10, 10, 11, 12, 12, 12, 13, 13, 14], [0, 1, 2, 1, 2, 2, 3, 4, 5, 4, 5, 5, 6, 7, 8, 7, 8, 8, 9, 10, 11, 10, 11, 11, 12, 13, 14, 13, 14, 14]]
	pytest_toindex = [30, 30]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_6():
	tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = False
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0, 0, 1, 3, 3, 4, 6, 6, 7, 9, 9, 10, 12, 12, 13], [1, 2, 2, 4, 5, 5, 7, 8, 8, 10, 11, 11, 13, 14, 14]]
	pytest_toindex = [15, 15]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_RegularArray_combinations_64_7():
	tocarry = [[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123], [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]]
	toindex = [123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	length = 5
	n = 2
	replacement = False
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_combinations_64')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,length = length,n = n,replacement = replacement,size = size)
	pytest_tocarry = [[0, 0, 0, 1, 1, 2, 4, 4, 4, 5, 5, 6, 8, 8, 8, 9, 9, 10, 12, 12, 12, 13, 13, 14, 16, 16, 16, 17, 17, 18], [1, 2, 3, 2, 3, 3, 5, 6, 7, 6, 7, 7, 9, 10, 11, 10, 11, 11, 13, 14, 15, 14, 15, 15, 17, 18, 19, 18, 19, 19]]
	pytest_toindex = [30, 30]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


