import pytest
import numpy
import kernels

def test_awkward_IndexedArray_ranges_carry_next_64_1():
	tocarry = []
	index = []
	fromstarts = []
	fromstops = []
	length = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_2():
	tocarry = [123]
	index = [1]
	fromstarts = [0]
	fromstops = [1]
	length = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_3():
	tocarry = []
	index = [-1]
	fromstarts = [0]
	fromstops = [1]
	length = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_4():
	tocarry = []
	index = [-1, -1, -1]
	fromstarts = [0, 2]
	fromstops = [2, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_5():
	tocarry = [123, 123, 123]
	index = [0, 1, 2]
	fromstarts = [0, 2]
	fromstops = [2, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_6():
	tocarry = [123, 123, 123]
	index = [0, -1, 1, -1, 2]
	fromstarts = [0, 2, 3]
	fromstops = [2, 3, 5]
	length = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_ranges_carry_next_64_7():
	tocarry = [123, 123, 123, 123]
	index = [3, -1, -1, 2, 1, 0, -1]
	fromstarts = [0, 1, 2, 3, 5]
	fromstops = [1, 2, 3, 5, 7]
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_ranges_carry_next_64')
	funcPy(tocarry = tocarry,index = index,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tocarry = [3, 2, 1, 0]
	assert tocarry == pytest_tocarry


