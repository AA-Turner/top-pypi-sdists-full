"""
utils/deid.py
-------------
Functions for HIPAA-compliant data de-identification and masking.
"""

import hashlib
import pandas as pd


def hash_identifier(value):
    """
    Generates a SHA256 hash for identifiers (e.g., patient_id, ssn).
    """
    if pd.isna(value):
        return None
    return hashlib.sha256(str(value).encode()).hexdigest()[:10]


def mask_phi(df, columns):
    """
    Replaces sensitive fields with hashed identifiers.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(hash_identifier)
    print(f"🔒 Masked PHI fields: {columns}")
    return df


def offset_dates(df, date_columns, offset_days=90):
    """
    Offsets all dates by a fixed number of days for privacy.
    """
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce") + pd.to_timedelta(offset_days, unit="D")
    print(f"📅 Offset dates in columns: {date_columns} by {offset_days} days.")
    return df
