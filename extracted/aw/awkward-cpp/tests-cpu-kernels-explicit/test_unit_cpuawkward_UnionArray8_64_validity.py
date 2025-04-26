# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import numpy as np
import pytest

from awkward_cpp.cpu_kernels import lib

def test_unit_cpuawkward_UnionArray8_64_validity_1():
    index = []
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = []
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 0
    numcontents = 2
    tags = []
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_2():
    index = [0, 1, 2, 3, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [4, 2, 0, 945]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 6
    numcontents = 2
    tags = [-1, 0, 0, 0, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    assert funcC(tags, index, length, numcontents, lencontents).str.decode('utf-8') == "tags[i] < 0"

def test_unit_cpuawkward_UnionArray8_64_validity_3():
    index = [-1, 1, 2, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [3, 4]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 7
    numcontents = 2
    tags = [0, 0, 0, 1, 1, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    assert funcC(tags, index, length, numcontents, lencontents).str.decode('utf-8') == "index[i] < 0"

def test_unit_cpuawkward_UnionArray8_64_validity_4():
    index = [0, 1, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [2, 4, 32, 49, 0, 0]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 6
    numcontents = 2
    tags = [0, 0, 1, 1, 1, 2]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    assert funcC(tags, index, length, numcontents, lencontents).str.decode('utf-8') == "tags[i] >= len(contents)"

def test_unit_cpuawkward_UnionArray8_64_validity_5():
    index = [5, 0, 1, 1, 2, 3, 2, 4]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [5, 3, 32, 33]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 8
    numcontents = 2
    tags = [0, 1, 1, 0, 0, 0, 1, 0]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    assert funcC(tags, index, length, numcontents, lencontents).str.decode('utf-8') == "index[i] >= len(content[tags[i]])"

def test_unit_cpuawkward_UnionArray8_64_validity_6():
    index = [0, 1, 2, 3, 0, 1]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [4, 2, 0, 945]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 6
    numcontents = 2
    tags = [0, 0, 0, 0, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_7():
    index = [0, 1, 2, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [3, 4]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 7
    numcontents = 2
    tags = [0, 0, 0, 1, 1, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_8():
    index = [0, 1, 0, 1, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [2, 4, 32, 49, 0, 0]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 6
    numcontents = 2
    tags = [0, 0, 1, 1, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_9():
    index = [0, 0, 1, 1, 2, 3, 2, 4]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [5, 3, 32, 33]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 8
    numcontents = 2
    tags = [0, 1, 1, 0, 0, 0, 1, 0]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_10():
    index = [0, 0, 1, 1, 2, 3, 2, 4]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [5, 3, 32, 625, 0, 0, 0]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 8
    numcontents = 2
    tags = [0, 1, 1, 0, 0, 0, 1, 0]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

def test_unit_cpuawkward_UnionArray8_64_validity_11():
    index = [0, 0, 1, 1, 2, 2, 3]
    index = (ctypes.c_int64*len(index))(*index)
    lencontents = [3, 4, 32, 177]
    lencontents = (ctypes.c_int64*len(lencontents))(*lencontents)
    length = 7
    numcontents = 2
    tags = [0, 1, 1, 0, 0, 1, 1]
    tags = (ctypes.c_int8*len(tags))(*tags)
    funcC = getattr(lib, 'awkward_UnionArray8_64_validity')
    ret_pass = funcC(tags, index, length, numcontents, lencontents)
    assert not ret_pass.str

