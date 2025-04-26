import pytest
import numpy
import kernels

def test_awkward_sorting_ranges_1():
	toindex = [123, 123]
	parents = []
	parentslength = 0
	tolength = 2
	funcPy = getattr(kernels, 'awkward_sorting_ranges')
	funcPy(toindex = toindex,parents = parents,parentslength = parentslength,tolength = tolength)
	pytest_toindex = [0, 0]
	assert toindex == pytest_toindex


def test_awkward_sorting_ranges_2():
	toindex = [123, 123, 123]
	parents = [0, 1]
	parentslength = 2
	tolength = 3
	funcPy = getattr(kernels, 'awkward_sorting_ranges')
	funcPy(toindex = toindex,parents = parents,parentslength = parentslength,tolength = tolength)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_sorting_ranges_3():
	toindex = [123, 123, 123, 123, 123]
	parents = [0, 3, 6, 9]
	parentslength = 4
	tolength = 5
	funcPy = getattr(kernels, 'awkward_sorting_ranges')
	funcPy(toindex = toindex,parents = parents,parentslength = parentslength,tolength = tolength)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


def test_awkward_sorting_ranges_4():
	toindex = [123, 123]
	parents = [3, 3, 3, 3]
	parentslength = 4
	tolength = 2
	funcPy = getattr(kernels, 'awkward_sorting_ranges')
	funcPy(toindex = toindex,parents = parents,parentslength = parentslength,tolength = tolength)
	pytest_toindex = [0, 4]
	assert toindex == pytest_toindex


def test_awkward_sorting_ranges_5():
	toindex = [123, 123, 123]
	parents = [2, 4, 4]
	parentslength = 3
	tolength = 3
	funcPy = getattr(kernels, 'awkward_sorting_ranges')
	funcPy(toindex = toindex,parents = parents,parentslength = parentslength,tolength = tolength)
	pytest_toindex = [0, 1, 3]
	assert toindex == pytest_toindex


