import pytest
import numpy
import kernels

def test_awkward_reduce_argmax_1():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_2():
	toptr = [123, 123, 123]
	fromptr = [1, -1, 1, -1, 1, 21]
	lenparents = 6
	outlength = 3
	parents = [0, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 2, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_3():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 4, 6, 7]
	lenparents = 6
	outlength = 3
	parents = [0, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 2, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_4():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [6, 1, 10, 33, -1, 21, 2, 45, 4]
	lenparents = 9
	outlength = 5
	parents = [0, 0, 3, 3, 1, 1, 4, 4, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 5, 8, 3, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_5():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 4, 6]
	lenparents = 5
	outlength = 3
	parents = [0, 0, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 2, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_6():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
	lenparents = 12
	outlength = 5
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 5, 6, 10, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_7():
	toptr = [123]
	fromptr = [1, 2, 3]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_8():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 6]
	lenparents = 6
	outlength = 3
	parents = [0, 0, 0, 1, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 4, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_9():
	toptr = [123, 123, 123]
	fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
	lenparents = 12
	outlength = 3
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 8, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_10():
	toptr = [123]
	fromptr = [0, 0, 4, 4, 6]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_11():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 6]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_12():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5]
	assert toptr == pytest_toptr


