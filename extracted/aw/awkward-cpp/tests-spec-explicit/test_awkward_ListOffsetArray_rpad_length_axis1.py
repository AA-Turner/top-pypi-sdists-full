import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_rpad_length_axis1_1():
	tolength = [123]
	tooffsets = [123]
	fromoffsets = []
	fromlength = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_length_axis1')
	funcPy(tolength = tolength,tooffsets = tooffsets,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_tolength = [0]
	pytest_tooffsets = [0]
	assert tolength == pytest_tolength
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_rpad_length_axis1_2():
	tolength = [123]
	tooffsets = [123, 123]
	fromoffsets = [0, 0]
	fromlength = 1
	target = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_length_axis1')
	funcPy(tolength = tolength,tooffsets = tooffsets,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_tolength = [3]
	pytest_tooffsets = [0, 3]
	assert tolength == pytest_tolength
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_rpad_length_axis1_3():
	tolength = [123]
	tooffsets = [123, 123]
	fromoffsets = [1, 3]
	fromlength = 1
	target = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_length_axis1')
	funcPy(tolength = tolength,tooffsets = tooffsets,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_tolength = [3]
	pytest_tooffsets = [0, 3]
	assert tolength == pytest_tolength
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_rpad_length_axis1_4():
	tolength = [123]
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 5, 7, 11]
	fromlength = 6
	target = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_length_axis1')
	funcPy(tolength = tolength,tooffsets = tooffsets,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_tolength = [19]
	pytest_tooffsets = [0, 3, 6, 9, 12, 15, 19]
	assert tolength == pytest_tolength
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_rpad_length_axis1_5():
	tolength = [123]
	tooffsets = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 4]
	fromlength = 4
	target = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_length_axis1')
	funcPy(tolength = tolength,tooffsets = tooffsets,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_tolength = [4]
	pytest_tooffsets = [0, 1, 2, 3, 4]
	assert tolength == pytest_tolength
	assert tooffsets == pytest_tooffsets


