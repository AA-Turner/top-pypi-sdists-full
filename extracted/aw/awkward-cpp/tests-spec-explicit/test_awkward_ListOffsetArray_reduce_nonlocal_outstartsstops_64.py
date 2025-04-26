import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_1():
	outstarts = []
	outstops = []
	distincts = []
	lendistincts = 0
	outlength = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = []
	pytest_outstops = []
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_2():
	outstarts = [123]
	outstops = [123]
	distincts = []
	lendistincts = 0
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [0]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_3():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 5, 15]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_4():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 5, 15]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_5():
	outstarts = [123]
	outstops = [123]
	distincts = [0, 0]
	lendistincts = 2
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [2]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_6():
	outstarts = [123]
	outstops = [123]
	distincts = [0, 0, 0]
	lendistincts = 3
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [3]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_7():
	outstarts = [123, 123]
	outstops = [123, 123]
	distincts = [0, 0, 0, 1, 1, -1]
	lendistincts = 6
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3]
	pytest_outstops = [3, 5]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_8():
	outstarts = [123, 123]
	outstops = [123, 123]
	distincts = [0, 0, 0, 1, 1, 1]
	lendistincts = 6
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3]
	pytest_outstops = [3, 6]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_9():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 1, 1, -1, 2, -1, -1]
	lendistincts = 9
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6]
	pytest_outstops = [3, 5, 7]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_10():
	outstarts = [123, 123, 123, 123]
	outstops = [123, 123, 123, 123]
	distincts = [0, 0, 0, 1, -1, -1, 2, 1, -1, 3, -1, -1]
	lendistincts = 12
	outlength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6, 9]
	pytest_outstops = [3, 4, 8, 10]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_11():
	outstarts = [123, 123, 123, 123]
	outstops = [123, 123, 123, 123]
	distincts = [0, 0, -1, 1, -1, -1, -1, -1, -1, 2, 1, 0]
	lendistincts = 12
	outlength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6, 9]
	pytest_outstops = [2, 4, 6, 12]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_12():
	outstarts = [123]
	outstops = [123]
	distincts = [0, 0, 0, 0]
	lendistincts = 4
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [4]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_13():
	outstarts = [123, 123]
	outstops = [123, 123]
	distincts = [0, 0, 0, -1, 1, 1, 1, 0]
	lendistincts = 8
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 4]
	pytest_outstops = [3, 8]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_14():
	outstarts = [123]
	outstops = [123]
	distincts = [0, 0, 0, 0, 0]
	lendistincts = 5
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [5]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_15():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, -1]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 10, 14]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_16():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 10, 15]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_17():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, 1, -1, -1, -1, -1, 2, 1, 1, 1, 1]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 6, 15]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_18():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, -1, 2, 2, 2, 2, 1]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 9, 15]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_19():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
	lendistincts = 15
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5, 10]
	pytest_outstops = [5, 10, 10]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_20():
	outstarts = [123, 123]
	outstops = [123, 123]
	distincts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	lendistincts = 10
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 5]
	pytest_outstops = [5, 10]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_21():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, -1, -1, -1, 1, 1, -1]
	lendistincts = 9
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6]
	pytest_outstops = [3, 3, 8]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_22():
	outstarts = [123, 123, 123]
	outstops = [123, 123, 123]
	distincts = [0, 0, 0, -1, -1, -1, 1, 1, 1]
	lendistincts = 9
	outlength = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6]
	pytest_outstops = [3, 3, 9]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_23():
	outstarts = [123, 123, 123, 123]
	outstops = [123, 123, 123, 123]
	distincts = [0, 0, -1, -1, -1, -1, 1, -1, -1, 2, 1, 0]
	lendistincts = 12
	outlength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6, 9]
	pytest_outstops = [2, 3, 7, 12]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_24():
	outstarts = [123, 123, 123, 123]
	outstops = [123, 123, 123, 123]
	distincts = [0, 0, -1, -1, -1, -1, -1, -1, -1, 1, 1, 0]
	lendistincts = 12
	outlength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6, 9]
	pytest_outstops = [2, 3, 6, 12]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_25():
	outstarts = [123, 123, 123, 123]
	outstops = [123, 123, 123, 123]
	distincts = [0, 0, 0, -1, -1, -1, -1, -1, -1, 1, 1, 1]
	lendistincts = 12
	outlength = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0, 3, 6, 9]
	pytest_outstops = [3, 3, 6, 12]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


def test_awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64_26():
	outstarts = [123]
	outstops = [123]
	distincts = []
	lendistincts = 0
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_outstartsstops_64')
	funcPy(outstarts = outstarts,outstops = outstops,distincts = distincts,lendistincts = lendistincts,outlength = outlength)
	pytest_outstarts = [0]
	pytest_outstops = [0]
	assert outstarts == pytest_outstarts
	assert outstops == pytest_outstops


