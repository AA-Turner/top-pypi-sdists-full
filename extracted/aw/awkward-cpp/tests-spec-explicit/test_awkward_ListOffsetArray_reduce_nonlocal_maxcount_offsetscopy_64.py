import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_1():
	maxcount = [123]
	offsetscopy = [123]
	length = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [0]
	pytest_offsetscopy = [0]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_2():
	maxcount = [123]
	offsetscopy = [123, 123]
	length = 1
	offsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [2]
	pytest_offsetscopy = [0, 2]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_3():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 2, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [2]
	pytest_offsetscopy = [0, 2, 3, 5]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_4():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 2, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [2]
	pytest_offsetscopy = [0, 2, 4, 6]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_5():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 3, 5]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_6():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 3, 5, 6, 8, 9]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_7():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 3, 5, 6, 9]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_8():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 5, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 5, 5, 6, 8, 9]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_9():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 5, 6, 7, 7, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 5, 6, 7, 7, 9]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_10():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 3, 5, 6, 7, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 5, 6, 7, 9]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_11():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 5, 7, 8, 9, 10]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 5, 7, 8, 9, 10]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_12():
	maxcount = [123]
	offsetscopy = [123, 123, 123]
	length = 2
	offsets = [0, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 6]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_13():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 3, 6, 9, 12, 15]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [3]
	pytest_offsetscopy = [0, 3, 6, 9, 12, 15]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_14():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 9
	offsets = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_15():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 3, 3, 7]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 3, 3, 7]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_16():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 3, 6, 10]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_17():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 4, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 4, 4, 6]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_18():
	maxcount = [123]
	offsetscopy = [123, 123, 123]
	length = 2
	offsets = [0, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 4, 6]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_19():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 4, 8, 12]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [4]
	pytest_offsetscopy = [0, 4, 8, 12]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_20():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 3, 8, 13, 18, 23, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 3, 8, 13, 18, 23, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_21():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 4, 9, 13, 18, 23, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 4, 9, 13, 18, 23, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_22():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 4, 9, 14, 19, 24, 29]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 4, 9, 14, 19, 24, 29]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_23():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 11, 12, 17, 22]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 11, 12, 17, 22]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_24():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 14, 18, 23, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 14, 18, 23, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_25():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_26():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 15, 19, 24, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 19, 24, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_27():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123]
	length = 4
	offsets = [0, 5, 10, 15, 20]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_28():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 15, 20, 24, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20, 24, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_29():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 5, 10, 15, 20, 25]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20, 25]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_30():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 15, 20, 25, 28]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 28]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_31():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 15, 20, 25, 29]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 29]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_32():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 10, 15, 20, 25, 30]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_33():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	offsets = [0, 5, 6, 11, 16, 17, 22]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 6, 11, 16, 17, 22]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_34():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123, 123, 123]
	length = 5
	offsets = [0, 5, 8, 11, 14, 17]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 8, 11, 14, 17]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


def test_awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64_35():
	maxcount = [123]
	offsetscopy = [123, 123, 123, 123]
	length = 3
	offsets = [0, 5, 9, 12]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_maxcount_offsetscopy_64')
	funcPy(maxcount = maxcount,offsetscopy = offsetscopy,length = length,offsets = offsets)
	pytest_maxcount = [5]
	pytest_offsetscopy = [0, 5, 9, 12]
	assert maxcount == pytest_maxcount
	assert offsetscopy == pytest_offsetscopy


