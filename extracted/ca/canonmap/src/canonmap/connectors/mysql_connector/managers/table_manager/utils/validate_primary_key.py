# src/canonmap/connectors/mysql_connector/managers/table_manager/utils/validate_primary_key.py

import logging
import pandas as pd
from typing import Union
from pathlib import Path

logger = logging.getLogger(__name__)

def validate_primary_key_field(data: Union[str, pd.DataFrame, list, Path], primary_key_field: str) -> bool:
    """
    Validate if a specified field can be used as a primary key by checking if it contains unique values.
    
    Args:
        data: The data source (CSV path, DataFrame, list of dicts, or Path)
        primary_key_field: The name of the field to validate as primary key
        
    Returns:
        bool: True if the field is unique and can be used as primary key, False otherwise
    """
    try:
        # Load data into DataFrame
        if isinstance(data, pd.DataFrame):
            df = data.copy()
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, str) and Path(data).exists():
            df = pd.read_csv(data, na_values=['', 'nan', 'NaN'], keep_default_na=True)
        else:
            logger.error(f"Unsupported data type for primary key validation: {type(data)}")
            return False
        
        # Check if the field exists in the data
        if primary_key_field not in df.columns:
            logger.warning(f"Primary key field '{primary_key_field}' not found in data columns: {list(df.columns)}")
            return False
        
        # Get the values for the primary key field
        pk_values = df[primary_key_field].tolist()
        
        # Check for null/empty values
        null_count = sum(1 for val in pk_values if pd.isna(val) or val is None or val == '')
        if null_count > 0:
            logger.warning(f"Primary key field '{primary_key_field}' contains {null_count} null/empty values")
            return False
        
        # Check for uniqueness
        unique_values = set(pk_values)
        if len(unique_values) != len(pk_values):
            logger.warning(f"Primary key field '{primary_key_field}' is not unique. Found {len(pk_values)} total values but only {len(unique_values)} unique values")
            return False
        
        logger.info(f"Primary key field '{primary_key_field}' is valid and unique")
        return True
        
    except Exception as e:
        logger.error(f"Error validating primary key field '{primary_key_field}': {e}")
        return False 