import pytest
import numpy
import kernels

def test_awkward_unique_ranges_1():
	toptr = []
	tooffsets = [123]
	toptr = []
	fromoffsets = [0]
	offsetslength = 1
	funcPy = getattr(kernels, 'awkward_unique_ranges')
	funcPy(toptr = toptr,tooffsets = tooffsets,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_toptr = []
	pytest_tooffsets = [0]
	assert toptr == pytest_toptr
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_ranges_2():
	toptr = [123, 123]
	tooffsets = [123, 123]
	toptr = [1, 2]
	fromoffsets = [0, 2]
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_unique_ranges')
	funcPy(toptr = toptr,tooffsets = tooffsets,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_toptr = [1, 2]
	pytest_tooffsets = [0, 2]
	assert toptr == pytest_toptr
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_ranges_3():
	toptr = [123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	toptr = [0, 1, 2, 3, 4, 5]
	fromoffsets = [0, 3, 5, 6]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_unique_ranges')
	funcPy(toptr = toptr,tooffsets = tooffsets,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_toptr = [0, 1, 2, 3, 4, 5]
	pytest_tooffsets = [0, 3, 5, 6]
	assert toptr == pytest_toptr
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_ranges_4():
	toptr = [123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	toptr = [3, 2, 1, 0]
	fromoffsets = [0, 0, 3, 3]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_unique_ranges')
	funcPy(toptr = toptr,tooffsets = tooffsets,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_toptr = [3, 3, 1, 0]
	pytest_tooffsets = [0, 1, 3, 4]
	assert toptr == pytest_toptr
	assert tooffsets == pytest_tooffsets


