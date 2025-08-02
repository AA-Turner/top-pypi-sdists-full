# src/canonmap/connectors/mysql_connector/managers/utils/check_existence.py

from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.exceptions import DatabaseManagerError

def check_existence(
    connector: MySQLConnector,
    table: str,
    column: str,
    value: str,
    schema: str = None
) -> bool:
    """
    Check if a value exists in a given table column.

    :param connector: Active MySQLConnector instance.
    :param table: Table name to query.
    :param column: Column name to search.
    :param value: Value to check for.
    :param schema: Optional schema name (e.g., 'information_schema', 'mysql').
    :return: True if value exists, False otherwise.
    """
    try:
        # Build fully qualified table name if schema is given
        table_ref = f"`{schema}`.`{table}`" if schema else f"`{table}`"

        query = f"""
            SELECT COUNT(*) AS count
            FROM {table_ref}
            WHERE `{column}` = %s
        """

        result = connector.run_query(query, (value,))
        return bool(result and result[0]["count"] > 0)

    except Exception as e:
        raise DatabaseManagerError(f"Error checking existence in {table}.{column}: {e}")


def check_table_existence(database_name: str, table_name: str, connector: MySQLConnector) -> bool:
    """
    Check if a table exists in a database.
    
    :param database_name: Name of the database.
    :param table_name: Name of the table.
    :param connector: Active MySQLConnector instance.
    :return: True if table exists, False otherwise.
    """
    try:
        query = """
            SELECT COUNT(*) AS count
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
        """
        result = connector.run_query(query, (database_name, table_name))
        return bool(result and result[0]["count"] > 0)
    except Exception as e:
        raise DatabaseManagerError(f"Error checking table existence: {e}")


def check_database_existence(database_name: str, connector: MySQLConnector) -> bool:
    """
    Check if a database exists.
    
    :param database_name: Name of the database.
    :param connector: Active MySQLConnector instance.
    :return: True if database exists, False otherwise.
    """
    return check_existence(connector, "schemata", "schema_name", database_name, "information_schema")


def check_user_existence(username: str, connector: MySQLConnector) -> bool:
    """
    Check if a user exists.
    
    :param username: Name of the user.
    :param connector: Active MySQLConnector instance.
    :return: True if user exists, False otherwise.
    """
    return check_existence(connector, "user", "User", username, "mysql")