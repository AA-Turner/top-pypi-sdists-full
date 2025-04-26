import pytest
import numpy
import kernels

def test_awkward_reduce_sum_1():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_2():
	toptr = [123]
	fromptr = [0]
	lenparents = 1
	outlength = 1
	parents = [0]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
	lenparents = 15
	outlength = 10
	parents = [0, 5, 5, 1, 6, 6, 2, 7, 7, 3, 8, 8, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 1, 2, 3, 4, 25, 27, 29, 31, 33]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_4():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [10, 0, 18, 13, 36, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_5():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 1, 0, 0]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 0, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_6():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24]
	lenparents = 15
	outlength = 3
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [10, 35, 110]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_7():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	lenparents = 30
	outlength = 6
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [10, 35, 60, 85, 110, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_8():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 3, 4, 5, 6]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 1, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 3, 0, 15]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 10, 15, 25, 1, 11, 16, 26, 2, 12, 17, 27, 8, 18, 28, 4, 9, 14, 29]
	lenparents = 20
	outlength = 10
	parents = [0, 0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 8, 8, 4, 4, 4, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 12, 14, 8, 27, 40, 42, 44, 46, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
	lenparents = 15
	outlength = 15
	parents = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_11():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 15, 5, 10, 25, 1, 16, 11, 26, 2, 17, 12, 27, 18, 8, 28, 4, 9, 14, 29]
	lenparents = 20
	outlength = 15
	parents = [0, 0, 5, 10, 10, 1, 1, 11, 11, 2, 2, 12, 12, 3, 8, 13, 4, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 17, 19, 18, 4, 5, 0, 0, 8, 9, 35, 37, 39, 28, 43]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 15, 5, 20, 10, 25, 1, 16, 6, 21, 11, 26, 2, 17, 7, 22, 12, 27, 3, 18, 8, 23, 13, 28, 4, 19, 9, 24, 14, 29]
	lenparents = 30
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_13():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 10, 15, 20, 25, 1, 6, 11, 16, 21, 26, 2, 7, 12, 17, 22, 27, 3, 8, 13, 18, 23, 28, 4, 9, 14, 19, 24, 29]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 18, 21, 24, 27, 60, 63, 66, 69, 72]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_14():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 4, 8, 16, 32, 64, 128, 0, 0, 0, 0]
	lenparents = 12
	outlength = 3
	parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 240, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_15():
	toptr = [123, 123]
	fromptr = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [15, 15]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_16():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [21]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_17():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [22, 14, 5, 0, 0, 0, 40, 19]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_18():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 16, 0, 2, 32, 0, 4, 64, 0, 8, 128, 0]
	lenparents = 12
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [17, 34, 68, 136]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_19():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 0, 7, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_20():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 4, 1, 3, 5, 6]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 1, 1, 1, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [4, 9, 0, 6]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_21():
	toptr = [123, 123]
	fromptr = [1, 4, 9, 16, 25, 1, 4, 9, 16, 25]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [55, 55]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_22():
	toptr = [123, 123]
	fromptr = [1, 4, 9, 16, 26, 1, 4, 10, 16, 24]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [56, 55]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
	lenparents = 15
	outlength = 10
	parents = [0, 0, 5, 1, 1, 6, 2, 2, 7, 3, 3, 8, 4, 4, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5, 7, 9, 11, 13, 20, 21, 22, 23, 24]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_24():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
	lenparents = 15
	outlength = 5
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [60, 63, 66, 69, 72]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_25():
	toptr = [123]
	fromptr = [1, 2, 3]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_26():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 25, 26, 27, 28, 29]
	lenparents = 20
	outlength = 6
	parents = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [7, 22, 47, 66, 0, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_27():
	toptr = [123, 123, 123]
	fromptr = [2, 2, 4, 5, 5]
	lenparents = 5
	outlength = 3
	parents = [0, 0, 0, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [8, 0, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_28():
	toptr = [123, 123, 123]
	fromptr = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	lenparents = 15
	outlength = 3
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [85, 110, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_29():
	toptr = [123, 123]
	fromptr = [4, 1, 0, 1, 4, 5, 1, 0, 1, 3]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [10, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_30():
	toptr = [123, 123]
	fromptr = [4, 1, 0, 1, 4, 4, 1, 0, 1, 4]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [10, 10]
	assert toptr == pytest_toptr


