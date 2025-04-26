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

def test_pyawkward_UnionArray64_regular_index_getsize_1():
    size = [123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray64_regular_index_getsize')
    funcPy(size=size, fromtags=fromtags, length=length)
    pytest_size = [1]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

def test_pyawkward_UnionArray64_regular_index_getsize_2():
    size = [123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray64_regular_index_getsize')
    funcPy(size=size, fromtags=fromtags, length=length)
    pytest_size = [2]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

def test_pyawkward_UnionArray64_regular_index_getsize_3():
    size = [123]
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray64_regular_index_getsize')
    funcPy(size=size, fromtags=fromtags, length=length)
    pytest_size = [2]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

def test_pyawkward_UnionArray64_regular_index_getsize_4():
    size = [123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray64_regular_index_getsize')
    funcPy(size=size, fromtags=fromtags, length=length)
    pytest_size = [1]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

def test_pyawkward_UnionArray64_regular_index_getsize_5():
    size = [123]
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray64_regular_index_getsize')
    funcPy(size=size, fromtags=fromtags, length=length)
    pytest_size = [1]
    assert size[:len(pytest_size)] == pytest.approx(pytest_size)

