import pytest
import numpy
import kernels

def test_awkward_sorting_ranges_length_1():
	tolength = [123]
	parents = []
	parentslength = 0
	funcPy = getattr(kernels, 'awkward_sorting_ranges_length')
	funcPy(tolength = tolength,parents = parents,parentslength = parentslength)
	pytest_tolength = [2]
	assert tolength == pytest_tolength


def test_awkward_sorting_ranges_length_2():
	tolength = [123]
	parents = [0, 1]
	parentslength = 2
	funcPy = getattr(kernels, 'awkward_sorting_ranges_length')
	funcPy(tolength = tolength,parents = parents,parentslength = parentslength)
	pytest_tolength = [3]
	assert tolength == pytest_tolength


def test_awkward_sorting_ranges_length_3():
	tolength = [123]
	parents = [0, 3, 6, 9]
	parentslength = 4
	funcPy = getattr(kernels, 'awkward_sorting_ranges_length')
	funcPy(tolength = tolength,parents = parents,parentslength = parentslength)
	pytest_tolength = [5]
	assert tolength == pytest_tolength


def test_awkward_sorting_ranges_length_4():
	tolength = [123]
	parents = [3, 3, 3, 3]
	parentslength = 4
	funcPy = getattr(kernels, 'awkward_sorting_ranges_length')
	funcPy(tolength = tolength,parents = parents,parentslength = parentslength)
	pytest_tolength = [2]
	assert tolength == pytest_tolength


def test_awkward_sorting_ranges_length_5():
	tolength = [123]
	parents = [2, 4, 4]
	parentslength = 3
	funcPy = getattr(kernels, 'awkward_sorting_ranges_length')
	funcPy(tolength = tolength,parents = parents,parentslength = parentslength)
	pytest_tolength = [3]
	assert tolength == pytest_tolength


