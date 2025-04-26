import pytest
import numpy
import kernels

def test_awkward_localindex_1():
	toindex = []
	length = 0
	funcPy = getattr(kernels, 'awkward_localindex')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = []
	assert toindex == pytest_toindex


def test_awkward_localindex_2():
	toindex = [123, 123]
	length = 2
	funcPy = getattr(kernels, 'awkward_localindex')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 1]
	assert toindex == pytest_toindex


def test_awkward_localindex_3():
	toindex = [123, 123, 123, 123]
	length = 4
	funcPy = getattr(kernels, 'awkward_localindex')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 1, 2, 3]
	assert toindex == pytest_toindex


def test_awkward_localindex_4():
	toindex = [123, 123, 123, 123, 123]
	length = 5
	funcPy = getattr(kernels, 'awkward_localindex')
	funcPy(toindex = toindex,length = length)
	pytest_toindex = [0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


