# src/canonmap/connectors/mysql_connector/managers/table_manager/utils/create_table_from_data.py

import logging
import re
from typing import Union
from pathlib import Path
import pandas as pd

from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest, IfExists
from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.utils.create_mysql_ddl import create_mysql_ddl
from canonmap.connectors.mysql_connector.managers.table_manager.utils._clean_field_names import clean_field_names
from canonmap.connectors.mysql_connector.managers.table_manager.utils.validate_primary_key import validate_primary_key_field
from canonmap.connectors.mysql_connector.utils.check_existence import check_table_existence
from canonmap.exceptions import TableManagerError

logger = logging.getLogger(__name__)

def _convert_boolean_values(value):
    """
    Convert Yes/No, True/False, Y/N, T/F values to 1/0 for MySQL TINYINT(1) fields.
    
    Args:
        value: The value to convert
        
    Returns:
        int: 1 for True/Yes/Y/T, 0 for False/No/N/F, or the original value if not boolean
    """
    if value is None or pd.isna(value):
        return None
    
    # Convert to string and normalize
    str_val = str(value).strip().lower()
    
    # Boolean true values
    if str_val in {'true', 'yes', 'y', 't', '1'}:
        return 1
    # Boolean false values
    elif str_val in {'false', 'no', 'n', 'f', '0'}:
        return 0
    else:
        # Not a boolean value, return as is
        return value

def _identify_boolean_columns(data):
    """
    Identify columns that contain boolean values (Yes/No, True/False, etc.).
    
    Args:
        data: DataFrame, list of dicts, or file path
        
    Returns:
        set: Set of column names that contain boolean values
    """
    # Load data if it's a file path
    if isinstance(data, str) and Path(data).exists():
        df = pd.read_csv(data, na_values=['', 'nan', 'NaN'], keep_default_na=True)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        return set()
    
    boolean_columns = set()
    missing_values = {"", None, "NULL", "null", "NA", "na", "N/A", "n/a"}
    
    for col in df.columns:
        values = df[col].tolist()
        # Filter out missing placeholders for type inference
        non_null_vals = [v for v in values if v not in missing_values]
        
        if non_null_vals:
            # Check for booleans (true/false, yes/no, 0/1)
            val_set = {str(v).strip().lower() for v in non_null_vals}
            boolean_vals = {"true", "false", "t", "f", "yes", "no", "y", "n", "0", "1"}
            
            # Use the same logic as DDL generation - check if ALL values are boolean-like
            if val_set <= boolean_vals:
                boolean_columns.add(col)
    
    return boolean_columns

