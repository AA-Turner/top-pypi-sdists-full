import pytest
import numpy
import kernels

def test_awkward_UnionArray_simplify_1():
	toindex = []
	totags = []
	base = 0
	innerindex = []
	innertags = []
	innerwhich = 0
	length = 0
	outerindex = []
	outertags = []
	outerwhich = 1
	towhich = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify')
	funcPy(toindex = toindex,totags = totags,base = base,innerindex = innerindex,innertags = innertags,innerwhich = innerwhich,length = length,outerindex = outerindex,outertags = outertags,outerwhich = outerwhich,towhich = towhich)
	pytest_toindex = []
	pytest_totags = []
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_2():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	totags = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	base = 0
	innerindex = [0, 0, 1, 1, 2, 3, 2]
	innertags = [0, 1, 0, 1, 0, 0, 1]
	innerwhich = 0
	length = 12
	outerindex = [0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4]
	outertags = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
	outerwhich = 1
	towhich = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify')
	funcPy(toindex = toindex,totags = totags,base = base,innerindex = innerindex,innertags = innertags,innerwhich = innerwhich,length = length,outerindex = outerindex,outertags = outertags,outerwhich = outerwhich,towhich = towhich)
	pytest_toindex = [123, 123, 0, 123, 1, 123, 123, 2, 3, 123, 123, 123]
	pytest_totags = [123, 123, 1, 123, 1, 123, 123, 1, 1, 123, 123, 123]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


def test_awkward_UnionArray_simplify_3():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	totags = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	base = 5
	innerindex = [0, 0, 1, 1, 2, 3, 2]
	innertags = [0, 1, 0, 1, 0, 0, 1]
	innerwhich = 1
	length = 12
	outerindex = [0, 1, 0, 1, 2, 2, 3, 4, 5, 3, 6, 4]
	outertags = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
	outerwhich = 1
	towhich = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_simplify')
	funcPy(toindex = toindex,totags = totags,base = base,innerindex = innerindex,innertags = innertags,innerwhich = innerwhich,length = length,outerindex = outerindex,outertags = outertags,outerwhich = outerwhich,towhich = towhich)
	pytest_toindex = [123, 123, 123, 5, 123, 123, 6, 123, 123, 123, 7, 123]
	pytest_totags = [123, 123, 123, 0, 123, 123, 0, 123, 123, 123, 0, 123]
	assert toindex == pytest_toindex
	assert totags == pytest_totags


