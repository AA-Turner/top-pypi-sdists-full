import os
import uuid
from typing import Generator, Any

import pandas
import pandas as pd
from teradataml import DataFrame, copy_to_sql


def to_dataframe(obj: dict | list) -> DataFrame | pandas.DataFrame:
    """
    Converts an object (list or dict) into a Teradata DataFrame.
    Falls back to returning a Pandas DataFrame if the Teradata conversion fails.

    Parameters:
        obj (dict, list): The object from the response to convert.

    Returns:
        teradataml.DataFrame | pandas.DataFrame: Teradata DataFrame if successful, otherwise Pandas DataFrame.
    """
    if obj is None:
        raise ValueError("Response object cannot be None")

    items = []
    if isinstance(obj, dict):
        if not any(isinstance(v, (dict, list)) for v in obj.values()):
            items = [obj]
    elif isinstance(obj, list):
        items = obj
    else:
        raise ValueError(f"Unsupported response_object type: {type(obj)}")

    if not items:
        raise ValueError("No items found in the response object")

    if not isinstance(items[0], dict):
        items = [{"value": item} for item in items]

    _normalized_keys, df_dict = _normalize_dict(items)

    pd_df = pd.DataFrame(df_dict)

    table_name = f"temp_modelops_table_{uuid.uuid4().hex[:8]}"

    try:
        copy_to_sql(pd_df, table_name=table_name, temporary=True)
        df = DataFrame.from_table(table_name)
        return df

    except Exception as e:
        print(f"[Fallback] Teradata DataFrame creation failed: {e}")
        print("[Fallback] Returning pandas DataFrame instead.")
        return pd_df


def get_files_in_path(path: str) -> Generator[str, Any, None]:
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def _normalize_dict(items: list) -> tuple[dict, dict]:
    """
    Normalize keys from items and initialize/populate df_dict.

    Returns:
        normalized_keys: mapping original_key -> normalized_key
        df_dict: dict with normalized_key -> list of values per item
    """
    all_keys = set()
    for item in items:
        all_keys.update(item.keys())

    df_dict = {}
    normalized_keys = {}

    for key in all_keys:
        normalized_key = "".join(
            ["_" + c.lower() if c.isupper() else c for c in key]
        ).lstrip("_")
        normalized_keys[key] = normalized_key
        df_dict[normalized_key] = []

    for item in items:
        for original_key in all_keys:
            normalized_key = normalized_keys[original_key]
            df_dict[normalized_key].append(item.get(original_key, None))

    return normalized_keys, df_dict
