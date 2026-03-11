import typing

import polars as pl

from ._explode_lookup_unpacked import explode_lookup_unpacked
from ._unpack_data_packed import unpack_data_packed


def explode_lookup_packed(
    df: pl.DataFrame,
    *,
    calc_Tbar_argv: bool = False,
    mp_context: str = "thread",
    mp_pool_size: int = 1,
    value_type: typing.Literal["hex", "uint64", "uint32", "uint16", "uint8"],
    result_schema: typing.Literal["coerce", "relax", "shrink"] = "coerce",
) -> pl.DataFrame:
    """Explode downstream-curated data from hexidecimal serialization of
    downstream buffers and counters to one-data-item-per-row, applying
    downstream lookup to identify origin time `Tbar` of each item.

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame containing packed data to be exploded.
    calc_Tbar_argv : bool, default False
        Include column indicating sorted order of `Tbar` values within each
        buffer.
    mp_context : str, default "thread"
        Deprecated. Previously selected the multiprocessing start
        method; now ignored since parity computation uses threads.
    mp_pool_size : int, default 1
        Number of worker threads for parity computation.
        When 1 (default), processing is sequential with no threading
        overhead. When > 1, parity check chunks are dispatched to a
        thread pool for parallel computation.
    value_type : {'hex', 'uint64', 'uint32', 'uint16', 'uint8'}
        Type of the packed data values. Determines how the packed data is
        interpreted.
    result_schema : {'coerce', 'relax', 'shrink'}, default 'coerce'
        Schema for the resulting DataFrame. Determines how the output DataFrame
        is structured and what types are used.

    Returns
    -------
    pl.DataFrame
        DataFrame with one row per data item, containing the original data and
        the corresponding `Tbar` value.
    """
    df = unpack_data_packed(
        df,
        mp_context=mp_context,
        mp_pool_size=mp_pool_size,
        result_schema=result_schema,
    )
    return explode_lookup_unpacked(
        df,
        calc_Tbar_argv=calc_Tbar_argv,
        result_schema=result_schema,
        value_type=value_type,
    )
