# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import numpy as np
import kernels

def test_pyawkward_ListArrayU32_combinations_length_64_1():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [9]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 5, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_2():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [139.0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_3():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_4():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 4, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_5():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [3]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_6():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = False
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_7():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = False
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [49.0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 35.0, 39.0, 49.0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_8():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = False
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_9():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = False
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_10():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = False
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_11():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [9]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 5, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_12():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [139.0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_13():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_14():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 4, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_15():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [3]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_16():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [9]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 5, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_17():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [139.0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_18():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_19():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 4, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_20():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [3]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_21():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    stops = [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [9]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 5, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_22():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
    stops = [8, 4, 5, 6, 5, 5, 7]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [139.0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 84.0, 104.0, 139.0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_23():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    stops = [1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [0]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_24():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2]
    stops = [1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [4]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 0, 4, 4]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListArrayU32_combinations_length_64_25():
    totallen = [123]
    tooffsets = [123, 123, 123, 123]
    n = 3
    replacement = True
    starts = [0, 0, 0, 0, 0, 0, 0, 0]
    stops = [1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArrayU32_combinations_length_64')
    funcPy(totallen=totallen, tooffsets=tooffsets, n=n, replacement=replacement, starts=starts, stops=stops, length=length)
    pytest_totallen = [3]
    assert totallen[:len(pytest_totallen)] == pytest.approx(pytest_totallen)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

