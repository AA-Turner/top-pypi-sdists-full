import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_1():
	missing = []
	nextshifts = []
	nummissing = []
	length = 0
	maxcount = 0
	nextcarry = []
	nextlen = 0
	offsets = []
	parents = []
	starts = []
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = []
	pytest_nextshifts = []
	pytest_nummissing = []
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_2():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123, 123]
	length = 3
	maxcount = 5
	nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	nextlen = 15
	offsets = [0, 5, 10, 15]
	parents = [0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nummissing = [0, 0, 0, 0, 0]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_3():
	missing = [123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 2
	maxcount = 3
	nextcarry = [0, 3, 1, 4, 2, 5]
	nextlen = 6
	offsets = [0, 3, 6]
	parents = [0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0]
	pytest_nummissing = [0, 0, 0]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_4():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123, 123]
	length = 3
	maxcount = 5
	nextcarry = [0, 5, 9, 1, 6, 10, 2, 7, 11, 3, 8, 4]
	nextlen = 12
	offsets = [0, 5, 9, 12]
	parents = [0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nummissing = [0, 0, 0, 1, 2]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_5():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123, 123]
	length = 5
	maxcount = 5
	nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
	nextlen = 17
	offsets = [0, 5, 8, 11, 14, 17]
	parents = [0, 0, 0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nummissing = [0, 0, 0, 4, 4]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_6():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 2, 5, 7, 1, 3, 6, 8, 4]
	nextlen = 9
	offsets = [0, 2, 5, 7, 9]
	parents = [0, 0, 1, 1]
	starts = [0, 2]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 1, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1]
	pytest_nummissing = [0, 0, 2]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_7():
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123]
	length = 3
	maxcount = 4
	nextcarry = [0, 2, 3, 1, 4, 5, 6]
	nextlen = 7
	offsets = [0, 2, 3, 7]
	parents = [0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 1, 2, 2]
	pytest_nextshifts = [0, 0, 0, 0, 1, 2, 2]
	pytest_nummissing = [0, 1, 2, 2]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_8():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 10
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
	pytest_nummissing = [0, 2, 4]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_9():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
	pytest_nummissing = [0, 2, 4]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_10():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
	pytest_nummissing = [0, 2, 4]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_11():
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123]
	length = 3
	maxcount = 4
	nextcarry = [0, 3, 1, 4, 2, 5, 6]
	nextlen = 7
	offsets = [0, 3, 3, 7]
	parents = [0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 1, 1, 1, 2]
	pytest_nextshifts = [0, 1, 0, 1, 0, 1, 2]
	pytest_nummissing = [1, 1, 1, 2]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_12():
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 3, 5, 1, 4, 6, 2]
	nextlen = 7
	offsets = [0, 3, 5, 5, 7]
	parents = [0, 0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 0, 0, 1, 1]
	pytest_nextshifts = [0, 0, 1, 0, 0, 1, 0]
	pytest_nummissing = [1, 1, 3]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_13():
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 3, 5, 1, 4, 6, 2]
	nextlen = 7
	offsets = [0, 3, 3, 5, 7]
	parents = [0, 0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 0, 1, 1, 1, 1]
	pytest_nextshifts = [0, 1, 1, 0, 1, 1, 0]
	pytest_nummissing = [1, 1, 3]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_14():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_15():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_16():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_17():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_18():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_19():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_20():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_21():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_22():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_23():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_24():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_25():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1, 3, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_26():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 2, 3, 2]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_27():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2, 1, 2, 2, 3, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_28():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3]
	pytest_nummissing = [1, 3, 5]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_29():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
	starts = [0, 5]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 3, 3, 3, 2, 4]
	pytest_nummissing = [2, 4, 6]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_30():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 13
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 3, 3, 3, 2, 4]
	pytest_nummissing = [2, 4, 6]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_31():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123]
	length = 13
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
	starts = [0, 6]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4]
	pytest_nummissing = [2, 4, 6]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_32():
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nummissing = [123, 123, 123, 123]
	length = 9
	maxcount = 4
	nextcarry = [0, 1, 3, 6, 10, 13, 15, 2, 4, 7, 11, 14, 5, 8, 12, 9]
	nextlen = 16
	offsets = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
	parents = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(missing = missing,nextshifts = nextshifts,nummissing = nummissing,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,parents = parents,starts = starts)
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4]
	pytest_nummissing = [2, 4, 6, 8]
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts
	assert nummissing == pytest_nummissing


