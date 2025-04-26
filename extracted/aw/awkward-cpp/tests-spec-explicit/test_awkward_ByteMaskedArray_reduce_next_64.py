import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_reduce_next_64_1():
	nextcarry = []
	nextparents = []
	outindex = []
	mask = []
	parents = []
	length = 0
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,mask = mask,parents = parents,length = length,validwhen = validwhen)
	pytest_nextcarry = []
	pytest_nextparents = []
	pytest_outindex = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_2():
	nextcarry = [123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123, 123]
	mask = [0, 0, 0, 1, 1, 0, 0]
	parents = [0, 0, 1, 1, 2, 2, 2]
	length = 7
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,mask = mask,parents = parents,length = length,validwhen = validwhen)
	pytest_nextcarry = [0, 1, 2, 5, 6]
	pytest_nextparents = [0, 0, 1, 2, 2]
	pytest_outindex = [0, 1, 2, -1, -1, 3, 4]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_3():
	nextcarry = [123]
	nextparents = [123]
	outindex = [123]
	mask = [0]
	parents = [2]
	length = 1
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,mask = mask,parents = parents,length = length,validwhen = validwhen)
	pytest_nextcarry = [0]
	pytest_nextparents = [2]
	pytest_outindex = [0]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_4():
	nextcarry = [123]
	nextparents = [123]
	outindex = [123]
	mask = [1]
	parents = [1]
	length = 1
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,mask = mask,parents = parents,length = length,validwhen = validwhen)
	pytest_nextcarry = [123]
	pytest_nextparents = [123]
	pytest_outindex = [-1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_5():
	nextcarry = [123, 123, 123]
	nextparents = [123, 123, 123]
	outindex = [123, 123, 123, 123, 123]
	mask = [0, 1, 0, 1, 1]
	parents = [0, 0, 1, 1, 1]
	length = 5
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,outindex = outindex,mask = mask,parents = parents,length = length,validwhen = validwhen)
	pytest_nextcarry = [1, 3, 4]
	pytest_nextparents = [0, 1, 1]
	pytest_outindex = [-1, 0, -1, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert outindex == pytest_outindex


