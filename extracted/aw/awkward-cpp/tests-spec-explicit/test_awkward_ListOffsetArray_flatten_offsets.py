import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_flatten_offsets_1():
	tooffsets = []
	inneroffsets = [0]
	outeroffsets = []
	outeroffsetslen = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = []
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_2():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 1, 2, 3]
	outeroffsets = [0, 0, 0, 1, 3]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 0, 0, 1, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_3():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 1, 2, 3, 4, 5, 6]
	outeroffsets = [0, 0, 1, 3, 6]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 0, 1, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_4():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 1, 1, 5]
	outeroffsets = [0, 0, 1, 3]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 0, 1, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_5():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 1, 1, 6, 6]
	outeroffsets = [0, 0, 1, 4]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 0, 1, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_6():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 4, 8, 12, 14, 16]
	outeroffsets = [0, 3, 3, 5]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 12, 12, 16]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_7():
	tooffsets = [123, 123, 123, 123, 123, 123]
	inneroffsets = [0, 1, 2, 5, 5, 7, 7, 11]
	outeroffsets = [0, 1, 2, 2, 5, 7]
	outeroffsetslen = 6
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 1, 2, 2, 7, 11]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_8():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 1, 2, 3, 4, 5, 6]
	outeroffsets = [0, 1, 3, 6]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 1, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_9():
	tooffsets = [123, 123, 123]
	inneroffsets = [0, 5, 10, 15, 20, 25, 30]
	outeroffsets = [0, 3, 6]
	outeroffsetslen = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 15, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_10():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 2, 6]
	outeroffsets = [0, 1, 1, 1, 2]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 2, 2, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_11():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 0, 2, 6]
	outeroffsets = [0, 2, 2, 2, 3]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 2, 2, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_12():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 0, 0, 2, 6]
	outeroffsets = [0, 3, 3, 3, 4]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 2, 2, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_13():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 0, 0, 0, 2, 7, 7]
	outeroffsets = [0, 4, 4, 4, 6]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 2, 2, 2, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_14():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 3, 5, 6, 6]
	outeroffsets = [0, 1, 2, 3, 4]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 3, 5, 6, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_15():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	inneroffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	outeroffsets = [0, 5, 10, 15, 20, 25, 30]
	outeroffsetslen = 7
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 35, 70, 105, 140, 175, 210]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_16():
	tooffsets = [123, 123, 123, 123, 123, 123]
	inneroffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
	outeroffsets = [0, 2, 4, 6, 8, 10]
	outeroffsetslen = 6
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 4, 8, 12, 14, 16]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_17():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 3, 5, 6, 6, 10]
	outeroffsets = [0, 2, 2, 3, 5]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 5, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_18():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 3, 3, 5, 6, 6, 10]
	outeroffsets = [0, 3, 3, 4, 6]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 5, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_19():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 3, 3, 3, 5, 6, 6, 10]
	outeroffsets = [0, 4, 4, 5, 7]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 5, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_20():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 3, 3, 5, 5, 8]
	outeroffsets = [0, 3, 3, 5]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 5, 5, 8]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_21():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	inneroffsets = [0, 3, 6, 9, 12, 14, 16]
	outeroffsets = [0, 2, 4, 5, 6, 6, 6]
	outeroffsetslen = 7
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 6, 12, 14, 16, 16, 16]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_22():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 2, 4, 6, 8, 10]
	outeroffsets = [0, 3, 3, 5]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 6, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_23():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	inneroffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	outeroffsets = [0, 3, 3, 5, 8, 8, 10]
	outeroffsetslen = 7
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 6, 6, 10, 16, 16, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_24():
	tooffsets = [123, 123, 123, 123, 123]
	inneroffsets = [0, 4, 4, 4, 4, 6, 7, 7, 12, 12]
	outeroffsets = [0, 5, 5, 6, 9]
	outeroffsetslen = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 6, 6, 7, 12]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_25():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 3, 6, 9, 11, 13, 14]
	outeroffsets = [0, 3, 5, 6]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [0, 9, 13, 14]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_26():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 3, 5, 6, 6]
	outeroffsets = [1, 2, 3, 4]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [3, 5, 6, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_27():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 3, 3, 5, 6, 6, 10]
	outeroffsets = [3, 3, 4, 6]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [5, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_flatten_offsets_28():
	tooffsets = [123, 123, 123, 123]
	inneroffsets = [0, 3, 3, 3, 5, 6, 6, 10]
	outeroffsets = [4, 4, 5, 7]
	outeroffsetslen = 4
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_flatten_offsets')
	funcPy(tooffsets = tooffsets,inneroffsets = inneroffsets,outeroffsets = outeroffsets,outeroffsetslen = outeroffsetslen)
	pytest_tooffsets = [5, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


