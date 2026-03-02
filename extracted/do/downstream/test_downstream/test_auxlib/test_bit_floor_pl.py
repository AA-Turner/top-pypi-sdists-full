import numpy as np
import polars as pl

from downstream._auxlib._bit_floor_pl import bit_floor_pl


def test_bit_floor_pl_basic():
    """Test bit_floor_pl with basic integers."""
    df = pl.DataFrame({"values": [1, 2, 3, 4, 255, 256]})
    expected = [1, 2, 2, 4, 128, 256]
    result = df.select(bit_floor_pl(pl.col("values"))).to_series().to_list()
    assert result == expected


def test_bit_floor_pl_zero():
    """Test bit_floor_pl with zero."""
    df = pl.DataFrame({"values": [0, 1, 3]})
    expected = [0, 1, 2]
    result = df.select(bit_floor_pl(pl.col("values"))).to_series().to_list()
    assert result == expected


def test_bit_floor_pl_large_numbers():
    """Test bit_floor_pl with large numbers."""
    df = pl.DataFrame(
        {"values": np.array([2**63, 2**64 - 1], dtype=np.uint64)},
    )
    expected = [2**63, 2**63]
    result = df.select(bit_floor_pl(pl.col("values"))).to_series().to_list()
    assert result == expected
