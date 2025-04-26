import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_next_range_1():
	tocarry = []
	length = 0
	nextsize = 0
	regular_start = 0
	size = 0
	step = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_2():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 0
	size = 1
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_3():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 0
	size = 2
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_4():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_5():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 0
	size = 3
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_6():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 0
	size = 5
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_7():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 0
	size = 2
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_8():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 0
	size = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_9():
	tocarry = [123, 123, 123]
	length = 1
	nextsize = 3
	regular_start = 0
	size = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_10():
	tocarry = [123, 123, 123, 123]
	length = 1
	nextsize = 4
	regular_start = 0
	size = 4
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_11():
	tocarry = [123, 123, 123, 123]
	length = 1
	nextsize = 4
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_12():
	tocarry = [123, 123, 123, 123]
	length = 2
	nextsize = 2
	regular_start = 0
	size = 2
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_13():
	tocarry = [123, 123, 123, 123, 123]
	length = 1
	nextsize = 5
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_14():
	tocarry = [123, 123, 123, 123, 123]
	length = 1
	nextsize = 5
	regular_start = 0
	size = 6
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_15():
	tocarry = [123, 123, 123, 123, 123, 123]
	length = 1
	nextsize = 6
	regular_start = 0
	size = 6
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_16():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	length = 1
	nextsize = 8
	regular_start = 0
	size = 8
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_17():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 1
	nextsize = 10
	regular_start = 0
	size = 10
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_18():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	nextsize = 5
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_19():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	nextsize = 5
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_20():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	length = 2
	nextsize = 4
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_21():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	nextsize = 4
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_22():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	nextsize = 4
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_23():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	nextsize = 4
	regular_start = 0
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 28]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_24():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 0
	size = 3
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_25():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 0
	size = 5
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_26():
	tocarry = [123, 123, 123]
	length = 1
	nextsize = 3
	regular_start = 0
	size = 5
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_27():
	tocarry = [123, 123, 123]
	length = 1
	nextsize = 3
	regular_start = 0
	size = 6
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_28():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	nextsize = 3
	regular_start = 0
	size = 5
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_29():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	nextsize = 3
	regular_start = 0
	size = 5
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, 27, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_30():
	tocarry = [123, 123, 123, 123]
	length = 1
	nextsize = 4
	regular_start = 0
	size = 8
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 2, 4, 6]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_31():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 0
	size = 5
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [0, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_32():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 1
	size = 2
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_33():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 1
	size = 3
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_34():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 1
	size = 3
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_35():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 1
	size = 5
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_36():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 1
	size = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_37():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 1
	size = 4
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_38():
	tocarry = [123, 123, 123]
	length = 1
	nextsize = 3
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_39():
	tocarry = [123, 123, 123, 123]
	length = 1
	nextsize = 4
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_40():
	tocarry = [123, 123, 123, 123, 123]
	length = 1
	nextsize = 5
	regular_start = 1
	size = 6
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_41():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	nextsize = 4
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_42():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	nextsize = 4
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_43():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	nextsize = 4
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_44():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	length = 2
	nextsize = 4
	regular_start = 1
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 2, 3, 4, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_45():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 1
	size = 5
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_46():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 1
	size = 5
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [1, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_47():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 2
	size = 3
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_48():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 2
	size = 3
	step = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_49():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 2
	size = 3
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_50():
	tocarry = [123]
	length = 1
	nextsize = 1
	regular_start = 2
	size = 5
	step = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_51():
	tocarry = [123, 123, 123]
	length = 1
	nextsize = 3
	regular_start = 2
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_range_52():
	tocarry = [123, 123]
	length = 1
	nextsize = 2
	regular_start = 3
	size = 5
	step = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range')
	funcPy(tocarry = tocarry,length = length,nextsize = nextsize,regular_start = regular_start,size = size,step = step)
	pytest_tocarry = [3, 4]
	assert tocarry == pytest_tocarry


