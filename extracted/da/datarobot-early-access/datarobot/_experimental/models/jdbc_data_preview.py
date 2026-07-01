#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, List, Optional, Union, cast

import pandas as pd

from datarobot.models.jdbc_data_preview import JdbcPreview as BaseJdbcPreview
from datarobot.models.jdbc_data_preview import JdbcPreviewData as BaseJdbcPreviewData
from datarobot.models.jdbc_data_preview import JdbcResultSchemaEntry
from datarobot.utils import rawdict, to_api


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _to_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y"}:
            return True
        if normalized in {"false", "0", "no", "n"}:
            return False
    return None


def _to_datetime(value: Any) -> Optional[datetime.datetime]:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
    if not isinstance(value, str):
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _to_date(value: Any) -> Optional[datetime.date]:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        pass
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _to_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


# Map java.sql.Types codes to a per-value converter that normalizes JSON-decoded
# values into the appropriate Python type before DataFrame construction.
_TYPE_INT_CONVERTERS = {
    -7: _to_bool,  # BIT
    -6: _to_int,  # TINYINT
    -5: _to_int,  # BIGINT
    -1: _to_string,  # LONGVARCHAR
    1: _to_string,  # CHAR
    2: _to_float,  # NUMERIC
    3: _to_float,  # DECIMAL
    4: _to_int,  # INTEGER
    5: _to_int,  # SMALLINT
    6: _to_float,  # FLOAT
    7: _to_float,  # REAL
    8: _to_float,  # DOUBLE
    12: _to_string,  # VARCHAR
    16: _to_bool,  # BOOLEAN
    91: _to_date,  # DATE
    92: _to_datetime,  # TIME
    93: _to_datetime,  # TIMESTAMP
    -9: _to_string,  # NVARCHAR
    -15: _to_string,  # NCHAR
    -16: _to_string,  # LONGNVARCHAR
    2013: _to_datetime,  # TIME_WITH_TIMEZONE
    2014: _to_datetime,  # TIMESTAMP_WITH_TIMEZONE
}

# Fallback converters keyed by data type name. Used when type code is missing or unknown.
_TYPE_NAME_CONVERTERS = {
    "BIT": _to_bool,
    "BOOL": _to_bool,
    "BOOLEAN": _to_bool,
    "TINYINT": _to_int,
    "SMALLINT": _to_int,
    "INT": _to_int,
    "INTEGER": _to_int,
    "BIGINT": _to_int,
    "NUMERIC": _to_float,
    "DECIMAL": _to_float,
    "FLOAT": _to_float,
    "REAL": _to_float,
    "DOUBLE": _to_float,
    "CHAR": _to_string,
    "VARCHAR": _to_string,
    "LONGVARCHAR": _to_string,
    "NCHAR": _to_string,
    "NVARCHAR": _to_string,
    "LONGNVARCHAR": _to_string,
    "TEXT": _to_string,
    "DATE": _to_date,
    "TIME": _to_datetime,
    "TIMESTAMP": _to_datetime,
    "DATETIME": _to_datetime,
}


def _get_converter_for_schema(schema_entry: Optional[JdbcResultSchemaEntry]) -> Optional[Callable[[Any], Any]]:
    """Get a converter function for a value based on a JDBC schema for a column."""
    if schema_entry is None:
        return None
    if schema_entry.data_type_int in _TYPE_INT_CONVERTERS:
        return _TYPE_INT_CONVERTERS[schema_entry.data_type_int]
    if schema_entry.data_type is not None and schema_entry.data_type.upper() in _TYPE_NAME_CONVERTERS:
        return _TYPE_NAME_CONVERTERS[schema_entry.data_type.upper()]
    return None


class JdbcPreviewData(BaseJdbcPreviewData):
    """
    Data preview. Contains columns, records, and optional result schema.
    """

    @property
    def df(self) -> pd.DataFrame:
        """
        DataFrame representation of the preview data.
        Best-efforts parsing of records based on the result schema.

        Returns
        -------
        pandas.DataFrame
        """
        if not self.result_schema:
            return pd.DataFrame(self.records, columns=self.columns)

        schema_by_name = {entry.name: entry for entry in self.result_schema}
        converters = {}
        for idx, column_name in enumerate(self.columns):
            schema_entry = schema_by_name.get(column_name)
            if schema_entry is None:
                continue
            converter = _get_converter_for_schema(schema_entry)
            if converter is not None:
                converters[idx] = converter

        if not converters:
            return pd.DataFrame(self.records, columns=self.columns)

        parsed_records = (
            [converters[idx](value) if idx in converters else value for idx, value in enumerate(row)]
            for row in self.records
        )
        return pd.DataFrame(parsed_records, columns=self.columns)


