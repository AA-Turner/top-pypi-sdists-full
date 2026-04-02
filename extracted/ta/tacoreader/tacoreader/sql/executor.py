"""SQL execution branch — returns native DataFrames immediately.

This is one of two main branches in tacoreader:
    - sql/     -> free SQL over flat views → native DataFrame (this module)
    - nav/     -> typed filters + navigation → TacoDataset

No lazy evaluation. No TacoDataset returned. No chaining.
"""

from typing import TYPE_CHECKING, Any

import duckdb

if TYPE_CHECKING:
    pass


def execute_sql(
    db: duckdb.DuckDBPyConnection,
    query: str,
    backend: str,
) -> Any:
    """Execute SQL query and return native DataFrame immediately.

    Runs query against DuckDB and converts result to the requested backend.
    Flat views (l0, l1, l2, ...) are available with prefixed columns.

    Args:
        db: DuckDB connection with flat views registered
        query: SQL query string using l0, l1, l2, ... as table names
        backend: One of "pyarrow", "polars", "pandas"

    Returns:
        - pa.Table       if backend == "pyarrow" (default)
        - pl.DataFrame   if backend == "polars"
        - pd.DataFrame   if backend == "pandas"
    """
    arrow_table = db.execute(query).fetch_arrow_table()

    if backend == "pandas":
        return arrow_table.to_pandas()
    elif backend == "polars":
        import polars as pl
        return pl.from_arrow(arrow_table)

    return arrow_table  # pyarrow default