import pytest
import numpy
import kernels

def test_awkward_IndexedArray_reduce_next_64_1():
	nextcarry = []
	nextparents = []
	outindex = []
	index = []
	length = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = []
	pytest_nextparents = []
	pytest_outindex = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_2():
	nextcarry = [123, 123]
	nextparents = [123, 123]
	outindex = [123, 123]
	index = [0, 1]
	length = 2
	parents = [0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [0, 1]
	pytest_nextparents = [0, 0]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_3():
	nextcarry = [123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123, 123]
	index = [0, 1, 2, 3, 4, 5, 6]
	length = 7
	parents = [0, 0, 2, 2, 3, 4, 4]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [0, 1, 2, 3, 4, 5, 6]
	pytest_nextparents = [0, 0, 2, 2, 3, 4, 4]
	pytest_outindex = [0, 1, 2, 3, 4, 5, 6]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_4():
	nextcarry = [123, 123]
	nextparents = [123, 123]
	outindex = [123, 123]
	index = [1, 2]
	length = 2
	parents = [0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [1, 2]
	pytest_nextparents = [0, 0]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_5():
	nextcarry = [123, 123, 123]
	nextparents = [123, 123, 123]
	outindex = [123, 123, 123]
	index = [1, 2, 3]
	length = 3
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [1, 2, 3]
	pytest_nextparents = [0, 0, 0]
	pytest_outindex = [0, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_6():
	nextcarry = [123, 123, 123, 123]
	nextparents = [123, 123, 123, 123]
	outindex = [123, 123, 123, 123]
	index = [1, 2, 3, 4]
	length = 4
	parents = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [1, 2, 3, 4]
	pytest_nextparents = [0, 0, 0, 0]
	pytest_outindex = [0, 1, 2, 3]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_7():
	nextcarry = [123, 123]
	nextparents = [123, 123]
	outindex = [123, 123]
	index = [2, 3]
	length = 2
	parents = [0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [2, 3]
	pytest_nextparents = [0, 0]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_8():
	nextcarry = [123, 123, 123]
	nextparents = [123, 123, 123]
	outindex = [123, 123, 123]
	index = [2, 3, 4]
	length = 3
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [2, 3, 4]
	pytest_nextparents = [0, 0, 0]
	pytest_outindex = [0, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_9():
	nextcarry = [123, 123]
	nextparents = [123, 123]
	outindex = [123, 123]
	index = [3, 4]
	length = 2
	parents = [0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [3, 4]
	pytest_nextparents = [0, 0]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_10():
	nextcarry = [123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123]
	index = [4, 3, 2, 1, 0]
	length = 5
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [4, 3, 2, 1, 0]
	pytest_nextparents = [0, 0, 0, 0, 0]
	pytest_outindex = [0, 1, 2, 3, 4]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_11():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123]
	index = [5, 2, 4, 1, 3, 0]
	length = 6
	parents = [0, 0, 1, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [5, 2, 4, 1, 3, 0]
	pytest_nextparents = [0, 0, 1, 1, 2, 2]
	pytest_outindex = [0, 1, 2, 3, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_12():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123]
	index = [5, 4, 3, 2, 1, 0]
	length = 6
	parents = [0, 0, 0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,index = index,length = length,parents = parents)
	pytest_nextcarry = [5, 4, 3, 2, 1, 0]
	pytest_nextparents = [0, 0, 0, 1, 1, 1]
	pytest_outindex = [0, 1, 2, 3, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


