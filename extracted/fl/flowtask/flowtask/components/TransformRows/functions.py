"""
Functions.

Tree of TransformRows functions.

"""
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
from enum import Enum
from decimal import Decimal
import math
import re
import ast
import json
import base64
import orjson
import requests
import numpy as np
from numba import njit
import datetime as dtime
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo
from dateutil.tz import tzoffset, tzutc, tzlocal
import pandas
from pydantic import BaseModel
from datamodel.parsers.json import json_encoder
from ...conf import BARCODELOOKUP_API_KEY
from ...utils.executor import getFunction


_BRACKET_RE = re.compile(r"\[([^\]]+)\]")

def _create_tzinfo(offset_str: str) -> dtime.timezone:
    """Create a timezone from various formats."""
    offset_str = offset_str.strip()

    # Handle UTC
    if offset_str.upper() == 'UTC':
        return dtime.timezone.utc

    # Handle offset format: -04:00, +05:30, -0400, +0530
    offset_match = re.match(r'^([+-]?)(\d{1,2}):?(\d{2})?$', offset_str)
    if offset_match:
        sign = -1 if offset_match.group(1) == '-' else 1
        hours = int(offset_match.group(2))
        minutes = int(offset_match.group(3) or 0)
        total_seconds = sign * (hours * 3600 + minutes * 60)
        return dtime.timezone(dtime.timedelta(seconds=total_seconds))

    # Try zoneinfo for named timezones like America/New_York
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(offset_str)
    except (ImportError, KeyError):
        pass

    # Fallback to UTC if unrecognized
    return dtime.timezone.utc


def _preprocess_tzinfo(s: str) -> str:
    """Convert various TzInfo formats to quoted versions for eval."""
    # Match TzInfo(...) where content is NOT already quoted
    # Handles: TzInfo(-04:00), TzInfo(UTC), TzInfo(America/New_York), etc.
    pattern = r"TzInfo\(([^')]+)\)"
    s = re.sub(pattern, r"TzInfo('\1')", s)
    return s


def _build_eval_namespace() -> dict:
    """Build a safe namespace for eval with datetime and timezone support."""
    namespace = {
        "__builtins__": {},
        "datetime": dtime,
        "None": None,
        "True": True,
        "False": False,
        "TzInfo": _create_tzinfo,  # Our custom TzInfo parser
    }

    if ZoneInfo:
        namespace["ZoneInfo"] = ZoneInfo

    return namespace


EVAL_NAMESPACE = _build_eval_namespace()


def apply_function(
    df: pandas.DataFrame,
    field: str,
    fname: str,
    column: Optional[str] = None,
    **kwargs
) -> pandas.DataFrame:
    """
    Apply any scalar function to a column in the DataFrame.

    Parameters:
    - df: pandas DataFrame
    - field: The column where the result will be stored.
    - fname: The name of the function to apply.
    - column: The column to which the function is applied (if None, apply to `field` column).
    - **kwargs: Additional arguments to pass to the function.
    """

    # Retrieve the scalar function using getFunc
    try:
        func = getFunction(fname)
    except Exception:
        raise

    # If a different column is specified, apply the function to it,
    # but save result in `field`
    try:
        if column is not None:
            df[field] = df[column].apply(lambda x: func(x, **kwargs))
        else:
            if field not in df.columns:
                # column doesn't exist
                df[field] = None
            # Apply the function to the field itself
            df[field] = df[field].apply(lambda x: func(x, **kwargs))
    except Exception as err:
        print(
            f"Error in apply_function for field {field}:", err
        )
    return df


def get_product(row, field, columns):
    """
    Retrieves product information from the Barcode Lookup API based on a barcode.

    :param row: The DataFrame row containing the barcode.
    :param field: The name of the field containing the barcode.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame row with the product information.
    """

    barcode = row[field]
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode}&key={BARCODELOOKUP_API_KEY}'
    response = requests.get(url)
    result = response.json()['products'][0]
    for col in columns:
        try:
            row[col] = result[col]
        except KeyError:
            row[col] = None
    return row


def upc_to_product(
    df: pandas.DataFrame,
    field: str,
    columns: list = ['barcode_formats', 'mpn', 'asin', 'title', 'category', 'model', 'brand']
) -> pandas.DataFrame:
    """
    Converts UPC codes in a DataFrame to product information using the Barcode Lookup API.

    :param df: The DataFrame containing the UPC codes.
    :param field: The name of the field containing the UPC codes.
    :param columns: The list of columns to extract from the API response.
    :return: The DataFrame with the product information.
    """
    try:
        df = df.apply(lambda x: get_product(x, field, columns), axis=1)
        return df
    except Exception as err:
        print(f"Error on upc_to_product {field}:", err)
        return df

def day_of_week(
    df: pandas.DataFrame,
    field: str,
    column: str,
    locale: str = 'en_US.utf8'
) -> pandas.DataFrame:
    """
    Extracts the day of the week from a date column.

    :param df: The DataFrame containing the date column.
    :param field: The name of the field to store the day of the week.
    :param column: The name of the date column.
    :return: The DataFrame with the day of the week.
    """
    try:
        df[field] = df[column].dt.day_name(locale=locale)
        return df
    except Exception as err:
        print(f"Error on day_of_week {field}:", err)
        return df

def duration(
    df: pandas.DataFrame,
    field: str,
    columns: List[str],
    unit: str = 's'
) -> pandas.DataFrame:
    """
    Converts a duration column to a specified unit.

    :param df: The DataFrame containing the duration column.
    :param field: The name of the field to store the converted duration.
    :param column: The name of the duration column.
    :param unit: The unit to convert the duration to.
    :return: The DataFrame with the converted duration.
    """
    try:
        if unit == 's':
            _unit = 1.0
        if unit == 'm':
            _unit = 60.0
        elif unit == 'h':
            _unit = 3600.0
        elif unit == 'd':
            _unit = 86400.0
        # Calculate duration in minutes as float
        df[field] = (
            (df[columns[1]] - df[columns[0]]).dt.total_seconds() / _unit
        )
        return df
    except Exception as err:
        print(f"Error on duration {field}:", err)
        return df


def get_moment(
    df: pandas.DataFrame,
    field: str,
    column: str,
    moments: List[tuple] = None,
) -> pandas.DataFrame:
    """
    df: pandas DataFrame
    column: name of the column to compare (e.g. "updated_hour")
    ranges: list of tuples [(label, (start, end)), ...]
            e.g. [("night",(0,7)), ("morning",(7,10)), ...]
    returns: a Series of labels corresponding to each row
    """
    if not moments:
        moments = [
            ("night", (0, 7)),   # >= 0 and < 7
            ("morning", (7, 10)),  # >= 7 and < 10
            ("afternoon", (10, 16)),  # >= 10 and < 16
            ("evening", (16, 20)),  # >= 16 and < 20
            ("night", (20, 24)),  # >= 20 and < 24 (or use float("inf") for open-ended)
        ]
    conditions = [
        (df[column] >= start) & (df[column] < end)
        for _, (start, end) in moments
    ]
    df[field] = np.select(conditions, [label for label, _ in moments], default=None)
    return df


