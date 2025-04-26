import pytest
import numpy
import kernels

def test_awkward_missing_repeat_1():
	outindex = []
	index = []
	indexlength = 0
	regularsize = 0
	repetitions = 0
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = []
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_2():
	outindex = [123]
	index = [0]
	indexlength = 1
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_3():
	outindex = [123, 123]
	index = [0, 1]
	indexlength = 2
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_4():
	outindex = [123, 123, 123]
	index = [0, 1, 1]
	indexlength = 3
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_5():
	outindex = [123, 123, 123]
	index = [0, 1, 1]
	indexlength = 3
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_6():
	outindex = [123, 123, 123, 123]
	index = [0, 1, 1, 1]
	indexlength = 4
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_7():
	outindex = [123, 123, 123, 123]
	index = [0, 1, 1, 1]
	indexlength = 4
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_8():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 1, 1, 1]
	indexlength = 5
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_9():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 1, 1, 1]
	indexlength = 5
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_10():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 1, 1, 2]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1, 2]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_11():
	outindex = [123, 123, 123, 123, 123, 123]
	index = [0, 1, 1, 1, 2, 3]
	indexlength = 6
	regularsize = 4
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 1, 2, 3]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_12():
	outindex = [123, 123, 123, 123]
	index = [0, 1, 1, 2]
	indexlength = 4
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 2]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_13():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 1, 2, 1]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 2, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_14():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 1, 2, 3]
	indexlength = 5
	regularsize = 4
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 2, 3]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_15():
	outindex = [123, 123, 123, 123, 123, 123, 123]
	index = [0, 1, 1, 2, 3, 4, 5]
	indexlength = 7
	regularsize = 6
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 1, 2, 3, 4, 5]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_16():
	outindex = [123, 123, 123, 123]
	index = [0, 1, 2, 1]
	indexlength = 4
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_17():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 2, 1, 1]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_18():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 2, 1, 3]
	indexlength = 5
	regularsize = 4
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 1, 3]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_19():
	outindex = [123, 123, 123, 123, 123]
	index = [0, 1, 2, 3, 1]
	indexlength = 5
	regularsize = 4
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 3, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_20():
	outindex = [123, 123, 123, 123, 123, 123, 123]
	index = [0, 1, 2, 3, 1, 4, 5]
	indexlength = 7
	regularsize = 6
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 3, 1, 4, 5]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_21():
	outindex = [123, 123, 123, 123, 123, 123]
	index = [0, 1, 2, 3, 4, 5]
	indexlength = 6
	regularsize = 6
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [0, 1, 2, 3, 4, 5]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_22():
	outindex = [123, 123]
	index = [1, 0]
	indexlength = 2
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_23():
	outindex = [123, 123, 123]
	index = [1, 0, 1]
	indexlength = 3
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_24():
	outindex = [123, 123, 123]
	index = [1, 0, 1]
	indexlength = 3
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_25():
	outindex = [123, 123, 123, 123]
	index = [1, 0, 1, 1]
	indexlength = 4
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_26():
	outindex = [123, 123, 123, 123]
	index = [1, 0, 1, 1]
	indexlength = 4
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_27():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 0, 1, 1, 1]
	indexlength = 5
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_28():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 0, 1, 1, 1]
	indexlength = 5
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_29():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 0, 1, 1, 2]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 1, 2]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_30():
	outindex = [123, 123, 123, 123]
	index = [1, 0, 1, 2]
	indexlength = 4
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 2]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_31():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 0, 1, 2, 1]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 2, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_32():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 0, 1, 2, 3]
	indexlength = 5
	regularsize = 4
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 0, 1, 2, 3]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_33():
	outindex = [123, 123, 123]
	index = [1, 1, 0]
	indexlength = 3
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_34():
	outindex = [123, 123, 123, 123]
	index = [1, 1, 0, 1]
	indexlength = 4
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_35():
	outindex = [123, 123, 123, 123]
	index = [1, 1, 0, 1]
	indexlength = 4
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_36():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 0, 1, 1]
	indexlength = 5
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_37():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 0, 1, 1]
	indexlength = 5
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_38():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 0, 1, 2]
	indexlength = 5
	regularsize = 3
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 0, 1, 2]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_39():
	outindex = [123, 123, 123, 123]
	index = [1, 1, 1, 0]
	indexlength = 4
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 0]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_40():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 1, 0, 1]
	indexlength = 5
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_41():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 1, 0, 1]
	indexlength = 5
	regularsize = 2
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 0, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_42():
	outindex = [123]
	index = [1]
	indexlength = 1
	regularsize = 0
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_43():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 1, 1, 0]
	indexlength = 5
	regularsize = 1
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 1, 0]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_44():
	outindex = [123, 123, 123, 123, 123]
	index = [1, 1, 1, 1, 1]
	indexlength = 5
	regularsize = 0
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_45():
	outindex = [123, 123, 123, 123]
	index = [1, 1, 1, 1]
	indexlength = 4
	regularsize = 0
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_46():
	outindex = [123, 123, 123]
	index = [1, 1, 1]
	indexlength = 3
	regularsize = 0
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1, 1]
	assert outindex == pytest_outindex


def test_awkward_missing_repeat_47():
	outindex = [123, 123]
	index = [1, 1]
	indexlength = 2
	regularsize = 0
	repetitions = 1
	funcPy = getattr(kernels, 'awkward_missing_repeat')
	funcPy(outindex = outindex,index = index,indexlength = indexlength,regularsize = regularsize,repetitions = repetitions)
	pytest_outindex = [1, 1]
	assert outindex == pytest_outindex


