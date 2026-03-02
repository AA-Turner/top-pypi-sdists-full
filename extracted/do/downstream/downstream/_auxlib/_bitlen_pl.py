import polars as pl


def bitlen_pl(col: pl.Expr) -> pl.Expr:
    """Create Polars expression for the bit length of  integers.

    Parameters
    ----------
    col : pl.Expr
        Polars expression representing a column of integer values.

    Returns
    -------
    pl.Expr
        Polars expression with the bit length of the input integers.
    """
    return pl.lit(64) - col.cast(pl.UInt64).bitwise_leading_zeros()
