# canonmap/services/artifact_generator/schema/augment_examples.py
# Module for augmenting database schemas with example data

import pandas as pd
import warnings
from typing import List, Dict, Any

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)


def augment_schema_with_examples(
    cleaned_df: pd.DataFrame,
    raw_schema_map: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """
    Enhance each column in the schema with up to 10 example values.
    Properly formats values for MariaDB insertion.

    - Skips any schema entries for columns not present in the DataFrame.
    - If cleaned_df[col] returns multiple columns (duplicate names), takes the first one.
    """
    if not isinstance(cleaned_df, pd.DataFrame):
        raise TypeError("Expected `cleaned_df` to be a pandas DataFrame.")

    augmented_schema: Dict[str, Dict[str, Any]] = {}

    for col, col_info in raw_schema_map.items():
        if col not in cleaned_df.columns:
            warnings.warn(f"Skipping examples for missing column '{col}'")
            continue

        entry = dict(col_info)

        # pull out column(s); handle duplicates by selecting the first
        col_data = cleaned_df[col]
        if isinstance(col_data, pd.DataFrame):
            series = col_data.iloc[:, 0]
        else:
            series = col_data

        # now ensure it's a Series
        if not isinstance(series, pd.Series):
            series = pd.Series(series, name=col)

        # drop nulls before sampling
        series = series.dropna()
        example_list: List[Any] = []

        if not series.empty:
            # take up to 10 unique values
            for v in series.drop_duplicates().head(10):
                if isinstance(v, pd.Timestamp):
                    if col_info.get("data_type") == "DATE":
                        fmt = col_info.get("date_format_in_database") or "%Y-%m-%d"
                        example_list.append(v.strftime(fmt))
                    elif col_info.get("data_type") == "DATETIME":
                        fmt = col_info.get("date_format_in_database") or "%Y-%m-%d %H:%M:%S"
                        example_list.append(v.strftime(fmt))
                    else:
                        example_list.append(str(v))
                elif isinstance(v, pd.Timedelta):
                    example_list.append(str(v))
                else:
                    example_list.append(v)

        entry["example_data"] = example_list
        augmented_schema[col] = entry

    return augmented_schema