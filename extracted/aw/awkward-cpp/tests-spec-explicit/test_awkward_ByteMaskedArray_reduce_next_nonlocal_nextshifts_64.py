import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_1():
	nextshifts = []
	length = 0
	mask = []
	valid_when = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = []
	assert nextshifts == pytest_nextshifts


def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_2():
	nextshifts = [123, 123, 123, 123, 123]
	length = 7
	mask = [0, 0, 0, 1, 1, 0, 0]
	valid_when = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [0, 0, 0, 2, 2]
	assert nextshifts == pytest_nextshifts


def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_3():
	nextshifts = [123]
	length = 1
	mask = [0]
	valid_when = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [0]
	assert nextshifts == pytest_nextshifts


def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_4():
	nextshifts = [123]
	length = 1
	mask = [0]
	valid_when = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [123]
	assert nextshifts == pytest_nextshifts


def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_5():
	nextshifts = [123, 123]
	length = 7
	mask = [0, 0, 0, 1, 1, 0, 0]
	valid_when = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [3, 3]
	assert nextshifts == pytest_nextshifts


def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_6():
	nextshifts = [123, 123, 123]
	length = 5
	mask = [0, 1, 0, 1, 1]
	valid_when = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [1, 2, 2]
	assert nextshifts == pytest_nextshifts


