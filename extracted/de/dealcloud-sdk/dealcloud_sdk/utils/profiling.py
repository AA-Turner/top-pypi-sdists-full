"""
Data profiling utilities for DealCloud field analysis.

These utilities help analyze data to recommend appropriate DealCloud field types.
Originally from data_health_report and field_report tools.
"""

import logging
import re
from typing import TYPE_CHECKING, Callable, Optional, Union

import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype

if TYPE_CHECKING:
    import polars as pl

logger = logging.getLogger(__name__)


# Data type constants for profiling results
class DataType:
    """Data type constants for profiling results."""
    TEXT = "Text"
    NUMBER = "Number"
    CURRENCY = "Currency"
    PERCENTAGE = "Percentage"
    MULTIPLIER = "Multiplier"
    EMAIL = "Email"
    DATE = "Date"
    DATETIME = "DateTime"
    BOOLEAN = "Boolean"
    CHOICE = "Choice"
    REFERENCE = "Reference"
    CHOICE_REFERENCE = "Choice/Reference"
    SINGLE_LINE = "SingleLine"
    MULTI_LINE = "MultiLine"
    EMPTY = "Empty"
    UNKNOWN = "Unknown"


# Threshold for multi-line text detection
MULTI_LINE_THRESHOLD = 100


def estimate_field_type(value, is_choice_candidate: bool = False) -> str:
    """
    Estimate the appropriate DealCloud field type for a value.
    
    Analyzes the value's format to suggest the best field type.
    
    Args:
        value: The value to analyze
        is_choice_candidate: If True and no specific type detected,
                            suggests Choice/Reference instead of Text
    
    Returns:
        Suggested data type string (from DataType constants)
    
    Example:
        >>> estimate_field_type("$1,000,000")
        'Currency'
        >>> estimate_field_type("user@example.com")
        'Email'
        >>> estimate_field_type("2024-01-15")
        'Date'
        >>> estimate_field_type("Active", is_choice_candidate=True)
        'Choice/Reference'
    """
    value = str(value)
    
    # Empty check
    if value == "" or value == " " or value.lower() == "none":
        return DataType.EMPTY
    
    # Regex patterns
    number_regex = r"^[0-9.,%xXmMbnB$£€GBPUSDEUR\-\+\s]+$"
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    date_regex = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}|"
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}|"
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}|"
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|"
        r"\d{2,4}-\d{2}-\d{2,4}|"
        r"\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}|"
        r"\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}|"
        r"\d{2,4}\/\d{2}\/\d{2,4})"
    )
    boolean_regex = r"^(true|false|yes|no|1|0)$"
    
    # Check for boolean
    if re.match(boolean_regex, value.lower()):
        return DataType.BOOLEAN
    
    # Check for email
    if re.search(email_regex, value):
        return DataType.EMAIL
    
    # Check for date/datetime
    if re.search(date_regex, value):
        if "T" in value or ":" in value:
            return DataType.DATETIME
        return DataType.DATE
    
    # Check for number types
    if re.search(number_regex, value):
        currency_indicators = ["m", "M", "bn", "B", "£", "$", "€", "GBP", "USD", "EUR"]
        if any(indicator in value for indicator in currency_indicators):
            return DataType.CURRENCY
        elif "%" in value:
            return DataType.PERCENTAGE
        elif "x" in value.lower():
            return DataType.MULTIPLIER
        else:
            return DataType.NUMBER
    
    # Text type determination
    if len(value) > MULTI_LINE_THRESHOLD:
        return DataType.MULTI_LINE
    elif is_choice_candidate:
        return DataType.CHOICE_REFERENCE
    else:
        return DataType.SINGLE_LINE


