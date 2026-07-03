import pytest
import numpy
import kernels

def test_awkward_reduce_max_complex_1():
	toptr = []
	identity = -9223372036854775808
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_max_complex')
	funcPy(toptr = toptr,identity = identity,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_max_complex_2():
	toptr = [123, 123]
	identity = -9223372036854775808
	fromptr = [0, 0]
	outlength = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_reduce_max_complex')
	funcPy(toptr = toptr,identity = identity,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_max_complex_3():
	toptr = [123, 123]
	identity = -9223372036854775808
	fromptr = [1, 0, 0, 1]
	outlength = 1
	offsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_reduce_max_complex')
	funcPy(toptr = toptr,identity = identity,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_max_complex_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	identity = -9223372036854775808
	fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_max_complex')
	funcPy(toptr = toptr,identity = identity,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [5, 5, -9223372036854775808, 0, 11, 11, 13, 13, 19, 19, 23, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_max_complex_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	identity = -9223372036854775808
	fromptr = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_max_complex')
	funcPy(toptr = toptr,identity = identity,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 1, -9223372036854775808, 0, 1, 1, 0, 1]
	assert toptr == pytest_toptr


