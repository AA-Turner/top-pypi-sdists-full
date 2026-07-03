# AUTO GENERATED ON 2026-07-02 AT 19:33:43
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

def test_unit_cpuawkward_reduce_count_64_1():
    toptr = []
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 0
    offsets = [0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = []
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_2():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 9
    offsets = [0, 0, 3, 3, 8, 12, 12, 16, 19, 19]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_3():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 0, 3, 3, 8, 12, 12, 16, 19]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_4():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 331
    offsets = [0, 626, 636, 646, 656, 666, 676, 686, 696, 706, 716, 726, 736, 746, 756, 766, 776, 786, 796, 806, 816, 826, 836, 846, 856, 866, 876, 886, 896, 896, 896, 896, 896, 896, 896, 906, 916, 926, 936, 946, 956, 966, 976, 976, 976, 976, 976, 976, 976, 976, 976, 976, 986, 996, 1006, 1016, 1026, 1036, 1046, 1056, 1056, 1056, 1056, 1056, 1056, 1056, 1056, 1056, 1056, 1066, 1076, 1086, 1096, 1106, 1116, 1126, 1136, 1136, 1136, 1136, 1136, 1136, 1136, 1136, 1136, 1136, 1146, 1156, 1166, 1176, 1186, 1196, 1206, 1216, 1216, 1216, 1216, 1216, 1216, 1216, 1216, 1216, 1216, 1226, 1236, 1246, 1256, 1266, 1276, 1286, 1296, 1296, 1296, 1296, 1296, 1296, 1296, 1296, 1296, 1296, 1306, 1316, 1326, 1336, 1346, 1356, 1366, 1376, 1376, 1376, 1376, 1376, 1376, 1376, 1376, 1376, 1376, 1386, 1396, 1406, 1416, 1426, 1436, 1446, 1456, 1456, 1456, 1456, 1456, 1456, 1456, 1456, 1456, 1456, 1466, 1476, 1486, 1496, 1506, 1516, 1526, 1536, 1536, 1536, 1536, 1536, 1536, 1536, 1536, 1536, 1536, 1546, 1556, 1566, 1576, 1586, 1596, 1606, 1616, 1616, 1616, 1616, 1616, 1616, 1616, 1616, 1616, 1616, 1626, 1636, 1646, 1656, 1666, 1676, 1686, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696, 1696]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [626, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_5():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 3
    offsets = [0, 2, 2, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [2, 0, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_6():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 1
    offsets = [0, 3]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_7():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 6
    offsets = [0, 3, 3, 5, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 0, 2, 1, 2, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_8():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 3, 5, 6, 6, 6, 6, 8, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 2, 1, 0, 0, 0, 2, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_9():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 9
    offsets = [0, 3, 6, 6, 10, 14, 14, 18, 21, 21]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_10():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 3, 6, 6, 10, 14, 14, 18, 21]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_11():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 9
    offsets = [0, 3, 6, 6, 11, 15, 15, 19, 22, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_12():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 3, 6, 6, 11, 15, 15, 19, 22]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_13():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 9
    offsets = [0, 3, 6, 8, 13, 17, 17, 21, 24, 24]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3, 0]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_14():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 8
    offsets = [0, 3, 6, 8, 13, 17, 17, 21, 24]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_15():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 3
    offsets = [0, 3, 6, 9]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_16():
    toptr = [123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 4
    offsets = [0, 3, 6, 9, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 1]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_17():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 6
    offsets = [0, 3, 6, 9, 12, 15, 18]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 3, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_18():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 3, 6, 9, 12, 15, 18, 21]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 3, 3, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_19():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 10
    offsets = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_20():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 3, 6, 9, 12, 15, 20, 23]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 3, 3, 5, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_21():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 3, 6, 9, 12, 17, 20, 23]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 3, 3, 5, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_22():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 3
    offsets = [0, 3, 6, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 4]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_23():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 10
    offsets = [0, 3, 6, 10, 12, 16, 21, 27, 31, 36, 43]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 4, 2, 4, 5, 6, 4, 5, 7]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_24():
    toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 10
    offsets = [0, 3, 6, 10, 13, 16, 21, 27, 31, 34, 39]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 4, 3, 3, 5, 6, 4, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_25():
    toptr = [123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 3
    offsets = [0, 3, 6, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_26():
    toptr = [123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 6
    offsets = [0, 3, 6, 11, 14, 17, 20]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 5, 3, 3, 3]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_27():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 3, 6, 11, 14, 17, 20, 25]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [3, 3, 5, 3, 3, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_28():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 1
    offsets = [0, 5]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_29():
    toptr = [123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 2
    offsets = [0, 5, 10]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [5, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_30():
    toptr = [123, 123, 123, 123, 123, 123, 123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 7
    offsets = [0, 5, 10, 15, 18, 21, 24, 29]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [5, 5, 5, 3, 3, 3, 5]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

def test_unit_cpuawkward_reduce_count_64_31():
    toptr = [123]
    toptr = (ctypes.c_int64*len(toptr))(*toptr)
    outlength = 1
    offsets = [0, 6]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    funcC = getattr(lib, 'awkward_reduce_count_64')
    ret_pass = funcC(toptr, offsets, outlength)
    pytest_toptr = [6]
    assert toptr[:len(pytest_toptr)] == pytest.approx(pytest_toptr)
    assert not ret_pass.str

