import pytest
import numpy
import kernels

def test_awkward_ListArray_getitem_jagged_expand_1():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromstarts = [0, 2]
	fromstops = [2, 4]
	jaggedsize = 1
	length = 2
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_expand')
	with pytest.raises(Exception):
		funcPy(multistarts = multistarts,multistops = multistops,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,jaggedsize = jaggedsize,length = length,singleoffsets = singleoffsets)


def test_awkward_ListArray_getitem_jagged_expand_2():
	multistarts = [123, 123]
	multistops = [123, 123]
	tocarry = [123, 123]
	fromstarts = [5]
	fromstops = [4]
	jaggedsize = 2
	length = 1
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_expand')
	with pytest.raises(Exception):
		funcPy(multistarts = multistarts,multistops = multistops,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,jaggedsize = jaggedsize,length = length,singleoffsets = singleoffsets)


def test_awkward_ListArray_getitem_jagged_expand_3():
	multistarts = [123, 123, 123, 123]
	multistops = [123, 123, 123, 123]
	tocarry = [123, 123, 123, 123]
	fromstarts = [0, 2]
	fromstops = [2, 4]
	jaggedsize = 2
	length = 2
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,jaggedsize = jaggedsize,length = length,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3, 0, 3]
	pytest_multistops = [3, 4, 3, 4]
	pytest_tocarry = [0, 1, 2, 3]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_jagged_expand_4():
	multistarts = []
	multistops = []
	tocarry = []
	fromstarts = []
	fromstops = []
	jaggedsize = 0
	length = 0
	singleoffsets = []
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,jaggedsize = jaggedsize,length = length,singleoffsets = singleoffsets)
	pytest_multistarts = []
	pytest_multistops = []
	pytest_tocarry = []
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops
	assert tocarry == pytest_tocarry


def test_awkward_ListArray_getitem_jagged_expand_5():
	multistarts = [123, 123]
	multistops = [123, 123]
	tocarry = [123, 123]
	fromstarts = [2]
	fromstops = [4]
	jaggedsize = 2
	length = 1
	singleoffsets = [0, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_jagged_expand')
	funcPy(multistarts = multistarts,multistops = multistops,tocarry = tocarry,fromstarts = fromstarts,fromstops = fromstops,jaggedsize = jaggedsize,length = length,singleoffsets = singleoffsets)
	pytest_multistarts = [0, 3]
	pytest_multistops = [3, 4]
	pytest_tocarry = [2, 3]
	assert multistarts == pytest_multistarts
	assert multistops == pytest_multistops
	assert tocarry == pytest_tocarry


