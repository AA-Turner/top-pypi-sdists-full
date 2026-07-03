import pytest
import numpy
import kernels

def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_1():
	toptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	outlength = 10
	offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	outlength = 8
	offsets = [0, 5, 8, 11, 11, 16, 20, 21, 22]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0, 0, 1, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	outlength = 8
	offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0, 0, 1, 1, 1, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_6():
	toptr = [123, 123, 123, 123]
	outlength = 4
	offsets = [0, 5, 5, 8, 9]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_mask_ByteMaskedArray_64_7():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	outlength = 7
	offsets = [0, 3, 3, 5, 6, 6, 6, 9]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_mask_ByteMaskedArray_64')
	funcPy(toptr = toptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 0, 0, 1, 1, 0]
	assert toptr == pytest_toptr


