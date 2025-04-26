import pytest
import numpy
import kernels

def test_awkward_sort_1():
	toptr = []
	fromptr = []
	offsets = []
	offsetslength = 0
	parentslength = 0
	length = 1
	ascending = True
	stable = True
	funcPy = getattr(kernels, 'awkward_sort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,parentslength = parentslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_sort_2():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [8, 6, 7, 5, 3, 0, 9]
	offsets = [0, 3, 3, 7]
	offsetslength = 4
	parentslength = 7
	length = 7
	ascending = True
	stable = True
	funcPy = getattr(kernels, 'awkward_sort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,parentslength = parentslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [6, 7, 8, 0, 3, 5, 9]
	assert toptr == pytest_toptr


def test_awkward_sort_3():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [8, 6, 7, 5, 3, 0, 9]
	offsets = [0, 3, 3, 7]
	offsetslength = 4
	parentslength = 7
	length = 7
	ascending = False
	stable = True
	funcPy = getattr(kernels, 'awkward_sort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,parentslength = parentslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [8, 7, 6, 9, 5, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_sort_4():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [8, 6, 7, 5, 3, 0, 9]
	offsets = [0, 3, 3, 7]
	offsetslength = 4
	parentslength = 7
	length = 7
	ascending = True
	stable = False
	funcPy = getattr(kernels, 'awkward_sort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,parentslength = parentslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [6, 7, 8, 0, 3, 5, 9]
	assert toptr == pytest_toptr


def test_awkward_sort_5():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [8, 6, 7, 5, 3, 0, 9]
	offsets = [0, 3, 3, 7]
	offsetslength = 4
	parentslength = 7
	length = 7
	ascending = False
	stable = False
	funcPy = getattr(kernels, 'awkward_sort')
	funcPy(toptr = toptr,fromptr = fromptr,offsets = offsets,offsetslength = offsetslength,parentslength = parentslength,length = length,ascending = ascending,stable = stable)
	pytest_toptr = [8, 7, 6, 9, 5, 3, 0]
	assert toptr == pytest_toptr


