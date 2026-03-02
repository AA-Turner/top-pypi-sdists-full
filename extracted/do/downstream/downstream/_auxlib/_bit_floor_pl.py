import numpy as np
import polars as pl

from ._bitlen_pl import bitlen_pl


def bit_floor_pl(col: pl.Expr) -> pl.Expr:
    """Create Polars expression for the bit floor of integers.

    Parameters
    ----------
    col : pl.Expr
        Polars expression representing a column of integer values.

    Returns
    -------
    pl.Expr
        Polars expression with the bit floor of the input integers, cast as
        UInt64.
    """
    mask = np.left_shift(
        1,
        bitlen_pl(np.right_shift(col, 1)),
        dtype=np.uint64,
    )
    return np.bitwise_and(col.cast(pl.UInt64), mask)
