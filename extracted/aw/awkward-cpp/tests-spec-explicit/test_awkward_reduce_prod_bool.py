import pytest
import numpy
import kernels

def test_awkward_reduce_prod_bool_1():
	toptr = []
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 1, 0, 0, 1, 1]
	outlength = 8
	offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, False, False, True, True, True, False, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_3():
	toptr = [123, 123]
	fromptr = [0, 0, 0, 1, 1, 1]
	outlength = 2
	offsets = [0, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_4():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 0, 1, 0, 0, 1, 0, 1, 1]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, False, True, False, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_5():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
	outlength = 4
	offsets = [0, 3, 6, 9, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, False, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_6():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 2, 2, 2, 3, 0, 0, 4]
	outlength = 4
	offsets = [0, 3, 6, 9, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, False, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_7():
	toptr = [123, 123, 123]
	fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
	outlength = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_8():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 6
	offsets = [0, 3, 6, 10, 15, 21, 25]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, True, False, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_9():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
	outlength = 5
	offsets = [0, 3, 6, 9, 12, 15]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [False, True, True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_10():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
	outlength = 6
	offsets = [0, 3, 6, 11, 15, 19, 22]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False, False, True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_11():
	toptr = [123, 123, 123]
	fromptr = [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
	outlength = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_12():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 5
	offsets = [0, 5, 8, 11, 14, 19]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False, False, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_13():
	toptr = [123, 123, 123]
	fromptr = [1, 2, 3, 0, 2, 0, 0, 2, 0, 4]
	outlength = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_14():
	toptr = [123, 123]
	fromptr = [1, 1, 1, 0, 0, 0]
	outlength = 2
	offsets = [0, 3, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_15():
	toptr = [123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0]
	outlength = 3
	offsets = [0, 3, 6, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, False]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_16():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	outlength = 5
	offsets = [0, 3, 6, 9, 12, 15]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, False, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_17():
	toptr = [123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 3
	offsets = [0, 3, 6, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_18():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 5
	offsets = [0, 3, 6, 10, 14, 17]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, True, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_19():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 5
	offsets = [0, 3, 8, 12, 16, 19]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, True, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_20():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	outlength = 6
	offsets = [0, 3, 6, 11, 15, 19, 22]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True, True, True, True, True, True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_21():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_bool_22():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod_bool')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [True]
	assert toptr == pytest_toptr


