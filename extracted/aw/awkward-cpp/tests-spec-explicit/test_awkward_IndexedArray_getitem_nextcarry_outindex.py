import pytest
import numpy
import kernels

def test_awkward_IndexedArray_getitem_nextcarry_outindex_1():
	tocarry = []
	toindex = []
	fromindex = []
	lencontent = 0
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry_outindex')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = []
	pytest_toindex = []
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_getitem_nextcarry_outindex_2():
	tocarry = []
	toindex = []
	fromindex = [0, 1, 2, 4]
	lencontent = 0
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry_outindex')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_getitem_nextcarry_outindex_3():
	tocarry = [123, 123, 123, 123]
	toindex = [123, 123, 123, 123]
	fromindex = [0, 1, 2, 4]
	lencontent = 4
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry_outindex')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_getitem_nextcarry_outindex_4():
	tocarry = [123, 123, 123, 123]
	toindex = [123, 123, 123, 123]
	fromindex = [0, 1, 2, 3]
	lencontent = 4
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry_outindex')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1, 2, 3]
	pytest_toindex = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_getitem_nextcarry_outindex_5():
	tocarry = [123, 123, 123, 123]
	toindex = [123, 123, 123, 123]
	fromindex = [3, 2, 1, 0]
	lencontent = 4
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry_outindex')
	funcPy(tocarry = tocarry,toindex = toindex,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [3, 2, 1, 0]
	pytest_toindex = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry
	assert toindex == pytest_toindex


