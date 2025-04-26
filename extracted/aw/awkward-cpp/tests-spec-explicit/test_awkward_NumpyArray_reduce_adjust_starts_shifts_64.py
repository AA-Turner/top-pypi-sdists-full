import pytest
import numpy
import kernels

def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_1():
	toptr = []
	toptr = []
	starts = []
	shifts = []
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	starts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	shifts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_3():
	toptr = [123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 0, 0, 0]
	starts = [0, 0, 0, 0, 0, 0]
	shifts = [4, 0, 5, 2, 1, 3]
	outlength = 6
	parents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [4, 4, 4, 4, 4, 4]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_4():
	toptr = [123]
	toptr = [0]
	starts = [-1]
	shifts = [-1]
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 1, 0, 0, 0, 0]
	starts = [8, 7, 6, 5, 4, 3, 2, 1]
	shifts = [1, 2, 3, 4, 5, 6, 7, 8]
	outlength = 8
	parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [-7, -7, -7, -5, -7, -7, -7, -7]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_6():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 1, 0, 0, 0, 0]
	starts = [1, 2, 3, 4, 5, 6, 7, 8]
	shifts = [8, 7, 6, 5, 4, 3, 2, 1]
	outlength = 8
	parents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 5, 2, 6, 6, 6, 7]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [7, 7, 7, 7, 7, 7, 7, 7]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_7():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, 1, 1, 1, 0, 0]
	starts = [-1, -2, -3, -4, -5, -6, -7, -8]
	shifts = [-1, -2, -3, -4, -5, -6, -7, -8]
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 0, 0, -1, -1, -1, 0, 0]
	starts = [-1, -2, -3, -4, -5, -6, -7, -8]
	shifts = [-1, 2, -3, 4, -5, 6, -7, 8]
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [0, 0, 0, -1, -1, -1, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_9():
	toptr = [123, 123, 123, 123, 123, 123]
	toptr = [0, 1, 0, 0, 0, 0]
	starts = [-1, 1, 0, -5, 2, 3]
	shifts = [1, -1, 0, 5, -2, -3]
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [2, 1, 2, 2, 2, 2]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_10():
	toptr = [123, 123, 123]
	toptr = [0, 1, 0]
	starts = [-1, 0, 1]
	shifts = [1, -1, 1]
	outlength = 3
	parents = [0, 0, 2]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [2, 1, 2]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_11():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	toptr = [-1, -1, -1, -1, -1, -1, -1]
	starts = [0, 1, 0, 2, 1, 0, 3]
	shifts = [1, 0, 2, 0, 1, 2, 0]
	outlength = 7
	parents = [0, 0, 0, 2, 2, 3, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [-1, -1, -1, -1, -1, -1, -1]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_12():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	toptr = [0, 1, 0, 0, 1, 1, 0]
	starts = [0, 1, 0, 2, 1, 0, 3]
	shifts = [0, 1, 0, 2, 1, 0, 3]
	outlength = 7
	parents = [0, 0, 0, 2, 2, 3, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,parents = parents)
	pytest_toptr = [0, 2, 0, 0, 2, 2, 0]
	assert toptr == pytest_toptr


