import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_next_at_1():
	tocarry = [123]
	at = -2
	length = 1
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,at = at,length = length,size = size)


def test_awkward_RegularArray_getitem_next_at_2():
	tocarry = [123, 123]
	at = 6
	length = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,at = at,length = length,size = size)


def test_awkward_RegularArray_getitem_next_at_3():
	tocarry = [123]
	at = 0
	length = 1
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_4():
	tocarry = []
	at = 0
	length = 0
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_5():
	tocarry = [123]
	at = 0
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_6():
	tocarry = [123]
	at = 0
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_7():
	tocarry = [123]
	at = 0
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_8():
	tocarry = [123]
	at = 0
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_9():
	tocarry = [123, 123]
	at = 0
	length = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [0, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_10():
	tocarry = [123]
	at = 1
	length = 1
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_11():
	tocarry = [123]
	at = 1
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_12():
	tocarry = [123]
	at = 1
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_13():
	tocarry = [123]
	at = 1
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_14():
	tocarry = [123]
	at = 1
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_15():
	tocarry = [123, 123]
	at = 1
	length = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [1, 6]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_16():
	tocarry = [123]
	at = 2
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_17():
	tocarry = [123]
	at = 2
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_18():
	tocarry = [123]
	at = 2
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_19():
	tocarry = [123]
	at = 2
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_20():
	tocarry = [123, 123, 123, 123, 123]
	at = 2
	length = 5
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [2, 7, 12, 17, 22]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_21():
	tocarry = [123]
	at = 3
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_22():
	tocarry = [123]
	at = 3
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [3]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_23():
	tocarry = [123]
	at = 4
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_getitem_next_at_24():
	tocarry = [123]
	at = 4
	length = 1
	size = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,length = length,size = size)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


