import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_overlay_mask_1():
	tomask = []
	length = 0
	mymask = []
	theirmask = []
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = []
	assert tomask == pytest_tomask


def test_awkward_ByteMaskedArray_overlay_mask_2():
	tomask = [123, 123]
	length = 2
	mymask = [0, 0]
	theirmask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [0, 0]
	assert tomask == pytest_tomask


def test_awkward_ByteMaskedArray_overlay_mask_3():
	tomask = [123, 123]
	length = 2
	mymask = [0, 0]
	theirmask = [0, 0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [1, 1]
	assert tomask == pytest_tomask


def test_awkward_ByteMaskedArray_overlay_mask_4():
	tomask = [123, 123]
	length = 2
	mymask = [1, 0]
	theirmask = [0, 1]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [1, 1]
	assert tomask == pytest_tomask


def test_awkward_ByteMaskedArray_overlay_mask_5():
	tomask = [123, 123]
	length = 2
	mymask = [0, 0]
	theirmask = [0, 1]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [0, 1]
	assert tomask == pytest_tomask


def test_awkward_ByteMaskedArray_overlay_mask_6():
	tomask = [123, 123]
	length = 2
	mymask = [1, 0]
	theirmask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [1, 0]
	assert tomask == pytest_tomask


