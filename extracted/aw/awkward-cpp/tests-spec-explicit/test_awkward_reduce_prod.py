import pytest
import numpy
import kernels

def test_awkward_reduce_prod_1():
	toptr = [123, 123, 123, 123]
	fromptr = [1, 0, 0, 1, 0, 0]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_2():
	toptr = []
	fromptr = []
	outlength = 0
	offsets = [0]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_3():
	toptr = [123, 123, 123, 123]
	fromptr = [0, 1, 2, 3, 4, 5]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [0, 1, 12, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 31, 101, 3, 59, 37, 103, 5, 61, 41, 107, 7, 67, 43, 109, 11, 71, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 12, 14, 16, 18, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 3131, 177, 3811, 305, 1, 1, 1, 1, 1, 4387, 469, 4687, 781, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_5():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 18, 20, 22, 24, 26, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 1, 469, 2047, 4687, 781, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_6():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 11, 71, 29, 97, 47]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 27, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 473, 2059, 97, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_7():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97]
	outlength = 14
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 29]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 97, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 469, 2047, 4687, 781, 2813, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 53, 13, 73, 31, 101, 3, 59, 17, 79, 37, 103, 5, 61, 19, 83, 41, 107, 7, 67, 23, 89, 43, 109, 11, 71, 29, 47]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [106, 949, 3131, 177, 1343, 3811, 305, 1577, 4387, 7, 1541, 3827, 1199, 2059, 47]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_11():
	toptr = [123, 123, 123]
	fromptr = [0]
	outlength = 3
	offsets = [0, 0, 0, 1]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [1, 1, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_12():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
	outlength = 6
	offsets = [0, 5, 5, 10, 15, 15, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [13710311357, 1, 907383479, 95041567, 1, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_13():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 73, 79, 83, 89, 97, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 13, 17, 19, 23, 29, 2, 3, 5, 7, 11]
	outlength = 6
	offsets = [0, 5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [13710311357, 4132280413, 907383479, 95041567, 2800733, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_14():
	toptr = [123, 123, 123, 123]
	fromptr = [101, 103, 107, 109, 113, 53, 59, 61, 67, 71, 31, 37, 41, 43, 47, 2, 3, 5, 7, 11]
	outlength = 4
	offsets = [0, 5, 10, 15, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [13710311357, 907383479, 95041567, 2310]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_15():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 17, 29, 3, 11, 19, 31, 5, 13, 23, 37]
	outlength = 6
	offsets = [0, 2, 4, 6, 8, 10, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [14, 493, 33, 589, 65, 851]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_16():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [159, 949, 3131, 5, 59, 1343, 3811, 427, 1577, 4387, 1541, 3827, 7739, 2813, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_17():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [159, 949, 3131, 295, 17, 2923, 721, 1159, 3403, 1177, 1541, 3827, 7739, 2813, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_18():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [3, 53, 13, 73, 31, 101, 5, 59, 17, 79, 37, 103, 7, 61, 19, 83, 41, 107, 11, 67, 23, 89, 43, 109, 71, 97, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [159, 949, 3131, 295, 17, 2923, 721, 1159, 3403, 107, 737, 2047, 4687, 6887, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_19():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 13, 17, 23, 3, 11, 19, 5]
	outlength = 8
	offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [182, 391, 3, 1, 1, 1, 209, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_20():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
	outlength = 3
	offsets = [0, 4, 8, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [210, 46189, 765049]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_21():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
	outlength = 6
	offsets = [0, 5, 5, 10, 15, 15, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [2310, 1, 95041567, 907383479, 1, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_22():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
	outlength = 6
	offsets = [0, 5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [2310, 2800733, 95041567, 907383479, 4132280413, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_23():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 101, 103, 107, 109, 113]
	outlength = 4
	offsets = [0, 5, 10, 15, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [2310, 95041567, 907383479, 13710311357]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_24():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 7, 3, 11, 5]
	outlength = 8
	offsets = [0, 1, 2, 3, 3, 3, 3, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [2, 7, 3, 1, 1, 1, 11, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_25():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [5, 53, 13, 73, 31, 101, 7, 59, 17, 79, 37, 103, 11, 61, 19, 83, 41, 107, 67, 23, 89, 43, 109, 71, 29, 97, 47, 113]
	outlength = 15
	offsets = [0, 2, 4, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [265, 949, 3131, 7, 59, 1343, 3811, 671, 1577, 4387, 1541, 3827, 7739, 2813, 5311]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_26():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
	outlength = 8
	offsets = [0, 3, 3, 3, 6, 9, 9, 9, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 1, 1001, 7429, 1, 1, 33263]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_27():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13]
	outlength = 4
	offsets = [0, 3, 3, 5, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 77, 13]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_28():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	outlength = 6
	offsets = [0, 3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 77, 13, 323, 23]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_29():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	outlength = 5
	offsets = [0, 3, 3, 5, 6, 8]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 77, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_30():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [6, 5, 7, 11, 13, 17, 19]
	outlength = 5
	offsets = [0, 2, 2, 4, 5, 7]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 77, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_31():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	outlength = 3
	offsets = [0, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 1, 77]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_32():
	toptr = [123]
	fromptr = [2, 3, 5]
	outlength = 1
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_33():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	outlength = 4
	offsets = [0, 3, 4, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 7, 11, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_34():
	toptr = [123, 123, 123]
	fromptr = [2, 3, 5, 7, 11]
	outlength = 3
	offsets = [0, 3, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [30, 7, 11]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_35():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 31, 53, 2, 103, 37, 59, 3, 107, 41, 61, 5, 109, 43, 67, 7, 113, 47, 71, 11]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 10, 10, 10, 10, 10, 12, 14, 16, 18, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [3131, 106, 3811, 177, 4387, 1, 1, 1, 1, 1, 305, 4687, 469, 5311, 781]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_36():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 31, 73, 13, 53, 2, 103, 37, 79, 17, 59, 3, 107, 41, 83, 19, 61, 5, 109, 43, 89, 23, 67, 7, 113, 47, 97, 29, 71, 11]
	outlength = 15
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [3131, 949, 106, 3811, 1343, 177, 4387, 1577, 305, 4687, 2047, 469, 5311, 2813, 781]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_37():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 5, 5, 5, 5, 5, 5, 7, 9, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -7, 1, 29, 1, 1, 1, 1, 1, 57, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_38():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 7, 29, 3, 19, 11, 31, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 5, 5, 5, 7, 9, 11]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -7, 1, 1, 1, 1, 29, 1, 1, 57, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_39():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 6, 8, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, 203, 1, 1, 1, 1, 1, 1, 1, 57, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_40():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 5, 5, 5, 5, 5, 5, 6, 7, 8]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -29, 1, 3, 1, 1, 1, 1, 1, 19, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_41():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 29, 3, 19, 31, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 5, 5, 5, 6, 7, 8]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -29, 1, 1, 1, 1, 3, 1, 1, 19, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_42():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 29, 3, 19, 31, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, 87, 1, 1, 1, 1, 1, 1, 1, 19, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_43():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 6, 6, 6, 8, 10, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -39, 1, 1, 1, 1, 203, 1, 1, 57, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_44():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 4, 4, 4, 6, 6, 6, 7, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -39, 1, 1, 1, 1, 87, 1, 1, 19, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_45():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 29, 3, 19, 11, 31, 5, 23, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 6, 6, 6, 6, 6, 6, 6, 8, 10, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, 203, 57, 1, 1, 1, 1, 1, 1, 341, 115, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_46():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 7, 29, 3, 19, 11, 31, 13, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 6, 6, 6, 6, 6, 6, 8, 10, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -39, 1, 203, 1, 1, 1, 1, 1, 57, 341, 481]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_47():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, -1, 39, 29, 3, 19, 31, 37]
	outlength = 12
	offsets = [0, 2, 4, 4, 6, 6, 6, 6, 6, 6, 7, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, -39, 1, 87, 1, 1, 1, 1, 1, 19, 31, 37]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_48():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 7, 23, 13, 29, 3, 19, 11, 5]
	outlength = 7
	offsets = [0, 2, 4, 5, 7, 8, 8, 10]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, 161, 13, 87, 19, 1, 55]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_49():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 17, 23, 7, 13, 3, 19, 11, 5]
	outlength = 10
	offsets = [0, 2, 4, 5, 6, 6, 6, 7, 8, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [34, 161, 13, 3, 1, 1, 19, 11, 1, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_50():
	toptr = [123, 123, 123, 123, 123]
	fromptr = [2, 11, 17, 7, 19, 3, 13, 23, 5]
	outlength = 5
	offsets = [0, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [374, 133, 3, 299, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_51():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 73, 53, 31, 13, 2, 103, 79, 59, 37, 17, 3, 107, 83, 61, 41, 19, 5, 109, 89, 67, 43, 23, 7, 113, 97, 71, 47, 29, 11]
	outlength = 10
	offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [390769, 806, 480083, 1887, 541741, 3895, 649967, 6923, 778231, 14993]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_52():
	toptr = [123, 123, 123, 123]
	fromptr = [2, 11, 23, 3, 13, 29, 5, 17, 31, 7, 19, 37]
	outlength = 4
	offsets = [0, 3, 6, 9, 12]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [506, 1131, 2635, 4921]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_53():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [101, 53, 31, 2, 103, 59, 37, 3, 107, 61, 41, 5, 109, 67, 43, 7, 113, 71, 47, 11]
	outlength = 10
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [5353, 62, 6077, 111, 6527, 205, 7303, 301, 8023, 517]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_54():
	toptr = [123]
	fromptr = [1, 2, 3]
	outlength = 1
	offsets = [0, 3]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_55():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 31, 53, 101, 3, 37, 59, 103, 5, 41, 61, 107, 7, 43, 67, 109, 11, 47, 71, 113]
	outlength = 10
	offsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [62, 5353, 111, 6077, 205, 6527, 301, 7303, 517, 8023]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_56():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	outlength = 7
	offsets = [0, 2, 3, 4, 5, 6, 7, 8]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [6, 5, 7, 11, 13, 17, 19]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_57():
	toptr = [123, 123, 123, 123, 123, 123]
	fromptr = [2, 3, 5, 7, 11, 13, 17, 19]
	outlength = 6
	offsets = [0, 2, 3, 4, 5, 6, 8]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [6, 5, 7, 11, 13, 323]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_58():
	toptr = [123]
	fromptr = [1, 2, 3, 4, 5, 6]
	outlength = 1
	offsets = [0, 6]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [720]
	assert toptr == pytest_toptr


def test_awkward_reduce_prod_59():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromptr = [2, 13, 31, 53, 73, 101, 3, 17, 37, 59, 79, 103, 5, 19, 41, 61, 83, 107, 7, 23, 43, 67, 89, 109, 11, 29, 47, 71, 97, 113]
	outlength = 10
	offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
	funcPy = getattr(kernels, 'awkward_reduce_prod')
	funcPy(toptr = toptr,fromptr = fromptr,outlength = outlength,offsets = offsets)
	pytest_toptr = [806, 390769, 1887, 480083, 3895, 541741, 6923, 649967, 14993, 778231]
	assert toptr == pytest_toptr


