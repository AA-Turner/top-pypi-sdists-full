import pytest
import numpy
import kernels

def test_awkward_reduce_prod_1():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 1, 0, 0]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 1, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_2():
	toptr = []
	fromptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_3():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 1, 12, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 31, 101, 3, 59, 37, 103, 5, 61, 41, 107, 7, 67, 43, 109, 11, 71, 47, 113]
	lenparents = 20
	outlength = 15
	parents = [0, 0, 10, 10, 1, 1, 11, 11, 2, 2, 12, 12, 3, 3, 13, 13, 4, 4, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 1, 1, 1, 1, 1, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 47, 113]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 1, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_6():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 11, 71, 29, 97, 47]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 4, 4, 9, 9, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 43, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_7():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97]
	lenparents = 28
	outlength = 14
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47]
	lenparents = 29
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47, 113]
	lenparents = 30
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 47]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [106, 177, 305, 469, 781, 949, 1343, 1577, 2047, 29, 3131, 3811, 4387, 4687, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_11():
	toptr = [123, 123, 123]
	fromptr = [0]
	lenparents = 1
	outlength = 3
	parents = [2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_12():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
	lenparents = 20
	outlength = 6
	parents = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [13710311357, 1, 907383479, 95041567, 1, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_13():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 73, 79, 83, 89, 97, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 13, 17, 19, 23, 29, 2, 3, 5, 7, 11]
	lenparents = 30
	outlength = 6
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [13710311357, 4132280413, 907383479, 95041567, 2800733, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_14():
	toptr = [123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
	lenparents = 20
	outlength = 4
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [13710311357, 907383479, 95041567, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_15():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 17, 29, 3, 11, 19, 31, 5, 13, 23, 37]
	lenparents = 12
	outlength = 6
	parents = [0, 0, 3, 3, 1, 1, 4, 4, 2, 2, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [14, 33, 65, 493, 589, 851]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_16():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [159, 295, 427, 67, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_17():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	lenparents = 29
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [159, 295, 427, 737, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_18():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 97, 47, 113]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [159, 295, 427, 737, 71, 949, 1343, 1577, 2047, 97, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_19():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [182, 33, 5, 1, 1, 1, 391, 19]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_20():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
	lenparents = 12
	outlength = 3
	parents = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [210, 46189, 765049]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_21():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
	lenparents = 20
	outlength = 6
	parents = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2310, 1, 95041567, 907383479, 1, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_22():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
	lenparents = 30
	outlength = 6
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2310, 2800733, 95041567, 907383479, 4132280413, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_23():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
	lenparents = 20
	outlength = 4
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2310, 95041567, 907383479, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_24():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 3, 11, 5]
	lenparents = 5
	outlength = 8
	parents = [0, 6, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 3, 5, 1, 1, 1, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_25():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [5, 53, 13, 73, 31, 101, 7, 59, 17, 79, 37, 103, 11, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	lenparents = 28
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 8, 8, 13, 13, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [265, 413, 671, 67, 71, 949, 1343, 1577, 2047, 2813, 3131, 3811, 4387, 4687, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_26():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
	lenparents = 12
	outlength = 8
	parents = [0, 0, 0, 3, 3, 3, 4, 4, 4, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 1, 1001, 7429, 1, 1, 33263]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_27():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13]
	lenparents = 6
	outlength = 4
	parents = [0, 0, 0, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 77, 13]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_28():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 77, 13, 323, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_29():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	lenparents = 8
	outlength = 5
	parents = [0, 0, 0, 2, 2, 3, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 77, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_30():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [6, 5, 7, 11, 13, 17, 19]
	lenparents = 7
	outlength = 5
	parents = [0, 0, 2, 2, 3, 4, 4]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 77, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_31():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	lenparents = 5
	outlength = 3
	parents = [0, 0, 0, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 1, 77]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_32():
	toptr = [123]
	fromptr = [2, 3, 5]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_33():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	lenparents = 5
	outlength = 4
	parents = [0, 0, 0, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 7, 11, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_34():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	lenparents = 5
	outlength = 3
	parents = [0, 0, 0, 1, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [30, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_35():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 31, 53, 2, 103, 37, 59, 3, 107, 41, 61, 5, 109, 43, 67, 7, 113, 47, 71, 11]
	lenparents = 20
	outlength = 15
	parents = [0, 0, 10, 10, 1, 1, 11, 11, 2, 2, 12, 12, 3, 3, 13, 13, 4, 4, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3131, 3811, 4387, 4687, 5311, 1, 1, 1, 1, 1, 106, 177, 305, 469, 781]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_36():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 31, 73, 13, 53, 2, 103, 37, 79, 17, 59, 3, 107, 41, 83, 19, 61, 5, 109, 43, 89, 23, 67, 7, 113, 47, 97, 29, 71, 11]
	lenparents = 30
	outlength = 15
	parents = [0, 0, 5, 5, 10, 10, 1, 1, 6, 6, 11, 11, 2, 2, 7, 7, 12, 12, 3, 3, 8, 8, 13, 13, 4, 4, 9, 9, 14, 14]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3131, 3811, 4387, 4687, 5311, 949, 1343, 1577, 2047, 2813, 106, 177, 305, 469, 781]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_37():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
	lenparents = 11
	outlength = 12
	parents = [0, 0, 3, 9, 9, 1, 1, 10, 10, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, -1, 1, 1, 1, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_38():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
	lenparents = 11
	outlength = 12
	parents = [0, 0, 6, 9, 9, 1, 1, 10, 10, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, -1, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_39():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 13, 37]
	lenparents = 10
	outlength = 12
	parents = [0, 0, 9, 9, 1, 1, 10, 10, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, 1, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_40():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
	lenparents = 8
	outlength = 12
	parents = [0, 0, 3, 9, 1, 1, 10, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, -1, 1, 1, 1, 1, 1, 29, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_41():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
	lenparents = 8
	outlength = 12
	parents = [0, 0, 6, 9, 1, 1, 10, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, -1, 1, 1, 29, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_42():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 29, 3, 19, 31, 37]
	lenparents = 7
	outlength = 12
	parents = [0, 0, 9, 1, 1, 10, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, 1, 1, 1, 29, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_43():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
	lenparents = 12
	outlength = 12
	parents = [0, 0, 6, 6, 9, 9, 1, 1, 10, 10, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, -39, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_44():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
	lenparents = 9
	outlength = 12
	parents = [0, 0, 6, 6, 9, 1, 1, 10, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, 1, 1, 1, -39, 1, 1, 29, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_45():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 5, 23, 13, 37]
	lenparents = 12
	outlength = 12
	parents = [0, 0, 9, 9, 1, 1, 10, 10, 2, 2, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 115, 1, 1, 1, 1, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_46():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
	lenparents = 12
	outlength = 12
	parents = [0, 0, 3, 3, 9, 9, 1, 1, 10, 10, 11, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, -39, 1, 1, 1, 1, 1, 203, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_47():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
	lenparents = 9
	outlength = 12
	parents = [0, 0, 3, 3, 9, 1, 1, 10, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 1, -39, 1, 1, 1, 1, 1, 29, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_48():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 23, 13, 29, 3, 19, 11, 5]
	lenparents = 10
	outlength = 7
	parents = [0, 0, 3, 3, 6, 6, 1, 1, 4, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 5, 161, 11, 1, 377]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_49():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 23, 7, 13, 3, 19, 11, 5]
	lenparents = 9
	outlength = 10
	parents = [0, 0, 3, 6, 9, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [34, 57, 5, 23, 1, 1, 7, 11, 1, 13]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_50():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 11, 17, 7, 19, 3, 13, 23, 5]
	lenparents = 9
	outlength = 5
	parents = [0, 0, 0, 3, 3, 1, 1, 4, 2]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [374, 39, 5, 133, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_51():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 73, 53, 31, 13, 2, 103, 79, 59, 37, 17, 3, 107, 83, 61, 41, 19, 5, 109, 89, 67, 43, 23, 7, 113, 97, 71, 47, 29, 11]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [390769, 480083, 541741, 649967, 778231, 806, 1887, 3895, 6923, 14993]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_52():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 11, 23, 3, 13, 29, 5, 17, 31, 7, 19, 37]
	lenparents = 12
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [506, 1131, 2635, 4921]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_53():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 53, 31, 2, 103, 59, 37, 3, 107, 61, 41, 5, 109, 67, 43, 7, 113, 71, 47, 11]
	lenparents = 20
	outlength = 10
	parents = [0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5353, 6077, 6527, 7303, 8023, 62, 111, 205, 301, 517]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_54():
	toptr = [123]
	fromptr = [1, 2, 3]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_55():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 31, 53, 101, 3, 37, 59, 103, 5, 41, 61, 107, 7, 43, 67, 109, 11, 47, 71, 113]
	lenparents = 20
	outlength = 10
	parents = [0, 0, 5, 5, 1, 1, 6, 6, 2, 2, 7, 7, 3, 3, 8, 8, 4, 4, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [62, 111, 205, 301, 517, 5353, 6077, 6527, 7303, 8023]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_56():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	lenparents = 8
	outlength = 7
	parents = [0, 0, 1, 2, 3, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6, 5, 7, 11, 13, 17, 19]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_57():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	lenparents = 8
	outlength = 6
	parents = [0, 0, 1, 2, 3, 4, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6, 5, 7, 11, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_58():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [720]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_59():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 13, 31, 53, 73, 101, 3, 17, 37, 59, 79, 103, 5, 19, 41, 61, 83, 107, 7, 23, 43, 67, 89, 109, 11, 29, 47, 71, 97, 113]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 5, 5, 5, 1, 1, 1, 6, 6, 6, 2, 2, 2, 7, 7, 7, 3, 3, 3, 8, 8, 8, 4, 4, 4, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [806, 1887, 3895, 6923, 14993, 390769, 480083, 541741, 649967, 778231]
	assert toptr == pytest_toptr


