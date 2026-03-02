from downstream._auxlib._ctz import ctz


def test_ctz():
    # fmt: off
    assert [*map(ctz, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]
