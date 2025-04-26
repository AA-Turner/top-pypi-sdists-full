import pytest
import numpy
import kernels

def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_1():
	nextshifts = []
	index = []
	length = 0
	shifts = []
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = []
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_2():
	nextshifts = [123, 123, 123, 123, 123, 123]
	index = [0, 3, 4, 1, -1, 5, 2]
	length = 7
	shifts = [0, 0, 1, 0, 0, 1, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = [0, 0, 1, 0, 2, 1]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_3():
	nextshifts = [123, 123, 123, 123, 123, 123]
	index = [0, 3, 4, 1, -1, 5, 2]
	length = 7
	shifts = [0, 1, 1, 0, 1, 1, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = [0, 1, 1, 0, 2, 1]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_4():
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	index = [0, -1, 3, 5, 6, 1, -1, 4, -1, 7, 2, -1, -1, -1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
	length = 25
	shifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = [0, 1, 1, 1, 1, 2, 3, 3, 6]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_5():
	nextshifts = [123, 123, 123, 123, 123, 123]
	index = [0, -1, 4, 1, 3, 5, 2]
	length = 7
	shifts = [0, 1, 1, 0, 1, 1, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = [0, 2, 1, 2, 2, 1]
	assert nextshifts == pytest_nextshifts


def test_awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64_6():
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	index = [-1, -1, 3, 5, 6, -1, -1, -1, -1, 7, 0, -1, 4, -1, 8, 1, 2]
	length = 17
	shifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_nonlocal_nextshifts_fromshifts_64')
	funcPy(nextshifts = nextshifts,index = index,length = length,shifts = shifts)
	pytest_nextshifts = [2, 2, 2, 6, 6, 7, 8, 8, 8]
	assert nextshifts == pytest_nextshifts


