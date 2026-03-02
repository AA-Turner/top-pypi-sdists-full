from downstream._auxlib._bit_floor32 import bit_floor32


def test_bit_floor32():
    # fmt: off
    assert [*map(bit_floor32, range(1, 17))] == [
        1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16
    ]
