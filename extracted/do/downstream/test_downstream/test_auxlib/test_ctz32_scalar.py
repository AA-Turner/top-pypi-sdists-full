import numpy as np

from downstream._auxlib._ctz32_scalar import ctz32_scalar


def test_ctz32_scalar():
    # fmt: off
    assert [*map(ctz32_scalar, np.arange(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]
