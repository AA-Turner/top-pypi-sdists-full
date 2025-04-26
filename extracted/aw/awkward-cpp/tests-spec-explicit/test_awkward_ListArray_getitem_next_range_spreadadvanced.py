import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_range_spreadadvanced_1():
	toadvanced = []
	fromadvanced = []
	fromoffsets = []
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_toadvanced = []
	assert toadvanced == pytest_toadvanced


def test_awkward_ListArray_getitem_next_range_spreadadvanced_2():
	toadvanced = [123, 123, 123]
	fromadvanced = [0]
	fromoffsets = [0, 3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_toadvanced = [0, 0, 0]
	assert toadvanced == pytest_toadvanced


def test_awkward_ListArray_getitem_next_range_spreadadvanced_3():
	toadvanced = [123, 123, 123, 123, 123, 123]
	fromadvanced = [0, 1]
	fromoffsets = [0, 3, 6]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_toadvanced = [0, 0, 0, 1, 1, 1]
	assert toadvanced == pytest_toadvanced


def test_awkward_ListArray_getitem_next_range_spreadadvanced_4():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromoffsets = [0, 4, 5, 7, 10]
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_toadvanced = [0, 0, 0, 0, 1, 2, 2, 3, 3, 3]
	assert toadvanced == pytest_toadvanced


