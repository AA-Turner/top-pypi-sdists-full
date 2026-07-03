import pytest
import numpy
import kernels

def test_awkward_IndexedArray_local_preparenext_64_1():
	tocarry = [123, 123, 123, 123, 123]
	starts = [0]
	offsets = [0, 5]
	nextoffsets = [0, 4]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext_64')
	funcPy(tocarry = tocarry,starts = starts,offsets = offsets,nextoffsets = nextoffsets,outlength = outlength)
	pytest_tocarry = [0, 1, 2, 3, -1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_64_2():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	starts = [0, 6]
	offsets = [0, 6, 11]
	nextoffsets = [0, 4, 7]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext_64')
	funcPy(tocarry = tocarry,starts = starts,offsets = offsets,nextoffsets = nextoffsets,outlength = outlength)
	pytest_tocarry = [0, 1, 2, 3, -1, -1, 4, 5, 6, -1, -1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_64_3():
	tocarry = []
	starts = []
	offsets = [0]
	nextoffsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext_64')
	funcPy(tocarry = tocarry,starts = starts,offsets = offsets,nextoffsets = nextoffsets,outlength = outlength)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_64_4():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	starts = [0, 5, 8, 11, 14]
	offsets = [0, 5, 8, 11, 14, 17]
	nextoffsets = [0, 3, 3, 5, 6, 9]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext_64')
	funcPy(tocarry = tocarry,starts = starts,offsets = offsets,nextoffsets = nextoffsets,outlength = outlength)
	pytest_tocarry = [0, 1, 2, -1, -1, -1, -1, -1, 3, 4, -1, 5, -1, -1, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_64_5():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	starts = [0, 5, 8, 11, 14]
	offsets = [0, 5, 8, 11, 14, 17]
	nextoffsets = [0, 3, 4, 6, 7, 10]
	outlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext_64')
	funcPy(tocarry = tocarry,starts = starts,offsets = offsets,nextoffsets = nextoffsets,outlength = outlength)
	pytest_tocarry = [0, 1, 2, -1, -1, 3, -1, -1, 4, 5, -1, 6, -1, -1, 7, 8, 9]
	assert tocarry == pytest_tocarry


