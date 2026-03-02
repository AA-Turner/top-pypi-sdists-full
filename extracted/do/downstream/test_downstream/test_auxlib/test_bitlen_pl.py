import numpy as np
import polars as pl

from downstream._auxlib._bitlen_pl import bitlen_pl


def test_bitlen_pl_basic():
    """Test bitlen_pl with basic integers."""
    df = pl.DataFrame({"values": [1, 2, 3, 4, 255, 256]})
    expected = [1, 2, 2, 3, 8, 9]
    result = df.select(bitlen_pl(pl.col("values"))).to_series().to_list()
    assert result == expected


def test_bitlen_pl_zero():
    """Test bitlen_pl with zero."""
    df = pl.DataFrame({"values": [0, 1, 3]})
    expected = [0, 1, 2]
    result = df.select(bitlen_pl(pl.col("values"))).to_series().to_list()
    assert result == expected


def test_bitlen_pl_large_numbers():
    """Test bitlen_pl with large numbers."""
    df = pl.DataFrame(
        {"values": np.array([2**63, 2**64 - 1], dtype=np.uint64)},
    )
    expected = [64, 64]
    result = df.select(bitlen_pl(pl.col("values"))).to_series().to_list()
    assert result == expected
