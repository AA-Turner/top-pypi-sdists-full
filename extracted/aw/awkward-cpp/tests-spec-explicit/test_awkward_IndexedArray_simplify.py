import pytest
import numpy
import kernels

def test_awkward_IndexedArray_simplify_1():
	toindex = []
	innerindex = []
	innerlength = 0
	outerindex = [0, 3]
	outerlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	with pytest.raises(Exception):
		funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)


def test_awkward_IndexedArray_simplify_2():
	toindex = []
	innerindex = []
	innerlength = 0
	outerindex = []
	outerlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_3():
	toindex = [123, 123]
	innerindex = [0, 1]
	innerlength = 2
	outerindex = []
	outerlength = 0
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [123, 123]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_4():
	toindex = [123, 123]
	innerindex = [0, 1]
	innerlength = 2
	outerindex = [0, 3]
	outerlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	with pytest.raises(Exception):
		funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)


def test_awkward_IndexedArray_simplify_5():
	toindex = [123, 123]
	innerindex = [0, 1]
	innerlength = 2
	outerindex = [0, 1]
	outerlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_6():
	toindex = [123, 123, 123]
	innerindex = [0, 1, 1, 1, 2]
	innerlength = 5
	outerindex = [0, 1, 2]
	outerlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_7():
	toindex = [123, 123, 123]
	innerindex = [0, 1, 1, 1, 4]
	innerlength = 5
	outerindex = [0, 1, 2]
	outerlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_8():
	toindex = [123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 2]
	innerlength = 3
	outerindex = [0, 1, 1, 1, 1, 2]
	outerlength = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_9():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [0, 1, 2, 1, 1]
	innerlength = 5
	outerindex = [0, 1, 1, 1, 2]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_10():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 1, 2]
	innerlength = 5
	outerindex = [0, 1, 2, 3, 4, 1, 1]
	outerlength = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 1, 2, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_11():
	toindex = [123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 1, 4]
	innerlength = 5
	outerindex = [0, 1, 2, 3, 4, 1, 1]
	outerlength = 7
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 1, 4, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_12():
	toindex = [123, 123, 123, 123]
	innerindex = [0, 1, 2, 1]
	innerlength = 4
	outerindex = [0, 1, 1, 2]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_13():
	toindex = [123, 123, 123, 123]
	innerindex = [0, 1, 1, 2]
	innerlength = 4
	outerindex = [0, 1, 1, 3]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_14():
	toindex = [123, 123, 123, 123]
	innerindex = [0, 1, 1, 2]
	innerlength = 4
	outerindex = [0, 1, 2, 3]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_15():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [0, 1, 2, 3]
	innerlength = 4
	outerindex = [0, 1, 1, 2, 3]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_16():
	toindex = [123, 123, 123, 123]
	innerindex = [0, 1, 2, 3]
	innerlength = 4
	outerindex = [0, 1, 1, 3]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 1, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_17():
	toindex = [123, 123, 123]
	innerindex = [0, 1, 2]
	innerlength = 3
	outerindex = [0, 1, 2]
	outerlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_18():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [0, 1, 2, 3]
	innerlength = 4
	outerindex = [0, 1, 2, 1, 3]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 2, 1, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_19():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [0, 1, 2, 1, 4]
	innerlength = 5
	outerindex = [0, 1, 2, 3, 4]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 2, 1, 4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_20():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 2, 3, 4, 5, 6, 7, 1, 1]
	innerlength = 10
	outerindex = [0, 1, 2, 3, 4, 1, 1, 1, 5, 6, 1, 1, 7, 8, 9, 1]
	outerlength = 16
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [0, 1, 2, 3, 4, 1, 1, 1, 5, 6, 1, 1, 7, 1, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_21():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 2, 1, 1, 3, 4]
	innerlength = 8
	outerindex = [2, 2, 1, 6, 5]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [1, 1, 1, 3, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_22():
	toindex = [123, 123, 123]
	innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
	innerlength = 11
	outerindex = [0, 3, 6]
	outerlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [13, 4, 15]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_23():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
	innerlength = 11
	outerindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	outerlength = 9
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [13, 9, 13, 4, 8, 3, 15, 1, 16]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_24():
	toindex = [123, 123, 123, 123, 123, 123]
	innerindex = [13, 9, 13, 4, 8, 3, 15, 1, 16, 2, 8]
	innerlength = 11
	outerindex = [0, 1, 3, 4, 6, 7]
	outerlength = 6
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [13, 9, 4, 8, 15, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_25():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [2, 1, 1, 0]
	innerlength = 4
	outerindex = [0, 1, 2, 1, 3]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [2, 1, 1, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_26():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [3, 1, 1, 7]
	innerlength = 4
	outerindex = [0, 1, 1, 2, 3]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [3, 1, 1, 1, 7]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_27():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [3, 1, 2, 1]
	innerlength = 4
	outerindex = [0, 1, 2, 1, 3]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [3, 1, 2, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_28():
	toindex = [123]
	innerindex = [4, 3, 2, 1, 0]
	innerlength = 5
	outerindex = [0]
	outerlength = 1
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_29():
	toindex = [123, 123]
	innerindex = [4, 3, 2, 1, 0]
	innerlength = 5
	outerindex = [0, 1]
	outerlength = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 3]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_30():
	toindex = [123, 123, 123, 123]
	innerindex = [4, 5, 6, 7, 3, 1, 2, 0, 1, 1]
	innerlength = 10
	outerindex = [0, 4, 5, 7]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 3, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_31():
	toindex = [123, 123, 123]
	innerindex = [4, 3, 2, 1, 0]
	innerlength = 5
	outerindex = [0, 1, 2]
	outerlength = 3
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 3, 2]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_32():
	toindex = [123, 123, 123, 123, 123]
	innerindex = [4, 3, 2, 1, 0]
	innerlength = 5
	outerindex = [0, 1, 2, 3, 4]
	outerlength = 5
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 3, 2, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_33():
	toindex = [123, 123, 123, 123]
	innerindex = [4, 3, 2, 1, 0]
	innerlength = 5
	outerindex = [0, 1, 2, 3]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 3, 2, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_34():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
	innerlength = 10
	outerindex = [6, 7, 8, 9, 5, 1, 1, 1, 3, 4, 1, 1, 0, 1, 2, 1]
	outerlength = 16
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 5, 6, 7, 3, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_35():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
	innerlength = 10
	outerindex = [6, 7, 8, 9, 5, 1, 1, 3, 4, 1, 0, 1, 2]
	outerlength = 13
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 5, 6, 7, 3, 1, 1, 1, 2, 1, 0, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_36():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	innerindex = [0, 1, 1, 1, 2, 3, 4, 5, 6, 7]
	innerlength = 10
	outerindex = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
	outerlength = 10
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [4, 5, 6, 7, 3, 1, 2, 0, 1, 1]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_37():
	toindex = [123, 123, 123, 123]
	innerindex = [6, 5, 1, 3, 1, 1, 0]
	innerlength = 7
	outerindex = [0, 2, 4, 6]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [6, 1, 1, 0]
	assert toindex == pytest_toindex


def test_awkward_IndexedArray_simplify_38():
	toindex = [123, 123, 123, 123]
	innerindex = [6, 5, 4, 3, 2, 1, 0]
	innerlength = 7
	outerindex = [0, 2, 4, 6]
	outerlength = 4
	funcPy = getattr(kernels, 'awkward_IndexedArray_simplify')
	funcPy(toindex = toindex,innerindex = innerindex,innerlength = innerlength,outerindex = outerindex,outerlength = outerlength)
	pytest_toindex = [6, 4, 2, 0]
	assert toindex == pytest_toindex


