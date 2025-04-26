import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_carrylen_1():
	carrylen = [123]
	slicestarts = []
	slicestops = []
	sliceouterlen = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,slicestarts = slicestarts,slicestops = slicestops,sliceouterlen = sliceouterlen)
	pytest_carrylen = [0]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_2():
	carrylen = [123]
	slicestarts = [0, 2]
	slicestops = [0, 2]
	sliceouterlen = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,slicestarts = slicestarts,slicestops = slicestops,sliceouterlen = sliceouterlen)
	pytest_carrylen = [0]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_3():
	carrylen = [123]
	slicestarts = [2]
	slicestops = [4]
	sliceouterlen = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,slicestarts = slicestarts,slicestops = slicestops,sliceouterlen = sliceouterlen)
	pytest_carrylen = [2]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_4():
	carrylen = [123]
	slicestarts = [1]
	slicestops = [1]
	sliceouterlen = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,slicestarts = slicestarts,slicestops = slicestops,sliceouterlen = sliceouterlen)
	pytest_carrylen = [0]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_5():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 0, 0, 0]
	slicestops = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [0]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_6():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 0, 0]
	slicestops = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [0]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_7():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 0, 1, 1]
	slicestops = [0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [1]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_8():
	carrylen = [123]
	sliceouterlen = 6
	slicestarts = [0, 1, 3, 5, 6, 8]
	slicestops = [1, 3, 5, 6, 8, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [10]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_9():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 5, 5, 6, 8]
	slicestops = [5, 5, 6, 8, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [10]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_10():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 3, 4, 7]
	slicestops = [3, 4, 7, 11]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [11]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_11():
	carrylen = [123]
	sliceouterlen = 6
	slicestarts = [0, 1, 3, 6, 7, 9]
	slicestops = [1, 3, 6, 7, 9, 12]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [12]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_12():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 0, 0]
	slicestops = [0, 0, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [2]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_13():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [2]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_14():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 1, 1]
	slicestops = [1, 1, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [3]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_15():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 1, 1, 2, 2]
	slicestops = [1, 1, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [3]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_16():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [3]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_17():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [3]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_18():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 2, 2]
	slicestops = [2, 2, 2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [4]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_19():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [4]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_20():
	carrylen = [123]
	sliceouterlen = 2
	slicestarts = [0, 3]
	slicestops = [3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [4]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_21():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 1, 1, 3, 3]
	slicestops = [1, 1, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [5]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_22():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 2, 3]
	slicestops = [2, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [5]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_23():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 2, 3, 3]
	slicestops = [2, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [5]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_24():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 3, 3]
	slicestops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [5]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_25():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 4, 5]
	slicestops = [4, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [5]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_26():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 1, 3, 4]
	slicestops = [1, 3, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [6]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_27():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 2, 2]
	slicestops = [2, 2, 2, 2, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [6]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_28():
	carrylen = [123]
	sliceouterlen = 2
	slicestarts = [0, 3]
	slicestops = [3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [6]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_29():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 4, 5]
	slicestops = [4, 5, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [6]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_30():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 4, 6]
	slicestops = [4, 6, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [6]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_31():
	carrylen = [123]
	sliceouterlen = 3
	slicestarts = [0, 2, 5]
	slicestops = [2, 5, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [7]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_32():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 3, 4]
	slicestops = [3, 3, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [7]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_33():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 1, 4, 5]
	slicestops = [1, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [8]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_34():
	carrylen = [123]
	sliceouterlen = 7
	slicestarts = [0, 2, 2, 4, 4, 5, 5]
	slicestops = [2, 2, 4, 4, 5, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [8]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_35():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 4, 5]
	slicestops = [2, 2, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [8]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_36():
	carrylen = [123]
	sliceouterlen = 4
	slicestarts = [0, 3, 0, 3]
	slicestops = [3, 4, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [8]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_37():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 4, 5]
	slicestops = [3, 3, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [8]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_38():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 4, 5]
	slicestops = [2, 2, 4, 5, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [9]
	assert carrylen == pytest_carrylen


def test_awkward_ListArray_getitem_jagged_carrylen_39():
	carrylen = [123]
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 5, 6]
	slicestops = [3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_carrylen')
	funcPy(carrylen = carrylen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_carrylen = [9]
	assert carrylen == pytest_carrylen


