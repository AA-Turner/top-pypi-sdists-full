import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_next_array_1():
	toadvanced = []
	tocarry = []
	fromarray = []
	lenarray = 0
	length = 0
	size = 0
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = []
	pytest_tocarry = []
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_2():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 0, 0, 0]
	lenarray = 4
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 0, 0, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_3():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 0]
	lenarray = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_4():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [0]
	lenarray = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_5():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 0, 1, 1, 1, 0]
	lenarray = 6
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [0, 0, 1, 1, 1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_6():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_7():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_8():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_9():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 1, 1, 1]
	lenarray = 4
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 1, 1, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_10():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 1, 2]
	lenarray = 3
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_11():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 1, 2]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_12():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 1, 2, 3]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 1, 2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_13():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromarray = [0, 1]
	lenarray = 2
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 0, 1, 0, 1, 0, 1]
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_14():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 1, 2, 4]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 1, 2, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_15():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 1, 3]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 1, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_16():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 1, 3, 4]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 1, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_17():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 5]
	lenarray = 5
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [0, 1, 3, 4, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_18():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 5]
	lenarray = 5
	length = 1
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [0, 1, 3, 4, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_19():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 6, 7]
	lenarray = 6
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [0, 1, 3, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_20():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 6, 7]
	lenarray = 6
	length = 1
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [0, 1, 3, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_21():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 1, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 1, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_22():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 4, 6, 7]
	lenarray = 5
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [0, 1, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_23():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 4, 6, 7]
	lenarray = 5
	length = 1
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [0, 1, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_24():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 2]
	lenarray = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_25():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 2]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_26():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 2, 1, 0]
	lenarray = 4
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 2, 1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_27():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 2, 3]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_28():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 2, 3, 4]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 2, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_29():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 2, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 2, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_30():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 3]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_31():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [0, 3, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [0, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_32():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [0, 3]
	lenarray = 2
	length = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 0, 1]
	pytest_tocarry = [0, 3, 4, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_33():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 3]
	lenarray = 2
	length = 3
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 0, 1, 0, 1]
	pytest_tocarry = [0, 3, 4, 7, 8, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_34():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [0, 4]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_35():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [1, 0, 0, 1]
	lenarray = 4
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 0, 0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_36():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [1, 0]
	lenarray = 2
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_37():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [1, 0, 1, 1, 1, 0]
	lenarray = 6
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [1, 0, 1, 1, 1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_38():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [1]
	lenarray = 1
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_39():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [1]
	lenarray = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_40():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromarray = [1, 0, 1]
	lenarray = 3
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	pytest_tocarry = [1, 0, 1, 3, 2, 3, 5, 4, 5, 7, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_41():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromarray = [1, 0]
	lenarray = 2
	length = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 0, 1, 0, 1, 0, 1]
	pytest_tocarry = [1, 0, 3, 2, 5, 4, 7, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_42():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [1, 1, 1, 1]
	lenarray = 4
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 1, 1, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_43():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [1, 2]
	lenarray = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_44():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [1, 2]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_45():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [1, 2, 3]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [1, 2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_46():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [1, 2, 3, 4]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 2, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_47():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [1, 2, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [1, 2, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_48():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [1, 3]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_49():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [1, 3, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [1, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_50():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [1, 3, 4, 6, 7]
	lenarray = 5
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [1, 3, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_51():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [1, 3, 4, 6, 7]
	lenarray = 5
	length = 1
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [1, 3, 4, 6, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_52():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [1, 4]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_53():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [1, 4, 0, 5]
	lenarray = 4
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 4, 0, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_54():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 0, 0, 1]
	lenarray = 4
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 0, 0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_55():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [2, 0]
	lenarray = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_56():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [2, 0, 0, 1, 4]
	lenarray = 5
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [2, 0, 0, 1, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_57():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 0, 0, 2]
	lenarray = 4
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 0, 0, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_58():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 0, 0, 4]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 0, 0, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_59():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [2]
	lenarray = 1
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_60():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [2]
	lenarray = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_61():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 1, 1, 2]
	lenarray = 4
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 1, 1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_62():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromarray = [2, 1, 1, 3]
	lenarray = 4
	length = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 0, 1, 2, 3]
	pytest_tocarry = [2, 1, 1, 3, 6, 5, 5, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_63():
	toadvanced = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromarray = [2, 1, 1, 3]
	lenarray = 4
	length = 3
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
	pytest_tocarry = [2, 1, 1, 3, 6, 5, 5, 7, 10, 9, 9, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_64():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [2, 2]
	lenarray = 2
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_65():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 2, 2, 2]
	lenarray = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 2, 2, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_66():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [2, 2, 2, 2]
	lenarray = 4
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 2, 2, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_67():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [2, 3]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_68():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [2, 3]
	lenarray = 2
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_69():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [2, 3, 4]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [2, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_70():
	toadvanced = [123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123]
	fromarray = [2, 3, 4, 5, 6]
	lenarray = 5
	length = 1
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4]
	pytest_tocarry = [2, 3, 4, 5, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_71():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [2, 4]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_72():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [3]
	lenarray = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_73():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [3, 1, 1, 7]
	lenarray = 4
	length = 1
	size = 10
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 1, 1, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_74():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [3, 2, 1, 0]
	lenarray = 4
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 2, 1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_75():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [3, 2, 1]
	lenarray = 3
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [3, 2, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_76():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [3, 3, 3]
	lenarray = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [3, 3, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_77():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [3, 4]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_78():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [3, 6, 8, 6]
	lenarray = 4
	length = 1
	size = 10
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 6, 8, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_79():
	toadvanced = [123]
	tocarry = [123]
	fromarray = [4]
	lenarray = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0]
	pytest_tocarry = [4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_80():
	toadvanced = [123, 123, 123]
	tocarry = [123, 123, 123]
	fromarray = [4, 3, 2]
	lenarray = 3
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2]
	pytest_tocarry = [4, 3, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_81():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [4, 3, 2, 1]
	lenarray = 4
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 3, 2, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_82():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [4, 4]
	lenarray = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [4, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_83():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromarray = [4, 4, 4, 4]
	lenarray = 4
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 4, 4, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_84():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromarray = [4, 5]
	lenarray = 2
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [4, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_85():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [7, 3, 0, 2, 3, 7]
	lenarray = 6
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [7, 3, 0, 2, 3, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_86():
	toadvanced = [123, 123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromarray = [7, 3, 2, 0, 2, 3, 7]
	lenarray = 7
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5, 6]
	pytest_tocarry = [7, 3, 2, 0, 2, 3, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_array_87():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromarray = [7, 3, 2, 0, 3, 7]
	lenarray = 6
	length = 1
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromarray = fromarray,lenarray = lenarray,length = length,size = size)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [7, 3, 2, 0, 3, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


