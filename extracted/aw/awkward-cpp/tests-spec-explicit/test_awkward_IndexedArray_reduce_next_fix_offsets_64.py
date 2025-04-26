import pytest
import numpy
import kernels

def test_awkward_IndexedArray_reduce_next_fix_offsets_64_1():
	outoffsets = [123, 123, 123, 123, 123]
	outindexlength = 6
	starts = [0, 1, 2, 5]
	startslength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 1, 2, 5, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_2():
	outoffsets = [123]
	outindexlength = 0
	starts = []
	startslength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_3():
	outoffsets = [123, 123]
	outindexlength = 2
	starts = [0]
	startslength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 2]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_4():
	outoffsets = [123, 123, 123, 123, 123, 123]
	outindexlength = 9
	starts = [0, 3, 3, 5, 6]
	startslength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 3, 3, 5, 6, 9]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_5():
	outoffsets = [123, 123, 123]
	outindexlength = 6
	starts = [0, 3]
	startslength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 3, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_6():
	outoffsets = [123, 123]
	outindexlength = 4
	starts = [0]
	startslength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 4]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_7():
	outoffsets = [123, 123]
	outindexlength = 5
	starts = [0]
	startslength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 5]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_reduce_next_fix_offsets_64_8():
	outoffsets = [123, 123]
	outindexlength = 8
	starts = [0]
	startslength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_reduce_next_fix_offsets_64')
	funcPy(outoffsets = outoffsets,outindexlength = outindexlength,starts = starts,startslength = startslength)
	pytest_outoffsets = [0, 8]
	assert outoffsets == pytest_outoffsets


