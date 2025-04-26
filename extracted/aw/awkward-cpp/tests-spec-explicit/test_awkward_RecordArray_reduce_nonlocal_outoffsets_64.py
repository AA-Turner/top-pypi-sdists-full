import pytest
import numpy
import kernels

def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_1():
	outoffsets = [123]
	outcarry = []
	outlength = 0
	parents = []
	lenparents = 0
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0]
	pytest_outcarry = []
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_2():
	outoffsets = [123, 123]
	outcarry = [123]
	outlength = 1
	parents = [0, 0]
	lenparents = 2
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 2]
	pytest_outcarry = [0]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_3():
	outoffsets = [123, 123, 123]
	outcarry = [123, 123]
	outlength = 2
	parents = [1, 1]
	lenparents = 2
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 2, 2]
	pytest_outcarry = [1, 0]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_4():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	outcarry = [123, 123, 123, 123, 123, 123]
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 2, 3, 5, 5, 5]
	lenparents = 11
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 3, 6, 7, 8, 11, 11]
	pytest_outcarry = [0, 1, 2, 3, 5, 4]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_5():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	outcarry = [123, 123, 123, 123, 123, 123]
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 5, 5, 5]
	lenparents = 11
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 3, 6, 8, 11, 11, 11]
	pytest_outcarry = [0, 1, 4, 2, 5, 3]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_6():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	outcarry = [123, 123, 123, 123, 123, 123]
	outlength = 6
	parents = [0, 0, 3, 3, 1, 1, 4, 4, 2, 2, 5]
	lenparents = 11
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 2, 4, 6, 8, 10, 11]
	pytest_outcarry = [0, 2, 4, 1, 3, 5]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_7():
	outoffsets = [123, 123, 123, 123, 123, 123, 123]
	outcarry = [123, 123, 123, 123, 123, 123]
	outlength = 6
	parents = [0, 0, 0, 3, 1, 1, 4, 4, 2, 2, 5]
	lenparents = 11
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 3, 4, 6, 8, 10, 11]
	pytest_outcarry = [0, 2, 4, 1, 3, 5]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


def test_awkward_RecordArray_reduce_nonlocal_outoffsets_64_8():
	outoffsets = [123, 123, 123, 123, 123, 123]
	outcarry = [123, 123, 123, 123, 123]
	outlength = 5
	parents = [0, 0, 1, 1, 1, 2, 3, 3, 4, 4]
	lenparents = 10
	funcPy = getattr(kernels, 'awkward_RecordArray_reduce_nonlocal_outoffsets_64')
	funcPy(outoffsets = outoffsets,outcarry = outcarry,outlength = outlength,parents = parents,lenparents = lenparents)
	pytest_outoffsets = [0, 2, 5, 6, 8, 10]
	pytest_outcarry = [0, 1, 2, 3, 4]
	assert outoffsets == pytest_outoffsets
	assert outcarry == pytest_outcarry


