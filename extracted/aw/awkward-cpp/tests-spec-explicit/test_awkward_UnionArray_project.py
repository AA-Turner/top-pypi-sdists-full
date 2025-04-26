import pytest
import numpy
import kernels

def test_awkward_UnionArray_project_1():
	lenout = [123]
	tocarry = []
	fromindex = []
	fromtags = []
	length = 0
	which = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [0]
	pytest_tocarry = []
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_2():
	lenout = [123]
	tocarry = []
	fromindex = []
	fromtags = []
	length = 0
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [0]
	pytest_tocarry = []
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_3():
	lenout = [123]
	tocarry = [123]
	fromindex = [1]
	fromtags = [1]
	length = 1
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [1]
	pytest_tocarry = [1]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_4():
	lenout = [123]
	tocarry = [123, 123]
	fromindex = [0, 0]
	fromtags = [1, 1]
	length = 2
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [2]
	pytest_tocarry = [0, 0]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_5():
	lenout = [123]
	tocarry = [123, 123]
	fromindex = [0, 1]
	fromtags = [0, 0]
	length = 2
	which = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [2]
	pytest_tocarry = [0, 1]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_6():
	lenout = [123]
	tocarry = [123, 123]
	fromindex = [0, 1]
	fromtags = [1, 1]
	length = 2
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [2]
	pytest_tocarry = [0, 1]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_7():
	lenout = [123]
	tocarry = [123, 123]
	fromindex = [2, 3]
	fromtags = [0, 0]
	length = 2
	which = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [2]
	pytest_tocarry = [2, 3]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_8():
	lenout = [123]
	tocarry = [123, 123]
	fromindex = [2, 3]
	fromtags = [1, 1]
	length = 2
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [2]
	pytest_tocarry = [2, 3]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_9():
	lenout = [123]
	tocarry = [123, 123, 123]
	fromindex = [0, 1, 2]
	fromtags = [0, 0, 0]
	length = 3
	which = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [3]
	pytest_tocarry = [0, 1, 2]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_10():
	lenout = [123]
	tocarry = [123, 123, 123]
	fromindex = [0, 1, 2]
	fromtags = [1, 1, 1]
	length = 3
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [3]
	pytest_tocarry = [0, 1, 2]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_11():
	lenout = [123]
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, 3, 4]
	fromtags = [0, 0, 0, 0, 0]
	length = 5
	which = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [5]
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


def test_awkward_UnionArray_project_12():
	lenout = [123]
	tocarry = [123, 123, 123, 123, 123]
	fromindex = [0, 1, 2, 3, 4]
	fromtags = [1, 1, 1, 1, 1]
	length = 5
	which = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_project')
	funcPy(lenout = lenout,tocarry = tocarry,fromindex = fromindex,fromtags = fromtags,length = length,which = which)
	pytest_lenout = [5]
	pytest_tocarry = [0, 1, 2, 3, 4]
	assert lenout == pytest_lenout
	assert tocarry == pytest_tocarry


