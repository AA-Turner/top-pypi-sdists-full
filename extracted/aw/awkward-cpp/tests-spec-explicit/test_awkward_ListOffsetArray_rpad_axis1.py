import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_rpad_axis1_1():
	toindex = []
	fromoffsets = []
	fromlength = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_2():
	toindex = [123, 123]
	fromoffsets = [0, 0]
	fromlength = 1
	target = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [-1, -1]
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_3():
	toindex = [123, 123, 123]
	fromoffsets = [1, 3]
	fromlength = 1
	target = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [1, 2, -1]
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_4():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 5, 7, 11]
	fromlength = 6
	target = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [0, -1, -1, 1, -1, -1, 2, -1, -1, 3, 4, -1, 5, 6, -1, 7, 8, 9, 10]
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_5():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 5, 7, 11]
	fromlength = 6
	target = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [0, -1, 1, -1, 2, -1, 3, 4, 5, 6, 7, 8, 9, 10]
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_6():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 5, 7, 11]
	fromlength = 6
	target = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	assert toindex == pytest_toindex


def test_awkward_ListOffsetArray_rpad_axis1_7():
	toindex = [123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 4]
	fromlength = 4
	target = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_rpad_axis1')
	funcPy(toindex = toindex,fromoffsets = fromoffsets,fromlength = fromlength,target = target)
	pytest_toindex = [0, 1, 2, 3]
	assert toindex == pytest_toindex


