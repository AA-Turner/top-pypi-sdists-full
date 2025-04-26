"""
This module contains utility functions for MySQL Databases.
"""
import os
import psycopg2

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")


def get_connection(schema_name, host, port, user, password, **kwargs):
    """
    This function will establish a database connection.
    """
    return psycopg2.connect(
        dbname=schema_name, host=host, port=port, user=user,
        password=password, **kwargs)


def load_from_s3(
        conn, table_name, s3_location, separator=",", header=True,
        file_format="csv"):
    """
    Loads data from an S3 location into a specified table in a PostgreSQL
    database managed by psycopg2.

    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        table_name (str): Name of the table to which data will be loaded.
        s3_location (str): S3 URI where the data files are stored.
        separator (str, optional): File separator.
          Defaults to ','.
        header (bool, optional): Whether files have a header line.
          Defaults to True.
        file_format (str, optional): Format of the files ("csv" or "parquet").
          Defaults to "csv".

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    # Setup conversion parameters for csv
    # TODO: implement header_info argument into redshift query format
    ignore_header = " IGNOREHEADER 1 " if header else " "
    conversion_params = (
        f"DELIMITER '{separator}'{ignore_header}MAXERROR AS 10000;")
    if file_format == "parquet":
        conversion_params = "FORMAT AS PARQUET MANIFEST;"
    # Fill parameters
    query = f"""
        COPY {table_name}
        FROM '{s3_location}'
        ACCESS_KEY_ID '{S3_ACCESS_KEY}'
        SECRET_ACCESS_KEY '{S3_SECRET_KEY}'
        {conversion_params}
    """
    # Execute query
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        # TODO: Improve logging here by standardizing query execution.
        print(e)
        return False
