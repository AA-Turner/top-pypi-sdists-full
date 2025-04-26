import pytest
import numpy
import kernels

def test_awkward_BitMaskedArray_to_IndexedOptionArray_1():
	toindex = []
	bitmasklength = 0
	frombitmask = []
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_2():
	toindex = []
	bitmasklength = 0
	frombitmask = []
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 1
	frombitmask = [66]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, -1, 2, 3, 4, 5, -1, 7]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_4():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, -1, 2, -1, -1, -1, 6, 7, -1, -1, 10, -1, -1, -1, 14, 15]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_5():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, -1, -1, -1, 5, -1, 7, 8, 9, -1, -1, -1, 13, -1, -1]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_6():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 1
	frombitmask = [27]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, 2, -1, -1, 5, -1, -1]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_7():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 3
	frombitmask = [1, 1, 1]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6, -1, 8, 9, 10, 11, 12, 13, 14, -1, 16, 17, 18, 19, 20, 21, 22, -1]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_8():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 3
	frombitmask = [1, 1, 1]
	lsb_order = False
	validwhen = True
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [-1, -1, -1, -1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, 23]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_9():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 4
	frombitmask = [0, 0, 0, 0]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_10():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 4
	frombitmask = [0, 0, 0, 0]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
	assert toindex == pytest_toindex


