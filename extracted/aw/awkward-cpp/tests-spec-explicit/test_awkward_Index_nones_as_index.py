import pytest
import numpy
import kernels

def test_awkward_Index_nones_as_index_1():
	toindex = []
	length = 0
	toindex = []
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_2():
	toindex = [123]
	length = 1
	toindex = [0]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_3():
	toindex = [123]
	length = 1
	toindex = [-1]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0]
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_4():
	toindex = [123, 123, 123]
	length = 3
	toindex = [-1, -1, -1]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_5():
	toindex = [123, 123, 123, 123, 123]
	length = 5
	toindex = [0, 1, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_6():
	toindex = [123, 123, 123, 123, 123]
	length = 5
	toindex = [0, -1, -1, 1, -1]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 2, 3, 1, 4]
	assert toindex == pytest_toindex


def test_awkward_Index_nones_as_index_7():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	length = 7
	toindex = [-1, 0, -1, -1, 1, -1, 2]
	funcPy = getattr(kernels, 'awkward_Index_nones_as_index')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [3, 0, 4, 5, 1, 6, 2]
	assert toindex == pytest_toindex


