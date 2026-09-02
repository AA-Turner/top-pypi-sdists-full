from typing import Union, Any
import pandas as pd
from navconfig.logging import logging


def average(
    df: pd.DataFrame,
    desc: Any,
    column_name: str,
    threshold: Union[int, float],
    deviation: Union[int, float] = 2,
    allow_below: bool = False,
    allow_above: bool = False,
) -> tuple:
    """average.

    Args:
        df (pd.DataFrame): Dataframe.
        desc (Any): Description of the DataFrame.
        colname (str): Column Name.
        threshold (Union[int, float]): Threshold value.
        deviation (Union[int, float]): percent of deviation from the threshold
        allow_below (bool): how many percent below the threshold is allowed
        allow_above (bool): how many percent above the threshold is allowed

    Returns:
        [type]: [description]
    """
    value = desc.loc["mean", column_name]
    allowed_deviation = threshold * deviation / 100
    _min = threshold - allowed_deviation
    _max = threshold + allowed_deviation
    print("MIN ", _min, "MAX ", _max)
    val = bool(_min <= value <= _max)
    logging.debug(f"Current Average value: {value}")
    if value <= _min and allow_below is True:
        val = True
    if value >= _max and allow_above is True:
        val = True
    return value, val


def between(df: pd.DataFrame, desc: Any, column_name: str, values: tuple) -> tuple:
    """
    Check if the values in a DataFrame column are between the given min and max values.

    Args:
    - df (pd.DataFrame): The DataFrame to check.
    - desc (Any): The description (usually from df.describe()) of the DataFrame.
    - column_name (str): The name of the column to check.
    - values (tuple): A tuple containing the (min, max) values.

    """
    min_value = desc.loc["min", column_name]
    max_value = desc.loc["max", column_name]
    min_threshold, max_threshold = values
    val = min_threshold <= min_value and max_value <= max_threshold
    return (min_value, max_value), val


def equal(df: pd.DataFrame, desc: Any, column_name: str, values: tuple) -> tuple:
    """
    Check if all values in a DataFrame column are within the provided list of strings.

    Args:
    - df (pd.DataFrame): The DataFrame to check.
    - desc (Any): The description (usually from df.describe()) of the DataFrame.
    - column_name (str): The name of the column to check.
    - values (tuple): A tuple containing the allowed strings.

    """
    return values, bool(df[column_name].isin(values).all())


def count_nulls(df: pd.DataFrame, desc: Any, column_name: str, value: int) -> tuple:
    """
    Check if the number of non-null values in a column is greater than a given threshold.

    Args:
        - df (pd.DataFrame): The DataFrame to check.
        - desc (Any): The description (usually from df.describe()) of the DataFrame.
        - column_name (str): The name of the column to check.
        - min_length (int): The minimum number of non-null values required.

    Returns:
        tuple: (min_length, True/False)
    """
    actual_length = df[column_name].notnull().sum()  # Count non-null values
    return actual_length, actual_length < value

def not_null(df: pd.DataFrame, desc: Any, column_name: str):
    """
    Check if a DataFrame column contains only non-null values.

    Args:
        - df (pd.DataFrame): The DataFrame to check.
        - desc (Any): The description (usually from df.describe()) of the DataFrame.
        - column_name (str): The name of the column to check.

    Returns:
        tuple: (column_name, True/False)
    """
    return column_name, df[column_name].notnull().all()

def column_size(df: pd.DataFrame, desc: Any, column_name: str, min_length: int, max_length: int) -> tuple:
    """
    Check if all values in a string column have lengths within the specified range.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        desc (Any): Ignored, used for compatibility.
        column_name (str): The name of the column to check.
        min_length (int): The minimum length allowed for strings.
        max_length (int): The maximum length allowed for strings.

    Returns:
        tuple: (column_name, min_length, max_length, True/False)
    """
    # Ensure the column exists
    if column_name not in df.columns:
        return column_name, min_length, max_length, False

    # Ensure all values are strings
    if not df[column_name].map(lambda x: isinstance(x, str)).all():
        return column_name, min_length, max_length, False

    # Check string lengths
    lengths = df[column_name].str.len()
    within_range = (lengths >= min_length) & (lengths <= max_length)

    return (min_length, max_length), within_range.all()
