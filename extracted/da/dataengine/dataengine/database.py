"""
This module contains the logic associated with the Database class.
"""
import logging
from contextlib import contextmanager
from marshmallow import fields, validates, post_load, ValidationError
import psycopg2
import pymysql
from .assets import AssetSchema, Asset
from .utilities import mysql_utils, postgresql_utils


@contextmanager
def get_cursor(conn):
    """Context manager for database cursor."""
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def execute_query(conn, query, message=None, auto_commit=True):
    """
    Safely execute the given query and log the result.

    Args:
        conn: Database connection object (e.g., psycopg2 or pymysql connection)
        query (str): SQL query string
        message (str): Logging message corresponding to query
        auto_commit (bool): Whether to commit the transaction automatically

    Returns:
        bool: Query success status
    """
    success = True
    try:
        with get_cursor(conn) as cur:
            cur.execute(query)
        if auto_commit:
            conn.commit()
        if message:
            logging.info(f"{message} success.")
    except (psycopg2.DatabaseError, pymysql.MySQLError) as e:
        success = False
        if auto_commit:
            conn.rollback()
        if message:
            logging.error(f"{message} failed.", exc_info=True)
    return success


class DatabaseSchema(AssetSchema):
    """
    Schema for specifying database specs.
    """
    database_type = fields.String(required=True)
    host = fields.String(required=True)
    port = fields.Integer(required=True)
    user = fields.String(required=True)
    password = fields.String(required=True)
    connection_kwargs = fields.Dict(keys=fields.Str(), values=fields.Raw())

    @validates("database_type")
    def validate_database_type(self, database_type, **kwargs):
        """ This function will validate the database type """
        valid_args = ["postgresql", "mysql"]
        if database_type not in valid_args:
            raise ValidationError(
                f"Invalid database_type '{database_type}' provided, "
                "please choose among the list: [{}]".format(
                    ", ".join(valid_args)))

    @post_load
    def create_database(self, input_data, **kwargs):
        return Database(**input_data)


class Database(Asset):
    """
    This class will provide an generic interface layer on top of our database.
    """
    def __init__(
                self,
                asset_name: str,
                dirname: str,
                database_type,
                host,
                port,
                user,
                password,
                connection_kwargs={}
        ):
        """
        Setup database interface arguments.
        """
        super().__init__(asset_name, dirname)
        self.database_type = database_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection_kwargs = connection_kwargs

    def get_connection(self, schema_name):
        """
        This wrapper function will get a database connection.
        """
        if self.database_type == "mysql":
            return mysql_utils.get_connection(
                schema_name, self.host, self.port, self.user, self.password,
                **self.connection_kwargs)
        return postgresql_utils.get_connection(
            schema_name, self.host, self.port, self.user, self.password,
            **self.connection_kwargs)
    
    def truncate(
            self, schema_name, table_name
    ):
        """
        Truncates the specified table in the given schema.

        Args:
            schema_name (str): The name of the schema where the table resides
            table_name (str): The name of the table to be truncated

        Returns:
            bool: True if the table was successfully truncated, False otherwise
        """
        truncate_success = False
        conn = self.get_connection(schema_name)
        try:
            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE TABLE {table_name};")
            conn.commit()
            truncate_success = True
            logging.info(f"Successfully truncated {table_name}")
        except Exception as e:
            logging.error(f"Failed table truncation: {e}")
        
        return truncate_success

    def delete(
            self, schema_name, table_name, delete_all=False, days=None,
            column_header=None):
        """
        This method will delete and optimize a table provided inputs.

        Args:
            schema_name (str): name of database schema
            table_name (str): name of database table
            delete_all (bool): whether to delete all rows
            days (int): number of days out to delete
            column_header (str): header for day filter

        Returns:
            deletion success boolean
        """
        delete_success = False
        # Connect to database
        conn = self.get_connection(schema_name)
        # Construct delete query string
        delete_query = f"DELETE FROM {table_name}"
        if delete_all:
            delete_query += ";"
        elif ((days is not None) and (column_header is not None)):
            delete_query += (
                f" WHERE DATE({column_header}) <= "
                f"CURDATE() - INTERVAL {days} DAY;")
        else:
            logging.error(
                "Either provide delete_all True or both days and column_header")
            return delete_success
        # Add table optimization if load location is Aurora
        if self.database_type == "mysql":
            delete_query += f"\nOPTIMIZE TABLE {table_name};"
        try:
            with conn.cursor() as cur:
                cur.execute(delete_query)
            conn.commit()
            delete_success = True
            logging.info(
                f"Successfully deleted rows beyond {days} days from {table_name}")
        except Exception as e:
            logging.error(f"Failed table deletion: {e}")

        return delete_success

    def load_into(self, schema_name, table_name, s3_location, **kwargs):
        """
        This wrapper function will load data into the database from S3.
        """
        # Connect to database
        conn = self.get_connection(schema_name)
        # TODO: Add connection check here
        # Wrap load data method
        if self.database_type == "mysql":
            success = mysql_utils.load_from_s3(
                conn, table_name, s3_location, **{
                    key: value for key, value in kwargs.items()
                    if key in (
                        "separator", "header", "replace", "header_list")})
        else:
            success = postgresql_utils.load_from_s3(
                conn, table_name, s3_location, **{
                    key: value for key, value in kwargs.items()
                    if key in ("separator", "header", "file_format")})
        # Log either success or failure
        if success:
            logging.info(
                f"Successfully loaded into the {self.asset_name} "
                f"table {schema_name}.{table_name}")
        else:
            logging.error(
                f"Failed loading into the {self.asset_name} "
                f"table {schema_name}.{table_name}")
        # Close connection
        conn.close()

        return success

    def drop_table(self, schema_name: str, table_name: str):
        """
        This method will allow users to drop tables from a database provided
        schema and table names.

        Args:
            schema_name (str): name of database schema
            table_name (str): name of database table            

        Returns:
            success boolean
        """
        # Connect to database
        conn = self.get_connection(schema_name)
        try:
            with conn.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            logging.info(f"Successfully dropped {schema_name}.{table_name}")
            conn.close()
        except Exception as e:
            logging.error(f"Failed to drop table: {e}")
            return False

        return True

    def check_table_existence(
            self, database_name: str, table_name: str,
            schema_name: str = 'public'):
        """
        This method will check whether a table exists in a provided schema.

        Args:
            database_name (str): name of the database
            table_name (str): name of the table
            schema_name (str, optional): name of the schema

        Returns:
            boolean for whether the table exists
        """
        conn = self.get_connection(database_name)
        exists = False
        try:
            with conn.cursor() as cur:
                if self.database_type == "mysql":
                    # MySQL query
                    query = f"SHOW TABLES LIKE '{table_name}'"
                    cur.execute(query)
                    result = cur.fetchone()
                    exists = result is not None
                else:
                    # PostgreSQL / Redshift query
                    query = f"""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables 
                        WHERE table_schema = '{schema_name}' AND
                        table_name = '{table_name}'
                    );
                    """
                    cur.execute(query)
                    result = cur.fetchone()
                    exists = result[0]
        except Exception as e:
            print(f"Error checking table existence: {e}")
        finally:
            conn.close()

        return exists

    def execute_query(self, database_name, query, **kwargs):
        """
        Wrapper function for query execution.
        """
        success = False
        conn = self.get_connection(database_name)
        try:
            success = execute_query(conn, query, **kwargs)
        except Exception as e:
            print(f"Error in Database.execute_query: {e}")
        finally:
            conn.close()
        
        return success
