import pytest
import numpy
import kernels

def test_awkward_ListArray_min_range_1():
	tomin = []
	fromstarts = []
	fromstops = []
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_min_range')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tomin = []
	assert tomin == pytest_tomin


def test_awkward_ListArray_min_range_2():
	tomin = [123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lenstarts = 5
	funcPy = getattr(kernels, 'awkward_ListArray_min_range')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tomin = [0]
	assert tomin == pytest_tomin


def test_awkward_ListArray_min_range_3():
	tomin = [123]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 7]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_min_range')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tomin = [0]
	assert tomin == pytest_tomin


def test_awkward_ListArray_min_range_4():
	tomin = [123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	lenstarts = 5
	funcPy = getattr(kernels, 'awkward_ListArray_min_range')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tomin = [0]
	assert tomin == pytest_tomin


def test_awkward_ListArray_min_range_5():
	tomin = [123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_min_range')
	funcPy(tomin = tomin,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tomin = [1]
	assert tomin == pytest_tomin


