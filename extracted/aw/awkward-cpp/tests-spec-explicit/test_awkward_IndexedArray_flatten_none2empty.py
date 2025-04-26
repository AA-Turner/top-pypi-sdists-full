import pytest
import numpy
import kernels

def test_awkward_IndexedArray_flatten_none2empty_1():
	outoffsets = [123]
	offsets = [0]
	offsetslength = 1
	outindex = []
	outindexlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_2():
	outoffsets = [123]
	offsets = [0]
	offsetslength = 0
	outindex = [0]
	outindexlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	with pytest.raises(Exception):
		funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)


def test_awkward_IndexedArray_flatten_none2empty_3():
	outoffsets = [123, 123, 123, 123, 123]
	offsets = [0, 1, 1, 6]
	offsetslength = 4
	outindex = [0, 1, 2, 1]
	outindexlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 1, 1, 6, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_4():
	outoffsets = [123, 123, 123, 123, 123]
	offsets = [0, 1, 1, 6]
	offsetslength = 4
	outindex = [0, 1, 2, 1]
	outindexlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 1, 1, 6, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_5():
	outoffsets = [123, 123, 123, 123, 123]
	offsets = [0, 1, 1, 6]
	offsetslength = 4
	outindex = [0, -1, 2, -1]
	outindexlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 1, 1, 6, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_6():
	outoffsets = [123, 123, 123, 123, 123, 123]
	offsets = [0, 3, 3, 5]
	offsetslength = 4
	outindex = [0, 1, 1, 1, 2]
	outindexlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 3, 3, 3, 3, 5]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_7():
	outoffsets = [123, 123, 123, 123, 123, 123]
	offsets = [0, 3, 3, 5]
	offsetslength = 4
	outindex = [0, -1, 1, -1, 2]
	outindexlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 3, 3, 3, 3, 5]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_8():
	outoffsets = [123, 123, 123, 123, 123, 123]
	offsets = [0, 3, 3, 4, 7]
	offsetslength = 5
	outindex = [0, 1, 2, 1, 3]
	outindexlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 3, 3, 4, 4, 7]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_9():
	outoffsets = [123, 123, 123, 123, 123, 123]
	offsets = [0, 3, 3, 4, 7]
	offsetslength = 5
	outindex = [0, -1, 2, -1, 3]
	outindexlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 3, 3, 4, 4, 7]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_10():
	outoffsets = [123, 123, 123, 123, 123, 123, 123, 123]
	offsets = [0, 3, 3, 5, 6, 6, 10]
	offsetslength = 7
	outindex = [0, 1, 2, 3, 4, 1, 5]
	outindexlength = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 3, 3, 5, 6, 6, 6, 10]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_11():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	offsets = [0, 4, 4, 6]
	offsetslength = 4
	outindex = [0, 1, 1, 1, 2, 1]
	outindexlength = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 4, 4, 4, 4, 6, 6]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_12():
	outoffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	offsets = [0, 4, 4, 6, 7, 7, 12]
	offsetslength = 7
	outindex = [0, 1, 1, 1, 2, 3, 4, 5, 1]
	outindexlength = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 4, 4, 4, 4, 6, 7, 7, 12, 12]
	assert outoffsets == pytest_outoffsets


def test_awkward_IndexedArray_flatten_none2empty_13():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	offsets = [0, 5, 5, 6, 9]
	offsetslength = 5
	outindex = [0, 1, 1, 2, 1, 3]
	outindexlength = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_none2empty')
	funcPy(outoffsets = outoffsets,offsets = offsets,offsetslength = offsetslength,outindex = outindex,outindexlength = outindexlength)
	pytest_outoffsets = [0, 5, 5, 5, 6, 6, 9]
	assert outoffsets == pytest_outoffsets


