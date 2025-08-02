# src/canonmap/connectors/mysql_connector/managers/table_manager/utils/create_table_from_data.py

import logging
from typing import Union
from pathlib import Path
import pandas as pd

from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest, IfExists
from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.connectors.mysql_connector.utils.create_mysql_ddl import create_mysql_ddl
from canonmap.connectors.mysql_connector.managers.table_manager.utils._clean_field_names import clean_field_names
from canonmap.connectors.mysql_connector.utils.check_existence import check_table_existence
from canonmap.exceptions import TableManagerError

logger = logging.getLogger(__name__)

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
    
    # Only create table if not skipping table creation
    if not skip_table_creation:
        ddl_response = create_mysql_ddl(table_name, data)
        
        # Add default primary key if not present in the DDL
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
    else:
        logger.info(f"Skipping table creation for {table_name} (APPEND mode)")
    
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
            
            # Use cleaned column names for INSERT
            original_cols = list(data_list[0].keys())
            cleaned_cols = [col_name_map[col] for col in original_cols]
            cols_sql = ", ".join(f"`{c}`" for c in cleaned_cols)
            ph = ", ".join(["%s"] * len(cleaned_cols))
            total = 0

            # Insert data using executemany for efficiency
            conn = connector.pool.get_connection()
            try:
                cursor = conn.cursor()
                sql = f"INSERT INTO `{table_name}` ({cols_sql}) VALUES ({ph})"
                vals = [tuple(None if pd.isna(row[col]) else row[col] for col in original_cols) for row in data_list]
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
