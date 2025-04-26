import pytest
import numpy
import kernels

def test_awkward_NumpyArray_pad_zero_to_length_1():
	toptr = [123, 123, 123, 123]
	fromoffsets = [0, 2, 3]
	fromptr = [0, 1, 3]
	offsetslength = 3
	target = 2
	funcPy = getattr(kernels, 'awkward_NumpyArray_pad_zero_to_length')
	funcPy(toptr = toptr,fromoffsets = fromoffsets,fromptr = fromptr,offsetslength = offsetslength,target = target)
	pytest_toptr = [0, 1, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_pad_zero_to_length_2():
	toptr = []
	fromoffsets = []
	fromptr = []
	offsetslength = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_NumpyArray_pad_zero_to_length')
	funcPy(toptr = toptr,fromoffsets = fromoffsets,fromptr = fromptr,offsetslength = offsetslength,target = target)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_pad_zero_to_length_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 2, 4]
	fromptr = [1, 3, 3, 5]
	offsetslength = 4
	target = 4
	funcPy = getattr(kernels, 'awkward_NumpyArray_pad_zero_to_length')
	funcPy(toptr = toptr,fromoffsets = fromoffsets,fromptr = fromptr,offsetslength = offsetslength,target = target)
	pytest_toptr = [1, 3, 0, 0, 0, 0, 0, 0, 3, 5, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_pad_zero_to_length_4():
	toptr = [123, 123, 123, 123]
	fromoffsets = [0, 0]
	fromptr = [3, 5]
	offsetslength = 2
	target = 4
	funcPy = getattr(kernels, 'awkward_NumpyArray_pad_zero_to_length')
	funcPy(toptr = toptr,fromoffsets = fromoffsets,fromptr = fromptr,offsetslength = offsetslength,target = target)
	pytest_toptr = [0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_pad_zero_to_length_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 5]
	fromptr = [0, 3, 3, 5, 6]
	offsetslength = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_NumpyArray_pad_zero_to_length')
	funcPy(toptr = toptr,fromoffsets = fromoffsets,fromptr = fromptr,offsetslength = offsetslength,target = target)
	pytest_toptr = [0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 5, 6, 0, 0]
	assert toptr == pytest_toptr


