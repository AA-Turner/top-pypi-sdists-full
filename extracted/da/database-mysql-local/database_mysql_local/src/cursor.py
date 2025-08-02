from typing import Any

from logger_local.MetaLogger import MetaLogger
from mysql.connector.cursor import MySQLCursor
from mysql import connector
from .constants_src import LOGGER_CONNECTOR_CODE_OBJECT
# from python_sdk_remote.utilities import our_get_env

# MYSQL_VERSION = our_get_env("MYSQL_VERSION", raise_if_not_found=False)
# TODO Is it the MySQL engine version or the connector version?
MYSQL_VERSION = connector.__version__


# TODO Move this function to a method in DatabaseMysql class. Add this method to the database abstract class
def version_tuple(version):
    return tuple(map(int, version.split(".")))  # Converts "9.2.0" → (9, 2, 0)


class Cursor(metaclass=MetaLogger, object=LOGGER_CONNECTOR_CODE_OBJECT):
    def __init__(self, cursor: MySQLCursor) -> None:
        self.cursor = cursor
        self.__is_closed = False

    # TODO: If environment <> prod1 and dvlp1 break down using 3rd party package and analyze the formatted_sql
    #  and call private method _validate_select_table_name(table_name)
    def execute(self, sql_statement: str, sql_parameters: tuple | list = None, multi: bool = False) -> None:
        # TODO: validate_select_table_name(table_name)
        if sql_parameters:
            quoted_parameters = tuple(
                "'" + str(param) + "'" for param in sql_parameters)
            formatted_sql = sql_statement % quoted_parameters
            sql_parameters_str = ", ".join(quoted_parameters)
        else:
            formatted_sql = sql_statement
            sql_parameters_str = "None"

        formatted_sql = ' '.join(formatted_sql.split())

        self.logger.info(object={
            "formatted_sql": formatted_sql,
            "sql_parameters": sql_parameters_str,
            "sql_statement": sql_statement.replace("\n", " ")
        })
        if MYSQL_VERSION is not None and version_tuple(MYSQL_VERSION) < version_tuple("9.2.0"):
            self.cursor.execute(sql_statement, sql_parameters, multi=multi)
        else:
            self.cursor.execute(sql_statement, sql_parameters)

    def executemany(self, sql_statement: str, sql_parameters: tuple | list = None) -> None:
        try:
            if sql_parameters:  # sql_parameters is list of tuples, each tuple is a row
                sql_parameters_str = [
                    tuple(f'"{param}"' if not isinstance(param, str) else param for param in sql_parameter) for
                    sql_parameter in sql_parameters]
                # Num of placeholders is the same as the num of columns in the table,
                # but there are multiple rows in sql_parameters, so we should add more placeholders before formatting
                sql, values = sql_statement.split("VALUES")
                values = values.strip()
                if not values.startswith("("):
                    values = "(" + values
                if not values.endswith(")"):
                    values = values + ")"
                placeholders = "[" + \
                    ", ".join([values] * len(sql_parameters)) + "]"
                concat_params_tuple = tuple(
                    [param for tup in sql_parameters_str for param in tup])
                formatted_sql = f"{sql} VALUES {placeholders}" % concat_params_tuple
            else:
                formatted_sql = sql_statement
                sql_parameters_str = "None"
            self.logger.info(object={
                "formatted_sql": formatted_sql.replace("\n", " "),
                "sql_parameters": sql_parameters_str,
                "sql_statement": sql_statement.replace("\n", " ")
            })
        except Exception as e:
            self.logger.warning('Unable to format parameters', object={
                "sql_statement": sql_statement,
                "sql_parameters": sql_parameters,
                "error": str(e)
            })

        self.cursor.executemany(sql_statement, sql_parameters)

    def fetchall(self) -> Any:
        result = self.cursor.fetchall()
        return result

    def fetchmany(self, size: int) -> Any:
        result = self.cursor.fetchmany(size)
        return result

    def fetchone(self) -> Any:
        result = self.cursor.fetchone()
        return result

    def description(self) -> list[tuple]:
        """Returns description of columns in a result

        This property returns a list of tuples describing the columns
        in a result set. A tuple is described as follows::

                (column_name,
                 type,
                 None,
                 None,
                 None,
                 None,
                 null_ok,
                 column_flags)  # Addition to PEP-249 specs

        Returns a list of tuples.
        """
        result = self.cursor.description
        return result

    def column_names(self) -> tuple:
        # TODO Please change all result variables to meaningful names i.e. column_names
        result = self.cursor.column_names
        return result

    def lastrowid(self) -> int | None:
        """Returns the value generated for an AUTO_INCREMENT column by the previous INSERT or UPDATE statement."""
        result = self.cursor.lastrowid
        return result

    def get_affected_row_count(self) -> int:
        """Returns the number of rows produced or affected"""
        result = self.cursor.rowcount
        return result

    def get_last_executed_statement(self) -> str:
        result = self.cursor.statement
        return result

    def close(self) -> None:
        if self.__is_closed:
            self.logger.warning('Cursor is already closed')
        try:
            self.cursor.close()
            self.__is_closed = True
        except Exception as exception:
            self.logger.error('Unable to close cursor',
                              object={"exception": exception})

    def is_closed(self) -> bool:
        result = self.__is_closed
        return result
