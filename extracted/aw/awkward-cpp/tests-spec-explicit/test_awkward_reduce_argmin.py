import pytest
import numpy
import kernels

def test_awkward_reduce_argmin_1():
	toptr = [123]
	fromptr = [0, 0, 4, 4, 6]
	outlength = 1
	starts = [0]
	offsets = [0, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_2():
	toptr = []
	fromptr = []
	outlength = 0
	starts = []
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_3():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	starts = [0]
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_4():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	starts = [0]
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_5():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 6]
	outlength = 3
	starts = [0, 3, 5]
	offsets = [0, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_6():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 4, 2, 6, 3, 0, -10]
	outlength = 4
	starts = [0, 3, 5, 6]
	offsets = [0, 3, 5, 6, 7]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 4, 5, 6]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_7():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 1, 3, 4, 6, 6, -4, -6, -7]
	outlength = 5
	starts = [0, -1, 3, 5, 6]
	offsets = [0, 3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, -1, 3, 5, 8]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_8():
	toptr = [123, 123, 123]
	fromptr = [2, 1, 3, -4, -6, -7]
	outlength = 3
	starts = [0, -1, 3]
	offsets = [0, 3, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, -1, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_9():
	toptr = [123, 123, 123]
	fromptr = [2, 1, 3, 2, 1]
	outlength = 3
	starts = [0, 2, 3]
	offsets = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 2, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_10():
	toptr = [123, 123, 123]
	fromptr = [2, 2, 1, 0, 1, 0]
	outlength = 3
	starts = [0, 2, 5]
	offsets = [0, 2, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_11():
	toptr = [123, 123, 123]
	fromptr = [2, 0, 2, 1, 1, 0]
	outlength = 3
	starts = [0, 3, 5]
	offsets = [0, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, -3, 4, 4, 2, 2, 2, 2, 2, -2, 1, 1, 6, -6, 1, 1, 4, 4, 1, 1, 3, -3, 3, 3, 4, 4, 6, 6, 6, -6]
	outlength = 15
	starts = [0, 6, 12, 18, 24, 2, 8, 14, 20, 26, 4, 10, 16, 22, 28]
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 2, 4, 6, 9, 10, 13, 14, 16, 18, 21, 22, 24, 26, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_13():
	toptr = [123, 123, 123]
	fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
	outlength = 3
	starts = [0, 5, 9]
	offsets = [0, 5, 9, 12]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_14():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [-4, -6, -7, 6, 4, 6, 2, 1, 3]
	outlength = 5
	starts = [0, 3, 4, -1, 6]
	offsets = [0, 3, 4, 6, 6, 9]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 3, 4, -1, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_15():
	toptr = [123, 123, 123, 123]
	fromptr = [-4, -6, -7, 6, -4, -6, -7, 2, 1, 3]
	outlength = 4
	starts = [0, 3, 4, 7]
	offsets = [0, 3, 4, 7, 10]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 3, 6, 8]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_16():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
	outlength = 5
	starts = [0, 3, 6, 9, 11]
	offsets = [0, 3, 6, 9, 11, 12]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 3, 8, 9, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_17():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 2, 2, 1, 6, 1, 4, 1, 3, 3, 4, 6, 6]
	outlength = 5
	starts = [0, 3, 6, 9, 12]
	offsets = [0, 3, 6, 9, 12, 15]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 5, 7, 9, 12]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_18():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, -3, 4, 2, 2, 2, 1, 2, -2, 1, 6, 1, 4, -6, 1, 4, 1, 3, 3, 1, -3, 3, 4, 6, 6, 4, 6, -6]
	outlength = 10
	starts = [0, 6, 12, 18, 24, 3, 9, 15, 21, 27]
	offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 3, 8, 10, 13, 15, 18, 22, 24, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_19():
	toptr = [123]
	fromptr = [6, 3, 2, 1, 2]
	outlength = 1
	starts = [0]
	offsets = [0, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [3]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_20():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6, -3, 2, -6, 1, 4, 4, -2, 1, -3, 6, 2, 1, 4, 3, -6]
	outlength = 6
	starts = [0, 5, 10, 15, 20, 25]
	offsets = [0, 5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [3, 7, 11, 17, 23, 29]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_21():
	toptr = [123, 123, 123]
	fromptr = [3, 2, 6, 1, 4, 4, 2, 1, 3, 6, 2, 1, 4, 3, 6]
	outlength = 3
	starts = [0, 5, 10]
	offsets = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [3, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_22():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 2, 2, 2, 3, 3]
	outlength = 6
	starts = [0, 10, 16, 5, 13, 17]
	offsets = [0, 5, 8, 9, 14, 17, 18]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 5, 8, 9, 14, 17]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3, 999]
	outlength = 8
	starts = [0, 10, 17, -1, 5, 13, 18, 21]
	offsets = [0, 5, 8, 9, 9, 14, 18, 21, 22]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 5, 8, -1, 9, 14, 20, 21]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmin_24():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 999, 1, 1, 1, 1, 999, 1, 2, 2, 2, 999, 2, 2, 2, 3, 999, 999, 3]
	outlength = 6
	starts = [0, 10, 17, 5, 13, 18]
	offsets = [0, 5, 8, 9, 14, 18, 21]
	funcPy = getattr(kernels, 'awkward_reduce_argmin')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 5, 8, 9, 14, 20]
	assert toptr == pytest_toptr


