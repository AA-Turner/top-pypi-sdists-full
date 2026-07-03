import pytest
import numpy
import kernels

def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_1():
	nextcarry = []
	nextoffsets = [123]
	offsets = [0]
	size = 3
	length = 0
	outlength = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_2():
	nextcarry = []
	nextoffsets = [123]
	offsets = [0, 1, 2]
	size = 0
	length = 2
	outlength = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_3():
	nextcarry = [123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123]
	offsets = [0, 1, 2]
	size = 2
	length = 2
	outlength = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = [0, 1, 2, 3]
	pytest_nextoffsets = [0, 1, 2, 3, 4]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_4():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123]
	offsets = [0, 2]
	size = 3
	length = 2
	outlength = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = [0, 3, 1, 4, 2, 5]
	pytest_nextoffsets = [0, 2, 4, 6]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_5():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123]
	offsets = [0, 2, 3]
	size = 2
	length = 3
	outlength = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = [0, 2, 1, 3, 4, 5]
	pytest_nextoffsets = [0, 2, 4, 5, 6]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_6():
	nextcarry = [123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123, 123]
	offsets = [0, 0, 2, 2]
	size = 2
	length = 2
	outlength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = [0, 2, 1, 3]
	pytest_nextoffsets = [0, 0, 0, 2, 4, 4, 4]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


def test_awkward_RegularArray_reduce_nonlocal_preparenext_64_7():
	nextcarry = [123]
	nextoffsets = [123, 123]
	offsets = [0, 1]
	size = 1
	length = 1
	outlength = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,offsets = offsets,size = size,length = length,outlength = outlength)
	pytest_nextcarry = [0]
	pytest_nextoffsets = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets


