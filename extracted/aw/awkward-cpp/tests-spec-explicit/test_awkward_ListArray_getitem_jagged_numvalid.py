import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_numvalid_1():
	numvalid = [123]
	length = 0
	missing = []
	missinglength = 0
	slicestarts = []
	slicestops = []
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [0]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_2():
	numvalid = [123]
	length = 4
	missing = [0, 0, 0, 0]
	missinglength = 4
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [4]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_3():
	numvalid = [123]
	length = 4
	missing = [0, -1, 0, -1, 0, -1, 0]
	missinglength = 7
	slicestarts = [0, 2, 3, 5]
	slicestops = [2, 3, 5, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [4]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_4():
	numvalid = [123]
	length = 4
	missing = [0, 0, 0, 0]
	missinglength = 4
	slicestarts = [0, 0, 0, 0]
	slicestops = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [0]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_5():
	numvalid = [123]
	length = 4
	missing = [0, -1, 0, -1]
	missinglength = 4
	slicestarts = [0, 2, 2, 2]
	slicestops = [2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [1]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_6():
	numvalid = [123]
	length = 4
	missing = [0, -1, 0, -1]
	missinglength = 4
	slicestarts = [0, 1, 2, 3]
	slicestops = [1, 2, 3, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [2]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_7():
	numvalid = [123]
	length = 4
	missing = [0, -1, 0, -1]
	missinglength = 4
	slicestarts = [0, 2, 2, 2]
	slicestops = [2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [1]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_8():
	numvalid = [123]
	length = 4
	missing = [-1, -1, -1, -1]
	missinglength = 4
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [0]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_9():
	numvalid = [123]
	length = 4
	missing = [-1, -1, -1, -1]
	missinglength = 4
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)
	pytest_numvalid = [0]
	assert numvalid == pytest_numvalid


def test_awkward_ListArray_getitem_jagged_numvalid_10():
	numvalid = []
	length = 2
	missing = [0, 0]
	missinglength = 2
	slicestarts = [4, 2]
	slicestops = [2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	with pytest.raises(Exception):
		funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)


def test_awkward_ListArray_getitem_jagged_numvalid_11():
	numvalid = []
	length = 2
	missing = [0]
	missinglength = 1
	slicestarts = [0, 2]
	slicestops = [2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_numvalid')
	with pytest.raises(Exception):
		funcPy(numvalid = numvalid,length = length,missing = missing,missinglength = missinglength,slicestarts = slicestarts,slicestops = slicestops)


