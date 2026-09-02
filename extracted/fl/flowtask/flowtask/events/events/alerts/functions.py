from typing import Union, Tuple


def average(
    data: dict,
    column: str,
    threshold: Union[int, float],
    deviation: Union[int, float],
    allow_below: bool = False,
):
    """average.

    Calculates the average of a value compared with a threshold.
    Args:
        data (dict): extract column from data.
        column (str): column to calculate.
        threshold (float): value to be used for threshold
        deviation (float): max deviation acceptable for threshold
        allow_below (bool): if True, the threshold is not evaluated on minimum values.
    """
    value = data.get(column, None)
    allowed_deviation = threshold * deviation / 100
    _min = threshold - allowed_deviation
    _max = threshold + allowed_deviation
    print("MIN ", _min, "MAX ", _max)
    val = _min <= value <= _max
    if value <= _min and allow_below is True:
        val = True
    return column, value, val


def max_value(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Checks if the actual value of a specified column in the data is less than or equal to the
    given threshold value.

    Args:
        data (dict): Dictionary containing the data to be checked.
        column (str): Name of the column in the data whose value needs to be checked.
        value (Union[int, float]): The threshold value. The actual value in the data
        should be less than or equal to this.

    Returns:
        tuple: A tuple containing:
            - column (str): Name of the column that was checked.
            - actual_value (Union[int, float]): The actual value from the data for the specified column.
            - val (bool): True if the actual value is less than or equal to the threshold, False otherwise.
    """
    actual_value = data.get(column, None)
    val = actual_value <= value
    return column, actual_value, val


def min_value(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Checks if the actual value of a specified column in the data is greater than or
    equal to the given threshold value.

    Args:
        data (dict): Dictionary containing the data to be checked.
        column (str): Name of the column in the data whose value needs to be checked.
        value (Union[int, float]): The threshold value. The actual value in the data
          should be greater than or equal to this.

    Returns:
        tuple: A tuple containing:
            - column (str): Name of the column that was checked.
            - actual_value (Union[int, float]): The actual value from the data for the specified column.
            - val (bool): True if the actual value is greater than or equal
            to the threshold, False otherwise.
    """
    actual_value = data.get(column, None)
    val = actual_value >= value
    return column, actual_value, val

def has_columns(data: dict, column: str = 'columns', value: list = []) -> Tuple[str, Union[int, float], bool]:
    """
    Check if the actual value on a specified column in the data is equal to the given threshold value.
    """
    actual_value = data.get(column, None)
    val = actual_value in value
    return column, actual_value, val

def missing_columns(data: dict, column: str = 'columns', value: list = []) -> Tuple[str, Union[int, float], bool]:
    """
    Check if all required columns exist in the 'columns' field of the given data.

    :param data: Dictionary containing the structure with "columns".
    :param column: Name of the column to check (by default: "columns").
    :param value: List of columns to check.
    :return: Tuple (checked_key, missing_columns, bool)
    """
    available_columns = data.get(column, None)
    missing_columns = [col for col in value if col not in available_columns]
    return "columns", missing_columns, len(missing_columns) == 0

def equal(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Check if the actual value on a specified column in the data is equal to the given threshold value.
    """
    actual_value = data.get(column, None)
    val = actual_value == value
    return column, actual_value, val

def gt(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Check if the actual value on a specified column in the data is greater than to the given threshold value.
    """
    try:
        actual_value = data.get(column, None)
        val = float(actual_value) >= float(value)
        return column, actual_value, val
    except Exception as e:
        return column, None, False

def lt(
    data: dict, column: str, value: Union[int, float]
) -> Tuple[str, Union[int, float], bool]:
    """
    Check if the actual value on a specified column in the data is less than to the given threshold value.
    """
    try:
        actual_value = data.get(column, None)
        val = float(actual_value) <= float(value)
        return column, actual_value, val
    except Exception as e:
        return column, None, False

def between(data: dict, column: str, value: list) -> Tuple[str, Union[int, float], bool]:
    """
    Checks if the actual value in the specified column is between two given values.

    Args:
        data (dict): Dictionary containing the column data.
        column (str): Column name to evaluate.
        value (list): A list containing two values: [min_value, max_value].

    Returns:
        tuple: (column, actual_value, True/False)
    """
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"Invalid value for 'between': {value}. Must be a list of two numbers.")

    min_val, max_val = value  # Unpack min and max
    actual_value = data.get(column, None)  # Extract the value from data

    if actual_value is None:
        return column, None, False  # Column not found

    return column, actual_value, min_val <= actual_value <= max_val
