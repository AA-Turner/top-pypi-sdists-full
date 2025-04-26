import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_range_counts_1():
	total = [123]
	fromoffsets = []
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [0]
	assert total == pytest_total


def test_awkward_ListArray_getitem_next_range_counts_2():
	total = [123]
	fromoffsets = [0, 2, 2, 4, 4, 5, 6, 7, 9, 9]
	lenstarts = 9
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [9]
	assert total == pytest_total


def test_awkward_ListArray_getitem_next_range_counts_3():
	total = [123]
	fromoffsets = [0, 2, 4, 5, 6, 7, 9]
	lenstarts = 6
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [9]
	assert total == pytest_total


def test_awkward_ListArray_getitem_next_range_counts_4():
	total = [123]
	fromoffsets = [0, 0, 0, 0]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [0]
	assert total == pytest_total


def test_awkward_ListArray_getitem_next_range_counts_5():
	total = [123]
	fromoffsets = [0, 3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [3]
	assert total == pytest_total


