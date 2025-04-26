import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_array_advanced_1():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [0, 0]
	fromstarts = [0, 0]
	fromstops = [-1, 1]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_advanced_2():
	toadvanced = [123]
	tocarry = [123]
	fromadvanced = [0]
	fromarray = [0]
	fromstarts = [0]
	fromstops = [5]
	lencontent = 4
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_advanced_3():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -4, 1]
	fromstarts = [0, 0, 0, 0]
	fromstops = [3, 3, 3, 3]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	with pytest.raises(Exception):
		funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_array_advanced_4():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [0, 0]
	fromstarts = [0, 0]
	fromstops = [1, 1]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [0, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_5():
	toadvanced = [123]
	tocarry = [123]
	fromadvanced = [0]
	fromarray = [0]
	fromstarts = [0]
	fromstops = [2]
	lencontent = 4
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0]
	pytest_tocarry = [0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_6():
	toadvanced = []
	tocarry = []
	fromadvanced = []
	fromarray = []
	fromstarts = []
	fromstops = []
	lencontent = 0
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = []
	pytest_tocarry = []
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_7():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [0, 0, 0, 0]
	fromstops = [3, 3, 3, 3]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 1, 2, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_8():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 0, 0, 0]
	fromstarts = [0, 3, 3, 3]
	fromstops = [3, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [0, 3, 3, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_9():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [1, 0]
	fromstarts = [0, 0]
	fromstops = [3, 3]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_10():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [0, 0, 0, 0]
	fromstops = [3, 3, 3, 3]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 0, 0, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_11():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [0, 0]
	fromstarts = [1, 0]
	fromstops = [3, 2]
	lencontent = 3
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_12():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [10, 10, 10, 10]
	fromstops = [15, 15, 15, 15]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [10, 11, 14, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_13():
	toadvanced = [123]
	tocarry = [123]
	fromadvanced = [0]
	fromarray = [0]
	fromstarts = [1]
	fromstops = [3]
	lencontent = 3
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0]
	pytest_tocarry = [1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_14():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [10, 10, 10, 10]
	fromstops = [15, 15, 15, 15]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [11, 10, 10, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_15():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, -2, 0, -1]
	fromstarts = [10, 10, 10, 10]
	fromstops = [15, 15, 15, 15]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [11, 13, 10, 14]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_16():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, -2, 0, -1]
	fromstarts = [10, 0, 0, 5]
	fromstops = [15, 5, 5, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [11, 3, 0, 9]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_17():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [0, 15, 15, 15]
	fromstops = [5, 20, 20, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 15, 15, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_18():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [1, 2]
	fromstarts = [0, 0]
	fromstops = [3, 3]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [1, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_19():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [2, 0, 0, 1]
	fromstarts = [10, 10, 10, 10]
	fromstops = [15, 15, 15, 15]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [12, 10, 10, 11]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_20():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [2, 2, 2, 2]
	fromstarts = [10, 0, 0, 5]
	fromstops = [15, 5, 5, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [12, 2, 2, 7]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_21():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-2, -2, -2, -2]
	fromstarts = [10, 10, 10, 10]
	fromstops = [15, 15, 15, 15]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [13, 13, 13, 13]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_22():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-2, -2, -2, -2]
	fromstarts = [10, 0, 0, 5]
	fromstops = [15, 5, 5, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [13, 3, 3, 8]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_23():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [0, 3, 3, 3]
	fromstops = [3, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 3, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_24():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [0, 5, 10, 5]
	fromstops = [5, 10, 15, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [1, 5, 10, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_25():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [15, 0, 0, 15]
	fromstops = [20, 5, 5, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [15, 1, 4, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_26():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [15, 15, 15, 15]
	fromstops = [20, 20, 20, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [15, 16, 19, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_27():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [15, 15, 15, 15]
	fromstops = [20, 20, 20, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [16, 15, 15, 16]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_28():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [15, 0, 0, 15]
	fromstops = [20, 5, 5, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [19, 4, 4, 19]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_29():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [-1, 0]
	fromstarts = [0, 0]
	fromstops = [3, 3]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_30():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [0, 0, 0, 0]
	fromstops = [3, 3, 3, 3]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 2, 2, 2]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_31():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [1, 2]
	fromstarts = [1, 1]
	fromstops = [4, 4]
	lencontent = 4
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [2, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_32():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [0, 3, 3, 3]
	fromstops = [3, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [2, 5, 5, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_33():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 0, 0, 0]
	fromstarts = [3, 0, 0, 3]
	fromstops = [6, 3, 3, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 0, 0, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_34():
	toadvanced = [123]
	tocarry = [123]
	fromadvanced = [0]
	fromarray = [1]
	fromstarts = [2]
	fromstops = [5]
	lencontent = 5
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0]
	pytest_tocarry = [3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_35():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [-1, 0]
	fromstarts = [1, 1]
	fromstops = [4, 4]
	lencontent = 4
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [3, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_36():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [3, 0, 0, 3]
	fromstops = [6, 3, 3, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 1, 2, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_37():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 0, 0, 0]
	fromstarts = [3, 3, 3, 3]
	fromstops = [6, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 3, 3, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_38():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [3, 3, 3, 3]
	fromstops = [6, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [3, 4, 5, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_39():
	toadvanced = [123, 123]
	tocarry = [123, 123]
	fromadvanced = [0, 1]
	fromarray = [1, 1]
	fromstarts = [3, 0]
	fromstops = [5, 3]
	lencontent = 5
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1]
	pytest_tocarry = [4, 1]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_40():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 1, 0, 0]
	fromstarts = [3, 0, 0, 6]
	fromstops = [5, 3, 3, 9]
	lencontent = 9
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 1, 0, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_41():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [0, 15, 15, 15]
	fromstops = [5, 20, 20, 20]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 19, 19, 19]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_42():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, -1, 0, 0]
	fromstarts = [3, 0, 0, 3]
	fromstops = [5, 3, 3, 5]
	lencontent = 5
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 2, 0, 3]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_43():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 0, 0, 1]
	fromstarts = [3, 3, 3, 3]
	fromstops = [6, 6, 6, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 3, 3, 4]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_44():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [0, 5, 10, 5]
	fromstops = [5, 10, 15, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [4, 9, 14, 9]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_45():
	toadvanced = [123, 123, 123, 123, 123, 123]
	tocarry = [123, 123, 123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3, 4, 5]
	fromarray = [2, 0, 1, 1, 2, 0]
	fromstarts = [3, 0, 3, 3, 3, 0]
	fromstops = [6, 3, 6, 6, 6, 3]
	lencontent = 6
	lenstarts = 6
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3, 4, 5]
	pytest_tocarry = [5, 0, 4, 4, 5, 0]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_46():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [0, 1, -1, 1]
	fromstarts = [5, 0, 0, 5]
	fromstops = [10, 5, 5, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [5, 1, 4, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_47():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [3, 0, 0, 3]
	fromstops = [6, 3, 3, 6]
	lencontent = 6
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [5, 2, 2, 5]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_48():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [1, 1, 0, 0]
	fromstarts = [6, 0, 0, 6]
	fromstops = [9, 3, 3, 9]
	lencontent = 9
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [7, 1, 0, 6]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_array_advanced_49():
	toadvanced = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromadvanced = [0, 1, 2, 3]
	fromarray = [-1, -1, -1, -1]
	fromstarts = [5, 0, 0, 5]
	fromstops = [10, 5, 5, 10]
	lencontent = 30
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_array_advanced')
	funcPy(toadvanced = toadvanced,tocarry = tocarry,fromadvanced = fromadvanced,fromarray = fromarray,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,lenstarts = lenstarts)
	pytest_toadvanced = [0, 1, 2, 3]
	pytest_tocarry = [9, 4, 4, 9]
	assert toadvanced == pytest_toadvanced
	assert tocarry == pytest_tocarry


