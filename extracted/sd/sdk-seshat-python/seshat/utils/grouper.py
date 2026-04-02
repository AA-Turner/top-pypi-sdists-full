import pandas as pd
from typing import List, Dict, Tuple, Iterator, Any, Union
from pyspark.sql import DataFrame as PySparkDataFrame


def pandas_group_by_columns(
    df: pd.DataFrame, columns: List[str]
) -> Dict[Tuple, pd.DataFrame]:
    """
    Group a pandas DataFrame by one or more columns.

    Args:
        df: The pandas DataFrame to group
        columns: The columns to group by

    Returns:
        A dictionary mapping group keys to DataFrames
    """
    result = {}
    for name, group in df.groupby(columns):
        # Ensure the key is always a tuple, even for single column grouping
        if not isinstance(name, tuple):
            name = (name,)
        result[name] = group
    return result


def pandas_get_group(
    grouped: Dict[Tuple, pd.DataFrame], key: Union[Tuple, Any]
) -> pd.DataFrame:
    """
    Get a specific group from a grouped pandas DataFrame.

    Args:
        grouped: The result of pandas_group_by_columns
        key: The group key to retrieve. If not a tuple, it will be converted to a single-element tuple.

    Returns:
        The DataFrame for the specified group
    """
    if not isinstance(key, tuple):
        key = (key,)
    return grouped[key]


def pandas_get_group_iterator(
    grouped: Dict[Tuple, pd.DataFrame]
) -> Iterator[Tuple[Tuple, pd.DataFrame]]:
    """
    Get an iterator over the groups in a grouped pandas DataFrame.

    Args:
        grouped: The result of pandas_group_by_columns

    Returns:
        An iterator yielding (key, group) pairs
    """
    return grouped.items()


def pyspark_group_by_columns(
    df: PySparkDataFrame, columns: List[str]
) -> Dict[Tuple, PySparkDataFrame]:
    """
    Group a PySpark DataFrame by one or more columns.

    Args:
        df: The PySpark DataFrame to group
        columns: The columns to group by

    Returns:
        A dictionary mapping group keys to DataFrames
    """
    # Collect the distinct values for the grouping columns
    distinct_values = df.select(columns).distinct().collect()

    result = {}
    for row in distinct_values:
        # Create a tuple key from the row values
        key = tuple(row[col] for col in columns)

        # Create a filter condition for this group
        filter_conditions = [df[col] == val for col, val in zip(columns, key)]
        filter_expr = filter_conditions[0]
        for condition in filter_conditions[1:]:
            filter_expr = filter_expr & condition

        # Filter the DataFrame to get this group
        group_df = df.filter(filter_expr)

        result[key] = group_df

    return result


def pyspark_get_group(
    grouped: Dict[Tuple, PySparkDataFrame], key: Union[Tuple, Any]
) -> PySparkDataFrame:
    """
    Get a specific group from a grouped PySpark DataFrame.

    Args:
        grouped: The result of pyspark_group_by_columns
        key: The group key to retrieve. If not a tuple, it will be converted to a single-element tuple.

    Returns:
        The DataFrame for the specified group
    """
    if not isinstance(key, tuple):
        key = (key,)
    return grouped[key]


def pyspark_get_group_iterator(
    grouped: Dict[Tuple, PySparkDataFrame]
) -> Iterator[Tuple[Tuple, PySparkDataFrame]]:
    """
    Get an iterator over the groups in a grouped PySpark DataFrame.

    Args:
        grouped: The result of pyspark_group_by_columns

    Returns:
        An iterator yielding (key, group) pairs
    """
    return grouped.items()
