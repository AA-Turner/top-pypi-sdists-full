import pytest
import numpy
import kernels

def test_awkward_RegularArray_getitem_jagged_expand_1():
	multistarts = []
	multistops = []
	regularlength = 0
	regularsize = 0
	singleoffsets = [0]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = []
	pytest_multistops = []
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_2():
	multistarts = []
	multistops = []
	regularlength = 1
	regularsize = 0
	singleoffsets = [1]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = []
	pytest_multistops = []
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_3():
	multistarts = []
	multistops = []
	regularlength = 0
	regularsize = 0
	singleoffsets = [0]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = []
	pytest_multistops = []
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_4():
	multistarts = [123]
	multistops = [123]
	regularlength = 1
	regularsize = 1
	singleoffsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0]
	pytest_multistops = [2]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_5():
	multistarts = [123, 123]
	multistops = [123, 123]
	regularlength = 2
	regularsize = 1
	singleoffsets = [0, 2]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 0]
	pytest_multistops = [2, 2]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_6():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 1
	regularsize = 4
	singleoffsets = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 0, 0, 0]
	pytest_multistops = [0, 0, 0, 0]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_7():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 0, 0]
	pytest_multistops = [0, 0, 0]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_8():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 1
	regularsize = 4
	singleoffsets = [0, 0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 0, 1, 1]
	pytest_multistops = [0, 1, 1, 1]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_9():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 1, 1, 3]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 1, 1]
	pytest_multistops = [1, 1, 3]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_10():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 1, 1, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 1, 1, 3, 3]
	pytest_multistops = [1, 1, 3, 3, 5]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_11():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 2, 2, 2, 2, 6]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2, 2, 2]
	pytest_multistops = [2, 2, 2, 2, 6]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_12():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2]
	pytest_multistops = [2, 2, 3]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_13():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 2, 2, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2]
	pytest_multistops = [2, 2, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_14():
	multistarts = [123, 123]
	multistops = [123, 123]
	regularlength = 1
	regularsize = 2
	singleoffsets = [0, 2, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2]
	pytest_multistops = [2, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_15():
	multistarts = [123, 123, 123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 7
	singleoffsets = [0, 2, 2, 4, 4, 5, 5, 8]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2, 4, 4, 5, 5]
	pytest_multistops = [2, 2, 4, 4, 5, 5, 8]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_16():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 2, 2, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2, 4, 5]
	pytest_multistops = [2, 2, 4, 5, 6]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_17():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 2, 2, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2, 4, 5]
	pytest_multistops = [2, 2, 4, 5, 8]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_18():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 2, 2, 4, 5, 9]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 2, 4, 5]
	pytest_multistops = [2, 2, 4, 5, 9]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_19():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 2, 3, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 3]
	pytest_multistops = [2, 3, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_20():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 1
	regularsize = 4
	singleoffsets = [0, 2, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 3, 3]
	pytest_multistops = [2, 3, 3, 5]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_21():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 1
	regularsize = 4
	singleoffsets = [0, 2, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 3, 4]
	pytest_multistops = [2, 3, 4, 7]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_22():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 2, 5, 7]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 5]
	pytest_multistops = [2, 5, 7]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_23():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 2, 6, 8]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 2, 6]
	pytest_multistops = [2, 6, 8]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_24():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 2
	regularsize = 2
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 0, 3]
	pytest_multistops = [3, 4, 3, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_25():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 3, 3, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3]
	pytest_multistops = [3, 3, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_26():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3]
	pytest_multistops = [3, 3, 5]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_27():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 3, 3, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3, 3, 4]
	pytest_multistops = [3, 3, 3, 4, 7]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_28():
	multistarts = [123, 123]
	multistops = [123, 123]
	regularlength = 1
	regularsize = 2
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3]
	pytest_multistops = [3, 4]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_29():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	regularlength = 1
	regularsize = 4
	singleoffsets = [0, 3, 3, 4, 5]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3, 4]
	pytest_multistops = [3, 3, 4, 5]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_30():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 3, 3, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3, 4, 5]
	pytest_multistops = [3, 3, 4, 5, 8]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_31():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 3, 5, 6]
	pytest_multistops = [3, 3, 5, 6, 9]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_32():
	multistarts = [123, 123]
	multistops = [123, 123]
	regularlength = 1
	regularsize = 2
	singleoffsets = [0, 3, 6]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3]
	pytest_multistops = [3, 6]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_33():
	multistarts = [123, 123, 123]
	multistops = [123, 123, 123]
	regularlength = 1
	regularsize = 3
	singleoffsets = [0, 4, 6, 6]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 4, 6]
	pytest_multistops = [4, 6, 6]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


def test_awkward_RegularArray_getitem_jagged_expand_34():
	multistarts = [123, 123, 123, 123, 123]
	multistops = [123, 123, 123, 123, 123]
	regularlength = 1
	regularsize = 5
	singleoffsets = [0, 5, 5, 6, 8, 10]
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,regularlength = regularlength,regularsize = regularsize,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 5, 5, 6, 8]
	pytest_multistops = [5, 5, 6, 8, 10]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops


