import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_1():
	nextstarts = []
	nextlen = 0
	nextparents = []
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = []
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_2():
	nextstarts = [123, 123, 123, 123, 123, 123]
	nextlen = 18
	nextparents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 10, 16, 5, 13, 17]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_3():
	nextstarts = [123, 123, 123, 123, 123, 123]
	nextlen = 21
	nextparents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 4, 2, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 10, 17, 5, 13, 18]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_4():
	nextstarts = [123, 123, 123]
	nextlen = 3
	nextparents = [0, 1, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 1, 2]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_5():
	nextstarts = [123, 123, 123, 123]
	nextlen = 5
	nextparents = [0, 0, 1, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 2, 3, 4]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_6():
	nextstarts = [123, 123, 123]
	nextlen = 6
	nextparents = [0, 0, 1, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 2, 4]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_7():
	nextstarts = [123, 123, 123, 123]
	nextlen = 6
	nextparents = [0, 0, 1, 1, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 2, 4, 5]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_8():
	nextstarts = [123, 123, 123, 123]
	nextlen = 8
	nextparents = [0, 0, 1, 1, 2, 2, 3, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 2, 4, 6]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_9():
	nextstarts = [123, 123, 123, 123]
	nextlen = 7
	nextparents = [0, 0, 1, 1, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 2, 4, 6]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_10():
	nextstarts = [123, 123]
	nextlen = 6
	nextparents = [0, 0, 0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_11():
	nextstarts = [123, 123]
	nextlen = 5
	nextparents = [0, 0, 0, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_12():
	nextstarts = [123, 123, 123, 123]
	nextlen = 7
	nextparents = [0, 0, 0, 1, 1, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 5, 6]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_13():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 0, 1, 1, 2, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 5, 7, 8]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_14():
	nextstarts = [123, 123, 123]
	nextlen = 7
	nextparents = [0, 0, 0, 1, 1, 1, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_15():
	nextstarts = [123, 123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 8]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_16():
	nextstarts = [123, 123, 123, 123]
	nextlen = 10
	nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_17():
	nextstarts = [123, 123, 123, 123]
	nextlen = 12
	nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_18():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 12
	nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9, 11]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_19():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 15
	nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9, 12]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_20():
	nextstarts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 15
	nextparents = [0, 5, 5, 1, 6, 6, 2, 7, 7, 3, 8, 8, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9, 12, 1, 4, 7, 10, 13]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_21():
	nextstarts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 15
	nextparents = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9, 12, 1, 4, 7, 10, 13, 2, 5, 8, 11, 14]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_22():
	nextstarts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 15
	nextparents = [0, 0, 5, 1, 1, 6, 2, 2, 7, 3, 3, 8, 4, 4, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 3, 6, 9, 12, 2, 5, 8, 11, 14]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_23():
	nextstarts = [123, 123]
	nextlen = 6
	nextparents = [0, 0, 0, 0, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_24():
	nextstarts = [123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 0, 0, 1, 1, 1, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4, 7]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_25():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 20
	nextparents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4, 8, 12, 16]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_26():
	nextstarts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 20
	nextparents = [0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4, 8, 12, 16, 2, 6, 10, 14, 18]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_27():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 3, 3, 1, 1, 4, 4, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4, 8, 2, 6]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_28():
	nextstarts = [123, 123, 123, 123, 123, 123]
	nextlen = 12
	nextparents = [0, 0, 3, 3, 1, 1, 4, 4, 2, 2, 5, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 4, 8, 2, 6, 10]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_29():
	nextstarts = [123, 123, 123]
	nextlen = 15
	nextparents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 5, 10]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_30():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 17
	nextparents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 5, 10, 15, 16]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_31():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 25
	nextparents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 5, 10, 15, 20]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_32():
	nextstarts = [123, 123, 123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 0, 3, 3, 1, 1, 4, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 5, 8, 3, 7]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_33():
	nextstarts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 22
	nextparents = [0, 0, 0, 5, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 6, 10, 14, 18, 3, 8, 12, 16, 20]
	assert nextstarts == pytest_nextstarts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64_34():
	nextstarts = [123, 123, 123, 123]
	nextlen = 16
	nextparents = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextstarts_64')
	funcPy(nextstarts = nextstarts,nextlen = nextlen,nextparents = nextparents)
	pytest_nextstarts = [0, 7, 12, 15]
	assert nextstarts == pytest_nextstarts


