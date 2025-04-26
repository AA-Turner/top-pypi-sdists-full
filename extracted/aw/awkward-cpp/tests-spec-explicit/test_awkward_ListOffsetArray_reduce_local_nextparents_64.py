import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_local_nextparents_64_1():
	nextparents = []
	length = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = []
	assert nextparents == pytest_nextparents


def test_awkward_ListOffsetArray_reduce_local_nextparents_64_2():
	nextparents = [123]
	length = 1
	offsets = [0, 1]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = [0]
	assert nextparents == pytest_nextparents


def test_awkward_ListOffsetArray_reduce_local_nextparents_64_3():
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 18
	offsets = [0, 0, 1, 3, 3, 6, 8, 9, 9, 9, 10, 10, 12, 15, 15, 17, 18, 18, 18]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = [1, 2, 2, 4, 4, 4, 5, 5, 6, 9, 11, 11, 12, 12, 12, 14, 14, 15]
	assert nextparents == pytest_nextparents


def test_awkward_ListOffsetArray_reduce_local_nextparents_64_4():
	nextparents = [123, 123, 123, 123, 123]
	length = 4
	offsets = [0, 1, 3, 5, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = [0, 1, 1, 2, 2]
	assert nextparents == pytest_nextparents


def test_awkward_ListOffsetArray_reduce_local_nextparents_64_5():
	nextparents = [123, 123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 1, 1, 3, 5, 7]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = [0, 2, 2, 3, 3, 4, 4]
	assert nextparents == pytest_nextparents


def test_awkward_ListOffsetArray_reduce_local_nextparents_64_6():
	nextparents = [123, 123]
	length = 5
	offsets = [0, 0, 1, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,length = length,offsets = offsets)
	pytest_nextparents = [1, 3]
	assert nextparents == pytest_nextparents