def detect_choice_field(
    distinct_count: int,
    total_count: int,
    choice_ratio_threshold: float = 0.05,
    max_distinct_values: int = 10,
) -> bool:
    """
    Determine if a field should be a Choice field based on value distribution.
    
    A field is a good Choice candidate if:
    - It has a small number of distinct values (< max_distinct_values), OR
    - The ratio of distinct values to total values is low (< choice_ratio_threshold)
    - AND it's not all unique values (would be a key field)
    - AND it's not empty
    
    Args:
        distinct_count: Number of unique values in the field
        total_count: Total number of values (rows)
        choice_ratio_threshold: Max ratio of distinct/total to be a choice
        max_distinct_values: Max distinct values to automatically be a choice
    
    Returns:
        True if the field should be a Choice field
    
    Example:
        >>> detect_choice_field(distinct_count=5, total_count=1000)
        True  # Only 5 unique values
        >>> detect_choice_field(distinct_count=100, total_count=100)
        False  # All unique (probably a key field)
        >>> detect_choice_field(distinct_count=50, total_count=10000)
        True  # Low ratio (0.005)
    """
    if distinct_count == 0:
        return False
    
    if total_count == 0:
        return False
    
    # All unique values = probably a key, not a choice
    if distinct_count == total_count:
        return False
    
    choice_ratio = distinct_count / total_count
    
    # Either small number of values OR low ratio
    return distinct_count < max_distinct_values or choice_ratio < choice_ratio_threshold


def most_common(values: list) -> Optional[any]:
    """
    Return the most common element in a list.
    
    Args:
        values: List of values to analyze
    
    Returns:
        The most frequently occurring value, or None if list is empty
    
    Example:
        >>> most_common(["A", "B", "A", "C", "A"])
        'A'
    """
    if not values:
        return None
    return max(set(values), key=values.count)


def analyze_field_values(values: list) -> dict:
    """
    Analyze a list of field values and return profiling statistics.
    
    Args:
        values: List of values from a field
    
    Returns:
        Dict with profiling statistics:
        - total_count: Number of values
        - distinct_count: Number of unique values
        - null_count: Number of null/empty values
        - choice_ratio: Ratio of distinct to total
        - is_choice_candidate: Whether field should be Choice
        - suggested_type: Most common detected type
        - type_distribution: Count of each detected type
    
    Example:
        stats = analyze_field_values(["Active", "Inactive", "Active", ""])
        print(stats["suggested_type"])  # "Choice/Reference"
        print(stats["is_choice_candidate"])  # True
    """
    total_count = len(values)
    
    if total_count == 0:
        return {
            "total_count": 0,
            "distinct_count": 0,
            "null_count": 0,
            "choice_ratio": 0.0,
            "is_choice_candidate": False,
            "suggested_type": DataType.UNKNOWN,
            "type_distribution": {},
        }
    
    # Count nulls and get distinct
    non_null_values = [v for v in values if v is not None and str(v).strip() != ""]
    null_count = total_count - len(non_null_values)
    distinct_values = set(str(v) for v in non_null_values)
    distinct_count = len(distinct_values)
    
    # Choice detection
    choice_ratio = distinct_count / total_count if total_count > 0 else 0
    is_choice_candidate = detect_choice_field(distinct_count, total_count)
    
    # Type detection for each value
    type_counts = {}
    for v in non_null_values:
        detected_type = estimate_field_type(v, is_choice_candidate)
        type_counts[detected_type] = type_counts.get(detected_type, 0) + 1
    
    # Get most common type
    suggested_type = max(type_counts, key=type_counts.get) if type_counts else DataType.UNKNOWN
    
    return {
        "total_count": total_count,
        "distinct_count": distinct_count,
        "null_count": null_count,
        "choice_ratio": choice_ratio,
        "is_choice_candidate": is_choice_candidate,
        "suggested_type": suggested_type,
        "type_distribution": type_counts,
    }


# Profile report schema constants
PROFILE_COLUMNS = [
    "Source",
    "Field",
    "Count",
    "Populated",
    "Unique",
    "Datatype",
    "TopValues",
    "Choices",
]


