import pytest
import numpy
import kernels

def test_awkward_UnionArray_simplify_one_1():
	toindex = []
	totags = []
	base = 0
	fromindex = []
	fromtags = []
	fromwhich = 0
	length = 0
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = []
	pytest_totags = []
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_2():
	toindex = [123, 123, 123, 123, 123]
	totags = [123, 123, 123, 123, 123]
	base = 0
	fromindex = [0, 0, 0, 0, 0]
	fromtags = [1, 1, 1, 1, 1]
	fromwhich = 1
	length = 5
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = [0, 0, 0, 0, 0]
	pytest_totags = [0, 0, 0, 0, 0]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	totags = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	base = 9
	fromindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
	fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1]
	fromwhich = 1
	length = 9
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = [9, 10, 11, 12, 13, 14, 15, 16, 17]
	pytest_totags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_4():
	toindex = [123, 123]
	totags = [123, 123]
	base = 0
	fromindex = [0, 1]
	fromtags = [1, 1]
	fromwhich = 1
	length = 2
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = [0, 1]
	pytest_totags = [0, 0]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_5():
	toindex = [123]
	totags = [123]
	base = 0
	fromindex = [0]
	fromtags = [1]
	fromwhich = 1
	length = 1
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = [0]
	pytest_totags = [0]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_6():
	toindex = []
	totags = []
	base = 0
	fromindex = []
	fromtags = []
	fromwhich = 1
	length = 0
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = []
	pytest_totags = []
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_one_7():
	toindex = []
	totags = []
	base = 0
	fromindex = []
	fromtags = []
	fromwhich = 1
	length = 0
	towhich = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify_one')
	funcPy(toindex = toindex,totags = totags,base = base,fromindex = fromindex,fromtags = fromtags,fromwhich = fromwhich,length = length,towhich = towhich)
	pytest_toindex = []
	pytest_totags = []
	assert toindex == pytest_toindex
	assert totags == pytest_totags


