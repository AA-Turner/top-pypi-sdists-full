import pytest
import numpy
import kernels

def test_awkward_reduce_argmin_1():
	toptr = [123]
	fromptr = [0, 0, 4, 4, 6]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_2():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_3():
	toptr = [123]
	fromptr = [1, 2, 3]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_4():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_5():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 6]
	lenparents = 6
	outlength = 3
	parents = [0, 0, 0, 1, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_6():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 4, 2, 6, 3, 0, -10]
	lenparents = 7
	outlength = 4
	parents = [0, 0, 0, 1, 1, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 4, 5, 6]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_7():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 1, 3, 4, 6, 6, -4, -6, -7]
	lenparents = 9
	outlength = 5
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, -1, 3, 5, 8]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_8():
	toptr = [123, 123, 123]
	fromptr = [2, 1, 3, -4, -6, -7]
	lenparents = 6
	outlength = 3
	parents = [0, 0, 0, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, -1, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_9():
	toptr = [123, 123, 123]
	fromptr = [2, 1, 3, 2, 1]
	lenparents = 5
	outlength = 3
	parents = [0, 0, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 2, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_10():
	toptr = [123, 123, 123]
	fromptr = [2, 2, 1, 0, 1, 0]
	lenparents = 6
	outlength = 3
	parents = [0, 0, 1, 1, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_11():
	toptr = [123, 123, 123]
	fromptr = [2, 0, 2, 1, 1, 0]
	lenparents = 6
	outlength = 3
	parents = [0, 0, 0, 1, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, -3, 4, 4, 2, 2, 2, 2, 2, -2, 1, 1, 6, -6, 1, 1, 4, 4, 1, 1, 3, -3, 3, 3, 4, 4, 6, 6, 6, -6]
	lenparents = 30
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 6, 13, 18, 24, 2, 9, 14, 21, 26, 4, 10, 16, 22, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_13():
	toptr = [123, 123, 123]
	fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
	lenparents = 12
	outlength = 3
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_14():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [-4, -6, -7, 6, 4, 6, 2, 1, 3]
	lenparents = 9
	outlength = 5
	parents = [0, 0, 0, 1, 2, 2, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 3, 4, -1, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_15():
	toptr = [123, 123, 123, 123]
	fromptr = [-4, -6, -7, 6, -4, -6, -7, 2, 1, 3]
	lenparents = 10
	outlength = 4
	parents = [0, 0, 0, 1, 2, 2, 2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 3, 6, 8]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_16():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
	lenparents = 12
	outlength = 5
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 3, 8, 9, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_17():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 2, 2, 1, 6, 1, 4, 1, 3, 3, 4, 6, 6]
	lenparents = 15
	outlength = 5
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 5, 7, 9, 12]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_18():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, -3, 4, 2, 2, 2, 1, 2, -2, 1, 6, 1, 4, -6, 1, 4, 1, 3, 3, 1, -3, 3, 4, 6, 6, 4, 6, -6]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 8, 13, 18, 24, 3, 10, 15, 22, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_19():
	toptr = [123]
	fromptr = [6, 3, 2, 1, 2]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_20():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6, -3, 2, -6, 1, 4, 4, -2, 1, -3, 6, 2, 1, 4, 3, -6]
	lenparents = 30
	outlength = 6
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 7, 11, 17, 23, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_21():
	toptr = [123, 123, 123]
	fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6]
	lenparents = 15
	outlength = 3
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_22():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 2, 2, 2, 3, 3]
	lenparents = 18
	outlength = 6
	parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 10, 16, 5, 13, 17]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3, 999]
	lenparents = 22
	outlength = 8
	parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 10, 17, -1, 5, 14, 20, 21]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_24():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3]
	lenparents = 21
	outlength = 6
	parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 4, 2, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 10, 17, 5, 14, 20]
	assert toptr == pytest_toptr


