import pytest
import numpy
import kernels

def test_awkward_ListArray_rpad_and_clip_length_axis1_1():
	tomin = [123]
	fromstarts = []
	fromstops = []
	lenstarts = 0
	target = 1
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [0]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_2():
	tomin = [123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lenstarts = 5
	target = 1
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [10]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_3():
	tomin = [123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	lenstarts = 4
	target = 1
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [10]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_4():
	tomin = [123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lenstarts = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [12]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_5():
	tomin = [123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	lenstarts = 4
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [13]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_6():
	tomin = [123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	lenstarts = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [13]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_7():
	tomin = [123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lenstarts = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [15]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_8():
	tomin = [123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	lenstarts = 4
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [16]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_9():
	tomin = [123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	lenstarts = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [16]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_10():
	tomin = [123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lenstarts = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [20]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_11():
	tomin = [123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	lenstarts = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [20]
	assert tomin == pytest_tomin


def test_awkward_ListArray_rpad_and_clip_length_axis1_12():
	tomin = [123]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 7]
	lenstarts = 3
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_and_clip_length_axis1')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,target = target)
	pytest_tomin = [9]
	assert tomin == pytest_tomin


