import pytest
import numpy
import kernels

def test_awkward_index_rpad_and_clip_axis1_1():
	tostarts = []
	tostops = []
	length = 0
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = []
	pytest_tostops = []
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_2():
	tostarts = [123, 123, 123, 123]
	tostops = [123, 123, 123, 123]
	length = 4
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 1, 2, 3]
	pytest_tostops = [1, 2, 3, 4]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_3():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	length = 5
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 1, 2, 3, 4]
	pytest_tostops = [1, 2, 3, 4, 5]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_4():
	tostarts = [123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 1
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 1, 2, 3, 4, 5]
	pytest_tostops = [1, 2, 3, 4, 5, 6]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_5():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	length = 3
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 2, 4]
	pytest_tostops = [2, 4, 6]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_6():
	tostarts = [123, 123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123, 123]
	length = 7
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 2, 4, 6, 8, 10, 12]
	pytest_tostops = [2, 4, 6, 8, 10, 12, 14]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_7():
	tostarts = [123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 2, 4, 6, 8, 10]
	pytest_tostops = [2, 4, 6, 8, 10, 12]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_8():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	length = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 2, 4, 6, 8]
	pytest_tostops = [2, 4, 6, 8, 10]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_9():
	tostarts = [123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 3
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 3, 6, 9, 12, 15]
	pytest_tostops = [3, 6, 9, 12, 15, 18]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_10():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	length = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 3, 6, 9, 12]
	pytest_tostops = [3, 6, 9, 12, 15]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_11():
	tostarts = [123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 4
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 4, 8, 12, 16, 20]
	pytest_tostops = [4, 8, 12, 16, 20, 24]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_12():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	length = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 4, 8, 12, 16]
	pytest_tostops = [4, 8, 12, 16, 20]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_13():
	tostarts = [123, 123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123, 123]
	length = 6
	target = 5
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 5, 10, 15, 20, 25]
	pytest_tostops = [5, 10, 15, 20, 25, 30]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_index_rpad_and_clip_axis1_14():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	length = 5
	target = 5
	funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1')
	funcPy(tostarts = tostarts,tostops = tostops,length = length,target = target)
	pytest_tostarts = [0, 5, 10, 15, 20]
	pytest_tostops = [5, 10, 15, 20, 25]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


