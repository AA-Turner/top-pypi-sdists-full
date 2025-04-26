import pytest
import numpy
import kernels

def test_awkward_reduce_sum_bool_complex_1():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool_complex')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_complex_2():
	toptr = [123]
	fromptr = [0, 0]
	lenparents = 1
	outlength = 1
	parents = [0]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool_complex')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_complex_3():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 2, 3, 3, 5, 5, 7, 7, 11, 11, 13, 13, 17, 17, 19, 19, 23, 23]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool_complex')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 1, 1, 1, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_complex_4():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool_complex')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_complex_5():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool_complex')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 1, 1]
	assert toptr == pytest_toptr


