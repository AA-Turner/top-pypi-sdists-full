#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Runtime patching for filtering METADATA$ columns from user-visible DataFrame operations.

This module provides monkey-patching functionality to hide METADATA$ columns from
user-facing operations like show(), printSchema(), and the columns property while
keeping them accessible internally for functions like input_file_name().
"""

import functools
from typing import List


def filter_metadata_from_columns(original_method):
    """Decorator to filter METADATA$FILENAME column from DataFrame.columns property."""
    @functools.wraps(original_method)
    def wrapper(self):
        from snowflake.snowpark_connect.relation.read.metadata_utils import METADATA_FILENAME_COLUMN
        columns = original_method(self)
        # Filter out METADATA$FILENAME column from user-visible columns
        return [col for col in columns if col != METADATA_FILENAME_COLUMN]
    return wrapper


def filter_metadata_from_show_string(original_method):
    """Decorator to filter METADATA$FILENAME column from DataFrame._show_string_spark method."""
    @functools.wraps(original_method)
    def wrapper(self, num_rows=20, truncate=True, vertical=False, _spark_column_names=None, _spark_session_tz=None, **kwargs):
        # Get the schema to check for METADATA$FILENAME column
        schema_fields = self.schema.fields if hasattr(self, 'schema') else []
        
        # Check if METADATA$FILENAME exists and filter it efficiently
        from snowflake.snowpark_connect.relation.read.metadata_utils import METADATA_FILENAME_COLUMN
        has_metadata_filename = any(field.name == METADATA_FILENAME_COLUMN for field in schema_fields)
        
        if has_metadata_filename:
            from snowflake.snowpark.functions import col
            from snowflake.snowpark_connect.relation.read.metadata_utils import get_non_metadata_column_names
            
            # Create filtered DataFrame excluding METADATA$FILENAME
            non_metadata_column_names = get_non_metadata_column_names(schema_fields)
            non_metadata_columns = [col(name) for name in non_metadata_column_names]
            
            if non_metadata_columns:
                filtered_df = self.select(non_metadata_columns)
                
                # Filter spark column names if provided
                filtered_spark_columns = None
                if _spark_column_names:
                    filtered_spark_columns = [
                        _spark_column_names[i] for i in range(len(_spark_column_names))
                        if i < len(schema_fields) and schema_fields[i].name != METADATA_FILENAME_COLUMN
                    ]
                
                # Call the original method on the filtered DataFrame
                return original_method(
                    filtered_df, 
                    num_rows=num_rows, 
                    truncate=truncate, 
                    vertical=vertical, 
                    _spark_column_names=filtered_spark_columns, 
                    _spark_session_tz=_spark_session_tz, 
                    **kwargs
                )
        
        # No METADATA$FILENAME column, call original
        return original_method(self, num_rows=num_rows, truncate=truncate, vertical=vertical, 
                              _spark_column_names=_spark_column_names, _spark_session_tz=_spark_session_tz, **kwargs)
    
    return wrapper


def apply_metadata_filtering_patches():
    """Apply runtime patches to hide METADATA$ columns from user-facing operations."""
    try:
        # Patch the Spark Connect DataFrame columns property
        from pyspark.sql.connect.dataframe import DataFrame as ConnectDataFrame
        if hasattr(ConnectDataFrame, 'columns') and not hasattr(ConnectDataFrame.columns.fget, '_metadata_filtered'):
            original_columns = ConnectDataFrame.columns.fget
            filtered_columns = filter_metadata_from_columns(original_columns)
            filtered_columns._metadata_filtered = True
            ConnectDataFrame.columns = property(filtered_columns)
        
        # Patch the Snowpark DataFrame _show_string_spark method
        from snowflake.snowpark.dataframe import DataFrame as SnowparkDataFrame
        if hasattr(SnowparkDataFrame, '_show_string_spark') and not hasattr(SnowparkDataFrame._show_string_spark, '_metadata_filtered'):
            original_show_string = SnowparkDataFrame._show_string_spark
            filtered_show_string = filter_metadata_from_show_string(original_show_string)
            filtered_show_string._metadata_filtered = True
            SnowparkDataFrame._show_string_spark = filtered_show_string
            
        return True
        
    except Exception as e:
        # If patching fails, log but don't break the system
        print(f"Warning: Could not apply metadata filtering patches: {e}")
        return False
