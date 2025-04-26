import pytest
import numpy
import kernels

def test_awkward_IndexedArray_numnull_1():
	numnull = [123]
	fromindex = []
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_2():
	numnull = [123]
	fromindex = [1]
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_3():
	numnull = [123]
	fromindex = [-1]
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [1]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_4():
	numnull = [123]
	fromindex = [-1, -1, -1, -1]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [4]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_5():
	numnull = [123]
	fromindex = [0, -1, 2, -1, -1, -1, -1]
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [5]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_6():
	numnull = [123]
	fromindex = [0, 1]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_7():
	numnull = [123]
	fromindex = [0, 1, 2, 3]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_8():
	numnull = [123]
	fromindex = [0, 1, 2, 3, 4, 5, 6]
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_9():
	numnull = [123]
	fromindex = [1, 2]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_10():
	numnull = [123]
	fromindex = [1, 2, 3]
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_11():
	numnull = [123]
	fromindex = [1, 2, 3, 4]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_12():
	numnull = [123]
	fromindex = [2, 3]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_13():
	numnull = [123]
	fromindex = [2, 3, 4]
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_14():
	numnull = [123]
	fromindex = [3, 2, 1, 0]
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_15():
	numnull = [123]
	fromindex = [3, 4]
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_16():
	numnull = [123]
	fromindex = [4, 3, 2, 1, 0]
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_17():
	numnull = [123]
	fromindex = [5, 2, 4, 1, 3, 0]
	lenindex = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_IndexedArray_numnull_18():
	numnull = [123]
	fromindex = [5, 4, 3, 2, 1, 0]
	lenindex = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_numnull')
	funcPy(numnull = numnull,fromindex = fromindex,lenindex = lenindex)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


