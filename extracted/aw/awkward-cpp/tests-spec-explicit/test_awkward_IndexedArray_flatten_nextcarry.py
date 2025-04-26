import pytest
import numpy
import kernels

def test_awkward_IndexedArray_flatten_nextcarry_1():
	tocarry = []
	fromindex = []
	lencontent = 0
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_flatten_nextcarry_2():
	tocarry = []
	fromindex = [0, 1]
	lencontent = 0
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_nextcarry')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_flatten_nextcarry_3():
	tocarry = [123, 123]
	fromindex = [0, 2]
	lencontent = 2
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_nextcarry')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_flatten_nextcarry_4():
	tocarry = [123, 123]
	fromindex = [0, 1]
	lencontent = 2
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


