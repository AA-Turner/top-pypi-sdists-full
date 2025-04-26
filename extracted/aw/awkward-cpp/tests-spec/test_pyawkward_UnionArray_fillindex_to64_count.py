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

def test_pyawkward_UnionArray_fillindex_to64_count_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length)
    pytest_toindex = [123, 123, 123, 0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

