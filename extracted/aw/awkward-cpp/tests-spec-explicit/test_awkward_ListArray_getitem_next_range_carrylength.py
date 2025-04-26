import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_range_carrylength_1():
	carrylength = [123]
	fromstarts = []
	fromstops = []
	lenstarts = 0
	start = 0
	stop = 0
	step = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [0]
	assert carrylength == pytest_carrylength


def test_awkward_ListArray_getitem_next_range_carrylength_2():
	carrylength = [123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 0
	stop = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [7]
	assert carrylength == pytest_carrylength


def test_awkward_ListArray_getitem_next_range_carrylength_3():
	carrylength = [123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 7
	stop = 0
	step = -1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [3]
	assert carrylength == pytest_carrylength


def test_awkward_ListArray_getitem_next_range_carrylength_4():
	carrylength = [123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 0
	stop = 2
	step = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [0]
	assert carrylength == pytest_carrylength


def test_awkward_ListArray_getitem_next_range_carrylength_5():
	carrylength = [123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 0
	stop = 6
	step = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [4]
	assert carrylength == pytest_carrylength


def test_awkward_ListArray_getitem_next_range_carrylength_6():
	carrylength = [123]
	fromstarts = [0, 2, 2, 3, 5]
	fromstops = [2, 2, 3, 5, 7]
	lenstarts = 5
	start = 7
	stop = 0
	step = -2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_carrylength')
	funcPy(carrylength = carrylength,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts,start = start,stop = stop,step = step)
	pytest_carrylength = [3]
	assert carrylength == pytest_carrylength


