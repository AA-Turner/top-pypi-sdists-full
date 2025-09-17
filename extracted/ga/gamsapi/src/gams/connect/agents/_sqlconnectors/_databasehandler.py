#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2025 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2025 GAMS Software GmbH <support@gams.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from gams import transfer as gt

from abc import ABC, abstractmethod
from enum import Enum

import pandas as pd


class ConnectionType(Enum):
    SQLITE = "sqlite"
    PYODBC = "pyodbc"
    SQLALCHEMY = "sqlalchemy"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLSERVER = "sqlserver"
    ACCESS = "access"


class DatabaseConnector(ABC):
    SUPPORTED_INSERT_METHODS = []
    QUOTE_CHAR = []

    def __init__(
        self,
        error_callback: Callable[[str], None],
        printLog_callback: Callable[[str], None],
        trace: int = 0,
    ):
        self._raise_error: Callable[[str], None] = error_callback
        self._traceLog: Callable[[str], None] = printLog_callback
        self._traceValue = trace
        self._engine = None
        self._conn = None

    def validate_insert_method(self, method: str):
        """Checks if the insert method is supported by this handler."""
        if method not in self.SUPPORTED_INSERT_METHODS:
            self._raise_error(
                f"insertMethod >{method}< is not valid for this connection type. "
                f"Valid methods are >{self.SUPPORTED_INSERT_METHODS}<"
            )

    def read_table(self, sql_query: str, read_sql_args: dict) -> pd.DataFrame:
        """
        Read data from select DBMS using the provided SQL Query. Returns a pandas.DataFrame

        Note: All except SQLAlchemy use the same method
        """
        if len(read_sql_args) > 0:
            self._conn.execute(sql_query, read_sql_args)  # type: ignore
        else:
            self._conn.execute(sql_query)  # type: ignore

        return pd.DataFrame.from_records(
            self._conn.fetchall(),  # type: ignore
            columns=[col[0] for col in self._conn.description],  # type: ignore
        )

    def pre_write_procedures(self, **kwargs) -> gt.Container:
        assert (
            "container" in kwargs
        ), ">pre_write_procedures< args must include the container."
        return kwargs["container"]

    def post_write_procedures(self, **kwargs):
        pass

    def write_dataframe(self, df: pd.DataFrame, writeFunction_args: dict):
        """Delegates the write operation."""
        if self._traceValue > 2:
            self._traceLog(f"DataFrame before writing:\n{df}")
        if self._traceValue > 1:
            self._traceLog(f"writeFunction_args: >{writeFunction_args}<")

        self._execute_write(df, writeFunction_args)

    def _execute_write(self, df: pd.DataFrame, writeFunction_args: dict):
        """
        Main function to process the incoming write request.
        Since `SQLAlchemy` and `Access` handle >ifExists< differently,
        this method gets re-implemented in their respective subclasses.

        This method covers the following DBMS: ["PyODBC", "SQLite", "MySQL", "Postgres", "SQLServer"]
        """
        tableName = writeFunction_args["name"]
        schema = writeFunction_args["schema"]
        pyodbc_options = {
            "dtype_map": writeFunction_args["dtype_map"],
            "columnEncloser": writeFunction_args["columnEncloser"],
        }

        if writeFunction_args["if_exists"] == "replace":
            self._create_table(
                df=df,
                tableName=tableName,
                schema=schema,
                ifExists="replace",
                **pyodbc_options,
            )
            self._insert_data(df, writeFunction_args)

        elif writeFunction_args["if_exists"] == "append":
            if self._check_table_exists(tableName=tableName, schema=schema):
                self._insert_data(df, writeFunction_args)
            else:
                self._raise_error(
                    f"Table >{tableName}< does not exist in the database and ifExists is set to >append<."
                )

        elif writeFunction_args["if_exists"] == "fail":
            if not self._check_table_exists(tableName=tableName, schema=schema):
                self._create_table(
                    df=df,
                    tableName=tableName,
                    schema=schema,
                    ifExists="fail",
                    **pyodbc_options,
                )
                self._insert_data(df, writeFunction_args)
            else:
                self._raise_error(
                    f"Table >{tableName}< already exists in the database and ifExists is set to >fail<."
                )

    def rollback(self):
        """
        Method to rollback changes made to the database.
        Common for all but sqlalchemy."""
        self._engine.rollback()  # type: ignore

    def close(self):
        """
        Closes the connection to the database.
        Common for all but sqlalchemy."""
        self._conn.close()  # type: ignore

    def commit(self):
        """
        Commit all the changes made to the database.
        Common for all but sqlalchemy."""
        self._engine.commit()  # type: ignore

    @abstractmethod
    def connect(self, connection_details: dict, connection_args: dict, **kwargs):
        """
        Method to connect to each DBMS with its own library.
        Sets the _engine and _conn attribute.
        """
        pass

    @abstractmethod
    def create_transaction(self):
        """
        Method to start a SQL transaction.
        This helps in rolling back the changes made within a transaction in the event of a failure.
        This is useful when we commit globally once instead of committing each symbol.
        Apart from ["SQLAlchemy", "SQLITE", "Postgres"] other connection start a transaction implicitly.

        connectionType:pythonLibrary
            postgres:pyscopg2, mysql:pymysql, sqlserver:pymssql and pyodbc:pyodbc have autocommit = False by default

        mysql:pymysql
            DDL is autocommitted and as a result all the changes made till then also get committed.

        sqlserver:pymssql,postgres:pyscopg2
            postgres and sqlserver are transaction safe.
            Any change within a transaction does not get committed in case of a failure.

        sqlite:sqlite3
            Creates a blank table for the first symbol. Setting the transaction to begin resolves it.
            This also makes sqlite's behavior different when autocommit is True.
            It does not commit anything even when autocommit is True and failure occurs.

        sqlalchemy:sqlalchemy
            follows the default behavior of specific database
        """
        pass

    @abstractmethod
    def _create_table(
        self,
        df: pd.DataFrame,
        tableName: str,
        schema: str | None,
        ifExists: str,
        **kwargs,
    ) -> None:
        """
        Drops an exisiting table and creates a new table with the same name. Uses specific SQL queries for each DBMS flavour.
        """
        pass

    @abstractmethod
    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        pass

    @abstractmethod
    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict) -> None:
        """Each Database perform their own insert operation"""
        pass

    @staticmethod
    def _strip_escape_chars(tableName: str, quote_chars: list[str]) -> str:
        """
        Helper function to strip an enclosed `tableName`.
        For example, _strip_escape_chars("sqlite", "[new_table]") ==> new_table

        ["mysql","sqlite","access","pyodbc"]:
            These >db_types< are sensitive to the use of escape characters in their SQL queries.
            That is, the query would not find "[new_table]" even if "new_table" exist in the database.

        ["postgres","sqlserver"]:
            These are insensitive to the use of escape characters in the table name.
            The SQL query for both the DBs handle enclosed tableNames efficiently.
        """
        for esc in quote_chars:
            if tableName.startswith(esc[0]) and tableName.endswith(esc[-1]):
                return tableName[1:-1]

        return tableName
