import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_apply_1():
	tocarry = []
	tooffsets = [123]
	contentlen = 0
	fromstarts = []
	fromstops = []
	sliceindex = []
	sliceinnerlen = 0
	sliceouterlen = 0
	slicestarts = []
	slicestops = []
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = []
	pytest_tooffsets = [0]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_2():
	tocarry = []
	tooffsets = [123, 123, 123, 123, 123]
	contentlen = 0
	fromstarts = [0, 0, 0, 0]
	fromstops = [0, 0, 0, 0]
	sliceindex = []
	sliceinnerlen = 0
	sliceouterlen = 4
	slicestarts = [0, 0, 0, 0]
	slicestops = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = []
	pytest_tooffsets = [0, 0, 0, 0, 0]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_3():
	tocarry = []
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = []
	sliceinnerlen = 0
	sliceouterlen = 3
	slicestarts = [0, 0, 0]
	slicestops = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = []
	pytest_tooffsets = [0, 0, 0, 0]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_4():
	tocarry = [123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 1]
	sliceinnerlen = 2
	sliceouterlen = 3
	slicestarts = [0, 0, 0]
	slicestops = [0, 0, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [3, 4]
	pytest_tooffsets = [0, 0, 0, 2]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_5():
	tocarry = [123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 0, 1]
	sliceinnerlen = 3
	sliceouterlen = 3
	slicestarts = [0, 1, 1]
	slicestops = [1, 1, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 3, 4]
	pytest_tooffsets = [0, 1, 1, 3]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_6():
	tocarry = [123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [2, 0, 1]
	sliceinnerlen = 3
	sliceouterlen = 3
	slicestarts = [0, 1, 1]
	slicestops = [1, 1, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 3, 4]
	pytest_tooffsets = [0, 1, 1, 3]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_7():
	tocarry = [123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 10
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 10]
	sliceindex = [1, 0, 1, 0, 3]
	sliceinnerlen = 5
	sliceouterlen = 5
	slicestarts = [0, 1, 1, 3, 3]
	slicestops = [1, 1, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [1, 3, 4, 6, 9]
	pytest_tooffsets = [0, 1, 1, 3, 3, 5]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_8():
	tocarry = [123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 1]
	sliceinnerlen = 2
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1]
	pytest_tooffsets = [0, 2, 2, 2]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_9():
	tocarry = [123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 4
	fromstarts = [0, 1, 1, 1, 1]
	fromstops = [1, 1, 1, 1, 4]
	sliceindex = [0, 0, 2, 1, 1, 2]
	sliceinnerlen = 6
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 2, 2]
	slicestops = [2, 2, 2, 2, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 0, 3, 2, 2, 3]
	pytest_tooffsets = [0, 2, 2, 2, 2, 6]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_10():
	tocarry = [123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 1, 0]
	sliceinnerlen = 3
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 3]
	pytest_tooffsets = [0, 2, 2, 3]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_11():
	tocarry = [123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 1, 1]
	sliceinnerlen = 3
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 4]
	pytest_tooffsets = [0, 2, 2, 3]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_12():
	tocarry = [123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [2, 0, 1]
	sliceinnerlen = 3
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 0, 4]
	pytest_tooffsets = [0, 2, 2, 3]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_13():
	tocarry = [123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 2, 0, 1]
	sliceinnerlen = 4
	sliceouterlen = 3
	slicestarts = [0, 2, 2]
	slicestops = [2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 2, 3, 4]
	pytest_tooffsets = [0, 2, 2, 4]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_14():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 9
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 9]
	sliceindex = [0, 2, 0, 1, 0, 0, 1, 2]
	sliceinnerlen = 8
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 4, 5]
	slicestops = [2, 2, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 2, 3, 4, 5, 6, 7, 8]
	pytest_tooffsets = [0, 2, 2, 4, 5, 8]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_15():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 9
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 9]
	sliceindex = [1, 2, 0, 1, 0, 0, 1, 2]
	sliceinnerlen = 8
	sliceouterlen = 5
	slicestarts = [0, 2, 2, 4, 5]
	slicestops = [2, 2, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [1, 2, 3, 4, 5, 6, 7, 8]
	pytest_tooffsets = [0, 2, 2, 4, 5, 8]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_16():
	tocarry = [123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 9
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 9]
	sliceindex = [0, 1, 2, 0, 0, 1, 2]
	sliceinnerlen = 7
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 3, 4]
	slicestops = [3, 3, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 5, 6, 7, 8]
	pytest_tooffsets = [0, 3, 3, 3, 4, 7]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_17():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 9
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 9]
	sliceindex = [0, 1, 2, 1, 0, 0, 1, 2]
	sliceinnerlen = 8
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 4, 5]
	slicestops = [3, 3, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 4, 5, 6, 7, 8]
	pytest_tooffsets = [0, 3, 3, 4, 5, 8]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_18():
	tocarry = [123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [0, 1, 2, 0, 1]
	sliceinnerlen = 5
	sliceouterlen = 3
	slicestarts = [0, 3, 3]
	slicestops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3, 4]
	pytest_tooffsets = [0, 3, 3, 5]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_19():
	tocarry = [123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 5
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	sliceindex = [2, 1, 0, 0, 1]
	sliceinnerlen = 5
	sliceouterlen = 3
	slicestarts = [0, 3, 3]
	slicestops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 1, 0, 3, 4]
	pytest_tooffsets = [0, 3, 3, 5]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_20():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 9
	fromstarts = [0, 3, 3, 5, 6]
	fromstops = [3, 3, 5, 6, 9]
	sliceindex = [0, 1, 2, 0, 1, 0, 0, 1, 2]
	sliceinnerlen = 9
	sliceouterlen = 5
	slicestarts = [0, 3, 3, 5, 6]
	slicestops = [3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	pytest_tooffsets = [0, 3, 3, 5, 6, 9]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_21():
	tocarry = [123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123]
	contentlen = 6
	fromstarts = [0, 3]
	fromstops = [3, 6]
	sliceindex = [2, 1, 0, 2, 1, 0]
	sliceinnerlen = 6
	sliceouterlen = 2
	slicestarts = [0, 3]
	slicestops = [3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 1, 0, 5, 4, 3]
	pytest_tooffsets = [0, 3, 6]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_22():
	tocarry = [123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 6
	fromstarts = [0, 3, 5]
	fromstops = [3, 5, 6]
	sliceindex = [2, 1, 1, 0, 1, 0]
	sliceinnerlen = 6
	sliceouterlen = 3
	slicestarts = [0, 4, 5]
	slicestops = [4, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 1, 1, 0, 5]
	pytest_tooffsets = [0, 4, 4, 5]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_23():
	tocarry = [123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 6
	fromstarts = [0, 3, 5]
	fromstops = [3, 5, 6]
	sliceindex = [2, 1, 1, 0, 1, 0]
	sliceinnerlen = 6
	sliceouterlen = 3
	slicestarts = [0, 4, 5]
	slicestops = [4, 5, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [2, 1, 1, 0, 4, 5]
	pytest_tooffsets = [0, 4, 5, 6]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_24():
	tocarry = [123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123]
	contentlen = 8
	fromstarts = [0, 4, 7]
	fromstops = [4, 7, 8]
	sliceindex = [3, 2, 2, 1, 1, 2]
	sliceinnerlen = 6
	sliceouterlen = 3
	slicestarts = [0, 4, 6]
	slicestops = [4, 6, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [3, 2, 2, 1, 5, 6]
	pytest_tooffsets = [0, 4, 6, 6]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_getitem_jagged_apply_25():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	tooffsets = [123, 123, 123, 123, 123, 123]
	contentlen = 13
	fromstarts = [0, 4, 4, 7, 8]
	fromstops = [4, 4, 7, 8, 13]
	sliceindex = [3, 2, 1, 1, 0, 1, 0, 0, 1, 2]
	sliceinnerlen = 10
	sliceouterlen = 5
	slicestarts = [0, 5, 5, 6, 8]
	slicestops = [5, 5, 6, 8, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_apply')
	funcPy(tocarry = tocarry,tooffsets = tooffsets,contentlen = contentlen,fromstarts = fromstarts,fromstops = fromstops,sliceindex = sliceindex,sliceinnerlen = sliceinnerlen,sliceouterlen = sliceouterlen,slicestarts = slicestarts,slicestops = slicestops)
	pytest_tocarry = [3, 2, 1, 1, 0, 5, 7, 7, 9, 10]
	pytest_tooffsets = [0, 5, 5, 6, 8, 10]
	assert tocarry == pytest_tocarry
	assert tooffsets == pytest_tooffsets


