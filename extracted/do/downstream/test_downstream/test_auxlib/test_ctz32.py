from downstream._auxlib._ctz32 import ctz32


def test_ctz32():
    # fmt: off
    assert [*map(ctz32, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]
