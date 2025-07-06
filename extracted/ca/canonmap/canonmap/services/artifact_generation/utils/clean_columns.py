# canonmap/services/artifact_generator/ingestion/clean_columns.py
# Module for cleaning and formatting DataFrame columns

import re
from typing import List

import pandas as pd

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)



def clean_and_format_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean and format DataFrame columns by:
    - Converting column names to snake_case
    - Formatting name, email, and phone columns
    - Converting numeric columns to appropriate types
    
    Args:
        df: Input DataFrame to clean
        
    Returns:
        pd.DataFrame: DataFrame with cleaned columns
    """
    cleaned_cols: List[str] = []

    for orig in df.columns:
        cleaned = _clean_column_name(orig)
        cleaned_cols.append(cleaned)

    df = df.rename(columns=dict(zip(df.columns, cleaned_cols)))

    for col in df.columns:
        lower = col.lower()
        dtype_before = df[col].dtypes

        if 'name' in lower:
            df[col] = df[col].astype(str).apply(_format_name)
        elif 'email' in lower:
            df[col] = df[col].astype(str).apply(_format_email)
        elif 'phone' in lower or 'number' in lower:
            df[col] = df[col].astype(str).apply(_format_phone)

        numeric_hints = ['cost', 'price', 'amount', 'total', 'value', 'estimate', 'num', 'qty', 'quantity']
        is_numeric_col = str(dtype_before) == 'object' or any(hint in lower for hint in numeric_hints)
        if is_numeric_col:
            s = df[col].astype(str)
            cleaned_s = (
                s.str.replace(',', '', regex=False)
                    .str.replace('$', '', regex=False)
                    .str.replace('£', '', regex=False)
                    .str.replace('€', '', regex=False)
                    .str.replace('k', '', case=False, regex=False)
                    .str.replace('m', '', case=False, regex=False)
            )
            as_num = pd.to_numeric(cleaned_s, errors='coerce')
            mask = ~s.isna() & (s != '') & (s.str.lower() != 'null')
            if mask.any():
                rate = (~as_num[mask].isna()).mean()
                if rate >= 0.95:
                    df[col] = as_num

    return df



# -----------------------------
# Column name cleaning
# -----------------------------
def _clean_column_name(col: str) -> str:
    col_lower = col.lower()
    col_lower = re.sub(r'[\s\-./]+', '_', col_lower)
    # col_lower = re.sub(r'\d+', lambda m: _number_to_text(m.group()), col_lower)
    col_lower = re.sub(r'[^a-z_]', '', col_lower)
    col_lower = re.sub(r'_+', '_', col_lower)
    col_lower = col_lower.strip('_')
    if not col_lower or not col_lower[0].isalpha():
        col_lower = f"col_{col_lower}"
    return col_lower

# def _number_to_text(s: str) -> str:
#     num_map = {
#         '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
#         '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
#     }
#     return ''.join(num_map.get(ch, ch) for ch in s)



# -----------------------------
# Simple formatters for name/email/phone
# -----------------------------
def _format_name(name: str) -> str:
    return name.strip().title()

def _format_email(email: str) -> str:
    return email.strip().lower()

def _format_phone(phone: str) -> str:
    digits = re.sub(r'\D', '', phone or "")
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 7:
        return f"{digits[:3]}-{digits[3:]}"
    return phone

