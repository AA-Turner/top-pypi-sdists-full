import pytest
import numpy
import kernels

def test_awkward_reduce_prod_complex_1():
	toptr = []
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_complex_2():
	toptr = [123, 123]
	fromptr = [0, 0]
	outlength = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_complex_3():
	toptr = [123, 123]
	fromptr = [1, 0]
	outlength = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_complex_4():
	toptr = [123, 123]
	fromptr = [1, 0, 0, 1]
	outlength = 1
	offsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_complex_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [-60, 60, 1, 0, 0, 154, 13, 13, 0, 646, 23, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_complex_6():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod_complex')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [-1, -1, 1, 0, -1, 1, 0, 1]
	assert toptr == pytest_toptr


