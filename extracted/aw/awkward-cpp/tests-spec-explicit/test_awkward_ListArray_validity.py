import pytest
import numpy
import kernels

def test_awkward_ListArray_validity_1():
	lencontent = 0
	length = 0
	starts = []
	stops = []
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_2():
	lencontent = 2
	length = 0
	starts = []
	stops = []
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_3():
	lencontent = 0
	length = 3
	starts = [0, 0, 1]
	stops = [0, 1, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	with pytest.raises(Exception):
		funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_4():
	lencontent = 1
	length = 3
	starts = [1, 0, 1]
	stops = [0, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	with pytest.raises(Exception):
		funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_5():
	lencontent = 4
	length = 3
	starts = [0, 0, 1]
	stops = [0, 1, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	with pytest.raises(Exception):
		funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_6():
	lencontent = 1
	length = 4
	starts = [-1, 0, 1, 1]
	stops = [0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	with pytest.raises(Exception):
		funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_7():
	lencontent = 0
	length = 5
	starts = [0, 0, 0, 0, 0]
	stops = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_8():
	lencontent = 0
	length = 4
	starts = [0, 0, 0, 0]
	stops = [0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_9():
	lencontent = 0
	length = 3
	starts = [0, 0, 0]
	stops = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_10():
	lencontent = 1
	length = 3
	starts = [0, 0, 1]
	stops = [0, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_11():
	lencontent = 4
	length = 3
	starts = [0, 0, 1]
	stops = [0, 1, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_12():
	lencontent = 1
	length = 4
	starts = [0, 0, 1, 1]
	stops = [0, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_13():
	lencontent = 6
	length = 4
	starts = [0, 0, 1, 3]
	stops = [0, 1, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_14():
	lencontent = 10
	length = 5
	starts = [0, 0, 1, 3, 6]
	stops = [0, 1, 3, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_15():
	lencontent = 19
	length = 8
	starts = [0, 0, 3, 3, 8, 12, 12, 16]
	stops = [0, 3, 3, 8, 12, 12, 16, 19]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_16():
	lencontent = 19
	length = 9
	starts = [0, 0, 3, 3, 8, 12, 12, 16, 19]
	stops = [0, 3, 3, 8, 12, 12, 16, 19, 19]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_17():
	lencontent = 6
	length = 3
	starts = [0, 1, 3]
	stops = [1, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_18():
	lencontent = 15
	length = 5
	starts = [0, 1, 3, 6, 10]
	stops = [1, 3, 6, 10, 15]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_19():
	lencontent = 12
	length = 6
	starts = [0, 1, 3, 6, 7, 9]
	stops = [1, 3, 6, 7, 9, 12]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_20():
	lencontent = 8
	length = 4
	starts = [0, 1, 4, 5]
	stops = [1, 4, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_21():
	lencontent = 3
	length = 3
	starts = [0, 2, 2]
	stops = [2, 2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_22():
	lencontent = 4
	length = 3
	starts = [0, 2, 2]
	stops = [2, 2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_23():
	lencontent = 3
	length = 2
	starts = [0, 2]
	stops = [2, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_24():
	lencontent = 4
	length = 2
	starts = [0, 2]
	stops = [2, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_25():
	lencontent = 8
	length = 7
	starts = [0, 2, 2, 4, 4, 5, 5]
	stops = [2, 2, 4, 4, 5, 5, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_26():
	lencontent = 6
	length = 5
	starts = [0, 2, 2, 4, 5]
	stops = [2, 2, 4, 5, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_27():
	lencontent = 9
	length = 5
	starts = [0, 2, 2, 4, 5]
	stops = [2, 2, 4, 5, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_28():
	lencontent = 3
	length = 3
	starts = [0, 2, 3]
	stops = [2, 3, 3]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_29():
	lencontent = 4
	length = 3
	starts = [0, 2, 3]
	stops = [2, 3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_30():
	lencontent = 5
	length = 3
	starts = [0, 2, 3]
	stops = [2, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_31():
	lencontent = 6
	length = 3
	starts = [0, 2, 3]
	stops = [2, 3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_32():
	lencontent = 5
	length = 4
	starts = [0, 2, 3, 3]
	stops = [2, 3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_33():
	lencontent = 7
	length = 4
	starts = [0, 2, 3, 4]
	stops = [2, 3, 4, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_34():
	lencontent = 6
	length = 3
	starts = [0, 2, 4]
	stops = [2, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_35():
	lencontent = 7
	length = 3
	starts = [0, 2, 5]
	stops = [2, 5, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_36():
	lencontent = 8
	length = 3
	starts = [0, 2, 6]
	stops = [2, 6, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_37():
	lencontent = 5
	length = 3
	starts = [0, 3, 3]
	stops = [3, 3, 5]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_38():
	lencontent = 7
	length = 3
	starts = [0, 3, 3]
	stops = [3, 3, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_39():
	lencontent = 8
	length = 3
	starts = [0, 3, 3]
	stops = [3, 3, 8]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_40():
	lencontent = 4
	length = 2
	starts = [0, 3]
	stops = [3, 4]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_41():
	lencontent = 9
	length = 4
	starts = [0, 3, 3, 5]
	stops = [3, 3, 5, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_42():
	lencontent = 11
	length = 6
	starts = [0, 3, 3, 5, 6, 10]
	stops = [3, 3, 5, 6, 10, 11]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_43():
	lencontent = 9
	length = 5
	starts = [0, 3, 3, 5, 6]
	stops = [3, 3, 5, 6, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_44():
	lencontent = 9
	length = 6
	starts = [0, 3, 3, 5, 6, 8]
	stops = [3, 3, 5, 6, 8, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_45():
	lencontent = 6
	length = 2
	starts = [0, 3]
	stops = [3, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_46():
	lencontent = 7
	length = 2
	starts = [0, 3]
	stops = [3, 7]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_47():
	lencontent = 11
	length = 4
	starts = [0, 3, 4, 7]
	stops = [3, 4, 7, 11]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_48():
	lencontent = 25
	length = 7
	starts = [0, 3, 6, 11, 14, 17, 20]
	stops = [3, 6, 11, 14, 17, 20, 25]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_49():
	lencontent = 20
	length = 6
	starts = [0, 3, 6, 11, 14, 17]
	stops = [3, 6, 11, 14, 17, 20]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_50():
	lencontent = 19
	length = 5
	starts = [0, 3, 6, 11, 15]
	stops = [3, 6, 11, 15, 19]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_51():
	lencontent = 10
	length = 3
	starts = [0, 3, 6]
	stops = [3, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_52():
	lencontent = 11
	length = 3
	starts = [0, 3, 6]
	stops = [3, 6, 11]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_53():
	lencontent = 21
	length = 9
	starts = [0, 3, 6, 6, 10, 14, 14, 18, 21]
	stops = [3, 6, 6, 10, 14, 14, 18, 21, 21]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_54():
	lencontent = 21
	length = 8
	starts = [0, 3, 6, 6, 10, 14, 14, 18]
	stops = [3, 6, 6, 10, 14, 14, 18, 21]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_55():
	lencontent = 22
	length = 9
	starts = [0, 3, 6, 6, 11, 15, 15, 19, 22]
	stops = [3, 6, 6, 11, 15, 15, 19, 22, 22]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_56():
	lencontent = 22
	length = 8
	starts = [0, 3, 6, 6, 11, 15, 15, 19]
	stops = [3, 6, 6, 11, 15, 15, 19, 22]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_57():
	lencontent = 24
	length = 9
	starts = [0, 3, 6, 8, 13, 17, 17, 21, 24]
	stops = [3, 6, 8, 13, 17, 17, 21, 24, 24]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_58():
	lencontent = 24
	length = 8
	starts = [0, 3, 6, 8, 13, 17, 17, 21]
	stops = [3, 6, 8, 13, 17, 17, 21, 24]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_59():
	lencontent = 9
	length = 3
	starts = [0, 3, 7]
	stops = [3, 7, 9]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_60():
	lencontent = 10
	length = 2
	starts = [0, 4]
	stops = [4, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_61():
	lencontent = 6
	length = 3
	starts = [0, 4, 4]
	stops = [4, 4, 6]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_62():
	lencontent = 10
	length = 3
	starts = [0, 4, 6]
	stops = [4, 6, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_63():
	lencontent = 14
	length = 4
	starts = [0, 4, 6, 9]
	stops = [4, 6, 9, 14]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_64():
	lencontent = 11
	length = 6
	starts = [0, 4, 7, 7, 9, 9]
	stops = [4, 7, 7, 9, 9, 11]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_65():
	lencontent = 12
	length = 3
	starts = [0, 4, 8]
	stops = [4, 8, 12]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_66():
	lencontent = 30
	length = 6
	starts = [0, 5, 10, 15, 20, 25]
	stops = [5, 10, 15, 20, 25, 30]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_67():
	lencontent = 10
	length = 2
	starts = [0, 5]
	stops = [5, 10]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


def test_awkward_ListArray_validity_68():
	lencontent = 12
	length = 6
	starts = [3, 0, 999, 2, 6, 10]
	stops = [7, 3, 999, 4, 6, 12]
	funcPy = getattr(kernels, 'awkward_ListArray_validity')
	funcPy(lencontent = lencontent,length = length,starts = starts,stops = stops)


