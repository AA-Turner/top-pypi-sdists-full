import pytest
import numpy
import kernels

def test_awkward_UnionArray_nestedfill_tags_index_1():
	totags = []
	toindex = []
	tmpstarts = []
	tmpstarts = []
	fromcounts = []
	length = 0
	tag = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_nestedfill_tags_index')
	funcPy(totags = totags,toindex = toindex,tmpstarts = tmpstarts,fromcounts = fromcounts,length = length,tag = tag)
	pytest_totags = []
	pytest_toindex = []
	pytest_tmpstarts = []
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tmpstarts == pytest_tmpstarts


def test_awkward_UnionArray_nestedfill_tags_index_2():
	totags = [123]
	toindex = [123]
	tmpstarts = [123]
	tmpstarts = [0]
	fromcounts = [1]
	length = 1
	tag = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_nestedfill_tags_index')
	funcPy(totags = totags,toindex = toindex,tmpstarts = tmpstarts,fromcounts = fromcounts,length = length,tag = tag)
	pytest_totags = [1]
	pytest_toindex = [0]
	pytest_tmpstarts = [1]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tmpstarts == pytest_tmpstarts


def test_awkward_UnionArray_nestedfill_tags_index_3():
	totags = [123, 123, 123]
	toindex = [123, 123, 123]
	tmpstarts = [123, 123]
	tmpstarts = [0, 1]
	fromcounts = [1, 2]
	length = 2
	tag = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_nestedfill_tags_index')
	funcPy(totags = totags,toindex = toindex,tmpstarts = tmpstarts,fromcounts = fromcounts,length = length,tag = tag)
	pytest_totags = [0, 0, 0]
	pytest_toindex = [0, 1, 2]
	pytest_tmpstarts = [1, 3]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tmpstarts == pytest_tmpstarts


def test_awkward_UnionArray_nestedfill_tags_index_4():
	totags = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	tmpstarts = [123, 123, 123, 123, 123]
	tmpstarts = [0, 5, 5, 6, 8]
	fromcounts = [5, 0, 2, 3, 1]
	length = 5
	tag = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_nestedfill_tags_index')
	funcPy(totags = totags,toindex = toindex,tmpstarts = tmpstarts,fromcounts = fromcounts,length = length,tag = tag)
	pytest_totags = [1, 1, 1, 1, 1, 1, 1, 1, 1]
	pytest_toindex = [0, 1, 2, 3, 4, 5, 7, 8, 10]
	pytest_tmpstarts = [5, 5, 7, 9, 9]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tmpstarts == pytest_tmpstarts


def test_awkward_UnionArray_nestedfill_tags_index_5():
	totags = [123, 123, 123, 123, 123, 123, 123]
	toindex = [123, 123, 123, 123, 123, 123, 123]
	tmpstarts = [123, 123, 123, 123, 123]
	tmpstarts = [0, 2, 4, 5, 7]
	fromcounts = [2, 3, 2, 2, 0]
	length = 5
	tag = 1
	funcPy = getattr(kernels, 'awkward_UnionArray_nestedfill_tags_index')
	funcPy(totags = totags,toindex = toindex,tmpstarts = tmpstarts,fromcounts = fromcounts,length = length,tag = tag)
	pytest_totags = [1, 1, 1, 1, 1, 1, 1]
	pytest_toindex = [0, 1, 2, 3, 5, 7, 8]
	pytest_tmpstarts = [2, 5, 6, 7, 7]
	assert totags == pytest_totags
	assert toindex == pytest_toindex
	assert tmpstarts == pytest_tmpstarts


