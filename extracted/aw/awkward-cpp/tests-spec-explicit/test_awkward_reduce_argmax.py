import pytest
import numpy
import kernels

def test_awkward_reduce_argmax_1():
	toptr = []
	fromptr = []
	outlength = 0
	starts = []
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_2():
	toptr = [123, 123, 123]
	fromptr = [1, -1, 1, -1, 1, 21]
	outlength = 3
	starts = [0, 1, 3]
	offsets = [0, 1, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 2, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_3():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 4, 6, 7]
	outlength = 3
	starts = [0, 1, 3, 6]
	offsets = [0, 1, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 2, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_4():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [6, 1, 10, 33, -1, 21, 2, 45, 4]
	outlength = 5
	starts = [0, 2, 4, 5, 7]
	offsets = [0, 2, 4, 5, 7, 9]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [0, 3, 4, 5, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_5():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 4, 6]
	outlength = 3
	starts = [0, 2, 3, 5]
	offsets = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 2, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_6():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [3, 4, 2, 1, 2, 3, 6, 1, -1, 1, 7, 4]
	outlength = 5
	starts = [0, 3, 6, 9, 11]
	offsets = [0, 3, 6, 9, 11, 12]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [1, 5, 6, 10, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_7():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	starts = [0]
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_8():
	toptr = [123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 6]
	outlength = 3
	starts = [0, 3, 5]
	offsets = [0, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 4, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_9():
	toptr = [123, 123, 123]
	fromptr = [3, 1, 6, 1, 4, 4, 2, 1, 7, 2, 3, -1]
	outlength = 3
	starts = [0, 5, 9]
	offsets = [0, 5, 9, 12]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [2, 8, 10]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_10():
	toptr = [123]
	fromptr = [0, 0, 4, 4, 6]
	outlength = 1
	starts = [0]
	offsets = [0, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_11():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 6]
	outlength = 1
	starts = [0]
	offsets = [0, 5]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [4]
	assert toptr == pytest_toptr


def test_awkward_reduce_argmax_12():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	starts = [0]
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_argmax')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,starts = starts,offsets = offsets)
	pytest_toptr = [5]
	assert toptr == pytest_toptr


