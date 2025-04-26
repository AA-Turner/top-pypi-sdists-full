import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_next_at_1():
	tocarry = []
	at = -2
	fromstarts = []
	fromstops = []
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_2():
	tocarry = [123]
	at = -2
	fromstarts = [0]
	fromstops = [1]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_at_3():
	tocarry = [123, 123, 123]
	at = 1
	fromstarts = [3, 5, 6]
	fromstops = [5, 6, 9]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	with pytest.raises(Exception):
		funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)


def test_awkward_ListArray_getitem_next_at_4():
	tocarry = []
	at = 0
	fromstarts = []
	fromstops = []
	lenstarts = 0
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_5():
	tocarry = [123]
	at = 0
	fromstarts = [0]
	fromstops = [1]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_6():
	tocarry = [123]
	at = 0
	fromstarts = [0]
	fromstops = [2]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_7():
	tocarry = [123]
	at = 0
	fromstarts = [0]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_8():
	tocarry = [123]
	at = -5
	fromstarts = [0]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_9():
	tocarry = [123, 123]
	at = 0
	fromstarts = [0, 1]
	fromstops = [1, 2]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_10():
	tocarry = [123, 123, 123, 123]
	at = 0
	fromstarts = [0, 1, 2, 3]
	fromstops = [1, 2, 3, 4]
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0, 1, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_11():
	tocarry = [123, 123, 123, 123, 123]
	at = 0
	fromstarts = [0, 1, 2, 3, 4]
	fromstops = [1, 2, 3, 4, 5]
	lenstarts = 5
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_12():
	tocarry = [123, 123, 123]
	at = 0
	fromstarts = [0, 2, 3]
	fromstops = [2, 3, 5]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0, 2, 3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_13():
	tocarry = [123, 123, 123, 123]
	at = 0
	fromstarts = [0, 3, 5, 6]
	fromstops = [3, 5, 6, 10]
	lenstarts = 4
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [0, 3, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_14():
	tocarry = [123]
	at = 0
	fromstarts = [10]
	fromstops = [15]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [10]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_15():
	tocarry = [123]
	at = 1
	fromstarts = [0]
	fromstops = [2]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_16():
	tocarry = [123]
	at = 1
	fromstarts = [0]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_17():
	tocarry = [123]
	at = -2
	fromstarts = [0]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_18():
	tocarry = [123]
	at = 1
	fromstarts = [0]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_19():
	tocarry = [123]
	at = 1
	fromstarts = [10]
	fromstops = [15]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [11]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_20():
	tocarry = [123]
	at = 0
	fromstarts = [1]
	fromstops = [2]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_21():
	tocarry = [123]
	at = 0
	fromstarts = [1]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_22():
	tocarry = [123]
	at = -2
	fromstarts = [10]
	fromstops = [15]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [13]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_23():
	tocarry = [123, 123]
	at = 1
	fromstarts = [0, 3]
	fromstops = [3, 5]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1, 4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_24():
	tocarry = [123, 123]
	at = 1
	fromstarts = [0, 5]
	fromstops = [5, 10]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [1, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_25():
	tocarry = [123]
	at = 1
	fromstarts = [15]
	fromstops = [20]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [16]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_26():
	tocarry = [123]
	at = -2
	fromstarts = [15]
	fromstops = [20]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [18]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_27():
	tocarry = [123]
	at = -1
	fromstarts = [15]
	fromstops = [20]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [19]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_28():
	tocarry = [123]
	at = -1
	fromstarts = [0]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_29():
	tocarry = [123]
	at = 1
	fromstarts = [1]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_30():
	tocarry = [123]
	at = 1
	fromstarts = [1]
	fromstops = [4]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_31():
	tocarry = [123]
	at = 0
	fromstarts = [2]
	fromstops = [3]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [2]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_32():
	tocarry = [123]
	at = 1
	fromstarts = [2]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_33():
	tocarry = [123]
	at = 0
	fromstarts = [3]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_34():
	tocarry = [123]
	at = 0
	fromstarts = [3]
	fromstops = [6]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [3]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_35():
	tocarry = [123, 123, 123]
	at = 0
	fromstarts = [3, 5, 6]
	fromstops = [5, 6, 9]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [3, 5, 6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_36():
	tocarry = [123]
	at = -1
	fromstarts = [0]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_37():
	tocarry = [123]
	at = 4
	fromstarts = [0]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_38():
	tocarry = [123]
	at = 1
	fromstarts = [3]
	fromstops = [5]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_39():
	tocarry = [123]
	at = 1
	fromstarts = [3]
	fromstops = [6]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_40():
	tocarry = [123]
	at = -2
	fromstarts = [3]
	fromstops = [6]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_41():
	tocarry = [123, 123, 123]
	at = -1
	fromstarts = [3, 5, 6]
	fromstops = [5, 6, 9]
	lenstarts = 3
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4, 5, 8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_42():
	tocarry = [123, 123]
	at = -1
	fromstarts = [0, 5]
	fromstops = [5, 10]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [4, 9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_43():
	tocarry = [123, 123]
	at = 0
	fromstarts = [5, 10]
	fromstops = [10, 15]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [5, 10]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_44():
	tocarry = [123]
	at = -1
	fromstarts = [3]
	fromstops = [6]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_45():
	tocarry = [123]
	at = 0
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_46():
	tocarry = [123]
	at = -5
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [5]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_47():
	tocarry = [123, 123]
	at = 1
	fromstarts = [5, 10]
	fromstops = [10, 15]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [6, 11]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_48():
	tocarry = [123]
	at = 1
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [6]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_49():
	tocarry = [123]
	at = 1
	fromstarts = [6]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [7]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_50():
	tocarry = [123]
	at = 1
	fromstarts = [6]
	fromstops = [9]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [7]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_51():
	tocarry = [123]
	at = -2
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [8]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_52():
	tocarry = [123, 123]
	at = -1
	fromstarts = [5, 10]
	fromstops = [10, 15]
	lenstarts = 2
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [9, 14]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_53():
	tocarry = [123]
	at = -1
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [9]
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_next_at_54():
	tocarry = [123]
	at = 4
	fromstarts = [5]
	fromstops = [10]
	lenstarts = 1
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_at')
	funcPy(tocarry = tocarry,at = at,fromstarts = fromstarts,fromstops = fromstops,lenstarts = lenstarts)
	pytest_tocarry = [9]
	assert tocarry == pytest_tocarry


