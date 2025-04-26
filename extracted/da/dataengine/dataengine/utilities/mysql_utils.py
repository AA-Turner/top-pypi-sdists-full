"""
This module contains utility functions for MySQL Databases.
"""
import logging
import pymysql
from pymysql.constants import CLIENT


def get_connection(
        schema_name, host, port, user, password, **kwargs):
    """
    Establish a database connection using the provided parameters.

    This function attempts to connect to a MySQL database using the provided
    schema name, host, port, username, and password. It returns the connection
    object if successful; otherwise, it returns None and prints an error
    message.

    Args:
        schema_name (str): The name of the database schema.
        host (str): The hostname of the database server.
        port (int): The port number to connect to the database server.
        user (str): The username to connect to the database.
        password (str): The password for the provided username.

    Returns:
        pymysql.connections.Connection or None: The database connection object
        if successful, or None otherwise.

    Raises:
        This function will catch and handle all exceptions internally,
        therefore it does not raise exceptions itself.

    Examples:
        >>> conn = get_connection(
        >>>     "my_schema", "localhost", 3306, "user", "password")
        >>> type(conn)
        <class 'pymysql.connections.Connection'>
    """
    try:
        connection = pymysql.connect(
            db=schema_name, host=host, port=port, user=user, passwd=password,
            client_flag=CLIENT.MULTI_STATEMENTS, **kwargs)
        return connection
    # Handle operational errors like connection failure, etc.
    except pymysql.OperationalError as oe:
        print(f"Operational Error: {oe}")
        return None
    # Handle programming errors like database not found, etc.
    except pymysql.ProgrammingError as pe:
        print(f"Programming Error: {pe}")
        return None
    # General exception to catch any other errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def load_from_s3(
        conn, table_name, s3_prefix, separator=",", header=True,
        replace=False, header_list=None):
    """
    Load data from an AWS S3 bucket into a MySQL database table.

    This function attempts to load data from a specified S3 prefix into a
    MySQL database table. The S3 dataset is expected to be in CSV format. 
    The function will commit the transaction if successful and rollback in
    case of failure. Errors that occur are logged.

    Args:
        conn (pymysql.connections.Connection): A valid database connection.
        table_name (str): The name of the target database table.
        s3_prefix (str): The S3 prefix where the dataset is stored.
        separator (str, optional): 
            The separator used in the CSV file. 
            Defaults to ','.
        header (bool, optional): 
            Indicates whether the first row of the CSV is a header. 
            Defaults to True.
        replace (bool, optional): 
            If True, existing records in the table will be replaced. 
            Defaults to False.
        header_list (list, optional): 
            An ordered list of header names that match the table columns. 
            Only needed if 'header' is False. 
            Defaults to None.

    Returns:
        bool: True if data loading is successful, otherwise False.

    Note:
        This function is designed to catch and log all exceptions, therefore
        it does not raise exceptions itself.

    Examples:
        >>> conn = pymysql.connect(...)  # Establish a database connection first
        >>> load_from_s3(
        >>>     conn, 'my_table', 's3://my-bucket/data', separator=';',
        >>>     header=True)
        True
    """
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    # Set ignore row string given header boolean
    ignore_rows = "\n    IGNORE 1 ROWS" if header else ""
    replace_rows = "REPLACE " if replace else ""
    # Setup list of headers if applicable
    header_info = ""
    if header_list:
        header_info = "\n({})".format(
            ", ".join([f'`{header}`' for header in header_list]))
    # Fill parameters
    query = f"""
        LOAD DATA FROM S3 PREFIX '{s3_prefix}'
        {replace_rows}INTO TABLE {table_name}
        FIELDS TERMINATED BY '{separator}'{ignore_rows}{header_info};
    """
    # Execute query
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        logging.info(f"Data successfully loaded into {table_name} from {s3_prefix}.")
        return True
    except pymysql.MySQLError as e:
        logging.error(f"MySQL Error: {e}")
        conn.rollback()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        conn.rollback()

    return False
