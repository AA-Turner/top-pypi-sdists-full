"""
utils/cleaner.py
----------------
Contains general data cleaning functions for healthcare datasets.
"""

import pandas as pd
import numpy as np


def clean_dates(df, columns):
    """
    Converts columns to datetime, handles invalid formats gracefully.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    print(f"🧹 Cleaned date columns: {columns}")
    return df


def fill_missing(df, strategy="mean"):
    """
    Fills missing numeric values based on chosen strategy (mean, median, zero).
    """
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if strategy == "mean":
            df[col].fillna(df[col].mean(), inplace=True)
        elif strategy == "median":
            df[col].fillna(df[col].median(), inplace=True)
        elif strategy == "zero":
            df[col].fillna(0, inplace=True)
    print(f"🩹 Missing values filled using {strategy} strategy.")
    return df


def standardize_text(df, columns):
    """
    Converts all text columns to lowercase and trims whitespace.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    print(f"🔤 Standardized text columns: {columns}")
    return df
