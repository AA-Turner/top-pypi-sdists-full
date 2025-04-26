# AUTO GENERATED ON 2025-03-19 AT 21:19:36
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import cupy
import cupy.testing as cpt
import numpy as np
import pytest

import awkward as ak
import awkward._connect.cuda as ak_cu
from awkward._backends.cupy import CupyBackend

cupy_backend = CupyBackend.instance()

def test_cudaawkward_ListArray32_broadcast_tooffsets_64_1():
    tocarry = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    fromstarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int32)
    fromstops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int32)
    lencontent = 3
    funcC = cupy_backend['awkward_ListArray_broadcast_tooffsets', cupy.int64, cupy.int64, cupy.int32, cupy.int32]

def test_cudaawkward_ListArray32_broadcast_tooffsets_64_2():
    tocarry = cupy.array([123], dtype=cupy.int64)
    fromoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    offsetslength = 3
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    lencontent = 6
    funcC = cupy_backend['awkward_ListArray_broadcast_tooffsets', cupy.int64, cupy.int64, cupy.int32, cupy.int32]