def create_table_from_data_util(create_table_request: CreateTableRequest, connector: MySQLConnector, data: Union[str, pd.DataFrame, list, Path]) -> dict:
    database_name = create_table_request.database.name
    table_name = create_table_request.name
    if_exists = create_table_request.if_exists
    autoconnect = create_table_request.autoconnect

    # Connect to the database first
    connector.connect_to_database(database_name)
    
    # Check if table exists and handle according to if_exists parameter
    table_exists = check_table_existence(database_name, table_name, connector)
    skip_table_creation = False
    
    if table_exists:
        if if_exists == IfExists.REPLACE:
            # Drop the existing table for REPLACE mode
            drop_query = f"DROP TABLE {database_name}.{table_name}"
            try:
                connector.run_query(drop_query)
                logger.info(f"Table {table_name} dropped for REPLACE mode.")
            except Exception as e:
                logger.error(f"Failed to drop table {table_name}: {e}")
                raise TableManagerError(f"Failed to drop existing table '{table_name}': {e}")
        elif if_exists == IfExists.APPEND:
            logger.info(f"Table {table_name} already exists (APPEND mode); skipping table creation but will insert data.")
            skip_table_creation = True
        elif if_exists == IfExists.ERROR:
            logger.warning(f"Table {table_name} already exists and ERROR mode set.")
            raise TableManagerError(f"Table '{database_name}.{table_name}' already exists (ERROR mode).")
        elif if_exists == IfExists.SKIP:
            logger.info(f"Table {table_name} already exists; skipping creation entirely (SKIP mode).")
            if autoconnect:
                connector.connect_to_database(database_name)
                logger.info(f"Connected to database {database_name}")
            return {"action": "skipped", "reason": "table_exists", "mode": "skip"}  # Do nothing
    
    # Extract TINYINT(1) columns from DDL for boolean detection (needed for both creation and append modes)
    tinyint_columns = []
    if not skip_table_creation:
        # Handle primary key field validation
        primary_key_field = create_table_request.primary_key_field
        validated_pk_field = None
        
        if primary_key_field:
            logger.info(f"Validating primary key field: {primary_key_field}")
            if validate_primary_key_field(data, primary_key_field):
                validated_pk_field = primary_key_field
                logger.info(f"Using user-specified primary key field: {primary_key_field}")
            else:
                logger.warning(f"Primary key field '{primary_key_field}' is not unique or contains null values. Falling back to auto-increment ID.")
        
        ddl_response = create_mysql_ddl(table_name, data, primary_key_field=validated_pk_field)
        
        # Add default primary key if not present in the DDL and no validated PK field
        ddl = ddl_response.ddl
        logger.info(f"Original DDL: {ddl}")
        
        if "PRIMARY KEY" not in ddl.upper():
            # Find the position of the closing parenthesis
            last_paren_pos = ddl.rfind(")")
            if last_paren_pos != -1:
                # Insert the primary key before the closing parenthesis
                ddl = ddl[:last_paren_pos] + ",\n  `id` INT AUTO_INCREMENT PRIMARY KEY" + ddl[last_paren_pos:]
            logger.info(f"Modified DDL: {ddl}")
        
        connector.run_query(ddl)
        logger.info(f"Table {table_name} created successfully")
        
        # Extract TINYINT(1) columns from the DDL for boolean detection
        for line in ddl.split('\n'):
            if 'TINYINT(1)' in line:
                match = re.search(r'`([^`]+)`\s+TINYINT\(1\)', line)
                if match:
                    tinyint_columns.append(match.group(1))
        logger.info(f"TINYINT(1) columns detected in DDL: {tinyint_columns}")
    else:
        logger.info(f"Skipping table creation for {table_name} (APPEND mode)")
        # For append mode, we still need to detect TINYINT(1) columns from existing table
        # This is a simplified approach - in a real implementation, you might want to query the table schema
    
    # Load and insert data if provided
    if data is not None:
        # Load data from CSV if it's a file path
        if isinstance(data, str) and Path(data).exists():
            df = pd.read_csv(data, na_values=['', 'nan', 'NaN'], keep_default_na=True)
            # Replace NaN with None for MySQL compatibility
            df = df.where(pd.notnull(df), None)
            data_list = df.to_dict('records')
        elif isinstance(data, pd.DataFrame):
            data_list = data.to_dict('records')
        elif isinstance(data, list):
            data_list = data
        else:
            logger.warning(f"Unsupported data type: {type(data)}")
            return {"action": "error", "reason": "unsupported_data_type"}
        
        if data_list:
            # Get the cleaned column names from the DDL response
            # We need to recreate the column mapping to match what was used in DDL creation
            if isinstance(data, str) and Path(data).exists():
                df_for_mapping = pd.read_csv(data, na_values=['', 'nan', 'NaN'], keep_default_na=True)
            elif isinstance(data, pd.DataFrame):
                df_for_mapping = data
            else:
                df_for_mapping = pd.DataFrame(data_list)
            
            # Use the helper function to get column name mapping
            col_name_map = clean_field_names(df_for_mapping.columns.tolist())
            
            # Identify boolean columns that need conversion
            boolean_columns = _identify_boolean_columns(data)
            logger.info(f"Identified boolean columns: {boolean_columns}")
            
            # Fallback: Use DDL-detected boolean columns if automatic detection failed
            if not boolean_columns and tinyint_columns:
                logger.info("Automatic boolean detection found no columns, using DDL-detected TINYINT(1) columns...")
                logger.info(f"Found TINYINT(1) columns in DDL: {tinyint_columns}")
                # Simple approach: just add the DDL-detected columns directly
                for tinyint_col in tinyint_columns:
                    boolean_columns.add(tinyint_col)
                    logger.info(f"Added DDL column '{tinyint_col}' as boolean column")
            
            # Fallback: Check for common boolean column names if still no columns found
            if not boolean_columns:
                logger.info("Still no boolean columns found, checking for common boolean column names...")
                common_boolean_patterns = [
                    'active', 'enabled', 'is_', 'has_', 'needed', 'required', 'warning', 'tag', 'potential'
                ]
                if isinstance(data, list) and len(data) > 0:
                    for col in data[0].keys():
                        col_lower = col.lower()
                        if any(pattern in col_lower for pattern in common_boolean_patterns):
                            logger.info(f"Found potential boolean column by name pattern: {col}")
                            boolean_columns.add(col)
                
                logger.info(f"Final boolean columns after fallback: {boolean_columns}")
            
            # Use cleaned column names for INSERT
            original_cols = list(data_list[0].keys())
            cleaned_cols = [col_name_map[col] for col in original_cols]
            
            # Map boolean columns to their cleaned names
            cleaned_boolean_columns = set()
            for col in boolean_columns:
                if col in col_name_map:
                    cleaned_boolean_columns.add(col_name_map[col])
                    logger.info(f"Boolean column '{col}' mapped to cleaned name '{col_name_map[col]}'")
                else:
                    logger.warning(f"Boolean column '{col}' not found in column name mapping")
            
            cols_sql = ", ".join(f"`{c}`" for c in cleaned_cols)
            ph = ", ".join(["%s"] * len(cleaned_cols))
            total = 0

            # Insert data using executemany for efficiency
            conn = connector.pool.get_connection()
            try:
                cursor = conn.cursor()
                sql = f"INSERT INTO `{table_name}` ({cols_sql}) VALUES ({ph})"
                
                # Convert boolean values before insertion
                vals = []
                for i, row in enumerate(data_list):
                    row_vals = []
                    for j, col in enumerate(original_cols):
                        val = row[col]
                        cleaned_col = cleaned_cols[j]
                        if pd.isna(val):
                            row_vals.append(None)
                        elif cleaned_col in cleaned_boolean_columns:
                            # Convert boolean values to 1/0
                            converted_val = _convert_boolean_values(val)
                            row_vals.append(converted_val)
                        else:
                            row_vals.append(val)
                    vals.append(tuple(row_vals))
                
                cursor.executemany(sql, vals)
                conn.commit()
                total = len(vals)
                cursor.close()
            finally:
                conn.close()
            logger.info(f"Inserted {total} row(s) into '{table_name}'")
            return {"action": "created", "reason": "new_table_with_data", "rows_inserted": total}
        else:
            # No data to insert, but table was created
            return {"action": "created", "reason": "new_table_no_data"}
    else:
        # No data provided, but table was created
        return {"action": "created", "reason": "new_table_no_data"}
