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

def test_pyawkward_UnionArray8_U32_project_64_1():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_2():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_3():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 3, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_4():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 4, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_5():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_6():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    which = 1
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_7():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    which = 1
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_8():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    which = 1
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 3, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_9():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    which = 1
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 4, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_10():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    which = 1
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_11():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_12():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 2, 2, 3, 0, 2, 0, 2, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 2, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_13():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 3, 0, 3, 5, 2, 0, 2, 1, 1]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 3, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_14():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [1, 4, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_UnionArray8_U32_project_64_15():
    lenout = [123]
    tocarry = [123, 123, 123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromindex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    which = 0
    funcPy = getattr(kernels, 'awkward_UnionArray8_U32_project_64')
    funcPy(lenout=lenout, tocarry=tocarry, fromtags=fromtags, fromindex=fromindex, length=length, which=which)
    pytest_lenout = [3]
    assert lenout[:len(pytest_lenout)] == pytest.approx(pytest_lenout)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