def fully_geoloc(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple],
    inverse: bool = False
) -> pandas.DataFrame:
    """
    Adds a boolean column (named `field`) to `df` that is True when,
    for each tuple in `columns`, all the involved columns are neither NaN nor empty.

    Parameters:
        df (pd.DataFrame): The DataFrame.
        field (str): The name of the output column.
        columns (list of tuple of str): List of tuples, where each tuple
            contains column names that must be valid (non-null and non-empty).
            Example: [("start_lat", "start_long"), ("end_lat", "end_log")]

    Returns:
        pd.DataFrame: The original DataFrame with the new `field` column.
    """
    # Start with an initial mask that's True for all rows.
    mask = pandas.Series(True, index=df.index)

    # Loop over each tuple of columns, then each column in the tuple.
    for col_group in columns:
        for col in col_group:
            if inverse:
                mask &= df[col].isna() | (df[col] == "")
            else:
                mask &= df[col].notna() & (df[col] != "")

    df[field] = mask
    return df


def any_tuple_valid(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple]
) -> pandas.DataFrame:
    """
    Adds a boolean column (named `field`) to `df` that is True when
    any tuple in `columns` has all of its columns neither NaN nor empty.

    Parameters:
        df (pd.DataFrame): The DataFrame.
        field (str): The name of the output column.
        columns (list of tuple of str): List of tuples, where each tuple
            contains column names that must be checked.
            Example: [("start_lat", "start_long"), ("end_lat", "end_log")]

    Returns:
        pd.DataFrame: The original DataFrame with the new `field` column.
    """
    # Start with an initial mask that's False for all rows
    result = pandas.Series(False, index=df.index)

    # Loop over each tuple of columns
    for col_group in columns:
        # For each group, assume all columns are valid initially
        group_all_valid = pandas.Series(True, index=df.index)

        # Check that all columns in this group are non-null and non-empty
        for col in col_group:
            group_all_valid &= df[col].notna() & (df[col] != "")

        # If all columns in this group are valid, update the result
        result |= group_all_valid

    df[field] = result
    return df


