import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_next_array_advanced_1():
	toadvanced = []
	tocarry = []
	fromadvanced = []
	fromarray = []
	length = 0
	size = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = []
	pytest_tocarry = []
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_2():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, 0, 1]
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 3, 4, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_3():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 0, 0, 0]
	length = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 3, 6, 9]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_4():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, 2, 1]
	length = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 4, 8, 10]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_5():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 0, 0, 0]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 5, 10, 15]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_6():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, 4, 1]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 6, 14, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_7():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 1, 0]
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 2, 5, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_8():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	length = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 3, 6, 10]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_9():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 5, 10, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_10():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 3, 0, 4]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 8, 10, 19]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_11():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [2, 0, 0, 1]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 5, 10, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_12():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [2, 2, 2, 2]
	length = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 5, 8, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_13():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [2, 2, 2, 2]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 7, 12, 17]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_14():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [3, 3, 3, 3]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 8, 13, 18]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_advanced_15():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [4, 4, 4, 4]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 9, 14, 19]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


