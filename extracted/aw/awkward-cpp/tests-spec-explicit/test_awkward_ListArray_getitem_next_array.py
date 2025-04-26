import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_array_1():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [-3, 0, 1, 1]
	fromstarts = [0]
	fromstops = [2]
	lenarray = 4
	lencontent = 3
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_2():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 3]
	fromstarts = [5, 4, 8]
	fromstops = [4, 8, 12]
	lenarray = 2
	lencontent = 13
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_3():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 3]
	fromstarts = [4, 8]
	fromstops = [8, 14]
	lenarray = 2
	lencontent = 13
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_4():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 0, 1, 1]
	fromstarts = [0]
	fromstops = [2]
	lenarray = 4
	lencontent = 3
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 0, 1, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_5():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 3]
	fromstarts = [0, 4, 8]
	fromstops = [4, 8, 12]
	lenarray = 2
	lencontent = 13
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 0, 1, 0, 1]
	pytest_tocarry = [0, 3, 4, 7, 8, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_6():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [1, 1, 0, 0]
	fromstarts = [0]
	fromstops = [2]
	lenarray = 4
	lencontent = 3
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 1, 0, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_7():
	toadvanced = []
	tocarry = []
	fromarray = []
	fromstarts = []
	fromstops = []
	lenarray = 0
	lencontent = 0
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = []
	pytest_tocarry = []
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_8():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 3]
	fromstarts = [4, 8]
	fromstops = [8, 12]
	lenarray = 2
	lencontent = 13
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 0, 1]
	pytest_tocarry = [4, 7, 8, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_9():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 1, 1, 0]
	fromstarts = [6]
	fromstops = [10]
	lenarray = 4
	lencontent = 10
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lenarray = lenarray,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [8, 7, 7, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


