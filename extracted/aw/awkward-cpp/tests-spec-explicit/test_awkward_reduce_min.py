import pytest
import numpy
import kernels

def test_awkward_reduce_min_1():
	toptr = []
	fromptr = []
	identity = 9223372036854775807
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_min_2():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 4, 1, 1, 5, 6]
	identity = 9223372036854775807
	lenparents = 6
	outlength = 4
	parents = [0, 0, 1, 1, 1, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 1, 9223372036854775807, 6]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_3():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 3, 4, 5, 6]
	identity = 9223372036854775807
	lenparents = 6
	outlength = 4
	parents = [0, 0, 1, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 9223372036854775807, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_4():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 3, 2, 5, 3, 7, 3, 1, 5, 8, 1, 9, 4, 2, 7, 10, 2, 4, 7, 2]
	identity = 9223372036854775807
	lenparents = 20
	outlength = 5
	parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 1, 1, 2, 2]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_5():
	toptr = [123]
	fromptr = [1, 2, 3]
	identity = 9223372036854775807
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_6():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	identity = 9223372036854775807
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_7():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 3, 6, 4, 2, 2, 3, 1, 6]
	identity = 4
	lenparents = 9
	outlength = 4
	parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 4, 1, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_8():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 3, 5, 4, 2, 3, 7, 8, 2, 4, 2, 3, 1, 7, 7, 5, 1, 9, 10, 2]
	identity = 9223372036854775807
	lenparents = 20
	outlength = 4
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 2, 1, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 4, 4, 2, 2, 5, 3, 3, 3, 6, 2, 4]
	identity = 9223372036854775807
	lenparents = 12
	outlength = 9
	parents = [0, 0, 6, 6, 1, 1, 7, 7, 2, 2, 8, 8]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 2, 3, 9223372036854775807, 9223372036854775807, 9223372036854775807, 2, 3, 2]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_10():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 2, 5, 3, 3, 5, 1, 4, 2]
	identity = 9223372036854775807
	lenparents = 9
	outlength = 5
	parents = [0, 0, 0, 1, 1, 2, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 3, 1, 4, 2]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_11():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
	identity = 4
	lenparents = 9
	outlength = 4
	parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 4, 1, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_12():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 3, 5, 4, 2, 2, 3, 1, 5]
	identity = 9223372036854775807
	lenparents = 9
	outlength = 4
	parents = [0, 0, 0, 0, 0, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 9223372036854775807, 1, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_13():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
	identity = 9223372036854775807
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 3, 5, 9223372036854775807, 9223372036854775807, 9223372036854775807, 17, 19]
	assert toptr == pytest_toptr


def test_awkward_reduce_min_14():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	identity = 9223372036854775807
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_min')
	funcPy(toptr = toptr,fromptr = fromptr,identity = identity,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 9223372036854775807, 7, 13, 17, 23]
	assert toptr == pytest_toptr


