import typing

import polars as pl


def check_expected_columns(
    df: pl.DataFrame,
    expected_columns: typing.Iterable[str],
) -> None:
    """
    Check if the DataFrame contains the expected columns.

    Verifies that all columns specified in `expected_columns` are present in
    the provided DataFrame `df`. Raises a ValueError if any expected columns
    are missing.

    Parameters
    ----------
    df : pl.DataFrame
        The DataFrame to be checked.
    expected_columns : Iterable of str
        An iterable of column names that are expected to be in the DataFrame.

    Raises
    ------
    ValueError
        If the DataFrame is missing any of the expected columns.
    """
    column_names = df.lazy().collect_schema().names()
    missing_columns = set(expected_columns) - set(column_names)
    if missing_columns:
        raise ValueError(
            f"Dataframe missing expected columns: {missing_columns}",
        )
