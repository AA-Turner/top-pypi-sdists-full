import pytest
import numpy
import kernels

def test_awkward_RegularArray_rpad_and_clip_axis1_1():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 3
	size = 0
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [-1, -1, -1, -1, -1, -1]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_2():
	toindex = []
	length = 0
	size = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_3():
	toindex = []
	length = 0
	size = 0
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_4():
	toindex = []
	length = 0
	size = 2
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_5():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 3
	size = 2
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 1, 2, 3, 4, 5]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_6():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 2
	size = 3
	target = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 1, 2, 3, 4, 5]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_7():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	size = 3
	target = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_8():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 3
	size = 3
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 1, 3, 4, 6, 7]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_9():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	size = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 1, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_10():
	toindex = [123, 123, 123]
	length = 3
	size = 2
	target = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 2, 4]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_rpad_and_clip_axis1_11():
	toindex = [123, 123, 123]
	length = 3
	size = 3
	target = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_rpad_and_clip_axis1')
	funcPy(toindex = toindex,length = length,size = size,target = target)
	pytest_toindex = [0, 3, 6]
	assert toindex == pytest_toindex


