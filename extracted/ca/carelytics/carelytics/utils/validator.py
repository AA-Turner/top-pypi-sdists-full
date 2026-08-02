"""
utils/validator.py
------------------
Performs schema validation for healthcare data consistency.
"""

import pandas as pd

   
def validate_columns(df, required_cols):
    """
    Ensures all required columns exist in the DataFrame.
    """
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    else:
        print("✅ All required columns validated.")
    return True
  
def validate_datatypes(df, expected_types):
    """
    Verifies that each column matches the expected data type.
    """
    mismatched = {}
    for col, dtype in expected_types.items():
        if col in df.columns and not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
            mismatched[col] = str(df[col].dtype)
    if mismatched:
        raise TypeError(f"Mismatched data types: {mismatched}")
    print("🧩 Column data types validated successfully.")
    return True
