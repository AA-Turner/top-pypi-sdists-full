import pytest
import numpy
import kernels

def test_awkward_IndexedArray_reduce_next_64_1():
	nextcarry = []
	nextoffsets = [123]
	outindex = []
	index = []
	offsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0]
	pytest_outindex = []
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_2():
	nextcarry = [123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123]
	index = [0, 1]
	offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [0, 1]
	pytest_nextoffsets = [0, 2]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_3():
	nextcarry = [123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123, 123]
	index = [0, 1, 2, 3, 4, 5, 6]
	offsets = [0, 2, 2, 4, 5, 7]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [0, 1, 2, 3, 4, 5, 6]
	pytest_nextoffsets = [0, 2, 2, 4, 5, 7]
	pytest_outindex = [0, 1, 2, 3, 4, 5, 6]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_4():
	nextcarry = [123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123]
	index = [1, 2]
	offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [1, 2]
	pytest_nextoffsets = [0, 2]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_5():
	nextcarry = [123, 123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123, 123]
	index = [1, 2, 3]
	offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [1, 2, 3]
	pytest_nextoffsets = [0, 3]
	pytest_outindex = [0, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_6():
	nextcarry = [123, 123, 123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123, 123, 123]
	index = [1, 2, 3, 4]
	offsets = [0, 4]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [1, 2, 3, 4]
	pytest_nextoffsets = [0, 4]
	pytest_outindex = [0, 1, 2, 3]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_7():
	nextcarry = [123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123]
	index = [2, 3]
	offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [2, 3]
	pytest_nextoffsets = [0, 2]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_8():
	nextcarry = [123, 123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123, 123]
	index = [2, 3, 4]
	offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [2, 3, 4]
	pytest_nextoffsets = [0, 3]
	pytest_outindex = [0, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_9():
	nextcarry = [123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123]
	index = [3, 4]
	offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [3, 4]
	pytest_nextoffsets = [0, 2]
	pytest_outindex = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_10():
	nextcarry = [123, 123, 123, 123, 123]
	nextoffsets = [123, 123]
	outindex = [123, 123, 123, 123, 123]
	index = [4, 3, 2, 1, 0]
	offsets = [0, 5]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [4, 3, 2, 1, 0]
	pytest_nextoffsets = [0, 5]
	pytest_outindex = [0, 1, 2, 3, 4]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_11():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123]
	index = [5, 2, 4, 1, 3, 0]
	offsets = [0, 2, 4, 6]
	outlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [5, 2, 4, 1, 3, 0]
	pytest_nextoffsets = [0, 2, 4, 6]
	pytest_outindex = [0, 1, 2, 3, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_IndexedArray_reduce_next_64_12():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123]
	index = [5, 4, 3, 2, 1, 0]
	offsets = [0, 3, 6]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,index = index,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [5, 4, 3, 2, 1, 0]
	pytest_nextoffsets = [0, 3, 6]
	pytest_outindex = [0, 1, 2, 3, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


