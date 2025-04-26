import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_descend_1():
	tooffsets = [123]
	fromstarts = []
	fromstops = []
	sliceouterlen = 0
	slicestarts = []
	slicestops = []
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_descend_2():
	tooffsets = [123, 123]
	fromstarts = [0]
	fromstops = [2]
	sliceouterlen = 1
	slicestarts = [0]
	slicestops = [2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0, 2]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_descend_3():
	tooffsets = []
	fromstarts = [0, 2]
	fromstops = [2, 4]
	sliceouterlen = 2
	slicestarts = [0, 2]
	slicestops = [3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	with pytest.raises(Exception):
		funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)


def test_awkward_ListArray_getitem_jagged_descend_4():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 2]
	fromstops = [2, 4]
	sliceouterlen = 2
	slicestarts = [0, 2]
	slicestops = [2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0, 2, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_descend_5():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 4]
	fromstops = [3, 3, 4, 5]
	sliceouterlen = 4
	slicestarts = [0, 3, 3, 4]
	slicestops = [3, 3, 4, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0, 3, 3, 4, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_descend_6():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceouterlen = 3
	slicestarts = [0, 3, 3]
	slicestops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0, 3, 3, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_descend_7():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 3]
	fromstops = [3, 6]
	sliceouterlen = 2
	slicestarts = [0, 3]
	slicestops = [3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_descend')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tooffsets = [0, 3, 6]
	assert tooffsets == pytest_tooffsets


