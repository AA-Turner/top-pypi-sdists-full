import pytest
import numpy
import kernels

def test_awkward_IndexedArray_validity_1():
	index = []
	isoption = True
	lencontent = 3
	length = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_2():
	index = []
	isoption = True
	lencontent = 0
	length = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_3():
	index = [0, 1, 1, 1, 1, 3]
	isoption = True
	lencontent = 0
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	with pytest.raises(Exception):
		funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_4():
	index = [0, 1, 1, 1, 1, 3]
	isoption = True
	lencontent = 3
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	with pytest.raises(Exception):
		funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_5():
	index = [2, -4, 4, 0, 8]
	isoption = False
	lencontent = 10
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	with pytest.raises(Exception):
		funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_6():
	index = [0, 1, 1, 1, 1, 2]
	isoption = True
	lencontent = 3
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_7():
	index = [0, 1, 1, 1, 1]
	isoption = True
	lencontent = 2
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_8():
	index = [0, 1, 1, 1, 2, 3, 4]
	isoption = True
	lencontent = 5
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_9():
	index = [0, 1, 1, 1, 2, 3]
	isoption = True
	lencontent = 4
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_10():
	index = [0, 1, 1, 1, 2]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_11():
	index = [0, 1, 1, 1]
	isoption = True
	lencontent = 2
	length = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_12():
	index = [0, 1, 1, 2, 1, 3]
	isoption = True
	lencontent = 4
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_13():
	index = [0, 1, 1, 2, 1]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_14():
	index = [0, 1, 1, 2, 3, 1, 4, 5, 6]
	isoption = True
	lencontent = 7
	length = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_15():
	index = [0, 1, 1, 2, 3, 4, 1, 5]
	isoption = True
	lencontent = 6
	length = 8
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_16():
	index = [0, 1, 1, 2, 3, 4, 5, 6, 7]
	isoption = True
	lencontent = 8
	length = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_17():
	index = [0, 1, 1, 2, 3, 4, 5]
	isoption = True
	lencontent = 6
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_18():
	index = [0, 1, 1, 2, 3]
	isoption = True
	lencontent = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_19():
	index = [0, 1, 1, 2]
	isoption = True
	lencontent = 3
	length = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_20():
	index = [0, 1, 1]
	isoption = True
	lencontent = 2
	length = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_21():
	index = [0, 1, 2, 1, 1]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_22():
	index = [0, 1, 2, 1, 3, 1, 4]
	isoption = True
	lencontent = 5
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_23():
	index = [0, 1, 2, 1, 3]
	isoption = True
	lencontent = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_24():
	index = [0, 1, 2, 1]
	isoption = True
	lencontent = 3
	length = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_25():
	index = [0, 1, 2, 3, 1, 4, 5, 6, 7, 8, 1, 9]
	isoption = True
	lencontent = 10
	length = 12
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_26():
	index = [0, 1, 2, 3, 1, 4, 5, 6]
	isoption = True
	lencontent = 7
	length = 8
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_27():
	index = [0, 1, 2, 3, 1, 4]
	isoption = True
	lencontent = 5
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_28():
	index = [0, 1, 2, 3, 1]
	isoption = True
	lencontent = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_29():
	index = [1, 0, 1, 1, 1]
	isoption = True
	lencontent = 2
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_30():
	index = [1, 0, 1, 1, 2]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_31():
	index = [1, 0, 1, 2, 1, 3]
	isoption = True
	lencontent = 4
	length = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_32():
	index = [1, 0, 1, 2, 1]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_33():
	index = [1, 0, 1, 2, 3]
	isoption = True
	lencontent = 4
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_34():
	index = [1, 0, 1, 2]
	isoption = True
	lencontent = 3
	length = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_35():
	index = [1, 1, 0, 1, 1]
	isoption = True
	lencontent = 2
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_36():
	index = [1, 1, 0, 1, 2]
	isoption = True
	lencontent = 3
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_37():
	index = [1, 1, 1, 0, 1]
	isoption = True
	lencontent = 2
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_38():
	index = [1, 4, 4, 1, 0]
	isoption = True
	lencontent = 10
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_39():
	index = [2, 1, 4, 0, 8]
	isoption = True
	lencontent = 10
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_40():
	index = [2, 2, 0, 1, 4]
	isoption = True
	lencontent = 5
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_41():
	index = [2, 4, 4, 0, 8]
	isoption = False
	lencontent = 10
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_42():
	index = [6, 4, 4, 8, 0]
	isoption = False
	lencontent = 10
	length = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


def test_awkward_IndexedArray_validity_43():
	index = [6, 5, 4, 3, 2, 1, 0]
	isoption = False
	lencontent = 7
	length = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_validity')
	funcPy(index = index,isoption = isoption,lencontent = lencontent,length = length)


