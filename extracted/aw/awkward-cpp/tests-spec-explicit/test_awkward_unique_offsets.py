import pytest
import numpy
import kernels

def test_awkward_unique_offsets_1():
	tooffsets = [123]
	fromoffsets = [0]
	starts = []
	startslength = 0
	length = 1
	funcPy = getattr(kernels, 'awkward_unique_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,starts = starts,startslength = startslength,length = length)
	pytest_tooffsets = [0]
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_offsets_2():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 2, 3, 4, 5]
	starts = [0, 2, 4, 6]
	startslength = 4
	length = 6
	funcPy = getattr(kernels, 'awkward_unique_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,starts = starts,startslength = startslength,length = length)
	pytest_tooffsets = [0, 2, 2, 3, 5, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_offsets_3():
	tooffsets = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 2, 3]
	starts = [0, 1, 3, 4]
	startslength = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_unique_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,starts = starts,startslength = startslength,length = length)
	pytest_tooffsets = [0, 1, 2, 2, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_unique_offsets_4():
	tooffsets = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 2, 3]
	starts = [0, 1, 2, 3]
	startslength = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_unique_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,starts = starts,startslength = startslength,length = length)
	pytest_tooffsets = [0, 1, 2, 2, 3]
	assert tooffsets == pytest_tooffsets


