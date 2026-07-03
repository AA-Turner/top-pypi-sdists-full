import pytest
import numpy
import kernels

def test_awkward_NumpyArray_rearrange_shifted_1():
	toptr = []
	fromshifts = []
	length = 0
	fromoffsets = []
	fromparents = []
	fromstarts = []
	outlength = 0
	toptr = []
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,fromparents = fromparents,fromstarts = fromstarts,outlength = outlength)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_rearrange_shifted_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromshifts = [0, 1, 2, 3, 4, 5, 6]
	length = 4
	fromoffsets = [0, 1, 3, 3, 5, 7, 9]
	fromparents = [0, 1, 3, 6]
	fromstarts = [0, 1, 2, 3, 4, 5, 6]
	outlength = 6
	toptr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,fromparents = fromparents,fromstarts = fromstarts,outlength = outlength)
	pytest_toptr = [0, 3, 3, 6, 7, 10, 11, 14, 15]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_rearrange_shifted_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromshifts = [0, 1, 2, 3, 4, 5, 6]
	length = 4
	fromoffsets = [0, 2, 5, 8]
	fromparents = [0, 1, 3, 6]
	fromstarts = [0, 1, 2, 3, 4, 5, 6]
	outlength = 3
	toptr = [0, 1, 2, 3, 4, 5, 6, 7]
	funcPy = getattr(kernels, 'awkward_NumpyArray_rearrange_shifted')
	funcPy(toptr = toptr,fromshifts = fromshifts,length = length,fromoffsets = fromoffsets,fromparents = fromparents,fromstarts = fromstarts,outlength = outlength)
	pytest_toptr = [0, 1, 5, 4, 6, 10, 11, 12]
	assert toptr == pytest_toptr


