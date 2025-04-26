import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_range_1():
	tooffsets = [123]
	tocarry = []
	fromstarts = []
	fromstops = []
	lenstarts = 0
	start = 0
	stop = 0
	step = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0]
	pytest_tocarry = []
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_2():
	tooffsets = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 0
	stop = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 2, 2, 3, 5, 7]
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_3():
	tooffsets = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 7
	stop = 0
	step = -1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 1, 1, 1, 2, 3]
	pytest_tocarry = [1, 4, 6]
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_4():
	tooffsets = [123, 123, 123, 123, 123, 123]
	tocarry = []
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 0
	stop = 2
	step = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 0, 0, 0, 0, 0]
	pytest_tocarry = []
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_5():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 5, 7, 9]
	fromstops = [3, 3, 5, 7, 9, 11]
	lenstarts = 6
	start = 0
	stop = 6
	step = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 2, 2, 3, 4, 5, 6]
	pytest_tocarry = [0, 2, 3, 5, 7, 9]
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_6():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	tocarry = [123]
	fromstarts = [0, 3, 3, 5, 7, 9]
	fromstops = [3, 3, 5, 7, 9, 11]
	lenstarts = 6
	start = 2
	stop = 6
	step = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 1, 1, 1, 1, 1, 1]
	pytest_tocarry = [2]
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_7():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	tocarry = []
	fromstarts = [0, 3, 3, 5, 7, 9]
	fromstops = [3, 3, 5, 7, 9, 11]
	lenstarts = 6
	start = 6
	stop = 2
	step = -2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 0, 0, 0, 0, 0, 0]
	pytest_tocarry = []
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_8():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	tocarry = []
	fromstarts = [0, 3, 3, 5, 7, 9]
	fromstops = [3, 3, 5, 7, 9, 11]
	lenstarts = 6
	start = 0
	stop = 6
	step = -2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 0, 0, 0, 0, 0, 0]
	pytest_tocarry = []
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_range_9():
	tooffsets = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 7
	stop = 0
	step = -2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range')
	funcPy(tooffsets = tooffsets,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_tooffsets = [0, 1, 1, 1, 2, 3]
	pytest_tocarry = [1, 4, 6]
	assert tooffsets == pytest_tooffsets
	assert tocarry == pytest_tocarry


