"""
Tests for the common module
"""

import numpy as np
from castepinput import common


def test_block():
    """Test setting a block"""
    b = common.Block(["1 1 1", "2 2 3 ", ""])
    expect = ["1 1 1", "2 2 3"]
    c = b.compact()
    assert c == expect
    assert b != expect

    b.compact(inplace=True)
    assert b == expect


def test_abc_to_cell():
    """Test setting cell through cell parameters"""

    abc = [1, 1, 1, 90.0, 90.0, 90.0]
    cell = common.cell_abcs_to_vec(abc)
    assert np.all(cell == np.identity(3))

    # Check a different cell
    abc = [1, 1, 1, 60.0, 60.0, 60.0]
    cell = common.cell_abcs_to_vec(abc)
    for vec in cell:
        assert np.dot(vec, vec) == 1

    # Check angles
    va, vb, vc = cell

    def get_ang(a, b):
        cos_alpha = (a.dot(b)) / (np.sqrt(a.dot(a)) * np.sqrt(b.dot(b)))
        return np.arccos(cos_alpha)

    assert get_ang(va, vb) == np.pi / 3
    assert get_ang(vc, vb) == np.pi / 3
    assert get_ang(va, vc) == np.pi / 3

    # Test gamma = -90 branch
    abc = [1, 1, 1, 90.0, 90.0, -90.0]
    cell = common.cell_abcs_to_vec(abc)
    assert cell[1, 1] < 0  # sin(-90) is negative
