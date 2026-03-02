import polars as pl
from polars.testing import assert_frame_equal as pl_assert_frame_equal
import pytest

from downstream._auxlib._collect_chunked import collect_chunked


@pytest.mark.parametrize("num_rows", [0, 1, 2, 3, 4, 5, 10, 100, 1000])
def test_collect_chunked_basic(num_rows: int):
    df = pl.DataFrame({"a": range(num_rows)}).lazy()
    df = df.with_columns(b=pl.col("a") * 2)

    result = collect_chunked(df, num_rows)
    pl_assert_frame_equal(result.collect(), df.collect())
