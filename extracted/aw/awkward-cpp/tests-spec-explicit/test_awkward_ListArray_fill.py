import pytest
import numpy
import kernels

def test_awkward_ListArray_fill_1():
	tostarts = []
	tostops = []
	base = 0
	fromstarts = []
	fromstops = []
	length = 0
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = []
	pytest_tostops = []
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_2():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 0, 1]
	fromstops = [0, 1, 3]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 0, 1]
	pytest_tostops = [0, 1, 3]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_3():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 2, 2]
	fromstops = [2, 2, 4]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 2, 2]
	pytest_tostops = [2, 2, 4]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_4():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 2, 4]
	fromstops = [2, 4, 6]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 2, 4]
	pytest_tostops = [2, 4, 6]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_5():
	tostarts = [123, 123, 123, 123, 123]
	tostops = [123, 123, 123, 123, 123]
	base = 0
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 10]
	length = 5
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 3, 3, 5, 6]
	pytest_tostops = [3, 3, 5, 6, 10]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_6():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 3, 3]
	pytest_tostops = [3, 3, 5]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_7():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 3, 6]
	fromstops = [3, 6, 11]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 3, 6]
	pytest_tostops = [3, 6, 11]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_8():
	tostarts = [123, 123, 123]
	tostops = [123, 123, 123]
	base = 0
	fromstarts = [0, 5, 10]
	fromstops = [5, 10, 15]
	length = 3
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 5, 10]
	pytest_tostops = [5, 10, 15]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_9():
	tostarts = [123, 123]
	tostops = [123, 123]
	base = 0
	fromstarts = [0, 7]
	fromstops = [7, 14]
	length = 2
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [0, 7]
	pytest_tostops = [7, 14]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_10():
	tostarts = [123, 123, 123, 123]
	tostops = [123, 123, 123, 123]
	base = 0
	fromstarts = [1, 3, 3, 3]
	fromstops = [3, 3, 3, 5]
	length = 4
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [1, 3, 3, 3]
	pytest_tostops = [3, 3, 3, 5]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


def test_awkward_ListArray_fill_11():
	tostarts = [123, 123]
	tostops = [123, 123]
	base = 0
	fromstarts = [3, 5]
	fromstops = [5, 5]
	length = 2
	tostartsoffset = 0
	tostopsoffset = 0
	funcPy = getattr(kernels, 'awkward_ListArray_fill')
	funcPy(tostarts = tostarts,tostops = tostops,base = base,fromstarts = fromstarts,fromstops = fromstops,length = length,tostartsoffset = tostartsoffset,tostopsoffset = tostopsoffset)
	pytest_tostarts = [3, 5]
	pytest_tostops = [5, 5]
	assert tostarts == pytest_tostarts
	assert tostops == pytest_tostops


