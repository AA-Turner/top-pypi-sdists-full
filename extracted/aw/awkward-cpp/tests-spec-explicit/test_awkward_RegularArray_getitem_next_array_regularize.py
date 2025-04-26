import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_next_array_regularize_1():
	toarray = []
	fromarray = []
	lenarray = 0
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = []
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_2():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 0, 0, 0]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 0, 0, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_3():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 0, 0, 0]
	lenarray = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 0, 0, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_4():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 0, 0, 0]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 0, 0, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_5():
	toarray = [123, 123]
	fromarray = [0, 0]
	lenarray = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_6():
	toarray = [123]
	fromarray = [0]
	lenarray = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_7():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 0, 1]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_8():
	toarray = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_9():
	toarray = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_10():
	toarray = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_11():
	toarray = [123, 123]
	fromarray = [0, 1]
	lenarray = 2
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_12():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 1, 1]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 1, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_13():
	toarray = [123, 123, 123]
	fromarray = [0, 1, 2]
	lenarray = 3
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_14():
	toarray = [123, 123, 123]
	fromarray = [0, 1, 2]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_15():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 1, 1]
	lenarray = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 1, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_16():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 2, 3]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 2, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_17():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 2, 4]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 2, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_18():
	toarray = [123, 123, 123]
	fromarray = [0, 1, 3]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_19():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 1, 3, 4]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_20():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 5]
	lenarray = 5
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3, 4, 5]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_21():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 5]
	lenarray = 5
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3, 4, 5]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_22():
	toarray = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 6, 7]
	lenarray = 6
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_23():
	toarray = [123, 123, 123, 123, 123, 123]
	fromarray = [0, 1, 3, 4, 6, 7]
	lenarray = 6
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 3, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_24():
	toarray = [123, 123, 123]
	fromarray = [0, 1, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_25():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 4, 6, 7]
	lenarray = 5
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_26():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [0, 1, 4, 6, 7]
	lenarray = 5
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 1, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_27():
	toarray = [123, 123]
	fromarray = [0, 2]
	lenarray = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_28():
	toarray = [123, 123]
	fromarray = [0, 2]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_29():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 2, 1, 0]
	lenarray = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2, 1, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_30():
	toarray = [123, 123, 123]
	fromarray = [0, 2, 3]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_31():
	toarray = [123, 123, 123, 123]
	fromarray = [0, 2, 3, 4]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_32():
	toarray = [123, 123, 123]
	fromarray = [0, 2, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 2, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_33():
	toarray = [123, 123]
	fromarray = [0, 3]
	lenarray = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_34():
	toarray = [123, 123]
	fromarray = [0, 3]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_35():
	toarray = [123, 123, 123]
	fromarray = [0, 3, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_36():
	toarray = [123, 123]
	fromarray = [0, 4]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [0, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_37():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 0, 0, 1]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_38():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 0, 0, 1]
	lenarray = 4
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_39():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 0, 0, 1]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_40():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 0, 1, 0]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 1, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_41():
	toarray = [123, 123]
	fromarray = [1, 0]
	lenarray = 2
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_42():
	toarray = [123, 123, 123]
	fromarray = [1, 0, 1]
	lenarray = 3
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_43():
	toarray = [123, 123, 123, 123, 123, 123]
	fromarray = [1, 0, 1, 1, 1, 0]
	lenarray = 6
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 0, 1, 1, 1, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_44():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 1, 1, 1]
	lenarray = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 1, 1, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_45():
	toarray = [123]
	fromarray = [1]
	lenarray = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_46():
	toarray = [123]
	fromarray = [1]
	lenarray = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_47():
	toarray = [123, 123]
	fromarray = [1, 2]
	lenarray = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_48():
	toarray = [123, 123]
	fromarray = [1, 2]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_49():
	toarray = [123, 123, 123]
	fromarray = [1, 2, 3]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 2, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_50():
	toarray = [123, 123, 123, 123]
	fromarray = [1, 2, 3, 4]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 2, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_51():
	toarray = [123, 123, 123]
	fromarray = [1, 2, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 2, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_52():
	toarray = [123, 123]
	fromarray = [1, 3]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_53():
	toarray = [123, 123, 123]
	fromarray = [1, 3, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_54():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [1, 3, 4, 6, 7]
	lenarray = 5
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 3, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_55():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [1, 3, 4, 6, 7]
	lenarray = 5
	size = 9
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 3, 4, 6, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_56():
	toarray = [123, 123]
	fromarray = [1, 4]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [1, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_57():
	toarray = [123, 123, 123, 123]
	fromarray = [2, 0, 0, 1]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 0, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_58():
	toarray = [123, 123, 123, 123]
	fromarray = [2, 0, 0, 1]
	lenarray = 4
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 0, 0, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_59():
	toarray = [123, 123]
	fromarray = [2, 0]
	lenarray = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_60():
	toarray = [123]
	fromarray = [2]
	lenarray = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_61():
	toarray = [123]
	fromarray = [2]
	lenarray = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_62():
	toarray = [123, 123, 123, 123]
	fromarray = [2, 2, 2, 2]
	lenarray = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 2, 2, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_63():
	toarray = [123, 123, 123, 123]
	fromarray = [2, 2, 2, 2]
	lenarray = 4
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 2, 2, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_64():
	toarray = [123, 123]
	fromarray = [2, 2]
	lenarray = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_65():
	toarray = [123, 123]
	fromarray = [2, 3]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_66():
	toarray = [123, 123]
	fromarray = [2, 3]
	lenarray = 2
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_67():
	toarray = [123, 123, 123]
	fromarray = [2, 3, 4]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_68():
	toarray = [123, 123, 123, 123, 123]
	fromarray = [2, 3, 4, 5, 6]
	lenarray = 5
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 3, 4, 5, 6]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_69():
	toarray = [123, 123]
	fromarray = [2, 4]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [2, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_70():
	toarray = [123, 123, 123, 123]
	fromarray = [3, 1, 1, 7]
	lenarray = 4
	size = 10
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3, 1, 1, 7]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_71():
	toarray = [123, 123, 123, 123]
	fromarray = [3, 2, 1, 0]
	lenarray = 4
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3, 2, 1, 0]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_72():
	toarray = [123, 123, 123]
	fromarray = [3, 2, 1]
	lenarray = 3
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3, 2, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_73():
	toarray = [123]
	fromarray = [3]
	lenarray = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_74():
	toarray = [123, 123, 123]
	fromarray = [3, 3, 3]
	lenarray = 3
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3, 3, 3]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_75():
	toarray = [123, 123]
	fromarray = [3, 4]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [3, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_76():
	toarray = [123, 123, 123, 123]
	fromarray = [4, 3, 2, 1]
	lenarray = 4
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [4, 3, 2, 1]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_77():
	toarray = [123, 123, 123]
	fromarray = [4, 3, 2]
	lenarray = 3
	size = 8
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [4, 3, 2]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_78():
	toarray = [123]
	fromarray = [4]
	lenarray = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_79():
	toarray = [123, 123]
	fromarray = [4, 4]
	lenarray = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [4, 4]
	assert toarray == pytest_toarray


def test_awkward_RegularArray_getitem_next_array_regularize_80():
	toarray = [123, 123]
	fromarray = [4, 5]
	lenarray = 2
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_array_regularize')
	funcPy(toarray = toarray,fromarray = fromarray,lenarray = lenarray,size = size)
	pytest_toarray = [4, 5]
	assert toarray == pytest_toarray


