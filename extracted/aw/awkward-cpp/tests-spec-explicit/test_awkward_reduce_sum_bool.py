import pytest
import numpy
import kernels

def test_awkward_reduce_sum_bool_1():
	toptr = []
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_2():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
	outlength = 4
	offsets = [0, 3, 6, 9, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_3():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False, False, True, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
	outlength = 8
	offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, False, False, False, False, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_5():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
	outlength = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_6():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 0, 2, 0, 0, 0, 0, 0]
	outlength = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_7():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 2, 2, 0, 3, 0, 0, 0]
	outlength = 4
	offsets = [0, 3, 6, 9, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_8():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_9():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True]
	assert toptr == pytest_toptr


