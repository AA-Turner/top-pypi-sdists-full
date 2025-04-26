import pytest
import numpy
import kernels

def test_awkward_reduce_count_64_1():
	toptr = []
	lenparents = 0
	outlength = 0
	parents = []
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = []
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 19
	outlength = 9
	parents = [1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 19
	outlength = 8
	parents = [1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_4():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 1696
	outlength = 331
	parents = [194, 194, 194, 194, 194, 194, 194, 194, 194, 194, 193, 193, 193, 193, 193, 193, 193, 193, 193, 193, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 187, 187, 187, 187, 187, 187, 187, 187, 187, 187, 177, 177, 177, 177, 177, 177, 177, 177, 177, 177, 176, 176, 176, 176, 176, 176, 176, 176, 176, 176, 175, 175, 175, 175, 175, 175, 175, 175, 175, 175, 174, 174, 174, 174, 174, 174, 174, 174, 174, 174, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 172, 172, 172, 172, 172, 172, 172, 172, 172, 172, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 155, 155, 155, 155, 155, 155, 155, 155, 155, 155, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 153, 153, 153, 153, 153, 153, 153, 153, 153, 153, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 89, 89, 89, 89, 89, 89, 89, 89, 89, 89, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 87, 87, 87, 87, 87, 87, 87, 87, 87, 87, 86, 86, 86, 86, 86, 86, 86, 86, 86, 86, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [626, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_5():
	toptr = [123, 123, 123]
	lenparents = 3
	outlength = 3
	parents = [0, 0, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 0, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_6():
	toptr = [123]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_7():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 0, 2, 1, 2, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 2, 1, 0, 0, 0, 2, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_11():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 22
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 22
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_13():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 24
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_14():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 24
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_15():
	toptr = [123, 123, 123]
	lenparents = 9
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_16():
	toptr = [123, 123, 123, 123]
	lenparents = 10
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_17():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 18
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_18():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_19():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_20():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 23
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 5, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_21():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 23
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 5, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_22():
	toptr = [123, 123, 123]
	lenparents = 10
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 43
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4, 2, 4, 5, 6, 4, 5, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_24():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 39
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4, 3, 3, 5, 6, 4, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_25():
	toptr = [123, 123, 123]
	lenparents = 11
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_26():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 20
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_27():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 25
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5, 3, 3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_28():
	toptr = [123]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_29():
	toptr = [123, 123]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_30():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 29
	outlength = 7
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5, 5, 5, 3, 3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_31():
	toptr = [123]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


