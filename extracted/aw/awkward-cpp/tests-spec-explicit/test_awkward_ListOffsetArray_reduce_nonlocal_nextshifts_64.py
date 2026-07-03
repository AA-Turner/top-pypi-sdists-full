import pytest
import numpy
import kernels

def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_1():
	nummissing = []
	missing = []
	nextshifts = []
	length = 0
	maxcount = 0
	nextcarry = []
	nextlen = 0
	offsets = []
	starts = []
	outer_offsets = [0]
	outlength = 0
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = []
	pytest_missing = []
	pytest_nextshifts = []
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_2():
	nummissing = [123, 123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	maxcount = 5
	nextcarry = [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
	nextlen = 15
	offsets = [0, 5, 10, 15]
	starts = [0]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 0, 0, 0, 0]
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_3():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123]
	length = 2
	maxcount = 3
	nextcarry = [0, 3, 1, 4, 2, 5]
	nextlen = 6
	offsets = [0, 3, 6]
	starts = [0]
	outer_offsets = [0, 2]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 0, 0]
	pytest_missing = [0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_4():
	nummissing = [123, 123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 3
	maxcount = 5
	nextcarry = [0, 5, 9, 1, 6, 10, 2, 7, 11, 3, 8, 4]
	nextlen = 12
	offsets = [0, 5, 9, 12]
	starts = [0]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 0, 0, 1, 2]
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_5():
	nummissing = [123, 123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 5
	maxcount = 5
	nextcarry = [0, 5, 8, 11, 14, 1, 6, 9, 12, 15, 2, 7, 10, 13, 16, 3, 4]
	nextlen = 17
	offsets = [0, 5, 8, 11, 14, 17]
	starts = [0]
	outer_offsets = [0, 5]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 0, 0, 4, 4]
	pytest_missing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_6():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 2, 5, 7, 1, 3, 6, 8, 4]
	nextlen = 9
	offsets = [0, 2, 5, 7, 9]
	starts = [0, 2]
	outer_offsets = [0, 2, 4]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 0, 2]
	pytest_missing = [0, 0, 0, 0, 1, 0, 0, 0, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_7():
	nummissing = [123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	length = 3
	maxcount = 4
	nextcarry = [0, 2, 3, 1, 4, 5, 6]
	nextlen = 7
	offsets = [0, 2, 3, 7]
	starts = [0]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 1, 2, 2]
	pytest_missing = [0, 0, 0, 0, 1, 2, 2]
	pytest_nextshifts = [0, 0, 0, 0, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_8():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 10
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 10]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 2, 4]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_9():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 2, 4]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_10():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [0, 2, 4]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_11():
	nummissing = [123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	length = 3
	maxcount = 4
	nextcarry = [0, 3, 1, 4, 2, 5, 6]
	nextlen = 7
	offsets = [0, 3, 3, 7]
	starts = [0]
	outer_offsets = [0, 3]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 1, 1, 2]
	pytest_missing = [0, 0, 0, 1, 1, 1, 2]
	pytest_nextshifts = [0, 1, 0, 1, 0, 1, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_12():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 3, 5, 1, 4, 6, 2]
	nextlen = 7
	offsets = [0, 3, 5, 5, 7]
	starts = [0]
	outer_offsets = [0, 4]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 1, 3]
	pytest_missing = [0, 0, 0, 0, 0, 1, 1]
	pytest_nextshifts = [0, 0, 1, 0, 0, 1, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_13():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123]
	length = 4
	maxcount = 3
	nextcarry = [0, 3, 5, 1, 4, 6, 2]
	nextlen = 7
	offsets = [0, 3, 3, 5, 7]
	starts = [0]
	outer_offsets = [0, 4]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 1, 3]
	pytest_missing = [0, 0, 0, 1, 1, 1, 1]
	pytest_nextshifts = [0, 1, 1, 0, 1, 1, 0]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_14():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_15():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_16():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_17():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_18():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 11
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 11]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_19():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_20():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_21():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_22():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_23():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_24():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 18, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 0]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 3, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_25():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1, 3, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_26():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 15, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 0, 1, 2, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 2, 3, 2]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_27():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 10, 12, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 0, 0, 1, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2, 1, 2, 2, 3, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_28():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [1, 3, 5]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_29():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 12
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 5]
	outer_offsets = [0, 5, 12]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [2, 4, 6]
	pytest_missing = [0, 0, 1, 0, 1, 2, 0, 1, 0, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 3, 3, 3, 2, 4]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_30():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 13
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 1, 3, 6, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 13]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [2, 4, 6]
	pytest_missing = [0, 0, 1, 0, 1, 2, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 3, 3, 3, 2, 4]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_31():
	nummissing = [123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 13
	maxcount = 3
	nextcarry = [0, 1, 3, 6, 8, 9, 10, 12, 15, 17, 2, 4, 7, 11, 13, 16, 5, 14]
	nextlen = 18
	offsets = [0, 0, 1, 3, 6, 8, 9, 9, 9, 10, 12, 15, 17, 18]
	starts = [0, 6]
	outer_offsets = [0, 6, 13]
	outlength = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [2, 4, 6]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 1, 2, 2, 3, 2, 3, 4, 2, 3, 2]
	pytest_nextshifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


def test_awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64_32():
	nummissing = [123, 123, 123, 123]
	missing = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextshifts = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 9
	maxcount = 4
	nextcarry = [0, 1, 3, 6, 10, 13, 15, 2, 4, 7, 11, 14, 5, 8, 12, 9]
	nextlen = 16
	offsets = [0, 0, 1, 3, 6, 10, 13, 15, 16, 16]
	starts = [0]
	outer_offsets = [0, 9]
	outlength = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_reduce_nonlocal_nextshifts_64')
	funcPy(nummissing = nummissing,missing = missing,nextshifts = nextshifts,length = length,maxcount = maxcount,nextcarry = nextcarry,nextlen = nextlen,offsets = offsets,starts = starts,outer_offsets = outer_offsets,outlength = outlength)
	pytest_nummissing = [2, 4, 6, 8]
	pytest_missing = [1, 1, 2, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1]
	pytest_nextshifts = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4]
	assert nummissing == pytest_nummissing
	assert missing == pytest_missing
	assert nextshifts == pytest_nextshifts


