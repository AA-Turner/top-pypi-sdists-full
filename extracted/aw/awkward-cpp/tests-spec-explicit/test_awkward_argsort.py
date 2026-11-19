import pytest
import numpy
import kernels

def test_awkward_argsort_1():
	toptr = [123, 123, 123, 123, 123]
	toptr = [-1, -1, -1, -1, -1]
	fromptr = [1, 0, 0, 1, 1]
	offsets = [0, 2]
	offsetslength = 2
	length = 5
	ascending = True
	stable = True
	funcPy = getattr(kernels, 'awkward_argsort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [1, 0, 2, 3, 4]
	assert toptr == pytest_toptr


def test_awkward_argsort_2():
	toptr = [123, 123, 123, 123, 123]
	toptr = [-1, -1, -1, -1, -1]
	fromptr = [1, 0, 0, 1, 1]
	offsets = [0, 0, 0]
	offsetslength = 3
	length = 5
	ascending = True
	stable = True
	funcPy = getattr(kernels, 'awkward_argsort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [0, 1, 2, 3, 4]
	assert toptr == pytest_toptr


def test_awkward_argsort_3():
	toptr = [123, 123, 123, 123, 123]
	toptr = [-1, -1, -1, -1, -1]
	fromptr = [1, 0, 0, 1, 1]
	offsets = [0, 2, 5]
	offsetslength = 2
	length = 5
	ascending = True
	stable = True
	funcPy = getattr(kernels, 'awkward_argsort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [1, 0, 2, 3, 4]
	assert toptr == pytest_toptr


