import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_getitem_nextcarry_outindex_1():
	outindex = []
	tocarry = []
	length = 0
	mask = []
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex')
	funcPy(outindex = outindex,tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_outindex = []
	pytest_tocarry = []
	assert outindex == pytest_outindex
	assert tocarry == pytest_tocarry


def test_awkward_ByteMaskedArray_getitem_nextcarry_outindex_2():
	outindex = [123]
	tocarry = [123]
	length = 1
	mask = [0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex')
	funcPy(outindex = outindex,tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_outindex = [-1]
	pytest_tocarry = [123]
	assert outindex == pytest_outindex
	assert tocarry == pytest_tocarry


def test_awkward_ByteMaskedArray_getitem_nextcarry_outindex_3():
	outindex = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	length = 4
	mask = [0, 0, 0, 0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex')
	funcPy(outindex = outindex,tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_outindex = [-1, -1, -1, -1]
	pytest_tocarry = [123, 123, 123, 123]
	assert outindex == pytest_outindex
	assert tocarry == pytest_tocarry


