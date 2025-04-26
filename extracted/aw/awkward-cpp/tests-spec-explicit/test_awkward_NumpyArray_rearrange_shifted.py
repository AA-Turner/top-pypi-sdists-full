import pytest
import numpy
import kernels

def test_awkward_NumpyArray_rearrange_shifted_1():
	toptr = []
	fromshifts = []
	length = 0
	fromoffsets = []
	offsetslength = 0
	fromparents = []
	fromstarts = []
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,offsetslength = offsetslength,fromparents = fromparents,fromstarts = fromstarts)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_rearrange_shifted_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	fromshifts = [0, 1, 2, 3, 4, 5, 6]
	length = 4
	fromoffsets = [0, 1, 3, 3, 5, 7, 9]
	offsetslength = 7
	fromparents = [0, 1, 3, 6]
	fromstarts = [0, 1, 2, 3, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,offsetslength = offsetslength,fromparents = fromparents,fromstarts = fromstarts)
	pytest_toptr = [0, 3, 3, 6, 7, 10, 11, 14, 15]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_rearrange_shifted_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	fromshifts = [0, 1, 2, 3, 4, 5, 6]
	length = 4
	fromoffsets = [0, 2, 5, 8]
	offsetslength = 4
	fromparents = [0, 1, 3, 6]
	fromstarts = [0, 1, 2, 3, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,offsetslength = offsetslength,fromparents = fromparents,fromstarts = fromstarts)
	pytest_toptr = [0, -1, 1, -2, 2, 5, 5, 5]
	assert toptr == pytest_toptr


