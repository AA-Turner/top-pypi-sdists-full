from typing import Generator, Dict, List, Any
import pandas as pd


def batch(data: list[dict], batch_size: int):
    """Batch a list of dictionaries into smaller lists."""
    return [data[i : i + batch_size] for i in range(0, len(data), batch_size)]


def batch_pandas_df(
    df: pd.DataFrame, batch_size: int
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Yield batches from a pandas DataFrame in dictionary format.

    Args:
        df: Input pandas DataFrame.
        batch_size: Size of each batch.

    Yields:
        List of dictionaries, where each dictionary represents a row.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    for start in range(0, len(df), batch_size):
        yield df.iloc[start : start + batch_size].to_dict("records")


def batch_spark_df(df, batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Yield batches from a PySpark DataFrame in dictionary format.

    Args:
        df: Input PySpark DataFrame.
        batch_size: Size of each batch.

    Yields:
        List of dictionaries, where each dictionary represents a row.
    """
    batch = []
    for row in df.toLocalIterator():
        batch.append(row.asDict())
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
