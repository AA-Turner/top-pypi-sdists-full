import pytest
import numpy
import kernels

def test_awkward_IndexedArray_numnull_parents_1():
	numnull = []
	tolength = [123]
	fromindex = []
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = []
	pytest_tolength = [0]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_2():
	numnull = [123]
	tolength = [123]
	fromindex = [1]
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	pytest_tolength = [0]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_3():
	numnull = [123]
	tolength = [123]
	fromindex = [-1]
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [1]
	pytest_tolength = [1]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_4():
	numnull = [123, 123, 123, 123]
	tolength = [123]
	fromindex = [-1, -1, -1, -1]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [1, 1, 1, 1]
	pytest_tolength = [4]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_5():
	numnull = [123, 123, 123, 123, 123, 123, 123]
	tolength = [123]
	fromindex = [0, -1, 2, -1, -1, -1, -1]
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0, 1, 0, 1, 1, 1, 1]
	pytest_tolength = [5]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_6():
	numnull = [123, 123]
	tolength = [123]
	fromindex = [0, 1]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0, 0]
	pytest_tolength = [0]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_7():
	numnull = [123, 123, 123, 123]
	tolength = [123]
	fromindex = [0, 1, 2, 3]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0, 0, 0, 0]
	pytest_tolength = [0]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


def test_awkward_IndexedArray_numnull_parents_8():
	numnull = [123, 123, 123, 123, 123, 123, 123]
	tolength = [123]
	fromindex = [0, 1, -2, 3, -4, 5, -6]
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull_parents')
	funcPy(numnull = numnull,tolength = tolength,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0, 0, 1, 0, 1, 0, 1]
	pytest_tolength = [3]
	assert numnull == pytest_numnull
	assert tolength == pytest_tolength


