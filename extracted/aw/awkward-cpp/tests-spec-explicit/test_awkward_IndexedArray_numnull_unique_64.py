import pytest
import numpy
import kernels

def test_awkward_IndexedArray_numnull_unique_64_1():
	toindex = [123, 123, 123, 123, 123]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_unique_64')
	funcPy(toindex = toindex,lenindex = lenindex)
	pytest_toindex = [0, 1, 2, 3, -1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_numnull_unique_64_2():
	toindex = [123, 123, 123]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_unique_64')
	funcPy(toindex = toindex,lenindex = lenindex)
	pytest_toindex = [0, 1, -1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_numnull_unique_64_3():
	toindex = [123]
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_unique_64')
	funcPy(toindex = toindex,lenindex = lenindex)
	pytest_toindex = [-1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_numnull_unique_64_4():
	toindex = [123, 123, 123, 123]
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_unique_64')
	funcPy(toindex = toindex,lenindex = lenindex)
	pytest_toindex = [0, 1, 2, -1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_numnull_unique_64_5():
	toindex = [123, 123]
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_unique_64')
	funcPy(toindex = toindex,lenindex = lenindex)
	pytest_toindex = [0, -1]
	assert toindex == pytest_toindex


