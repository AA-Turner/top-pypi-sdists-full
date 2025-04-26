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

def test_pyawkward_UnionArray_filltags_to8_const_1():
    totags = [123, 123, 123, 123, 123, 123]
    totagsoffset = 3
    length = 3
    base = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_filltags_to8_const')
    funcPy(totags=totags, totagsoffset=totagsoffset, length=length, base=base)
    pytest_totags = [123, 123, 123, 3, 3, 3]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)

