import itertools as it

import polars as pl


def collect_chunked(df: pl.LazyFrame, num_rows: int) -> pl.LazyFrame:
    """Collect a Polars LazyFrame, collecting in chunks for multithreaded
    processing.

    Parameters
    ----------
    df : pl.LazyFrame
        The LazyFrame to be processed in chunks.
    num_rows : int
        The total number of rows in the LazyFrame.

    Returns
    -------
    pl.LazyFrame
        The concatenated LazyFrame after collecting chunks in parallel.
    """
    if num_rows == 0:
        return df.collect().lazy()

    n_chunks = max(pl.thread_pool_size() - 1, 1)
    chunk_size = max(num_rows // n_chunks, 1)
    chunks = it.pairwise([*range(0, num_rows, chunk_size), num_rows])

    # collect_all uses polars threadpool to collect chunks in parallel
    collected = pl.collect_all([df[slice(*chunk)] for chunk in chunks])
    concatenated = pl.concat([c.lazy() for c in collected], rechunk=False)
    return concatenated
