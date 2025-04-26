import pytest
import numpy
import kernels

def test_awkward_ListArray_broadcast_tooffsets_1():
	tocarry = []
	fromoffsets = []
	fromstarts = []
	fromstops = []
	lencontent = 0
	offsetslength = 0
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_2():
	tocarry = [123]
	fromoffsets = [0, 1]
	fromstarts = [0]
	fromstops = [1]
	lencontent = 1
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_3():
	tocarry = []
	fromoffsets = [0, 1]
	fromstarts = [0]
	fromstops = [2]
	lencontent = 1
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)


def test_awkward_ListArray_broadcast_tooffsets_4():
	tocarry = []
	fromoffsets = [2, 1]
	fromstarts = [0]
	fromstops = [1]
	lencontent = 1
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)


def test_awkward_ListArray_broadcast_tooffsets_5():
	tocarry = []
	fromoffsets = [0, 2]
	fromstarts = [0]
	fromstops = [1]
	lencontent = 1
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)


def test_awkward_ListArray_broadcast_tooffsets_6():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
	fromstarts = [0, 0, 0, 0, 0, 0, 4, 4, 4, 4]
	fromstops = [2, 2, 2, 2, 2, 2, 5, 5, 5, 5]
	lencontent = 5
	offsetslength = 11
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 4, 4, 4, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_7():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10]
	fromstarts = [0, 0, 0, 3, 3]
	fromstops = [2, 2, 2, 5, 5]
	lencontent = 5
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_8():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	fromstarts = [0, 0, 0, 3, 3, 5, 5, 5, 8, 8]
	fromstops = [2, 2, 2, 5, 5, 7, 7, 7, 10, 10]
	lencontent = 10
	offsetslength = 11
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 0, 1, 0, 1, 3, 4, 3, 4, 5, 6, 5, 6, 5, 6, 8, 9, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_9():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 15, 18, 21]
	fromstarts = [0, 0, 0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3, 3, 3]
	lencontent = 3
	offsetslength = 8
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_10():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 15, 18]
	fromstarts = [0, 0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3, 3]
	lencontent = 3
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_11():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 15]
	fromstarts = [0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3]
	lencontent = 3
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_12():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9]
	fromstarts = [0, 0, 0]
	fromstops = [3, 3, 3]
	lencontent = 3
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_13():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6]
	fromstarts = [0, 0]
	fromstops = [3, 3]
	lencontent = 3
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_14():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 3, 3]
	fromstarts = [0, 3]
	fromstops = [3, 3]
	lencontent = 20
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_15():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 8, 13, 18, 23, 28]
	fromstarts = [0, 13, 3, 18, 8, 23]
	fromstops = [3, 18, 8, 23, 13, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 13, 14, 15, 16, 17, 3, 4, 5, 6, 7, 18, 19, 20, 21, 22, 8, 9, 10, 11, 12, 23, 24, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_16():
	tocarry = [123, 123, 123, 123]
	fromoffsets = [0, 2, 4]
	fromstarts = [0, 2]
	fromstops = [2, 4]
	lencontent = 4
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_17():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 9, 13, 18, 23, 28]
	fromstarts = [0, 13, 4, 18, 8, 23]
	fromstops = [4, 18, 8, 23, 13, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 13, 14, 15, 16, 17, 4, 5, 6, 7, 18, 19, 20, 21, 22, 8, 9, 10, 11, 12, 23, 24, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_18():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 9, 14, 19, 24, 29]
	fromstarts = [0, 14, 4, 19, 9, 24]
	fromstops = [4, 19, 9, 24, 14, 29]
	lencontent = 29
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 14, 15, 16, 17, 18, 4, 5, 6, 7, 8, 19, 20, 21, 22, 23, 9, 10, 11, 12, 13, 24, 25, 26, 27, 28]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_19():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 18, 21, 24, 29]
	fromstarts = [0, 0, 0, 8, 11, 11, 14]
	fromstops = [5, 5, 5, 11, 14, 14, 19]
	lencontent = 19
	offsetslength = 8
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 11, 12, 13, 14, 15, 16, 17, 18]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_20():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 4, 5]
	fromstarts = [0, 3, 3, 4]
	fromstops = [3, 3, 4, 5]
	lencontent = 5
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_21():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5]
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	lencontent = 10
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_22():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5]
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	lencontent = 5
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_23():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 5, 8]
	fromstarts = [0, 3, 3, 10, 10]
	fromstops = [3, 3, 5, 10, 13]
	lencontent = 13
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_24():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20]
	fromstarts = [0, 10, 15, 25]
	fromstops = [5, 15, 20, 30]
	lencontent = 30
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_25():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 11, 12, 17, 22]
	fromstarts = [0, 11, 5, 16, 6, 17]
	fromstops = [5, 16, 6, 17, 11, 22]
	lencontent = 22
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 11, 12, 13, 14, 15, 5, 16, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_26():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 14, 18, 23, 28]
	fromstarts = [0, 14, 5, 19, 9, 23]
	fromstops = [5, 19, 9, 23, 14, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 14, 15, 16, 17, 18, 5, 6, 7, 8, 19, 20, 21, 22, 9, 10, 11, 12, 13, 23, 24, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_27():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 24, 28]
	fromstarts = [0, 14, 5, 19, 10, 24]
	fromstops = [5, 19, 10, 24, 14, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 14, 15, 16, 17, 18, 5, 6, 7, 8, 9, 19, 20, 21, 22, 23, 10, 11, 12, 13, 24, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_28():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 6, 10]
	fromstarts = [0, 3, 3, 15, 16]
	fromstops = [3, 3, 5, 16, 20]
	lencontent = 20
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_29():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20]
	fromstarts = [0, 15, 10, 25]
	fromstops = [5, 20, 15, 30]
	lencontent = 30
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_30():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 19, 24, 28]
	fromstarts = [0, 15, 5, 20, 10, 24]
	fromstops = [5, 20, 10, 24, 15, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 10, 11, 12, 13, 14, 24, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_31():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 28]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 28]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_32():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 29]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 29]
	lencontent = 29
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_33():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 30]
	lencontent = 30
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_34():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [0, 45, 5, 50, 10, 55]
	fromstops = [5, 50, 10, 55, 15, 60]
	lencontent = 60
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 45, 46, 47, 48, 49, 5, 6, 7, 8, 9, 50, 51, 52, 53, 54, 10, 11, 12, 13, 14, 55, 56, 57, 58, 59]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_35():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6]
	fromstarts = [0, 3]
	fromstops = [3, 6]
	lencontent = 25
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_36():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6]
	fromstarts = [0, 3]
	fromstops = [3, 6]
	lencontent = 6
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_37():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 10, 14, 17]
	fromstarts = [0, 3, 10, 14, 18]
	fromstops = [3, 6, 14, 18, 21]
	lencontent = 21
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_38():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 15]
	fromstarts = [0, 3, 11, 14, 17]
	fromstops = [3, 6, 14, 17, 20]
	lencontent = 20
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_39():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 15]
	fromstarts = [0, 3, 11, 14, 17]
	fromstops = [3, 6, 14, 17, 20]
	lencontent = 25
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_40():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 10, 14, 17]
	fromstarts = [0, 3, 11, 15, 19]
	fromstops = [3, 6, 15, 19, 22]
	lencontent = 22
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_41():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 4, 6, 7]
	fromstarts = [0, 3, 3, 4, 6]
	fromstops = [3, 3, 4, 6, 7]
	lencontent = 7
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_42():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 7]
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 7]
	lencontent = 7
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_43():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 7]
	fromstarts = [0, 3]
	fromstops = [3, 7]
	lencontent = 7
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_44():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 6, 10]
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 10]
	lencontent = 10
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_45():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 8, 8, 10]
	fromstarts = [0, 3, 3, 5, 8, 8]
	fromstops = [3, 3, 5, 8, 8, 10]
	lencontent = 10
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_46():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10]
	fromstarts = [0, 5]
	fromstops = [5, 10]
	lencontent = 10
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_47():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 7, 7, 9, 9, 11]
	fromstarts = [0, 4, 7, 7, 9, 9]
	fromstops = [4, 7, 7, 9, 9, 11]
	lencontent = 11
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_48():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 8, 12, 16, 19]
	fromstarts = [0, 3, 8, 12, 16]
	fromstops = [3, 8, 12, 16, 19]
	lencontent = 19
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_49():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 11, 15, 19, 22]
	fromstarts = [0, 3, 6, 11, 15, 19]
	fromstops = [3, 6, 11, 15, 19, 22]
	lencontent = 22
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_50():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [0, 5, 10, 15, 20, 25]
	fromstops = [5, 10, 15, 20, 25, 30]
	lencontent = 30
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_51():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	fromstarts = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203]
	fromstops = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	lencontent = 210
	offsetslength = 31
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_52():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [0, 5, 10, 45, 50, 55]
	fromstops = [5, 10, 15, 50, 55, 60]
	lencontent = 60
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_53():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 11, 15, 19, 22]
	fromstarts = [0, 3, 8, 13, 17, 21]
	fromstops = [3, 6, 13, 17, 21, 24]
	lencontent = 24
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_54():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 8, 11, 14, 19]
	fromstarts = [0, 8, 11, 11, 14]
	fromstops = [5, 11, 14, 14, 19]
	lencontent = 19
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 11, 12, 13, 14, 15, 16, 17, 18]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_55():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 8, 9]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	lencontent = 10
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 4, 5, 5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_56():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 5, 6, 7, 7, 9]
	fromstarts = [0, 4, 6, 3, 6, 7]
	fromstops = [3, 6, 7, 4, 6, 9]
	lencontent = 9
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 4, 5, 6, 3, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_57():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 5, 6, 7, 9]
	fromstarts = [0, 4, 6, 3, 7]
	fromstops = [3, 6, 7, 4, 9]
	lencontent = 9
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 4, 5, 6, 3, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_58():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 3, 4, 5, 6, 8]
	fromstarts = [0, 2, 4, 5, 6, 9]
	fromstops = [2, 3, 5, 6, 7, 11]
	lencontent = 11
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 4, 5, 6, 9, 10]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_59():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 6, 8]
	fromstarts = [0, 4, 4, 6, 9]
	fromstops = [3, 4, 6, 7, 11]
	lencontent = 11
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 4, 5, 6, 9, 10]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_60():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 7]
	lencontent = 7
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_61():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 7]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 9]
	lencontent = 9
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_62():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 7]
	fromstarts = [0, 5]
	fromstops = [3, 9]
	lencontent = 9
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_63():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 5, 7, 8, 9, 10]
	fromstarts = [0, 6, 3, 8, 5, 9]
	fromstops = [3, 8, 5, 9, 6, 10]
	lencontent = 10
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 6, 7, 3, 4, 8, 5, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_64():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 5, 5, 6, 8, 9]
	fromstarts = [0, 6, 3, 8, 3, 5]
	fromstops = [3, 8, 3, 9, 5, 6]
	lencontent = 9
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 6, 7, 8, 3, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_65():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 7]
	fromstarts = [0, 3, 6]
	fromstops = [3, 3, 10]
	lencontent = 10
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_66():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 5, 6, 6, 6]
	fromstarts = [0, 3, 2, 5, 3, 6]
	fromstops = [2, 5, 3, 6, 3, 6]
	lencontent = 6
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 3, 4, 2, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_67():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 2, 4, 5, 6]
	fromstarts = [0, 3, 3, 5, 8]
	fromstops = [2, 3, 5, 6, 9]
	lencontent = 9
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 3, 4, 5, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_68():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9]
	fromstarts = [11, 14, 17]
	fromstops = [14, 17, 20]
	lencontent = 25
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [11, 12, 13, 14, 15, 16, 17, 18, 19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_69():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [1, 16, 6, 21, 11, 26]
	fromstops = [6, 21, 11, 26, 16, 31]
	lencontent = 31
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 11, 12, 13, 14, 15, 26, 27, 28, 29, 30]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_70():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5]
	fromstarts = [1, 99, 5]
	fromstops = [4, 99, 7]
	lencontent = 7
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [1, 2, 3, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_71():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20]
	fromstarts = [15, 10, 5, 0]
	fromstops = [20, 15, 10, 5]
	lencontent = 20
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_72():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20]
	fromstarts = [15, 5, 10, 0]
	fromstops = [20, 10, 15, 5]
	lencontent = 20
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [15, 16, 17, 18, 19, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_73():
	tocarry = [123, 123, 123, 123]
	fromoffsets = [0, 4]
	fromstarts = [16]
	fromstops = [20]
	lencontent = 20
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [16, 17, 18, 19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_74():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 0, 1, 3]
	fromstarts = [2, 2, 3]
	fromstops = [2, 3, 5]
	lencontent = 5
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_75():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 1, 2, 3]
	fromstarts = [2, 4, 5]
	fromstops = [3, 5, 6]
	lencontent = 6
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [2, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_76():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [25, 10, 20, 5, 15, 0]
	fromstops = [30, 15, 25, 10, 20, 5]
	lencontent = 30
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [25, 26, 27, 28, 29, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_77():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	fromstarts = [25, 20, 15, 10, 5, 0]
	fromstops = [30, 25, 20, 15, 10, 5]
	lencontent = 30
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [25, 26, 27, 28, 29, 20, 21, 22, 23, 24, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_78():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 2, 5, 7]
	fromstarts = [3, 3, 3, 0, 4]
	fromstops = [4, 4, 3, 3, 6]
	lencontent = 6
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 3, 0, 1, 2, 4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_79():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 2, 5, 6, 7, 11]
	fromstarts = [3, 3, 0, 5, 5, 6]
	fromstops = [5, 3, 3, 6, 6, 10]
	lencontent = 10
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 0, 1, 2, 5, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_80():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 2, 3]
	fromstarts = [3, 15]
	fromstops = [5, 16]
	lencontent = 20
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 15]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_81():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 4, 7]
	fromstarts = [3, 3, 3, 0]
	fromstops = [5, 5, 3, 3]
	lencontent = 5
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 3, 4, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_82():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 7, 7, 9, 9, 11]
	fromstarts = [3, 0, 999, 2, 6, 10]
	fromstops = [7, 3, 999, 4, 6, 12]
	lencontent = 12
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 5, 6, 0, 1, 2, 2, 3, 10, 11]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_83():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 2, 2, 2, 6]
	fromstarts = [3, 5, 5, 5, 5]
	fromstops = [5, 5, 5, 5, 9]
	lencontent = 9
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_84():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6, 9, 12, 14, 16]
	fromstarts = [3, 6, 17, 20, 11, 25]
	fromstops = [6, 9, 20, 23, 13, 27]
	lencontent = 28
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 11, 12, 25, 26]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_85():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 8, 12, 16, 19]
	fromstarts = [3, 6, 11, 15, 19]
	fromstops = [6, 11, 15, 19, 22]
	lencontent = 22
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_86():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 0, 2, 6]
	fromstarts = [3, 3, 6]
	fromstops = [3, 5, 10]
	lencontent = 10
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_87():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 6]
	fromstarts = [3, 6]
	fromstops = [5, 10]
	lencontent = 10
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [3, 4, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_88():
	tocarry = [123, 123]
	fromoffsets = [0, 0, 2]
	fromstarts = [4, 4]
	fromstops = [4, 6]
	lencontent = 6
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [4, 5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_89():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 0, 2, 7]
	fromstarts = [4, 4, 7]
	fromstops = [4, 6, 12]
	lencontent = 12
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [4, 5, 7, 8, 9, 10, 11]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_90():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 5, 5, 7, 7, 11]
	fromstarts = [5, 5, 0, 3, 3, 6, 6]
	fromstops = [6, 6, 3, 3, 5, 6, 10]
	lencontent = 10
	offsetslength = 8
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [5, 5, 0, 1, 2, 3, 4, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_91():
	tocarry = [123, 123, 123, 123]
	fromoffsets = [0, 0, 1, 4]
	fromstarts = [5, 5, 6]
	fromstops = [5, 6, 9]
	lencontent = 9
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [5, 6, 7, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_92():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 1, 5]
	fromstarts = [5, 6, 6]
	fromstops = [6, 6, 10]
	lencontent = 10
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_93():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 5]
	fromstarts = [5, 6]
	fromstops = [6, 10]
	lencontent = 10
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_94():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 4, 6, 6, 9]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [9, 6, 5, 3, 3]
	lencontent = 9
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 5, 3, 4, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_95():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 4, 7, 10]
	fromstarts = [6, 5, 6, 0]
	fromstops = [9, 6, 9, 3]
	lencontent = 9
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 5, 6, 7, 8, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_96():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 1, 6]
	fromstarts = [6, 7, 7]
	fromstops = [7, 7, 12]
	lencontent = 12
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 9, 10, 11]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_97():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 8, 11, 14, 19]
	fromstarts = [6, 11, 14, 17, 20]
	fromstops = [11, 14, 17, 20, 25]
	lencontent = 25
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_98():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 5, 7, 10]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	lencontent = 10
	offsetslength = 5
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_broadcast_tooffsets_99():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 5, 7, 7, 10]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	lencontent = 10
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_ListArray_broadcast_tooffsets')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,fromstarts = fromstarts,fromstops = fromstops,lencontent = lencontent,offsetslength = offsetslength)
	pytest_tocarry = [6, 7, 8, 9, 5, 3, 4, 0, 1, 2]
	assert tocarry == pytest_tocarry


