import pytest
import numpy
import kernels

def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_1():
	nextshifts = []
	index = []
	length = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = []
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_2():
	nextshifts = [123, 123, 123, 123, 123]
	index = [0, 1, 2, -1, 3, -1, 4]
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 0, 1, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_3():
	nextshifts = [123, 123, 123, 123, 123]
	index = [0, 1, 2, -1, -1, -1, -1, 7, 8]
	length = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 0, 4, 4]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_4():
	nextshifts = [123, 123, 123, 123]
	index = [0, 1, -1, 2, 3, -1]
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 1, 1]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_5():
	nextshifts = [123, 123, 123, 123, 123]
	index = [0, 1, -1, 2, 3, 4]
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 1, 1, 1]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_6():
	nextshifts = [123, 123, 123, 123, 123]
	index = [0, 1, -1, 2, 3, -1, 4]
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 1, 1, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_7():
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123]
	index = [0, 1, -1, 2, 3, -1, 4, 5, -1, 6, 7, -1]
	length = 12
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 1, 1, 2, 2, 3, 3]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_8():
	nextshifts = [123, 123, 123]
	index = [0, 1, -1, -1, 4]
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_9():
	nextshifts = [123, 123, 123, 123, 123]
	index = [4, 2, -1, -1, 1, 0, 1]
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [0, 0, 2, 2, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_10():
	nextshifts = [123, 123, 123]
	index = [-1, -1, 0, 1, 2]
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [2, 2, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64_11():
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	index = [-1, -1, 0, 1, 2, -1, -1, -1, 3, -1, 4, 5, -1, -1, 6, 7, 8]
	length = 17
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length)
	pytest_nextshifts = [2, 2, 2, 5, 6, 6, 8, 8, 8]
	assert nextshifts == pytest_nextshifts