class JdbcPreview(BaseJdbcPreview):
    """
    JDBC data preview API.

    Run SQL against a JDBC URL and get a row-limited preview without creating
    a data store.
    """

    # Message on execute update success
    SUCCESS_MESSAGE = "OK"

    @classmethod
    def preview(
        cls,
        jdbc_url: str,
        sql: str,
        max_rows: int = 1000,
        parameters: Optional[Dict[str, str]] = None,
        bind_parameters: Optional[
            List[Optional[Union[str, int, float, bool, datetime.datetime, datetime.date]]]
        ] = None,
    ) -> JdbcPreviewData:
        """
        Preview data from a JDBC URL by executing SQL without creating a data store.

        Executes the given SQL against the JDBC URL and returns a row-limited preview.
        Connection credentials and parameters may be specified in the JDBC URL and/or
        in the ``parameters`` dict (e.g. ``user``, ``password``, ``ssl``, ``timeout``).

        Parameters
        ----------
        jdbc_url:
            The JDBC URL (e.g. ``jdbc:postgresql://host:5432/dbname``).
        sql:
            The SQL to execute (e.g. ``SELECT * FROM my_table LIMIT 10``).
        max_rows:
            Row limit for the preview. Default is 1,000; maximum is 10,000.
        parameters:
            Optional connection parameters and credentials as key-value pairs
            (e.g. ``{"user": "u", "password": "p"}``).
        bind_parameters:
            List of values to bind to the SQL statement. Each value is bound to
            a `?` placeholder in the SQL statement. Binding is in-order.

        Returns
        -------
        JdbcPreviewData
            Object with ``columns`` (list of column names), ``records`` (list of rows),
            and ``result_schema`` (list of :class:`JdbcResultSchemaEntry`), if returned by the server.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot._experimental.models.jdbc_data_preview import JdbcPreview
            >>> preview = JdbcPreview.preview(
            ...     jdbc_url='jdbc:postgresql://localhost:5432/mydb',
            ...     sql='SELECT * FROM public.users WHERE id = ?',
            ...     max_rows=5,
            ...     parameters={'user': 'dbuser', 'password': 'secret'},
            ...     bind_parameters=[4],
            ... )
            >>> preview.columns
            ['id', 'name', 'email']
            >>> len(preview.records)
            5
        """

        path = "jdbcPreviewQuery/"
        payload = {
            "jdbc_url": jdbc_url,
            "sql": sql,
            "max_rows": max_rows,
            "bind_params": bind_parameters,
        }
        if parameters is not None:
            payload["parameters"] = cast(Dict[str, str], rawdict(parameters))
        response = cls._client.post(path, data=to_api(payload))
        return JdbcPreviewData.from_server_data(response.json())

    @classmethod
    def execute_update(
        cls,
        jdbc_url: str,
        sql: str,
        parameters: Optional[Dict[str, str]] = None,
        bind_parameters: Optional[
            List[Optional[Union[str, int, float, bool, datetime.datetime, datetime.date]]]
        ] = None,
    ) -> str:
        """
        Execute a SQL statement against a JDBC URL without creating a data store. Returns the message from the server.

        Connection credentials and parameters may be specified in the JDBC URL and/or
        in the ``parameters`` dict (e.g. ``user``, ``password``, ``ssl``, ``timeout``).

        Parameters
        ----------
        jdbc_url : str
            The JDBC URL (e.g. ``jdbc:postgresql://host:5432/dbname``).
        sql : str
            The SQL statement to execute (e.g. ``INSERT INTO my_table (id, name) VALUES (1, 'John')``).
        parameters : dict, optional
            Optional connection parameters and credentials as key-value pairs
            (e.g. ``{"user": "u", "password": "p"}``).
        bind_parameters:
            List of values to bind to the SQL statement. Each value is bound to
            a `?` placeholder in the SQL statement. Binding is in-order.

        Returns
        -------
        str
            The message from the server. Returns "OK" if successful.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot._experimental.models.jdbc_data_preview import JdbcPreview
            >>> JdbcPreview.execute_update(
            ...     jdbc_url='jdbc:postgresql://localhost:5432/mydb',
            ...     sql='INSERT INTO my_table (id, name) VALUES (?, ?)',
            ...     parameters={'user': 'dbuser', 'password': 'secret'},
            ...     bind_parameters=[1, 'John'],
            ... )
        """
        path = "jdbcExecution/"
        payload: Dict[str, Any] = {
            "jdbc_url": jdbc_url,
            "sql": sql,
            "bind_params": bind_parameters,
        }
        if parameters is not None:
            payload["parameters"] = cast(Dict[str, str], rawdict(parameters))
        response = cls._client.post(path, data=to_api(payload))
        return response.json().get("message") or ""
