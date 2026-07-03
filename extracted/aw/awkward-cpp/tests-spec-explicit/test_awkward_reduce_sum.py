import pytest
import numpy
import kernels

def test_awkward_reduce_sum_1():
	toptr = []
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_2():
	toptr = [123]
	fromptr = [0]
	outlength = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
	outlength = 10
	offsets = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 5, 20, 1, 6, 23, 29, 11, 27, 33]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_4():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [10, 0, 18, 13, 36, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_5():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 1, 0, 0]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 0, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_6():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24]
	outlength = 3
	offsets = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [10, 35, 110]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_7():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	outlength = 6
	offsets = [0, 5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [10, 35, 60, 85, 110, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_8():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 3, 4, 5, 6]
	outlength = 4
	offsets = [0, 2, 3, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 3, 0, 15]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 10, 15, 25, 1, 11, 16, 26, 2, 12, 17, 27, 8, 18, 28, 4, 9, 14, 29]
	outlength = 10
	offsets = [0, 3, 5, 7, 8, 11, 13, 15, 17, 19, 20]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 40, 12, 16, 40, 44, 26, 32, 23, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
	outlength = 15
	offsets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_11():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 15, 5, 10, 25, 1, 16, 11, 26, 2, 17, 12, 27, 18, 8, 28, 4, 9, 14, 29]
	outlength = 15
	offsets = [0, 2, 4, 6, 7, 8, 9, 9, 9, 10, 11, 13, 15, 17, 18, 20]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 15, 26, 16, 11, 26, 0, 0, 2, 17, 39, 26, 32, 9, 43]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 15, 5, 20, 10, 25, 1, 16, 6, 21, 11, 26, 2, 17, 7, 22, 12, 27, 3, 18, 8, 23, 13, 28, 4, 19, 9, 24, 14, 29]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 25, 35, 17, 27, 37, 19, 29, 39, 21, 31, 41, 23, 33, 43]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_13():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 10, 15, 20, 25, 1, 6, 11, 16, 21, 26, 2, 7, 12, 17, 22, 27, 3, 8, 13, 18, 23, 28, 4, 9, 14, 19, 24, 29]
	outlength = 10
	offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 60, 18, 63, 21, 66, 24, 69, 27, 72]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_14():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 4, 8, 16, 32, 64, 128, 0, 0, 0, 0]
	outlength = 3
	offsets = [0, 4, 8, 12]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 240, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_15():
	toptr = [123, 123]
	fromptr = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
	outlength = 2
	offsets = [0, 5, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [15, 15]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_16():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [21]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_17():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
	outlength = 8
	offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [22, 40, 3, 0, 0, 0, 30, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_18():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 16, 0, 2, 32, 0, 4, 64, 0, 8, 128, 0]
	outlength = 4
	offsets = [0, 3, 6, 9, 12]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [17, 34, 68, 136]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_19():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [3, 0, 7, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_20():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 4, 1, 3, 5, 6]
	outlength = 4
	offsets = [0, 2, 5, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [4, 9, 0, 6]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_21():
	toptr = [123, 123]
	fromptr = [1, 4, 9, 16, 25, 1, 4, 9, 16, 25]
	outlength = 2
	offsets = [0, 5, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [55, 55]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_22():
	toptr = [123, 123]
	fromptr = [1, 4, 9, 16, 26, 1, 4, 10, 16, 24]
	outlength = 2
	offsets = [0, 5, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [56, 55]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [0, 5, 20, 1, 6, 21, 2, 7, 22, 3, 8, 23, 4, 9, 24]
	outlength = 10
	offsets = [0, 2, 4, 6, 8, 10, 11, 12, 13, 14, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [5, 21, 27, 9, 25, 8, 23, 4, 9, 24]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_24():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [15, 20, 25, 16, 21, 26, 17, 22, 27, 18, 23, 28, 19, 24, 29]
	outlength = 5
	offsets = [0, 3, 6, 9, 12, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [60, 63, 66, 69, 72]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_25():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_26():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 25, 26, 27, 28, 29]
	outlength = 6
	offsets = [0, 4, 7, 11, 15, 15, 20]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [7, 22, 47, 66, 0, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_27():
	toptr = [123, 123, 123]
	fromptr = [2, 2, 4, 5, 5]
	outlength = 3
	offsets = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [8, 0, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_28():
	toptr = [123, 123, 123]
	fromptr = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	outlength = 3
	offsets = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [85, 110, 135]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_29():
	toptr = [123, 123]
	fromptr = [4, 1, 0, 1, 4, 5, 1, 0, 1, 3]
	outlength = 2
	offsets = [0, 5, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [10, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_sum_30():
	toptr = [123, 123]
	fromptr = [4, 1, 0, 1, 4, 4, 1, 0, 1, 4]
	outlength = 2
	offsets = [0, 5, 10]
	funcPy = getattr(kernels, 'awkward_reduce_sum')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [10, 10]
	assert toptr == pytest_toptr


