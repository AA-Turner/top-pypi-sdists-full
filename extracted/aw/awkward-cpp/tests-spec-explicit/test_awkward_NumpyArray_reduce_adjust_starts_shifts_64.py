import pytest
import numpy
import kernels

def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_1():
	toptr = []
	starts = []
	shifts = []
	outlength = 0
	offsets = [0]
	toptr = []
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	starts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	shifts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_3():
	toptr = [123, 123, 123, 123, 123, 123]
	starts = [0, 0, 0, 0, 0, 0]
	shifts = [4, 0, 5, 2, 1, 3]
	outlength = 6
	offsets = [0, 5, 8, 9, 14, 17, 18]
	toptr = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [4, 4, 4, 4, 4, 4]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_4():
	toptr = [123]
	starts = [-1]
	shifts = [-1]
	outlength = 1
	offsets = [0, 5]
	toptr = [0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	starts = [8, 7, 6, 5, 4, 3, 2, 1]
	shifts = [1, 2, 3, 4, 5, 6, 7, 8]
	outlength = 8
	offsets = [0, 5, 8, 9, 9, 14, 18, 21, 22]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [-7, -6, -5, -4, -3, -2, -1, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_6():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	starts = [1, 2, 3, 4, 5, 6, 7, 8]
	shifts = [8, 7, 6, 5, 4, 3, 2, 1]
	outlength = 8
	offsets = [0, 5, 8, 9, 9, 14, 18, 21, 22]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [7, 6, 5, 4, 3, 2, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_7():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	starts = [-1, -2, -3, -4, -5, -6, -7, -8]
	shifts = [-1, -2, -3, -4, -5, -6, -7, -8]
	outlength = 8
	offsets = [0, 3, 5, 5, 5, 5, 5, 7, 8]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 2, 3, 4, 5, 6, 7]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	starts = [-1, -2, -3, -4, -5, -6, -7, -8]
	shifts = [-1, 2, -3, 4, -5, 6, -7, 8]
	outlength = 8
	offsets = [0, 3, 5, 5, 5, 5, 5, 7, 8]
	toptr = [0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 2, 3, 4, 5, 6, 7]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_9():
	toptr = [123, 123, 123, 123, 123, 123]
	starts = [-1, 1, 0, -5, 2, 3]
	shifts = [1, -1, 0, 5, -2, -3]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	toptr = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [2, 0, 1, 6, -1, -2]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_10():
	toptr = [123, 123, 123]
	starts = [-1, 0, 1]
	shifts = [1, -1, 1]
	outlength = 3
	offsets = [0, 2, 2, 3]
	toptr = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [2, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_11():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	starts = [0, 1, 0, 2, 1, 0, 3]
	shifts = [1, 0, 2, 0, 1, 2, 0]
	outlength = 7
	offsets = [0, 3, 3, 5, 6, 6, 6, 9]
	toptr = [0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 0, 1, -1, 0, 1, -2]
	assert toptr == pytest_toptr


def test_awkward_NumpyArray_reduce_adjust_starts_shifts_64_12():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	starts = [0, 1, 0, 2, 1, 0, 3]
	shifts = [0, 1, 0, 2, 1, 0, 3]
	outlength = 7
	offsets = [0, 3, 3, 5, 6, 6, 6, 9]
	toptr = [0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_NumpyArray_reduce_adjust_starts_shifts_64')
	funcPy(toptr = toptr,starts = starts,shifts = shifts,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, -1, 0, -2, -1, 0, -3]
	assert toptr == pytest_toptr


