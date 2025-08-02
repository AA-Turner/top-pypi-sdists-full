# import logging

# from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
# from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import IfExists
# from canonmap.exceptions import TableManagerError

# logger = logging.getLogger(__name__)

# def handle_table_exists(database_name: str, table_name: str, if_exists: IfExists, connector: MySQLConnector, autoconnect: bool) -> None:
#     if if_exists == IfExists.REPLACE:
#         drop_query = f"DROP TABLE {database_name}.{table_name}"
#         try:
#             connector.run_query(drop_query)
#             logger.info(f"Table {table_name} dropped for REPLACE mode.")
#         except Exception as e:
#             logger.error(f"Failed to drop table {table_name}: {e}")
#             raise TableManagerError(f"Failed to drop existing table '{table_name}': {e}")
#     elif if_exists == IfExists.APPEND:
#         logger.info(f"Table {table_name} already exists (APPEND mode); not creating or altering schema.")
#         if autoconnect:
#             connector.connect_to_database(database_name)
#             logger.info(f"Connected to database {database_name}")
#         return  # Do nothing
#     elif if_exists == IfExists.ERROR:
#         logger.warning(f"Table {table_name} already exists and ERROR mode set.")
#         raise TableManagerError(f"Table '{database_name}.{table_name}' already exists (ERROR mode).")
#     elif if_exists == IfExists.SKIP:
#         logger.info(f"Table {table_name} already exists; skipping creation (SKIP mode).")
#         return
    
