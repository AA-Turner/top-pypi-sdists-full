from downstream._auxlib._bit_floor import bit_floor


def test_bit_floor():
    # fmt: off
    assert [*map(bit_floor, range(1, 17))] == [
        1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16
    ]