def profile_series(
    series: pd.Series,
    source_name: str = "",
) -> dict:
    """
    Profile a pandas Series (column) and return statistics.
    
    Args:
        series: Pandas Series to analyze
        source_name: Name of the source (table/file)
    
    Returns:
        Dict with profiling statistics matching PROFILE_COLUMNS
    """
    length = len(series)
    
    if length == 0:
        return {
            "Source": source_name,
            "Field": series.name,
            "Count": 0,
            "Populated": 0,
            "Unique": 0,
            "Datatype": DataType.EMPTY,
            "TopValues": "",
            "Choices": [],
        }
    
    # Calculate empty/null values (pandas 3+ often uses str/StringDtype, not object)
    if is_object_dtype(series.dtype) or is_string_dtype(series.dtype):
        empty = series.isin(['', ' ']).sum() + series.isna().sum()
    else:
        empty = series.isna().sum()
    
    populated = length - empty
    
    # Get unique count
    if populated == 0:
        unique = 0
    else:
        unique = series.nunique()
    
    # Determine choice candidacy
    choice_ratio = float(unique) / float(length) if length > 0 else 0
    choice_flag = detect_choice_field(unique, length)
    
    # Determine datatype
    if populated == 0:
        datatype = DataType.EMPTY
    else:
        sample_values = series.dropna().head(5).tolist()
        types = [estimate_field_type(v, choice_flag) for v in sample_values]
        datatype = most_common(types) if types else DataType.EMPTY
    
    # Get top values for display
    top_values = series.head(6).fillna('').astype(str)
    top_five = "; ".join([str(x)[:50] for x in top_values if x != ""])
    
    # Get choices if applicable
    choices = []
    if datatype == DataType.CHOICE_REFERENCE:
        choices = series.value_counts().index.tolist()
    
    return {
        "Source": source_name,
        "Field": series.name,
        "Count": length,
        "Populated": populated,
        "Unique": unique,
        "Datatype": datatype,
        "TopValues": top_five,
        "Choices": choices,
    }


def profile_dataframe(
    df: Union[pd.DataFrame, "pl.DataFrame"],
    source_name: str = "",
    messenger: Optional[Callable[[str], None]] = None,
) -> pd.DataFrame:
    """
    Profile all columns in a DataFrame.
    
    Analyzes each column to determine data types, null counts,
    unique values, and potential choice values.
    
    Args:
        df: pandas or Polars DataFrame to profile (Polars is converted with ``to_pandas()``)
        source_name: Name of the data source (table/file)
        messenger: Optional callback for progress messages
    
    Returns:
        DataFrame with profiling results (one row per column)
    
    Example:
        profile = profile_dataframe(df, "customers.csv")
        print(profile[["Field", "Datatype", "Populated"]])
    """
    if not isinstance(df, pd.DataFrame):
        try:
            import polars as pl
        except ImportError as e:
            raise ImportError(
                "Polars is not installed. Install with: pip install dealcloud-sdk[polars]"
            ) from e
        if isinstance(df, pl.DataFrame):
            df = df.to_pandas()
        else:
            raise TypeError(f"Expected pandas or polars DataFrame, got {type(df)!r}")

    if messenger:
        messenger(f"Profiling {source_name or 'DataFrame'}")
    
    results = []
    for column in df.columns:
        stats = profile_series(df[column], source_name)
        results.append(stats)
    
    return pd.DataFrame(results, columns=PROFILE_COLUMNS)


def profile_files(
    filepaths: list[Union[str, "Path"]],
    messenger: Optional[Callable[[str], None]] = None,
) -> pd.DataFrame:
    """
    Profile multiple data files.
    
    Reads and profiles each file, combining results into a single DataFrame.
    
    Args:
        filepaths: List of file paths to profile
        messenger: Optional callback for progress messages
    
    Returns:
        DataFrame with profiling results for all files
    
    Example:
        from dealcloud_sdk.utils.file_utils import get_data_files
        
        files = get_data_files("/path/to/data")
        profile = profile_files(files)
    """
    from .file_utils import read_file

    all_results = []

    for filepath in filepaths:
        path_str = str(filepath)
        source_name = path_str.rstrip("/").rsplit("/", 1)[-1].split("?", 1)[0]

        if messenger:
            messenger(f"Analyzing {source_name}")

        try:
            df = read_file(path_str)
            profile = profile_dataframe(df, source_name, messenger=None)
            all_results.append(profile)
        except Exception as e:
            logger.warning(f"Skipping file {source_name}: {e}")
            if messenger:
                messenger(f"Skipping file {source_name}: {e}")
    
    if all_results:
        return pd.concat(all_results, ignore_index=True)
    else:
        return pd.DataFrame(columns=PROFILE_COLUMNS)

