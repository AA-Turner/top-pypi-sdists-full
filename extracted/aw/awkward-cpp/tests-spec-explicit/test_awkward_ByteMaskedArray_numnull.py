import pytest
import numpy
import kernels

def test_awkward_ByteMaskedArray_numnull_1():
	numnull = [123]
	length = 0
	mask = []
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_2():
	numnull = [123]
	length = 4
	mask = [0, 0, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_3():
	numnull = [123]
	length = 2
	mask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_4():
	numnull = [123]
	length = 1
	mask = [0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [0]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_5():
	numnull = [123]
	length = 30
	mask = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [10]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_6():
	numnull = [123]
	length = 30
	mask = [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [10]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_7():
	numnull = [123]
	length = 30
	mask = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [10]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_8():
	numnull = [123]
	length = 4
	mask = [0, 1, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [1]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_9():
	numnull = [123]
	length = 1
	mask = [0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [1]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_10():
	numnull = [123]
	length = 3
	mask = [0, 1, 1]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [1]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_11():
	numnull = [123]
	length = 6
	mask = [0, 0, 1, 1, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_12():
	numnull = [123]
	length = 5
	mask = [0, 0, 1, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_13():
	numnull = [123]
	length = 9
	mask = [0, 1, 0, 0, 0, 0, 1, 0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_14():
	numnull = [123]
	length = 6
	mask = [0, 1, 0, 0, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_15():
	numnull = [123]
	length = 3
	mask = [0, 1, 0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_16():
	numnull = [123]
	length = 3
	mask = [1, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [2]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_17():
	numnull = [123]
	length = 8
	mask = [0, 1, 0, 0, 1, 0, 1, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [3]
	assert numnull == pytest_numnull


def test_awkward_ByteMaskedArray_numnull_18():
	numnull = [123]
	length = 10
	mask = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0]
	validwhen = True
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_numnull')
	funcPy(numnull = numnull,length = length,mask = mask,validwhen = validwhen)
	pytest_numnull = [5]
	assert numnull == pytest_numnull


