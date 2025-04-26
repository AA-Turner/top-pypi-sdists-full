import pytest
import numpy
import kernels

def test_awkward_index_rpad_and_clip_axis0_1():
	toindex = []
	length = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_2():
	toindex = [123, 123]
	length = 2
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_3():
	toindex = [123, 123]
	length = 3
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_4():
	toindex = [123, 123, 123]
	length = 3
	target = 3
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_5():
	toindex = [123, 123, 123, 123]
	length = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_6():
	toindex = [123, 123, 123, 123, 123]
	length = 5
	target = 5
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_7():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 6
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2, 3, 4, 5]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_8():
	toindex = [123, 123, 123]
	length = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_9():
	toindex = [123, 123, 123]
	length = 6
	target = 3
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_10():
	toindex = [123, 123]
	length = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_11():
	toindex = [123]
	length = 3
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_12():
	toindex = [123]
	length = 5
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


def test_awkward_index_rpad_and_clip_axis0_13():
	toindex = [123]
	length = 6
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis0')
	funcPy(toindex = toindex,length = length,target = target)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


