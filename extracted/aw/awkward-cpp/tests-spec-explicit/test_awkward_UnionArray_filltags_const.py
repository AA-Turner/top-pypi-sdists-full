import pytest
import numpy
import kernels

def test_awkward_UnionArray_filltags_const_1():
	totags = []
	base = 0
	length = 0
	totagsoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags_const')
	funcPy(totags = totags,base = base,length = length,totagsoffset = totagsoffset)
	pytest_totags = []
	assert totags == pytest_totags


def test_awkward_UnionArray_filltags_const_2():
	totags = [123, 123, 123, 123, 123, 123]
	base = 0
	length = 6
	totagsoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags_const')
	funcPy(totags = totags,base = base,length = length,totagsoffset = totagsoffset)
	pytest_totags = [0, 0, 0, 0, 0, 0]
	assert totags == pytest_totags


def test_awkward_UnionArray_filltags_const_3():
	totags = [123, 123, 123, 123, 123]
	base = 3
	length = 5
	totagsoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags_const')
	funcPy(totags = totags,base = base,length = length,totagsoffset = totagsoffset)
	pytest_totags = [3, 3, 3, 3, 3]
	assert totags == pytest_totags


def test_awkward_UnionArray_filltags_const_4():
	totags = [123, 123, 123, 123, 123, 123]
	base = 0
	length = 3
	totagsoffset = 3
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags_const')
	funcPy(totags = totags,base = base,length = length,totagsoffset = totagsoffset)
	pytest_totags = [123, 123, 123, 0, 0, 0]
	assert totags == pytest_totags


def test_awkward_UnionArray_filltags_const_5():
	totags = [123, 123, 123, 123]
	base = 2
	length = 2
	totagsoffset = 2
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags_const')
	funcPy(totags = totags,base = base,length = length,totagsoffset = totagsoffset)
	pytest_totags = [123, 123, 2, 2]
	assert totags == pytest_totags


