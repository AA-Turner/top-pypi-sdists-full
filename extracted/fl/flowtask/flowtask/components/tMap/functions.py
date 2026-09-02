"""
tMap Transformations functions based on Series.
"""
from typing import List
import pandas as pd
import numpy as np


def to_string(series: pd.Series, remove_nan: bool = False, **kwargs) -> pd.Series:
    """to_string.

    Converting to string a Pandas column (Series)
    Args:
        series (pandas.Series): Column Series to be converted
        remove_nan (bool, optional): remove Not a Number from Column. Defaults to False.

    Returns:
        pandas.Series: a New Serie is returned with string values.
    """
    series = series.astype("string")
    if remove_nan is True:
        series = series.replace(np.nan, "", regex=True)
    return series


def to_integer(series: pd.Series, **kwargs):
    """
    Converts a pandas Series to an integer type, handling errors by coercing invalid values to NaN.

    :param series: The pandas Series to be converted.
    :param kwargs: Additional keyword arguments.
    :return: The converted pandas Series with integer type.
    """
    try:
        series = pd.to_numeric(series, errors="coerce")
        # Replace non-finite values (NaN, inf, -inf) with pd.NA before converting to Int64
        series = series.where(np.isfinite(series), pd.NA)
        series = series.astype("Int64", copy=False)
    except Exception as err:
        print(f"Error on to_Integer: {err}")
    return series


def concat(df: pd.DataFrame, columns: List[str], sep: str = " ") -> pd.Series:
    """
    Concatenates the values of the specified columns in the given DataFrame.

    :param df: The input DataFrame
    :param columns: The list of columns to concatenate
    :param sep: The separator to use between the concatenated values (default is a space)
    :return: A Series with the concatenated values
    """
    combined = df[columns[0]].astype(str)
    for col in columns[1:]:
        combined += sep + df[col].astype(str)
    return combined
