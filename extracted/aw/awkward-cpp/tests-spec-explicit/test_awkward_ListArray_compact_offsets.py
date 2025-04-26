import pytest
import numpy
import kernels

def test_awkward_ListArray_compact_offsets_1():
	tooffsets = [123]
	fromstarts = []
	fromstops = []
	length = 0
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_2():
	tooffsets = [123, 123]
	fromstarts = [1]
	fromstops = [1]
	length = 1
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_3():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [2, 2, 6]
	fromstops = [2, 3, 5]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	with pytest.raises(Exception):
		funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)


def test_awkward_ListArray_compact_offsets_4():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [2, 2, 3]
	fromstops = [2, 3, 5]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0, 1, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_5():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [5, 5, 6]
	fromstops = [5, 6, 9]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0, 1, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_6():
	tooffsets = [123, 123, 123]
	fromstarts = [4, 4]
	fromstops = [4, 6]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0, 2]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_7():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [3, 3, 6]
	fromstops = [3, 5, 10]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_8():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [4, 4, 7]
	fromstops = [4, 6, 12]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 0, 2, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_9():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [5, 6, 6]
	fromstops = [6, 6, 10]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 1, 1, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_10():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [6, 7, 7]
	fromstops = [7, 7, 12]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 1, 1, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_11():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [3, 3, 3, 0, 4]
	fromstops = [4, 4, 3, 3, 6]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 1, 2, 2, 5, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_12():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [2, 4, 5]
	fromstops = [3, 5, 6]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 1, 2, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_13():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [5, 5, 0, 3, 3, 6, 6]
	fromstops = [6, 6, 3, 3, 5, 6, 10]
	length = 7
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 1, 2, 5, 5, 7, 7, 11]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_14():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [3, 5, 5, 5, 5]
	fromstops = [5, 5, 5, 5, 9]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 2, 2, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_15():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 5, 8]
	fromstops = [2, 3, 5, 6, 9]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 2, 4, 5, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_16():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [3, 3, 0, 5, 5, 6]
	fromstops = [5, 3, 3, 6, 6, 10]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 2, 5, 6, 7, 11]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_17():
	tooffsets = [123, 123, 123]
	fromstarts = [3, 15]
	fromstops = [5, 16]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_18():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 2, 4, 5, 6, 9]
	fromstops = [2, 3, 5, 6, 7, 11]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 3, 4, 5, 6, 8]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_19():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 2]
	fromstops = [2, 4]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_20():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [3, 3, 3, 0]
	fromstops = [5, 5, 3, 3]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4, 4, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_21():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 2, 5, 3, 6]
	fromstops = [2, 5, 3, 6, 3, 6]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4, 5, 6, 6, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_22():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 3, 3]
	fromstops = [2, 2, 2, 5, 5]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4, 6, 8, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_23():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 0, 0, 0, 4, 4, 4, 4]
	fromstops = [2, 2, 2, 2, 2, 2, 5, 5, 5, 5]
	length = 10
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_24():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 3, 3, 5, 5, 5, 8, 8]
	fromstops = [2, 2, 2, 5, 5, 7, 7, 7, 10, 10]
	length = 10
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_25():
	tooffsets = [123, 123, 123]
	fromstarts = [3, 6]
	fromstops = [5, 10]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_26():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 3]
	fromstops = [3, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_27():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 4]
	fromstops = [3, 3, 4, 5]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 4, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_28():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 3, 3]
	fromstops = [3, 3, 5]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_29():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 7]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_30():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [1, 99, 5]
	fromstops = [4, 99, 7]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_31():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 10, 10]
	fromstops = [3, 3, 5, 10, 13]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5, 5, 8]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_32():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 3, 15, 16]
	fromstops = [3, 3, 5, 16, 20]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5, 6, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_33():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 4, 4, 6, 9]
	fromstops = [3, 4, 6, 7, 11]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5, 6, 8]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_34():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 4, 5, 8]
	fromstops = [3, 3, 6, 8, 9]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 5, 8, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_35():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 3, 5]
	fromstops = [3, 3, 9]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_36():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 3, 6]
	fromstops = [3, 3, 10]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 3, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_37():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [9, 6, 5, 3, 3]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 4, 6, 6, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_38():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [6, 5, 6, 0]
	fromstops = [9, 6, 9, 3]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 4, 7, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_39():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 6, 3, 8, 3, 5]
	fromstops = [3, 8, 3, 9, 5, 6]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 5, 5, 6, 8, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_40():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 4, 6, 3, 6, 7]
	fromstops = [3, 6, 7, 4, 6, 9]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 5, 6, 7, 7, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_41():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 4, 6, 3, 7]
	fromstops = [3, 6, 7, 4, 9]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 5, 6, 7, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_42():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 6, 3, 8, 5, 9]
	fromstops = [3, 8, 5, 9, 6, 10]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 5, 7, 8, 9, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_43():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 0]
	fromstops = [3, 3]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_44():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 3]
	fromstops = [3, 6]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_45():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 10, 14, 18]
	fromstops = [3, 6, 14, 18, 21]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 10, 14, 17]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_46():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 6, 11, 15, 19]
	fromstops = [3, 6, 11, 15, 19, 22]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 11, 15, 19, 22]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_47():
	tooffsets = [123, 123, 123, 123]
	fromstarts = [0, 0, 0]
	fromstops = [3, 3, 3]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_48():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [3, 6, 17, 20, 11, 25]
	fromstops = [6, 9, 20, 23, 13, 27]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9, 12, 14, 16]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_49():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9, 12, 15]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_50():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 3, 11, 14, 17]
	fromstops = [3, 6, 14, 17, 20]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9, 12, 15]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_51():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3, 3]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9, 12, 15, 18]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_52():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 0, 0, 0, 0]
	fromstops = [3, 3, 3, 3, 3, 3, 3]
	length = 7
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 6, 9, 12, 15, 18, 21]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_53():
	tooffsets = [123, 123, 123]
	fromstarts = [0, 5]
	fromstops = [3, 9]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 7]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_54():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [3, 6, 11, 15, 19]
	fromstops = [6, 11, 15, 19, 22]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 8, 12, 16, 19]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_55():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 13, 3, 18, 8, 23]
	fromstops = [3, 18, 8, 23, 13, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 3, 8, 13, 18, 23, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_56():
	tooffsets = [123, 123]
	fromstarts = [16]
	fromstops = [20]
	length = 1
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_57():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 0]
	fromstops = [10, 6, 5, 3]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4, 5, 7, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_58():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [6, 5, 3, 3, 0]
	fromstops = [10, 6, 5, 3, 3]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4, 5, 7, 7, 10]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_59():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [3, 0, 999, 2, 6, 10]
	fromstops = [7, 3, 999, 4, 6, 12]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4, 7, 7, 9, 9, 11]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_60():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 13, 4, 18, 8, 23]
	fromstops = [4, 18, 8, 23, 13, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4, 9, 13, 18, 23, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_61():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 14, 4, 19, 9, 24]
	fromstops = [4, 19, 9, 24, 14, 29]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 4, 9, 14, 19, 24, 29]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_62():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 11, 5, 16, 6, 17]
	fromstops = [5, 16, 6, 17, 11, 22]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 11, 12, 17, 22]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_63():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 14, 5, 19, 9, 23]
	fromstops = [5, 19, 9, 23, 14, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 14, 18, 23, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_64():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 0, 0, 8, 11, 11, 14]
	fromstops = [5, 5, 5, 11, 14, 14, 19]
	length = 7
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 18, 21, 24, 29]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_65():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 15, 5, 20, 10, 24]
	fromstops = [5, 20, 10, 24, 15, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 19, 24, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_66():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [0, 10, 15, 25]
	fromstops = [5, 15, 20, 30]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_67():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [0, 15, 10, 25]
	fromstops = [5, 20, 15, 30]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_68():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [15, 10, 5, 0]
	fromstops = [20, 15, 10, 5]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_69():
	tooffsets = [123, 123, 123, 123, 123]
	fromstarts = [15, 5, 10, 0]
	fromstops = [20, 10, 15, 5]
	length = 4
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_70():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 14, 5, 19, 10, 24]
	fromstops = [5, 19, 10, 24, 14, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 24, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_71():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 28]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 28]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_72():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 29]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 29]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_73():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 15, 5, 20, 10, 25]
	fromstops = [5, 20, 10, 25, 15, 30]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_74():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 45, 5, 50, 10, 55]
	fromstops = [5, 50, 10, 55, 15, 60]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_75():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 5, 10, 15, 20, 25]
	fromstops = [5, 10, 15, 20, 25, 30]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_76():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 5, 10, 45, 50, 55]
	fromstops = [5, 10, 15, 50, 55, 60]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_77():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [1, 16, 6, 21, 11, 26]
	fromstops = [6, 21, 11, 26, 16, 31]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_78():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [25, 10, 20, 5, 15, 0]
	fromstops = [30, 15, 25, 10, 20, 5]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_79():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	fromstarts = [25, 20, 15, 10, 5, 0]
	fromstops = [30, 25, 20, 15, 10, 5]
	length = 6
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_80():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [0, 8, 11, 11, 14]
	fromstops = [5, 11, 14, 14, 19]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 8, 11, 14, 19]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_81():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromstarts = [6, 11, 14, 17, 20]
	fromstops = [11, 14, 17, 20, 25]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 5, 8, 11, 14, 19]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListArray_compact_offsets_82():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromstarts = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203]
	fromstops = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	length = 30
	funcPy = getattr(kernels, 'awkward_ListArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromstarts = fromstarts,fromstops = fromstops,length = length)
	pytest_tooffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	assert tooffsets == pytest_tooffsets