@njit
def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = 'km'
) -> float:
    """Distance between two points on Earth in kilometers."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = np.radians(lat1), np.radians(lon1), np.radians(lat2), np.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    # Select radius based on unit
    if unit == 'km':
        r = 6371.0  # Radius of earth in kilometers
    elif unit == 'm':
        r = 6371000.0  # Radius of earth in meters
    elif unit == 'mi':
        r = 3956.0  # Radius of earth in miles
    else:
        # Numba doesn't support raising exceptions, so default to km
        r = 6371.0

    return c * r

def calculate_distance(
    df: pandas.DataFrame,
    field: str,
    columns: List[tuple],
    unit: str = 'km',
    chunk_size: int = 1000
) -> pandas.DataFrame:
    """
    Add a distance column to a dataframe.

    Args:
        df: pandas DataFrame with columns 'latitude', 'longitude', 'store_lat', 'store_lng'
        columns: list of tuples with column names for coordinates
               - First tuple: [latitude1, longitude1]
               - Second tuple: [latitude2, longitude2]
        unit: unit of distance ('km' for kilometers, 'm' for meters, 'mi' for miles)
        chunk_size: number of rows to process at once for large datasets

    Returns:
        df with additional 'distance_km' column
    """
    result = df.copy()
    result[field] = np.nan
    # Unpack column names
    (lat1_col, lon1_col), (lat2_col, lon2_col) = columns
    try:
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size]
            # Convert to standard NumPy arrays before passing to haversine_distance
            lat1_values = chunk[lat1_col].to_numpy(dtype=np.float64)
            lon1_values = chunk[lon1_col].to_numpy(dtype=np.float64)
            lat2_values = chunk[lat2_col].to_numpy(dtype=np.float64)
            lon2_values = chunk[lon2_col].to_numpy(dtype=np.float64)
            result.loc[chunk.index, field] = haversine_distance(
                lat1_values,
                lon1_values,
                lat2_values,
                lon2_values,
                unit=unit
            )
    except Exception as err:
        print(f"Error on calculate_distance {field}:", err)
    return result


def drop_timezone(
    df: pandas.DataFrame,
    field: str,
    column: Optional[str] = None
) -> pandas.DataFrame:
    """
    Drop the timezone information from a datetime column.

    Args:
        df: pandas DataFrame with a datetime column
        field: name of the datetime column

    Returns:
        df with timezone-free datetime column
    """
    try:
        if column is None:
            column = field

        series = df[column]
        if pandas.api.types.is_datetime64tz_dtype(series):
            # This is a regular tz-aware pandas Series
            df[field] = series.dt.tz_localize(None)
            return df

        elif series.dtype == 'object':
            # Object-dtype: apply tz-localize(None) to each element
            def remove_tz(x):
                if isinstance(x, (pandas.Timestamp, datetime)) and x.tzinfo is not None:
                    return x.replace(tzinfo=None)
                return x  # leave as-is (could be NaT, None, or already naive)

            df[field] = series.apply(remove_tz).astype('datetime64[ns]')
            return df

        else:
            # already naive or not datetime
            df[field] = series
            return df
    except Exception as err:
        print(f"Error on drop_timezone {field}:", err)
    return df

def convert_timezone(
    df: pandas.DataFrame,
    field: str,
    *,
    column: str | None = None,
    from_tz: str = "UTC",
    to_tz: str | None = None,
    tz_column: str | None = None,
    default_timezone: str = "UTC",
) -> pandas.DataFrame:
    """
    Convert `field` to a target time‑zone.

    Parameters
    ----------
    df        : DataFrame
    field     : name of an existing datetime column
    column    : name of the output column (defaults to `field`)
    from_tz   : timezone used to localise *naive* timestamps
    to_tz     : target timezone (ignored if `tz_column` is given)
    tz_column : optional column that contains a timezone per row
    default_tz: fallback when a row's `tz_column` is null/NaN

    Returns:
        df with converted datetime column
    """
    if column is None:
        column = field

    try:
        # --- 1. make a working copy of current column
        out = df[column].copy()
        out = pandas.to_datetime(out, errors="coerce")  # force datetime dtype

        # --- 2. give tz‑naive stamps a timezone --------------------------------
        if out.dt.tz is None:
            out = out.dt.tz_localize(from_tz, ambiguous="infer", nonexistent="raise")

        # --- 3. convert ---------------------------------------------------------
        if tz_column is None:
            # same tz for every row
            target = to_tz or default_timezone
            out = out.dt.tz_convert(target)
        else:
            # using the timezone declared on column:
            timezones = (
                df[tz_column]
                .fillna(default_timezone)
                .astype("string")
            )

            # First, convert all timestamps to UTC to have a common base
            utc_times = out.dt.tz_convert('UTC')

            # Create a list to store the converted datetimes
            converted_times = []

            # Apply timezone conversion row by row
            for idx in df.index:
                try:
                    tz_name = timezones.loc[idx]
                    # Convert the UTC time to the target timezone
                    converted_dt = utc_times.loc[idx].tz_convert(ZoneInfo(tz_name))
                    converted_times.append(converted_dt)
                except Exception as e:
                    # Handle invalid timezones gracefully
                    converted_dt = utc_times.loc[idx].tz_convert(ZoneInfo(default_timezone))
                    converted_times.append(converted_dt)

            # Create a new Series with the converted values
            out = pandas.Series(converted_times, index=df.index)

        df[field] = out
    except Exception as err:
        print(f"Error on convert_timezone {field}:", err)

    return df


def add_timestamp_to_time(df: pandas.DataFrame, field: str, date: str, time: str):
    """
    Takes a pandas DataFrame and combines the values from a date column and a time column
    to create a new timestamp column.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the new column to store the combined timestamp.
    :param date: Name of the column in the df DataFrame containing date values.
    :param time: Name of the column in the df DataFrame containing time values.
    :return: Modified pandas DataFrame with the combined timestamp stored in a new column.
    """
    try:
        df[field] = pandas.to_datetime(df[date].astype(str) + " " + df[time].astype(str))
    except Exception as e:
        print(f"Error adding timestamp to time: {str(e)}")
        return df
    return df

def _convert_string_to_vector(vector_string):
    """
    Converts a string representation of a list into an actual list.

    :param vector_string: The string representation of the list.
    :return: The converted list.
    """
    try:
        # Extract the numbers from the string representation
        numbers = re.findall(r'-?\d+\.\d+', vector_string)
        # Convert the extracted strings to float values
        float_values = [float(num) for num in numbers]
        # Return as numpy array
        return np.array(float_values, dtype=np.float32)
    except Exception as err:
        print(
            f"Error converting string to vector: {err}"
        )
        return vector_string

def string_to_vector(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    """
    Converts a string representation of a list into an actual list.

    :param df: The DataFrame containing the string representation.
    :param field: The name of the field to convert.
    :return: The DataFrame with the converted field.
    """
    try:
        df[field] = df[field].apply(_convert_string_to_vector)
        return df
    except Exception as err:
        print(f"Error on vector_string_to_array {field}:", err)
        return df

def extract_from_dictionary(
    df: pandas.DataFrame,
    field: str,
    column: str,
    key: str,
    conditions: dict = None,
    as_timestamp: bool = False
) -> pandas.DataFrame:
    """
    Extracts a value from a JSON column in the DataFrame.

    :param df: The DataFrame containing the JSON column.
    :param field: The name of the field to store the extracted value.
    :param column: The name of the JSON column.
    :param key: The key to extract from the JSON object.
    :param conditions: Optional dictionary of conditions to filter rows before extraction.
    :param as_timestamp: If True, converts the extracted value to a timestamp.
    :return: The DataFrame with the extracted value.
    """
    def extract_from_dict(row, key, conditions=None, as_timestamp=False):
        items = row if isinstance(row, list) else []
        if not row:
            return None
        # Apply filtering
        if conditions:
            items = [
                item for item in items
                if all(item.get(k) == v for k, v in conditions.items())
            ]
        if not items:
            return None
        # Take last item if multiple
        value = items[-1].get(key)
        if as_timestamp and value:
            try:
                return pandas.to_datetime(value)
            except Exception:
                return None
        return value
    try:
        df[field] = df[column].apply(
            extract_from_dict, args=(key, conditions, as_timestamp)
        )
        return df
    except Exception as err:
        print(f"Error on extract_from_json {field}:", err)
        return df

def extract_from_object(
    df: pandas.DataFrame,
    field: str,
    column: str,
    key: str,
    as_string: bool = False,
    as_timestamp: bool = False
) -> pandas.DataFrame:
    """
    Extracts a value from an object column in the DataFrame.

    :param df: The DataFrame containing the object column.
    :param field: The name of the field to store the extracted value.
    :param column: The name of the object column.
    :param key: The key to extract from the object.
    :param as_string: If True, converts the extracted value to a string.
    :param as_timestamp: If True, converts the extracted value to a timestamp.
    :return: The DataFrame with the extracted value.
    """
    try:
        def _getter(obj):
            # 1) turn a BaseModel into a dict
            if isinstance(obj, BaseModel):
                obj = obj.model_dump()  # or .dict() on older Pydantic

            # 2) if it's not a dict now, we can't extract
            if not isinstance(obj, dict):
                return None

            # 3) pull the raw value
            val = obj.get(key)

            # 4) if it's an Enum, unwrap it
            if isinstance(val, Enum):
                val = val.value

            # 5) optional casts
            if val is not None:
                if as_string:
                    try:
                        return val if isinstance(val, str) else json_encoder(val)
                    except Exception:
                        return str(val)
                elif isinstance(val, (int, float)):
                    return val
                elif as_timestamp:
                    try:
                        val = pandas.to_datetime(val)
                    except Exception:
                        return None

            return val

        # create the column if it doesn't exist
        if field not in df.columns:
            df[field] = None

        # apply our getter
        df[field] = df[column].apply(_getter)
        if as_string:
            df[field] = df[field].astype("string")
        elif as_timestamp:
            df[field] = pandas.to_datetime(df[field], errors='coerce')
        return df
    except Exception as err:
        print(f"Error on extract_from_object {field}:", err)
        return df


def bytesio_to_base64(
    df: pandas.DataFrame,
    field: str,
    column: str,
    as_string: bool = False,
    as_image: bool = True,
    image_mime: str = 'image/png'
) -> pandas.DataFrame:
    """
    Converts bytes in a DataFrame column to a Base64 encoded string.

    :param df: The DataFrame containing the bytes column.
    :param field: The name of the field to store the Base64 encoded string.
    :param column: The name of the bytes column.
    :param as_string: If True, converts the Base64 bytes to a string.
    :return: The DataFrame with the Base64 encoded string.
    """
    def to_base64(x, mime: str = 'image/png'):
        """
        Converts BytesIO to Base64 encoded string.
        """
        return f"data:{mime};base64,{base64.b64encode(x.getvalue()).decode('ascii')}"

    try:
        if as_string:
            df[field] = df[column].apply(lambda x: x.decode('utf-8') if as_string else x)
        elif as_image:
            # Convert bytes to Base64 encoded string
            df[field] = df[column].apply(lambda x: to_base64(x, mime=image_mime))
        return df
    except Exception as err:
        print(f"Error on bytes_to_base64 {field}:", err)
        return df


def create_attachment_column(
    df: pandas.DataFrame,
    field: str,
    columns: List[str],
    colnames: Optional[Dict[str, str]] = None

) -> pandas.DataFrame:
    """
    Create a column with a list of attachments from one or more path/URL columns.

    Args:
        df: Input DataFrame.
        field: Name of the new column to store the list of attachments.
        columns: Column names to convert. You can pass either the exact column
              (e.g., "pdf_path_m0") or the base name (e.g., "pdf_path").
        colnames: Optional list of names for the attachments. If not provided,
                  the column names will be used as names.

    Returns:
        The same DataFrame with `field` added.
    """
    def _humanize(col: str, colname: dict) -> str:
        """
        Turn 'podcast_path' -> 'Podcast', 'pdf_path' -> 'PDF', etc.
        """
        if colname and col in colname:
            return colname[col]
        base = re.sub(r'(?:_)?path$', '', col, flags=re.IGNORECASE)  # drop trailing 'path'
        base = base.replace('_', ' ').strip()
        title = base.title()

        # Acronym fixes
        fixes = {
            "Pdf": "PDF",
            "Url": "URL",
            "Id": "ID",
            "Mp3": "MP3",
            "Csv": "CSV",
            "Html": "HTML",
            "Json": "JSON"
        }
        return fixes.get(title, title)

    def _row_to_attachments(row: pandas.Series) -> list[dict]:
        out = []
        for c in columns:
            if c not in row:
                continue
            val = row[c]
            if pandas.isna(val) or (isinstance(val, str) and not val.strip()):
                continue
            out.append({"name": _humanize(c, colnames), "url": str(val)})
        return out

    df[field] = df.apply(_row_to_attachments, axis=1)
    return df


def path_to_url(
    df: pandas.DataFrame,
    field: str,
    column: str = None,
    base_path: str = 'files/',
    base_url: str = "https://example.com/files/"
) -> pandas.DataFrame:
    """
    Converts a file path in a DataFrame column to a URL.
    Replaces the base path with the base URL.

    :param df: The DataFrame containing the file path column.
    :param field: The name of the field to store the URL.
    :param column: The name of the file path column (defaults to `field`).
    :param base_path: The base path to replace in the file path.
    :param base_url: The base URL to use for the conversion.

    :return: The DataFrame with the URL in the specified field.
    """
    if column is None:
        column = field

    try:
        def convert_path_to_url(path):
            if not isinstance(path, str):
                return None
            # Ensure the path starts with the base path
            if path.startswith(base_path):
                return base_url + path[len(base_path):]
            return base_url + path

        df[field] = df[column].apply(convert_path_to_url)
    except Exception as err:
        print(f"Error on path_to_url {field}:", err)
        return df
    return df

def load_from_file(
    df: pandas.DataFrame,
    field: str,
    column: str = None,
    as_text: bool = True
) -> pandas.DataFrame:
    """
    Loads the content of a file specified as a path in `column` into `field`.

    Args:
        df: pandas DataFrame with a column containing file paths.
        field: name of the new column to store the file content.
        column: name of the column with file paths (defaults to `field`).
        as_text: if True, read file as text; otherwise, read as bytes.
    """
    if column is None:
        column = field

    def read_file_content(path: str) -> str | bytes | None:
        if not isinstance(path, str):
            return None
        try:
            with open(path, 'r' if as_text else 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {path}: {e}")
            return None

    df[field] = df[column].apply(read_file_content)
    return df

def extract_address_components(
    df: pandas.DataFrame,
    field: str,
    column: str,
    component: str = 'city'  # 'city', 'state_code', or 'zipcode'
) -> pandas.DataFrame:
    """
    Extracts city, state code, or zipcode from a US address string.

    Handles formats:
    - "Street Address, City, ST 12345"
    - "Street Address, City, State Name 12345"

    :param df: The DataFrame containing the address column.
    :param field: The name of the field to store the extracted component.
    :param column: The name of the address column.
    :param component: Which component to extract ('city', 'state_code', 'zipcode').
    :return: The DataFrame with the extracted component.
    """
    # State name to code mapping
    state_mapping = {
        'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
        'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
        'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
        'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
        'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
        'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
        'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
        'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
        'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
        'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
        'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
        'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
        'wisconsin': 'WI', 'wyoming': 'WY'
    }

    # Pattern 1: 2-letter state code
    pattern1 = r',\s*([^,]+),\s*([A-Z]{2})\s*(\d{5}(?:-\d{4})?),?\s*$'
    # Pattern 2: Full state name
    pattern2 = r',\s*([^,]+),,?\s*([A-Za-z\s]+?)\s+(\d{5}(?:-\d{4})?),?\s*$'
    # Pattern 3: Falling back to state code and zipcode only:
    pattern3 = r',\s*([A-Z]{2})\s*(\d{4,5}(?:-\d{4})?),?\s*$'

    def extract_component(address):
        if not isinstance(address, str):
            return None

        # Try pattern 1 first (2-letter state code)
        match = re.search(pattern1, address)
        if match:
            if component == 'city':
                return match.group(1).strip()
            elif component == 'state_code':
                return match.group(2).strip()
            elif component == 'zipcode':
                return match.group(3).strip()

        # Fallback to pattern 2 (full state name)
        match = re.search(pattern2, address)
        if match:
            if component == 'city':
                return match.group(1).strip()
            elif component == 'state_code':
                state_name = match.group(2).strip().lower()
                return state_mapping.get(state_name, match.group(2).strip())
            elif component == 'zipcode':
                z = match.group(3).strip()
                if len(z) == 4:
                    z = '0' + z  # pad 4-digit zipcodes
                return z

        # Fallback to pattern 3 (state code and zipcode only)
        match = re.search(pattern3, address)
        if match:
            if component == 'state_code':
                return match.group(1).strip()
            elif component == 'zipcode':
                return match.group(2).strip()

        return None

    try:
        df[field] = df[column].apply(extract_component)
        return df
    except Exception as err:
        print(f"Error on extract_address_components {field}:", err)
        return df

def column_to_json(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    """
    Convert the values in df[field] into Python objects (list/dict) parsed from
    JSON or Python-literal strings. Examples of accepted inputs:
      - '["plumbing","heating"]'          -> ["plumbing","heating"]
      - "['plumbing', 'plumbing']"        -> ["plumbing","plumbing"]
      - [] / {}                           -> unchanged
      - NaN / None / "" / "null"          -> []
      - "plumbing, heating"               -> ["plumbing","heating"]  (fallback)

    Returns a new DataFrame (copy) with df[field] normalized to Python objects.
    """

    def _parse_cell(x):
        # Treat nullish as empty list
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return []

        # Already parsed
        if isinstance(x, (list, dict)):
            return x

        # Decode bytes
        if isinstance(x, (bytes, bytearray)):
            try:
                x = x.decode("utf-8", "ignore")
            except Exception:
                return []

        # Strings: try JSON -> Python literal -> fallbacks
        if isinstance(x, str):
            s = x.strip()
            if not s or s.lower() == "null":
                return []
            # Try strict JSON
            try:
                return orjson.loads(s)
            except Exception:
                pass
            # Try Python literal (handles single quotes, tuples, etc.)
            try:
                val = ast.literal_eval(s)
                # Ensure only list/dict/tuple/scalars; coerce tuple->list
                if isinstance(val, tuple):
                    return list(val)
                if isinstance(val, (list, dict)):
                    return val
                # Scalar -> wrap in list
                return [val]
            except Exception:
                pass
            # Fallback: comma-separated words
            if "," in s and "[" not in s and "{" not in s:
                return [t.strip().strip('"').strip("'") for t in s.split(",") if t.strip()]
            # Last resort: single string as single-item list
            return [s.strip().strip('"').strip("'")]

        # Unknown types: leave as-is
        return x

    df = df.copy()
    df[field] = df[field].map(_parse_cell)
    return df

def to_json_strings(df: pandas.DataFrame, field: str) -> pandas.DataFrame:
    df = column_to_json(df, field).copy()
    df[field] = df[field].map(lambda v: orjson.dumps(v).decode("utf-8"))
    return df


def _parse_python_object(value: Any) -> Any:
    """
    Safely parse a value that might be a string representation of a Python object.
    Recursively parses nested structures.
    """
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None

    if isinstance(value, list):
        return [_parse_python_object(item) for item in value]

    if isinstance(value, dict):
        return {k: _parse_python_object(v) for k, v in value.items()}

    if isinstance(value, tuple):
        return tuple(_parse_python_object(item) for item in value)

    if not isinstance(value, str):
        return value

    s = value.strip()
    if not s or s.lower() == "null":
        return None

    # Preprocess to fix TzInfo(-04:00) -> TzInfo('-04:00')
    s = _preprocess_tzinfo(s)

    # Use eval with extended namespace
    try:
        parsed = eval(s, EVAL_NAMESPACE, {})
        return _parse_python_object(parsed)
    except Exception as e:
        pass

    # Fallback to ast.literal_eval
    try:
        parsed = ast.literal_eval(s)
        return _parse_python_object(parsed)
    except (ValueError, SyntaxError):
        pass

    # Fallback to JSON parsing
    try:
        parsed = orjson.loads(s)
        return _parse_python_object(parsed)
    except Exception:
        pass

    return value


def _serialize_to_json(value: Any) -> str:
    """
    Serialize a Python object to a JSON string using orjson.

    Handles special types like datetime objects.
    """
    if value is None:
        return "null"

    try:
        # orjson handles datetime natively with OPT_NAIVE_UTC
        return json_encoder(value)
    except TypeError:
        # Fallback: use json_encoder for complex types
        try:
            return orjson.dumps(
                value,
                default=json_encoder,
                option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY
            ).decode("utf-8")
        except Exception:
            # Last resort: convert to string
            return str(value)

def from_json(df: pandas.DataFrame, field: str, column: str = None) -> pandas.DataFrame:
    """
    Parse JSON string representations in a DataFrame column into Python objects.

    Parameters:
    - df: pandas DataFrame
    - field: The column where the result will be stored
    - column: The source column (defaults to field if not specified)

    Returns:
        DataFrame with the field column containing Python objects
    """
    if column is None:
        column = field

    def _convert_from_json(value: Any) -> Any:
        # Step 1: Parse JSON string to Python object
        parsed = _parse_python_object(value)
        return parsed

    try:
        df[field] = df[column].apply(_convert_from_json)
    except Exception as err:
        print(f"Error on from_json {field}: {err}")

    return df


def to_json(df: pandas.DataFrame, field: str, column: str = None) -> pandas.DataFrame:
    """
    Convert column values to JSON string representation.

    This function:
    1. Safely converts string representations of Python objects into actual Python objects
       (e.g., "[{'author': 'John', 'created': datetime.datetime(...)}]" -> list of dicts)
    2. If the value is already a Python object, leaves it as-is
    3. Serializes the result to a JSON string using orjson.dumps()

    Parameters:
    - df: pandas DataFrame
    - field: The column where the result will be stored
    - column: The source column (defaults to field if not specified)

    Returns:
        DataFrame with the field column containing JSON strings
    """
    if column is None:
        column = field

    def _convert_to_json(value: Any) -> str:
        # Step 1: Parse string to Python object if needed
        parsed = _parse_python_object(value)
        # Step 2: Serialize to JSON string
        return _serialize_to_json(parsed)

    try:
        df[field] = df[column].apply(_convert_to_json)
        df[field] = df[field].astype("string")
    except Exception as err:
        print(f"Error on to_json {field}: {err}")

    return df


def _as_dict(x):
    """Accept dict / JSON string / None and return a dict."""
    if isinstance(x, dict):
        return x
    if isinstance(x, str) and x.strip():
        try:
            return json.loads(x)
        except Exception:
            return {}
    return {}

def _normalize(s):
    return s if s is None else str(s)

def _safe_col(prefix: str, key: str) -> str:
    """Make a safe column name: prefix + sanitized key."""
    key_sanitized = re.sub(r"\W+", "_", key.strip().lower()).strip("_")
    return f"{prefix}{key_sanitized}"

def expand_compliance_by_shelf(
    df: pandas.DataFrame,
    field: str,
    source_col: str = "compliance_by_shelf",
    shelf_prefix: str = "shelf_",
    make_wide_status_score: bool = True,
):
    """
    - Creates one column per shelf key (prefixed), plus optional *_status and *_score columns.
    - Adds two dict-mapping columns:
        * expected_by_shelf: {shelf: [expected_products]}
        * found_by_shelf:    {shelf: [found_products]}
    - Returns (df_with_columns, long_table) where long_table is a normalized per-shelf view.
    """
    shelves_series = df[source_col].apply(_as_dict)

    # All shelf names across the dataframe
    all_shelves = sorted({k for d in shelves_series for k in (d or {}).keys()})

    # 1) Wide columns per shelf (store the entire sub-object)
    for shelf in all_shelves:
        col_base = _safe_col(shelf_prefix, shelf)
        df[col_base] = shelves_series.apply(lambda d: (d or {}).get(shelf))

        if make_wide_status_score:
            df[f"{col_base}_status"] = df[col_base].apply(
                lambda v: (v or {}).get("compliance_status") if isinstance(v, dict) else np.nan
            )
            df[f"{col_base}_score"] = df[col_base].apply(
                lambda v: (v or {}).get("compliance_score") if isinstance(v, dict) else np.nan
            )

    # 2) Dict columns mapping shelf -> expected / found product lists
    df["expected_by_shelf"] = shelves_series.apply(
        lambda d: {k: (v.get("expected_products") or []) for k, v in (d or {}).items()}
    )
    df["found_by_shelf"] = shelves_series.apply(
        lambda d: {k: (v.get("found_products") or []) for k, v in (d or {}).items()}
    )

    # 3) Long/normalized view (one row per (original_row, shelf))
    rows = []
    for idx, d in shelves_series.items():
        for shelf, obj in (d or {}).items():
            rows.append(
                {
                    "_row": idx,
                    "shelf": shelf,
                    "compliance_score": obj.get("compliance_score"),
                    "compliance_status": obj.get("compliance_status"),
                    "expected_products": obj.get("expected_products", []),
                    "found_products": obj.get("found_products", []),
                }
            )
    long_df = pandas.DataFrame(rows).set_index("_row") if rows else pandas.DataFrame(
        columns=[
            "shelf",
            "compliance_score",
            "compliance_status",
            "expected_products",
            "found_products"
        ]
    )

    return df

def _len_total(d: dict) -> int:
    if not isinstance(d, dict):
        return 0
    return sum(len(v or []) for v in d.values())

def len_total(
    df: pandas.DataFrame,
    field: str,
    column: str
) -> pandas.DataFrame:
    """
    Creates a new column with the total length of strings across multiple JSON columns.

    :param df: The DataFrame containing the string columns.
    :param field: The name of the field to store the total length.
    :param column: The column to consider for length calculation.
    :return: The DataFrame with the total length column.
    """
    try:
        df[field] = df[column].apply(_len_total)
        return df
    except Exception as err:
        print(f"Error on len_total {field}:", err)
        return df

def _extract_bracket_token(s: str) -> Optional[str]:
    """Return the LOWERCASED token inside [...] from a found string. If multiple, take the LAST."""
    if s is None:
        return None
    m = None
    for m in _BRACKET_RE.finditer(str(s)):
        pass
    return m.group(1).lower() if m else None

def _by_position_alignment(expected_by_shelf: dict, found_by_shelf: dict) -> dict:
    e = _as_dict(expected_by_shelf)
    f = _as_dict(found_by_shelf)
    out = {}
    for shelf, exp_list in (e or {}).items():
        exp_list = exp_list or []
        f_list = list((f.get(shelf) or []))
        rows = []
        for i, exp in enumerate(exp_list):
            found_item = f_list[i] if i < len(f_list) else None
            rows.append({
                "expected": exp,
                "found": found_item,
                "match": found_item is not None
            })
        out[shelf] = rows
    return out

def _by_value_alignment(
    expected_by_shelf: dict,
    found_by_shelf: dict,
    report_positional_when_unmatched: bool = True
) -> dict:
    """
    Non-header shelves: match expected items to found items 1:1 by bracket token.
    If no token match: optionally record the found item at the same index (for reference).
    """
    e = _as_dict(expected_by_shelf)
    f = _as_dict(found_by_shelf)
    out = {}

    for shelf, exp_list in (e or {}).items():
        exp_list = exp_list or []
        found_list = list((f.get(shelf) or []))

        # token -> queue of found indices (multiset behavior)
        token_to_indices: Dict[str, List[int]] = defaultdict(list)
        for idx, fv in enumerate(found_list):
            tok = _extract_bracket_token(fv)
            if tok:
                token_to_indices[tok].append(idx)

        rows = []
        for i, exp in enumerate(exp_list):
            key = str(exp).lower()
            indices = token_to_indices.get(key, [])
            if indices:
                use_idx = indices.pop(0)
                found_item = found_list[use_idx]
                rows.append({"expected": exp, "found": found_item, "match": True})
            else:
                # no token match — show what was at the same position for reference
                found_at_position = found_list[i] if (report_positional_when_unmatched and i < len(found_list)) else None
                rows.append({"expected": exp, "found": found_at_position, "match": False})
        out[shelf] = rows

    return out

def align_mixed_rules(
    expected_by_shelf: dict,
    found_by_shelf: dict,
    header_keys: Optional[List[str]] = None
) -> dict:
    """
    Mixed rules:
      - shelves named in header_keys (case-insensitive) -> position-only alignment
      - other shelves -> value-based by bracket token from found strings
    """
    header_keys = [k.lower() for k in (header_keys or ["header"])]
    e = _as_dict(expected_by_shelf)
    f = _as_dict(found_by_shelf)

    out = {}
    # Position-only for header-like shelves
    pos_aligned = _by_position_alignment(e, f)
    # Value-based for all shelves
    val_aligned = _by_value_alignment(e, f)

    for shelf in e.keys():
        if shelf.lower() in header_keys:
            out[shelf] = pos_aligned.get(shelf, [])
        else:
            out[shelf] = val_aligned.get(shelf, [])
    return out

def _summarize_pos(aligned: dict) -> dict:
    total_expected = 0
    total_matched = 0
    for rows in (aligned or {}).values():
        total_expected += len(rows)
        total_matched += sum(1 for r in rows if r["match"])
    return {
        "total_expected_elements": total_expected,
        "total_matched_elements": total_matched,
        "total_unmatched_elements": total_expected - total_matched,
        "match_rate": (total_matched / total_expected) if total_expected else None,
    }

def component_match(
    df: pandas.DataFrame,
    field: str,
    expected_col: str = "expected_by_shelf",
    found_col: str = "found_by_shelf",
    out_summary_col: str = "element_match_summary",
    out_flat_col: Optional[str] = None,
    header_keys: Optional[List[str]] = None
) -> pandas.DataFrame:
    """
    Adds:
      - <field>: {shelf: [{expected, found, match}, ...]} using mixed rules (header by position, others by value token)
      - element_match_summary: totals across all shelves
      - (optional) flat list with {"shelf","expected","found","match"}
    """
    aligned_all = []
    summaries = []
    flats = [] if out_flat_col else None

    for e, f in zip(df[expected_col], df[found_col]):
        aligned = align_mixed_rules(e, f, header_keys=header_keys)
        aligned_all.append(aligned)
        summaries.append(_summarize_pos(aligned))

        if flats is not None:
            flat_rows = []
            for shelf, rows in aligned.items():
                for r in rows:
                    flat_rows.append({"shelf": shelf, **r})
            flats.append(flat_rows)

    df[field] = aligned_all
    df[out_summary_col] = summaries
    if flats is not None:
        df[out_flat_col] = flats

    df["total_found"] = df[found_col].apply(lambda d: sum(len(v or []) for v in _as_dict(d).values()))
    df["total_matched"] = df[out_summary_col].apply(lambda s: s["total_matched_elements"])
    df["match_rate"] = df[out_summary_col].apply(lambda s: s["match_rate"])
    return df

def to_integer(df: pandas.DataFrame, field: str):
    """
    Converts the values in a specified column of a pandas DataFrame to integers, handling various exceptions.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the column in the df DataFrame to be modified.
    :return: Modified pandas DataFrame with the values converted to integers.
    """
    try:
        df[field] = pandas.to_numeric(df[field], errors="coerce")
        # Replace non-finite values (NaN, inf, -inf) with pd.NA before converting to int64
        df[field] = df[field].where(np.isfinite(df[field]), pandas.NA)
        df[field] = df[field].astype("Int64", copy=False)
    except TypeError as err:
        print(f"TO Integer {field}: Unable to safely cast non-equivalent float to int.")
        numeric_col = pandas.to_numeric(df[field], errors="coerce")
        numeric_col = numeric_col.where(np.isfinite(numeric_col), pandas.NA)
        df[field] = np.floor(numeric_col).astype("Int64")
        print(err)
    except ValueError as err:
        print(
            f"TO Integer {field}: Unable to safely cast float to int due to out-of-range values: {err}"
        )
        numeric_col = pandas.to_numeric(df[field], errors="coerce")
        numeric_col = numeric_col.where(np.isfinite(numeric_col), pandas.NA)
        df[field] = np.floor(numeric_col).astype("Int64")
    except Exception as err:
        print(f"TO Integer {field}: An error occurred during conversion.")
        print(err)
    return df

def to_float(
    df: pandas.DataFrame,
    field: str
) -> pandas.DataFrame:
    """
    Converts the values in a specified column of a pandas DataFrame to floats, handling exceptions.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the column in the df DataFrame to be modified.
    :return: Modified pandas DataFrame with the values converted to floats.
    """
    try:
        df[field] = pandas.to_numeric(df[field], errors="coerce").astype("float64", copy=False)
    except Exception as err:
        print(f"TO Float {field}: An error occurred during conversion.")
        print(err)
    return df


def to_decimal(
    df: pandas.DataFrame,
    field: str,
    symbol: str = "$",
    scale: int = None,
) -> pandas.DataFrame:
    """
    Converts the values in a specified column of a pandas DataFrame to Decimals,
    handling currency strings like '$8,497,188.88'.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the column in the df DataFrame to be modified.
    :param symbol: Currency symbol to remove (default: '$').
    :param scale: Optional number of decimal places to quantize to (e.g. 9 for
                  BigQuery NUMERIC). Prevents 'Rescaling Decimal128 value would
                  cause data loss' errors when the source has floating-point noise.
    :return: Modified pandas DataFrame with the values converted to Decimals.
    """
    quantizer = Decimal(10) ** -scale if scale is not None else None

    def _parse_decimal(value):
        if pandas.isna(value) or value is None:
            return None
        s = str(value).strip()
        if not s:
            return None
        neg = "(" in s or s.startswith("-")
        s = s.replace(symbol, "").replace(",", "").replace("(", "").replace(")", "").replace(" ", "")
        if s.startswith("-"):
            s = s[1:]
        if not s:
            return None
        try:
            d = Decimal(s)
            if quantizer is not None:
                from decimal import ROUND_HALF_UP
                d = d.quantize(quantizer, rounding=ROUND_HALF_UP)
            return -d if neg else d
        except Exception:
            return None

    try:
        df[field] = df[field].apply(_parse_decimal)
    except Exception as err:
        print(f"TO Decimal {field}: An error occurred during conversion.")
        print(err)
    return df


def case_when(
    df: pandas.DataFrame,
    field: str,
    column: str,
    cases: List[Dict[str, Any]],
    default: Any = None,
) -> pandas.DataFrame:
    """
    Apply SQL-like CASE WHEN logic to create a new column based on conditions.

    Emulates SQL syntax like:
        CASE
            WHEN account BETWEEN 40105 AND 40999 THEN 1
            WHEN account BETWEEN 45000 AND 45999 THEN 2
            ...
            ELSE 99
        END AS account_sort

    Parameters:
        df: pandas DataFrame.
        field: Name of the new column to be created.
        column: Name of the column to apply conditions on.
        cases: List of case definitions. Each case is a dict with:
            - 'when': Condition specification (dict with operator and value)
            - 'then': Value to assign when condition is met
        default: Value to assign when no condition is met (default: None).

    Supported condition operators in 'when':
        - between: [min, max] - inclusive range check
        - eq: value - equal to
        - ne: value - not equal to
        - lt: value - less than
        - le: value - less than or equal
        - gt: value - greater than
        - ge: value - greater than or equal
        - in_list: [values...] - check if in list
        - not_in_list: [values...] - check if not in list
        - null: true/false - null check
        - not_null: true/false - not null check

    YAML Example:
        cases:
          - when:
              between: [40105, 40999]
            then: 1
          - when:
              between: [45000, 45999]
            then: 2
          - when:
              ge: 50000
            then: 3
        default: 99

    Example Usage:
        cases = [
            {"when": {"between": [40105, 40999]}, "then": 1},
            {"when": {"between": [45000, 45999]}, "then": 2},
            {"when": {"between": [50100, 50999]}, "then": 3},
        ]
        df = case_when(df, field="account_sort", column="account", cases=cases, default=99)

    Returns:
        DataFrame with the new column added.
    """
    if column not in df.columns:
        print(f"case_when: Column '{column}' not found in DataFrame")
        df[field] = default
        return df

    if not cases:
        print("case_when: No cases provided")
        df[field] = default
        return df

    try:
        col = df[column]
        conditions = []
        choices = []

        for case in cases:
            when_clause = case.get('when', {})
            then_value = case.get('then')

            condition = _build_case_condition(col, when_clause)
            if condition is not None:
                conditions.append(condition)
                choices.append(then_value)

        if conditions:
            df[field] = np.select(conditions, choices, default=default)
        else:
            df[field] = default

        return df

    except Exception as err:
        print(f"Error in case_when for field '{field}': {err}")
        df[field] = default
        return df


def _build_case_condition(
    col: pandas.Series,
    when_clause: Dict[str, Any]
) -> Optional[pandas.Series]:
    """
    Build a boolean condition Series from a 'when' clause specification.

    Parameters:
        col: pandas Series representing the column to evaluate.
        when_clause: Dictionary specifying the condition operator and value.

    Returns:
        pandas Series of boolean values representing the condition.
    """
    if not when_clause:
        return None

    conditions = []

    for operator, value in when_clause.items():
        try:
            if operator == 'between':
                # Expected: [min_val, max_val]
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    min_val, max_val = value
                    conditions.append((col >= min_val) & (col <= max_val))
                else:
                    print(f"case_when: 'between' expects [min, max], got: {value}")

            elif operator == 'eq':
                conditions.append(col == value)

            elif operator == 'ne':
                conditions.append(col != value)

            elif operator == 'lt':
                conditions.append(col < value)

            elif operator == 'le':
                conditions.append(col <= value)

            elif operator == 'gt':
                conditions.append(col > value)

            elif operator == 'ge':
                conditions.append(col >= value)

            elif operator == 'in_list':
                if isinstance(value, (list, tuple)):
                    conditions.append(col.isin(value))
                else:
                    print(f"case_when: 'in_list' expects a list, got: {type(value)}")

            elif operator == 'not_in_list':
                if isinstance(value, (list, tuple)):
                    conditions.append(~col.isin(value))
                else:
                    print(f"case_when: 'not_in_list' expects a list, got: {type(value)}")

            elif operator in ('null', 'is_null'):
                if value:
                    conditions.append(col.isna())
                else:
                    conditions.append(col.notna())

            elif operator in ('not_null', 'is_not_null'):
                if value:
                    conditions.append(col.notna())
                else:
                    conditions.append(col.isna())

            else:
                print(f"case_when: Unknown operator '{operator}'")

        except Exception as err:
            print(f"case_when: Error building condition for '{operator}': {err}")

    # Combine multiple conditions with AND
    if not conditions:
        return None
    elif len(conditions) == 1:
        return conditions[0]
    else:
        result = conditions[0]
        for cond in conditions[1:]:
            result = result & cond
        return result


def md5(df: pandas.DataFrame, field: str, columns: list, separator: str = "|") -> pandas.DataFrame:
    """Compute an MD5 hash of one or more columns and store it in *field*.

    Args:
        df: Input DataFrame.
        field: Target column name for the computed hash.
        columns: List of column names to include in the hash.
        separator: String used to join column values before hashing. Default ``"|"``.

    Returns:
        DataFrame with *field* populated with the hex-digest MD5 string.
    """
    import hashlib

    def _hash_row(row):
        raw = separator.join(
            "" if (v is None or (isinstance(v, float) and pandas.isna(v))) else str(v)
            for v in (row[c] for c in columns)
        )
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    df[field] = df.apply(_hash_row, axis=1)
    return df


def hash_updated_at(
    df: pandas.DataFrame,
    field: str,
    hash_col: str,
    old_hash_col: str,
    old_date_col: str,
) -> pandas.DataFrame:
    """Resolve *updated_at*: use NOW() when the hash changed or is new, keep old date otherwise.

    Args:
        df: Input DataFrame.
        field: Target column name (typically ``updated_at``).
        hash_col: Column with the newly computed content hash.
        old_hash_col: Column with the previously stored hash (may be NaN for new rows).
        old_date_col: Column with the previously stored timestamp.

    Returns:
        DataFrame with *field* set to ``pd.Timestamp.now(tz="UTC")`` for new/changed rows,
        or the existing timestamp for unchanged rows.
    """
    now = pandas.Timestamp.now(tz="UTC")

    def _resolve(row):
        old_hash = row.get(old_hash_col)
        new_hash = row.get(hash_col)
        old_date = row.get(old_date_col)
        if pandas.isna(old_hash) or new_hash != old_hash:
            return now
        return old_date if not pandas.isna(old_date) else now

    df[field] = df.apply(_resolve, axis=1)
    return df

def coalesce(df: pandas.DataFrame, field: str, columns: list = None, column: str = None, match: str = None):
    """
    Mimics the COALESCE function in databases, replacing null values in a specified column
    with values from another column or a specified value.

    :param df: pandas DataFrame to be modified.
    :param field: Name of the column in the df DataFrame to be coalesced.
    :param columns: Optional, list of columns to use for replacing null values sequentially. Defaults to None.
    :param column: Optional, name of the column to use for replacing null values. Defaults to None.
    :param match: Optional, value or function to use for replacing null values. Defaults to None.
    :return: Modified pandas DataFrame with null values replaced.
    """
    def _is_empty(series):
        return series.isnull() | series.apply(lambda x: str(x).strip() == "" if isinstance(x, str) else False)

    if field not in df.columns:
        df[field] = np.nan
        
    if columns:
        try:
            for col in columns:
                if col in df.columns:
                    mask = _is_empty(df[field])
                    df[field] = np.where(mask, df[col], df[field])
        except Exception as err:
            print("COALESCE Error: ", err)
    elif column:
        try:
            if column in df.columns:
                mask = _is_empty(df[field])
                df[field] = np.where(mask, df[column], df[field])
        except Exception as err:
            print("COALESCE Error: ", err)
    elif match:
        # if match is string then:
        if isinstance(match, list):
            # is a function
            fname = match[0]
            args = {}
            result = None
            func = globals()[fname]
            if len(match) > 1:
                args = match[1]
            if callable(func):
                try:
                    result = func(**args)
                except Exception as err:
                    print("Coalesce Error ", err)
                    result = func()
            if result:
                try:
                    df[field] = df[field].fillna(result)
                except Exception as err:
                    print("Coalesce Error ", err)
                    return df
        else:
            df[field] = np.where(df[field].isnull(), match, df[field])
    return df

def formula(
    df: pandas.DataFrame,
    field: str,
    expression: str
) -> pandas.DataFrame:
    """
    Evaluates a mathematical expression or formula string and assigns the result to a specified field.

    :param df: pandas DataFrame to evaluate expression on.
    :param field: Name of the column to store the formula result.
    :param expression: The mathematical expression in string format to evaluate on DataFrame columns.
    :return: Modified pandas DataFrame.
    """
    try:
        # We fillna with 0 for evaluating math correctly with potential null columns
        df[field] = df.fillna(0).eval(expression)
    except Exception as err:
        print(f"Error evaluating formula '{expression}' for field {field}: {err}")
    return df