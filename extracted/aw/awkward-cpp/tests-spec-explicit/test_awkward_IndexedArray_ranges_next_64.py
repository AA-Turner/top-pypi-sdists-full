import pytest
import numpy
import kernels

def test_awkward_IndexedArray_ranges_next_64_1():
	tostarts = []
	tostops = []
	tolength = [123]
	index = []
	fromstarts = []
	fromstops = []
	length = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = []
	pytest_tostops = []
	pytest_tolength = [0]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_2():
	tostarts = [123]
	tostops = [123]
	tolength = [123]
	index = [-1]
	fromstarts = [0]
	fromstops = [1]
	length = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0]
	pytest_tostops = [0]
	pytest_tolength = [0]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_3():
	tostarts = [123]
	tostops = [123]
	tolength = [123]
	index = [0, 1]
	fromstarts = [0]
	fromstops = [2]
	length = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0]
	pytest_tostops = [2]
	pytest_tolength = [2]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_4():
	tostarts = [123, 123]
	tostops = [123, 123]
	tolength = [123]
	index = [0, 1, 2]
	fromstarts = [0, 2]
	fromstops = [2, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0, 2]
	pytest_tostops = [2, 3]
	pytest_tolength = [3]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_5():
	tostarts = [123, 123]
	tostops = [123, 123]
	tolength = [123]
	index = [-1, -1, -1]
	fromstarts = [0, 2]
	fromstops = [2, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0, 0]
	pytest_tostops = [0, 0]
	pytest_tolength = [0]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_6():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	tolength = [123]
	index = [0, -1, 1, -1, 2]
	fromstarts = [0, 2, 3]
	fromstops = [2, 3, 5]
	length = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0, 1, 2]
	pytest_tostops = [1, 2, 3]
	pytest_tolength = [3]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_ranges_next_64_7():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	tolength = [123]
	index = [3, -1, -1, 2, 1, 0, -1]
	fromstarts = [0, 1, 2, 3, 5]
	fromstops = [1, 2, 3, 5, 7]
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_next_64')
	funcPy(tostarts = tostarts,tostops = tostops,tolength = tolength,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tostarts = [0, 1, 1, 1, 3]
	pytest_tostops = [1, 1, 1, 3, 4]
	pytest_tolength = [4]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops
	assert tolength == pytest_tolength


