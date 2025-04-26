import pytest
import numpy
import kernels

def test_awkward_IndexedArray_getitem_nextcarry_1():
	tocarry = []
	fromindex = []
	lencontent = 0
	lenindex = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_2():
	tocarry = []
	fromindex = [0, 1]
	lencontent = 0
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_getitem_nextcarry_3():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 1, 0, 2, 0]
	lencontent = 1
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)


def test_awkward_IndexedArray_getitem_nextcarry_4():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 0, 0, 0, 0]
	lencontent = 1
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0, 0, 0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_5():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 0, 0, 0]
	lencontent = 1
	lenindex = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0, 0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_6():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 0, 0]
	lencontent = 1
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_7():
	tocarry = [123, 123, 123]
	fromindex = [0, 0, 0]
	lencontent = 1
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_8():
	tocarry = [123, 123]
	fromindex = [0, 0]
	lencontent = 1
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_9():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 1, 1, 1, 2, 2, 2]
	lencontent = 3
	lenindex = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0, 1, 1, 1, 2, 2, 2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_10():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [0, 0, 0, 2, 3, 3, 4]
	lencontent = 5
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 0, 0, 2, 3, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_11():
	tocarry = [123, 123]
	fromindex = [0, 1]
	lencontent = 2
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_12():
	tocarry = [123, 123, 123]
	fromindex = [0, 1, 2]
	lencontent = 3
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_13():
	tocarry = [123, 123, 123, 123]
	fromindex = [0, 1, 2, 3]
	lencontent = 4
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_14():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, 3, 4]
	lencontent = 5
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_15():
	tocarry = [123, 123, 123]
	fromindex = [1, 1, 1]
	lencontent = 6
	lenindex = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [1, 1, 1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_16():
	tocarry = [123]
	fromindex = [1]
	lencontent = 5
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_17():
	tocarry = [123]
	fromindex = [1]
	lencontent = 6
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_18():
	tocarry = [123, 123]
	fromindex = [1, 2]
	lencontent = 3
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_19():
	tocarry = [123, 123]
	fromindex = [1, 3]
	lencontent = 6
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [1, 3]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_20():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromindex = [2, 1, 0, 3, 3, 4]
	lencontent = 5
	lenindex = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2, 1, 0, 3, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_21():
	tocarry = [123, 123, 123, 123]
	fromindex = [2, 2, 1, 0]
	lencontent = 3
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2, 2, 1, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_22():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [2, 2, 1, 0, 3]
	lencontent = 4
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2, 2, 1, 0, 3]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_23():
	tocarry = [123]
	fromindex = [2]
	lencontent = 3
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_24():
	tocarry = [123]
	fromindex = [2]
	lencontent = 5
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_25():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [2, 4, 4, 0, 8]
	lencontent = 10
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [2, 4, 4, 0, 8]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_26():
	tocarry = [123, 123, 123, 123]
	fromindex = [3, 2, 1, 0]
	lencontent = 4
	lenindex = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [3, 2, 1, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_27():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [4, 3, 2, 1, 0]
	lencontent = 5
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [4, 3, 2, 1, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_28():
	tocarry = [123]
	fromindex = [4]
	lencontent = 5
	lenindex = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_29():
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [6, 4, 4, 8, 0]
	lencontent = 10
	lenindex = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [6, 4, 4, 8, 0]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_getitem_nextcarry_30():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromindex = [6, 5, 4, 3, 2, 1, 0]
	lencontent = 7
	lenindex = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_getitem_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [6, 5, 4, 3, 2, 1, 0]
	assert tocarry == pytest_tocarry


