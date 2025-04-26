import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_shrink_1():
	tocarry = []
	tolargeoffsets = [123]
	tosmalloffsets = [123]
	length = 0
	missing = []
	slicestarts = []
	slicestops = []
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = []
	pytest_tolargeoffsets = [0]
	pytest_tosmalloffsets = [0]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_2():
	tocarry = [123, 123, 123, 123]
	tolargeoffsets = [123, 123]
	tosmalloffsets = [123, 123]
	length = 1
	missing = [0, 0, 0, 0]
	slicestarts = [0]
	slicestops = [4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3]
	pytest_tolargeoffsets = [0, 4]
	pytest_tosmalloffsets = [0, 4]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_3():
	tocarry = [123, 123]
	tolargeoffsets = [123, 123, 123]
	tosmalloffsets = [123, 123, 123]
	length = 2
	missing = [0, 0]
	slicestarts = [0, 2]
	slicestops = [2, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1]
	pytest_tolargeoffsets = [0, 2, 2]
	pytest_tosmalloffsets = [0, 2, 2]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_4():
	tocarry = [123, 123, 123, 123]
	tolargeoffsets = [123, 123, 123, 123]
	tosmalloffsets = [123, 123, 123, 123]
	length = 3
	missing = [0, 0, 0, 0]
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3]
	pytest_tolargeoffsets = [0, 2, 2, 4]
	pytest_tosmalloffsets = [0, 2, 2, 4]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_5():
	tocarry = [123, 123]
	tolargeoffsets = [123, 123, 123, 123]
	tosmalloffsets = [123, 123, 123, 123]
	length = 3
	missing = [-1, 0, -1, 0]
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [1, 3]
	pytest_tolargeoffsets = [0, 2, 2, 4]
	pytest_tosmalloffsets = [0, 1, 1, 2]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_6():
	tocarry = []
	tolargeoffsets = [123, 123, 123, 123, 123]
	tosmalloffsets = [123, 123, 123, 123, 123]
	length = 4
	missing = [-1, -1, -1, -1]
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = []
	pytest_tolargeoffsets = [0, 2, 3, 3, 4]
	pytest_tosmalloffsets = [0, 0, 0, 0, 0]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_7():
	tocarry = [123, 123, 123, 123]
	tolargeoffsets = [123, 123, 123, 123, 123]
	tosmalloffsets = [123, 123, 123, 123, 123]
	length = 4
	missing = [0, 0, 0, 0]
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3]
	pytest_tolargeoffsets = [0, 2, 3, 3, 4]
	pytest_tosmalloffsets = [0, 2, 3, 3, 4]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


def test_awkward_ListArray_getitem_jagged_shrink_8():
	tocarry = [123, 123, 123, 123, 123, 123]
	tolargeoffsets = [123, 123, 123, 123, 123]
	tosmalloffsets = [123, 123, 123, 123, 123]
	length = 4
	missing = [0, 0, 0, 0, 0, 0]
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_shrink')
	funcPy(tocarry = tocarry,tolargeoffsets = tolargeoffsets,tosmalloffsets = tosmalloffsets,length = length,missing = missing,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3, 4, 5]
	pytest_tolargeoffsets = [0, 2, 3, 3, 6]
	pytest_tosmalloffsets = [0, 2, 3, 3, 6]
	assert tocarry == pytest_tocarry
	assert tolargeoffsets == pytest_tolargeoffsets
	assert tosmalloffsets == pytest_tosmalloffsets


