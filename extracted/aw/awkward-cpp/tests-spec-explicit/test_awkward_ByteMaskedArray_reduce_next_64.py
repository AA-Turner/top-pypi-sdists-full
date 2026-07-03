import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_reduce_next_64_1():
	nextcarry = []
	nextoffsets = [123]
	outindex = []
	mask = []
	validwhen = False
	offsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,mask = mask,validwhen = validwhen,offsets = offsets,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0]
	pytest_outindex = []
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_2():
	nextcarry = [123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123]
	outindex = [123, 123, 123, 123, 123, 123, 123]
	mask = [0, 0, 0, 1, 1, 0, 0]
	validwhen = False
	offsets = [0, 2, 4, 7]
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,mask = mask,validwhen = validwhen,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [0, 1, 2, 5, 6]
	pytest_nextoffsets = [0, 2, 3, 5]
	pytest_outindex = [0, 1, 2, -1, -1, 3, 4]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_3():
	nextcarry = [123]
	nextoffsets = [123, 123, 123, 123]
	outindex = [123]
	mask = [0]
	validwhen = False
	offsets = [0, 0, 0, 1]
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,mask = mask,validwhen = validwhen,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [0]
	pytest_nextoffsets = [0, 0, 0, 1]
	pytest_outindex = [0]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_4():
	nextcarry = []
	nextoffsets = [123, 123, 123]
	outindex = [123]
	mask = [1]
	validwhen = False
	offsets = [0, 0, 1]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,mask = mask,validwhen = validwhen,offsets = offsets,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0, 0, 0]
	pytest_outindex = [-1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


def test_awkward_ByteMaskedArray_reduce_next_64_5():
	nextcarry = [123, 123, 123]
	nextoffsets = [123, 123, 123]
	outindex = [123, 123, 123, 123, 123]
	mask = [0, 1, 0, 1, 1]
	validwhen = True
	offsets = [0, 2, 5]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,outindex = outindex,mask = mask,validwhen = validwhen,offsets = offsets,outlength = outlength)
	pytest_nextcarry = [1, 3, 4]
	pytest_nextoffsets = [0, 1, 3]
	pytest_outindex = [-1, 0, -1, 1, 2]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert outindex == pytest_outindex


