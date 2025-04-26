import pytest
import numpy
import kernels

def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_1():
	nextcarry = []
	nextparents = []
	parents = []
	size = 3
	length = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = []
	pytest_nextparents = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_2():
	nextcarry = []
	nextparents = []
	parents = []
	size = 0
	length = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = []
	pytest_nextparents = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_3():
	nextcarry = []
	nextparents = []
	parents = [0, 1]
	size = 0
	length = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = []
	pytest_nextparents = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_4():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123]
	parents = [0, 1]
	size = 3
	length = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = [0, 3, 1, 4, 2, 5]
	pytest_nextparents = [0, 3, 1, 4, 2, 5]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_5():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	parents = [2, 4, 6]
	size = 3
	length = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = [0, 3, 6, 1, 4, 7, 2, 5, 8]
	pytest_nextparents = [6, 12, 18, 7, 13, 19, 8, 14, 20]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_6():
	nextcarry = [123]
	nextparents = [123]
	parents = [0]
	size = 1
	length = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,parents = parents,size = size,length = length)
	pytest_nextcarry = [0]
	pytest_nextparents = [0]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents


