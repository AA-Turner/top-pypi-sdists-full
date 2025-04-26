import pytest
import numpy
import kernels

def test_awkward_NumpyArray_subrange_equal_bool_1():
	toequal = [123]
	tmpptr = []
	fromstarts = []
	fromstops = []
	length = 0
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [0]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_2():
	toequal = [123]
	tmpptr = [0, 1, 2, 3, 4, 5, 6, 7]
	fromstarts = [0, 1, 3, 5]
	fromstops = [1, 3, 5, 7]
	length = 4
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_3():
	toequal = [123]
	tmpptr = [0, 2, 2, 3, 5]
	fromstarts = [0, 2, 3, 3]
	fromstops = [2, 3, 3, 5]
	length = 5
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [0]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_4():
	toequal = [123]
	tmpptr = [0, 2, 2, 0, 2]
	fromstarts = [0, 2, 3, 3]
	fromstops = [2, 3, 3, 5]
	length = 5
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_5():
	toequal = [123]
	tmpptr = [0, 0, 0, 0, 0]
	fromstarts = [0, 2, 3, 3]
	fromstops = [2, 3, 3, 5]
	length = 5
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_6():
	toequal = [123]
	tmpptr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	fromstarts = [0, 2, 4, 6, 8, 10]
	fromstops = [2, 4, 6, 8, 10, 12]
	length = 6
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_7():
	toequal = [123]
	tmpptr = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
	fromstarts = [0, 2, 4, 6, 8, 10]
	fromstops = [2, 4, 6, 8, 10, 12]
	length = 6
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_8():
	toequal = [123]
	tmpptr = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2]
	fromstarts = [0, 2, 4, 6, 8, 10]
	fromstops = [2, 4, 6, 8, 10, 12]
	length = 6
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_9():
	toequal = [123]
	tmpptr = [1, 1, 1, 1, 1, 1]
	fromstarts = [2, 2, 2, 2, 2, 2]
	fromstops = [4, 4, 4, 4, 4, 4]
	length = 6
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


def test_awkward_NumpyArray_subrange_equal_bool_10():
	toequal = [123]
	tmpptr = [1, 2, 3, 4, 5, 6]
	fromstarts = [2, 2, 2, 2, 2, 2]
	fromstops = [4, 4, 4, 4, 4, 4]
	length = 6
	funcPy = getattr(kernels, 'awkward_NumpyArray_subrange_equal_bool')
	funcPy(toequal = toequal,tmpptr = tmpptr,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_toequal = [1]
	assert toequal == pytest_toequal


