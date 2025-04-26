import pytest
import numpy
import kernels

def test_awkward_reduce_sum_bool_1():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_2():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
	lenparents = 10
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_3():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 0, 1, 1, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 1, 0, 0, 0, 1, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_5():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
	lenparents = 10
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_6():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 0, 2, 0, 0, 0, 0, 0]
	lenparents = 10
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_7():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 2, 2, 0, 3, 0, 0, 0]
	lenparents = 10
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_8():
	toptr = [123]
	fromptr = [1, 2, 3]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_bool_9():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_sum_bool')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1]
	assert toptr == pytest_toptr


