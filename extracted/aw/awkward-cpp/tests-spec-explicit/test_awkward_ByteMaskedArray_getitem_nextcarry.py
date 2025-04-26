import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_getitem_nextcarry_1():
	tocarry = []
	length = 0
	mask = []
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_ByteMaskedArray_getitem_nextcarry_2():
	tocarry = [123, 123]
	length = 2
	mask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_ByteMaskedArray_getitem_nextcarry_3():
	tocarry = [123, 123, 123]
	length = 5
	mask = [0, 0, 1, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,length = length,mask = mask,validwhen = validwhen)
	pytest_tocarry = [0, 1, 4]
	assert tocarry == pytest_tocarry


