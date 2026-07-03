import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_1():
	nextcarry = []
	nextoffsets = [123]
	maxnextparents = [123]
	distincts = []
	length = 0
	maxcount = 0
	distinctslen = 0
	nextlen = 0
	offsets = []
	offsetscopy = []
	outer_offsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = []
	pytest_nextoffsets = [0]
	pytest_maxnextparents = [-1]
	pytest_distincts = []
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_2():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = []
	length = 3
	maxcount = 5
	distinctslen = 0
	nextlen = 15
	offsets = [0, 5, 10, 15]
	offsetscopy = [0, 5, 10, 15]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	pytest_nextoffsets = [0, 3, 6, 9, 12, 15]
	pytest_maxnextparents = [4]
	pytest_distincts = []
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_3():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123]
	length = 3
	maxcount = 5
	distinctslen = 2
	nextlen = 15
	offsets = [0, 5, 10, 15]
	offsetscopy = [0, 5, 10, 15]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	pytest_nextoffsets = [0, 3, 6, 9, 12, 15]
	pytest_maxnextparents = [4]
	pytest_distincts = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_4():
	nextcarry = [123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123]
	length = 2
	maxcount = 3
	distinctslen = 2
	nextlen = 6
	offsets = [0, 3, 6]
	offsetscopy = [0, 3, 6]
	outer_offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 3, 1, 4, 2, 5]
	pytest_nextoffsets = [0, 2, 4, 6]
	pytest_maxnextparents = [2]
	pytest_distincts = [0, 1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_5():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 5
	maxcount = 5
	distinctslen = 6
	nextlen = 17
	offsets = [0, 5, 8, 11, 14, 17]
	offsetscopy = [0, 5, 8, 11, 14, 17]
	outer_offsets = [0, 5]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
	pytest_nextoffsets = [0, 5, 10, 15, 16, 17]
	pytest_maxnextparents = [4]
	pytest_distincts = [0, 1, 2, 3, 4, -1]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_6():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 10
	maxcount = 3
	distinctslen = 6
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	outer_offsets = [0, 5, 10]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 1, 3, 6, 8, 2, 4, 7, 5, 9, 10, 12, 15, 17, 11, 13, 16, 14]
	pytest_nextoffsets = [0, 5, 8, 9, 14, 17, 18]
	pytest_maxnextparents = [5]
	pytest_distincts = [0, 1, 2, 3, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


def test_awkward_ListOffsetArray_reduce_nonlocal_preparenext_64_7():
	nextcarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextoffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	maxnextparents = [123]
	distincts = [123, 123, 123, 123, 123, 123]
	length = 10
	maxcount = 4
	distinctslen = 6
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	offsetscopy = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	outer_offsets = [0, 5, 10]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_preparenext_64')
	funcPy(nextcarry = nextcarry,nextoffsets = nextoffsets,maxnextparents = maxnextparents,distincts = distincts,length = length,maxcount = maxcount,distinctslen = distinctslen,nextlen = nextlen,offsets = offsets,offsetscopy = offsetscopy,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nextcarry = [0, 1, 3, 6, 8, 2, 4, 7, 5, 9, 10, 12, 15, 17, 11, 13, 16, 14]
	pytest_nextoffsets = [0, 5, 8, 9, 9, 14, 17, 18, 18]
	pytest_maxnextparents = [6]
	pytest_distincts = [0, 1, 2, -1, 4, 5]
	assert nextcarry == pytest_nextcarry
	assert nextoffsets == pytest_nextoffsets
	assert maxnextparents == pytest_maxnextparents
	assert distincts == pytest_distincts


