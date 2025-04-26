import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_1():
	nextcarry = []
	nextparents = []
	maxnextparents = [123]
	distincts = []
	length = 0
	maxcount = 0
	distinctslen = 0
	nextlen = 0
	parents = []
	offsets = []
	offsetscopy = []
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = []
	pytest_nextparents = []
	pytest_maxnextparents = [0]
	pytest_distincts = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_2():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = []
	length = 3
	maxcount = 5
	distinctslen = 0
	nextlen = 15
	parents = [0, 0, 0]
	offsets = [0, 5, 10, 15]
	offsetscopy = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	pytest_nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	pytest_maxnextparents = [4]
	pytest_distincts = []
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_3():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123]
	length = 3
	maxcount = 5
	distinctslen = 2
	nextlen = 15
	parents = [0, 0, 0]
	offsets = [0, 5, 10, 15]
	offsetscopy = [0, 5, 10, 15]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	pytest_nextparents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	pytest_maxnextparents = [4]
	pytest_distincts = [0, 0]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_4():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123]
	length = 2
	maxcount = 3
	distinctslen = 2
	nextlen = 6
	parents = [0, 0]
	offsets = [0, 3, 6]
	offsetscopy = [0, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 3, 1, 4, 2, 5]
	pytest_nextparents = [0, 0, 1, 1, 2, 2]
	pytest_maxnextparents = [2]
	pytest_distincts = [0, 0]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_5():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 5
	maxcount = 5
	distinctslen = 6
	nextlen = 17
	parents = [0, 0, 0, 0, 0]
	offsets = [0, 5, 8, 11, 14, 17]
	offsetscopy = [0, 5, 8, 11, 14, 17]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
	pytest_nextparents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 4]
	pytest_maxnextparents = [4]
	pytest_distincts = [0, 0, 0, 0, 0, -1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_6():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 10
	maxcount = 3
	distinctslen = 6
	nextlen = 18
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	pytest_nextparents = [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 1, 1, 1, 4, 4, 4, 2, 5]
	pytest_maxnextparents = [5]
	pytest_distincts = [0, 0, 0, 1, 1, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_7():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextparents = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 10
	maxcount = 4
	distinctslen = 6
	nextlen = 18
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextparents = nextparents,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,parents = parents,offsets = offsets,offsetscopy = offsetscopy)
	pytest_nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	pytest_nextparents = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 1, 1, 1, 5, 5, 5, 2, 6]
	pytest_maxnextparents = [6]
	pytest_distincts = [0, 0, 0, -1, 1, 1]
	assert nextcarry == pytest_nextcarry
	assert nextparents == pytest_nextparents
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


