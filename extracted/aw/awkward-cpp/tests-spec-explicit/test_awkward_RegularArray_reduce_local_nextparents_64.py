import pytest
import numpy
import kernels

def test_awkward_RegularArray_reduce_local_nextparents_64_1():
	nextparents = []
	size = 3
	length = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,size = size,length = length)
	pytest_nextparents = []
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_local_nextparents_64_2():
	nextparents = []
	size = 0
	length = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,size = size,length = length)
	pytest_nextparents = []
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_local_nextparents_64_3():
	nextparents = []
	size = 0
	length = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,size = size,length = length)
	pytest_nextparents = []
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_local_nextparents_64_4():
	nextparents = [123, 123, 123, 123, 123, 123]
	size = 3
	length = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,size = size,length = length)
	pytest_nextparents = [0, 0, 0, 1, 1, 1]
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_local_nextparents_64_5():
	nextparents = [123]
	size = 1
	length = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_local_nextparents_64')
	funcPy(nextparents = nextparents,size = size,length = length)
	pytest_nextparents = [0]
	assert nextparents == pytest_nextparents


