import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_carry_1():
	tocarry = []
	fromcarry = [0, 0]
	lencarry = 2
	size = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_2():
	tocarry = []
	fromcarry = []
	lencarry = 0
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_3():
	tocarry = []
	fromcarry = []
	lencarry = 0
	size = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_4():
	tocarry = [123, 123]
	fromcarry = [0, 0]
	lencarry = 2
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_5():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0, 0, 1, 1, 1]
	lencarry = 6
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 0, 0, 1, 1, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_6():
	tocarry = [123, 123, 123, 123, 123]
	fromcarry = [0, 0, 0, 2, 2]
	lencarry = 5
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 0, 0, 2, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_7():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
	lencarry = 10
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_8():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
	lencarry = 10
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_9():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0, 1, 1]
	lencarry = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 0, 1, 2, 3, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_10():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0, 0, 0]
	lencarry = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_11():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 1, 1, 2]
	lencarry = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_12():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0]
	lencarry = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_13():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 0, 0, 1, 1, 1]
	lencarry = 6
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_14():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 2, 3, 5]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_15():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 2, 4]
	lencarry = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_16():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 3, 6, 9]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_17():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 3, 1, 4, 2, 5]
	lencarry = 6
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_18():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 4, 8, 10]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 50, 51, 52, 53, 54]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_19():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 1, 1, 1]
	lencarry = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_20():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	lencarry = 12
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_21():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [0, 1, 2, 3, 4, 5, 3, 4, 5, 3, 4, 5]
	lencarry = 12
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_22():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [2, 0, 0, 1]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_23():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [2, 2, 2, 2]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 10, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_24():
	tocarry = [123, 123, 123, 123, 123]
	fromcarry = [2]
	lencarry = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [10, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_25():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [2, 5, 8, 11]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [10, 11, 12, 13, 14, 25, 26, 27, 28, 29, 40, 41, 42, 43, 44, 55, 56, 57, 58, 59]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_26():
	tocarry = [123]
	fromcarry = [1]
	lencarry = 1
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_27():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [3, 4, 5, 0, 1, 2, 0, 1, 2, 3, 4, 5]
	lencarry = 12
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_28():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
	lencarry = 12
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_29():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [3, 4, 5]
	lencarry = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_30():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [4, 4, 4, 4]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_31():
	tocarry = [123, 123, 123, 123, 123]
	fromcarry = [4]
	lencarry = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [20, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_32():
	tocarry = [123]
	fromcarry = [2]
	lencarry = 1
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_33():
	tocarry = [123, 123, 123, 123]
	fromcarry = [1, 0]
	lencarry = 2
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [2, 3, 0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_34():
	tocarry = [123, 123]
	fromcarry = [1]
	lencarry = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_35():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 1, 0, 0]
	lencarry = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [2, 3, 2, 3, 0, 1, 0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_36():
	tocarry = [123, 123, 123, 123]
	fromcarry = [1, 2]
	lencarry = 2
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_37():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 0, 0, 1]
	lencarry = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [3, 4, 5, 0, 1, 2, 0, 1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_38():
	tocarry = [123, 123, 123]
	fromcarry = [1]
	lencarry = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_39():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 1, 1, 1]
	lencarry = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_40():
	tocarry = [123, 123]
	fromcarry = [2]
	lencarry = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_41():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 2]
	lencarry = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [4, 5, 6, 7, 8, 9, 10, 11]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_42():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 2]
	lencarry = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_43():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 2, 3, 4, 5]
	lencarry = 5
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_44():
	tocarry = [123, 123, 123, 123, 123]
	fromcarry = [1]
	lencarry = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_45():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 3, 6, 10]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 50, 51, 52, 53, 54]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_46():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [1, 4, 0, 5]
	lencarry = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_carry_47():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromcarry = [2, 1, 1, 2]
	lencarry = 4
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_carry')
	funcPy(tocarry = tocarry,fromcarry = fromcarry,lencarry = lencarry,size = size)
	pytest_tocarry = [8, 9, 10, 11, 4, 5, 6, 7, 4, 5, 6, 7, 8, 9, 10, 11]
	assert tocarry == pytest_tocarry


