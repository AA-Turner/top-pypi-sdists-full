"""Functions for FilterRows."""
import re
import pandas as pd
import numpy as np

def filter_rows_by_column(df: pd.DataFrame, column_source: str, pattern: str, column_destination: str) -> pd.DataFrame:
    """
    Filter rows in a DataFrame by removing rows where column_destination values are found in column_source values.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_source (str): The name of the column to extract values from.
        pattern (str): The regex pattern to match (for string columns) or None for integer columns.
        column_destination (str): The name of the column to check against.

    Returns:
        pd.DataFrame: A DataFrame with rows removed where column_destination values are in column_source values.
    """
    print(f"Filtering rows by column {column_source} with pattern {pattern} and removing from {column_destination}")
    if column_source not in df.columns:
        raise ValueError(f"Column '{column_source}' does not exist in the DataFrame.")
    if column_destination not in df.columns:
        raise ValueError(f"Column '{column_destination}' does not exist in the DataFrame.")

    # Check if columns are numeric (integer/float)
    if pd.api.types.is_numeric_dtype(df[column_source]) and pd.api.types.is_numeric_dtype(df[column_destination]):
        # For numeric columns, extract unique values directly
        values = df[column_source].dropna().unique()
        print(f"Extracted numeric values from {column_source}: {values}")
    else:
        # For string columns, use regex pattern
        values = df[column_source].astype(str).str.extract(pattern)[0].dropna().unique()
        print(f"Extracted string values from {column_source}: {values}")

    # Filter the DataFrame - remove rows where column_destination is in the values
    filtered_df = df[~df[column_destination].isin(values)]
    print(f"Filtered DataFrame: {len(df)} -> {len(filtered_df)} rows")
    return filtered_df
