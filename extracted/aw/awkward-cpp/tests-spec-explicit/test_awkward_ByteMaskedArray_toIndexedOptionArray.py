import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_toIndexedOptionArray_1():
	toindex = []
	length = 0
	mask = []
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_toIndexedOptionArray')
	funcPy(toindex = toindex,length = length,mask = mask,validwhen = validwhen)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_ByteMaskedArray_toIndexedOptionArray_2():
	toindex = [123, 123]
	length = 2
	mask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_toIndexedOptionArray')
	funcPy(toindex = toindex,length = length,mask = mask,validwhen = validwhen)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_ByteMaskedArray_toIndexedOptionArray_3():
	toindex = [123, 123, 123, 123]
	length = 4
	mask = [0, 0, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_toIndexedOptionArray')
	funcPy(toindex = toindex,length = length,mask = mask,validwhen = validwhen)
	pytest_toindex = [0, 1, 2, 3]
	assert toindex == pytest_toindex


