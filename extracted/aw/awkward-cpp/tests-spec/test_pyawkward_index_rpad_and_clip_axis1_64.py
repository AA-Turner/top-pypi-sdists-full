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

def test_pyawkward_index_rpad_and_clip_axis1_64_1():
    tostarts = [123, 123, 123]
    tostops = [123, 123, 123]
    target = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_index_rpad_and_clip_axis1_64')
    funcPy(tostarts=tostarts, tostops=tostops, target=target, length=length)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)

