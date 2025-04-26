import pytest
import numpy
import kernels

def test_awkward_ListArray_rpad_axis1_1():
	toindex = []
	tostarts = []
	tostops = []
	fromstarts = []
	fromstops = []
	length = 0
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = []
	pytest_tostarts = []
	pytest_tostops = []
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_2():
	toindex = []
	tostarts = []
	tostops = []
	fromstarts = []
	fromstops = []
	length = 0
	target = 0
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = []
	pytest_tostarts = []
	pytest_tostops = []
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	target = 0
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, 4, 5, 5, 6, 7, 8, 123, 123]
	pytest_tostarts = [0, 3, 3, 5, 8]
	pytest_tostops = [3, 3, 5, 8, 9]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_4():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, -1, -1, -1, -1, -1, 4, 5, -1, -1, 5, 6, 7, -1, 8, -1, -1, -1]
	pytest_tostarts = [0, 4, 8, 12, 16]
	pytest_tostops = [4, 8, 12, 16, 20]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_5():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, -1, -1, -1, 4, 5, -1, 5, 6, 7, 8, -1, -1]
	pytest_tostarts = [0, 3, 6, 9, 12]
	pytest_tostops = [3, 6, 9, 12, 15]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_6():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 7]
	length = 3
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, -1, -1, -1, 5, 6, -1]
	pytest_tostarts = [0, 3, 6]
	pytest_tostops = [3, 6, 9]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_7():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, -1, -1, 4, 5, 5, 6, 7, 8, -1]
	pytest_tostarts = [0, 3, 5, 7, 10]
	pytest_tostops = [3, 5, 7, 10, 12]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_8():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	target = 1
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [0, 1, 2, -1, 4, 5, 5, 6, 7, 8]
	pytest_tostarts = [0, 3, 4, 6, 9]
	pytest_tostops = [3, 4, 6, 9, 10]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_9():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123]
	tostops = [123, 123, 123, 123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	length = 4
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, -1, -1, -1, 3, 4, -1, -1, 0, 1, 2, -1]
	pytest_tostarts = [0, 4, 8, 12]
	pytest_tostops = [4, 8, 12, 16]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_10():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	length = 5
	target = 4
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, -1, -1, -1, 3, 4, -1, -1, -1, -1, -1, -1, 0, 1, 2, -1]
	pytest_tostarts = [0, 4, 8, 12, 16]
	pytest_tostops = [4, 8, 12, 16, 20]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_11():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123]
	tostops = [123, 123, 123, 123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	length = 4
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, -1, -1, 3, 4, -1, 0, 1, 2]
	pytest_tostarts = [0, 4, 7, 10]
	pytest_tostops = [4, 7, 10, 13]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_12():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	length = 5
	target = 3
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, -1, -1, 3, 4, -1, -1, -1, -1, 0, 1, 2]
	pytest_tostarts = [0, 4, 7, 10, 13]
	pytest_tostops = [4, 7, 10, 13, 16]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_13():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	length = 5
	target = 2
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, -1, 3, 4, -1, -1, 0, 1, 2]
	pytest_tostarts = [0, 4, 6, 8, 10]
	pytest_tostops = [4, 6, 8, 10, 13]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_rpad_axis1_14():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tostarts = [123, 123, 123, 123]
	tostops = [123, 123, 123, 123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	length = 4
	target = 1
	funcPy = getattr(kernels, 'awkward_ListArray_rpad_axis1')
	funcPy(toindex = toindex,tostarts = tostarts,tostops = tostops,fromstarts = fromstarts,fromstops = fromstops,length = length,target = target)
	pytest_toindex = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
	pytest_tostarts = [0, 4, 5, 7]
	pytest_tostops = [4, 5, 7, 10]
	assert toindex == pytest_toindex
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


