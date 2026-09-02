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
from typing import Any, Callable, Dict, Iterator, List, Optional, Union, cast

import pandas as pd
import trafaret as t

from datarobot._compat import String
from datarobot.enums import DEFAULT_READ_TIMEOUT
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict, to_api

_jdbc_result_schema_entry_schema = t.Dict({
    t.Key("name"): String(),
    t.Key("data_type"): String(),
    t.Key("precision", optional=True): t.Or(t.Int, t.Null()),
    t.Key("scale", optional=True): t.Or(t.Int, t.Null()),
    t.Key("data_type_int", optional=True): t.Or(t.Int, t.Null()),
}).ignore_extra("*")

_jdbc_data_preview_response_schema = t.Dict({
    t.Key("columns"): t.List(String()),
    t.Key("records"): t.List(t.List(t.Any)),
    t.Key("result_schema", optional=True): t.Or(t.List(_jdbc_result_schema_entry_schema), t.Null()),
}).ignore_extra("*")


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


def get_parsed_jdbc_data_records_iter(
    records: List[List[Any]], columns: List[str], result_schema: Optional[List[JdbcResultSchemaEntry]]
) -> Iterator[List[Any]]:
    """Generate parsed JDBC data records from a list of lists of values."""
    if result_schema is None:
        yield from records
        return

    schema_by_name = {entry.name: entry for entry in result_schema}
    converters = {}
    for idx, column_name in enumerate(columns):
        schema_entry = schema_by_name.get(column_name)
        if schema_entry is None:
            continue
        converter = _get_converter_for_schema(schema_entry)
        if converter is not None:
            converters[idx] = converter

    if not converters:
        yield from records
        return

    for row in records:
        yield [converters[idx](value) if idx in converters else value for idx, value in enumerate(row)]


class JdbcResultSchemaEntry(APIObject):
    """
    Column metadata for one column in a JDBC data preview result schema.

    Returned as elements of the ``result_schema`` attribute of :class:`JdbcPreviewData`. Built via
    validation in :class:`JdbcPreviewData`.

    Attributes
    ----------
    name : str
        Column name.
    data_type : str
        SQL/data type name (e.g., ``INTEGER``, ``VARCHAR``).
    precision : int or None
        Optional numeric precision.
    scale : int or None
        Optional numeric scale.
    data_type_int : int or None
        Optional integer code for the data type.
    """

    _converter = _jdbc_result_schema_entry_schema

    def __init__(
        self,
        name: str,
        data_type: str,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
        data_type_int: Optional[int] = None,
    ) -> None:
        self.name = name
        self.data_type = data_type
        self.precision = precision
        self.scale = scale
        self.data_type_int = data_type_int


class JdbcPreviewData(APIObject):
    """
    A JDBC data preview: columns, records, and optional result schema from running
    SQL against a JDBC URL.
    """

    _converter = _jdbc_data_preview_response_schema

    def __init__(
        self,
        columns: List[str],
        records: List[List[Any]],
        result_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.columns = columns
        self.records = records
        self.result_schema = (
            [JdbcResultSchemaEntry.from_data(entry) for entry in result_schema] if result_schema is not None else None
        )

    @property
    def df(self) -> pd.DataFrame:
        """
        DataFrame representation of the preview data.
        Best-efforts parsing of records based on the result schema.

        Returns
        -------
        pandas.DataFrame
        """
        parsed_records = tuple(get_parsed_jdbc_data_records_iter(self.records, self.columns, self.result_schema))
        return pd.DataFrame(parsed_records, columns=self.columns)


class JdbcPreview(APIObject):
    """
    JDBC data preview API.

    Run SQL against a JDBC URL and get a row-limited preview
    without creating a data store.
    """

    _path = "jdbcDataPreview/"

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
        *,
        read_timeout: int = 300,
    ) -> JdbcPreviewData:
        """
        Preview data from a JDBC URL by executing SQL without creating a data store.

        Executes the given SQL against the JDBC URL and returns a row-limited preview.
        Connection credentials and parameters may be specified in the JDBC URL and/or
        in the ``parameters`` dict (e.g., ``user``, ``password``, ``ssl``, ``timeout``).

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
        read_timeout:
            Seconds to wait for the response from the server.

        Returns
        -------
        JdbcPreviewData
            Object with ``columns`` (list of column names), ``records`` (list of rows),
            and ``result_schema`` (list of :class:`JdbcResultSchemaEntry`), if returned by the server.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.jdbc_data_preview import JdbcPreview
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
        response = cls._client.post(path, data=to_api(payload), timeout=(cls._client.connect_timeout, read_timeout))
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
        *,
        read_timeout: int = DEFAULT_READ_TIMEOUT,
    ) -> str:
        """
        Execute a SQL statement against a JDBC URL without creating a data store. Returns the message from the server.

        Connection credentials and parameters may be specified in the JDBC URL and/or
        in the ``parameters`` dict (e.g. ``user``, ``password``, ``ssl``, ``timeout``).

        Parameters
        ----------
        jdbc_url:
            The JDBC URL (e.g. ``jdbc:postgresql://host:5432/dbname``).
        sql:
            The SQL statement to execute (e.g. ``INSERT INTO my_table (id, name) VALUES (1, 'John')``).
        parameters:
            Optional connection parameters and credentials as key-value pairs
            (e.g. ``{"user": "u", "password": "p"}``).
        bind_parameters:
            List of values to bind to the SQL statement. Each value is bound to
            a ``?`` placeholder in the SQL statement. Binding is in-order.
        read_timeout:
            Seconds to wait for the response from the server.

        Returns
        -------
        str
            The message from the server. Returns "OK" if successful.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.jdbc_data_preview import JdbcPreview
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
        response = cls._client.post(path, data=to_api(payload), timeout=(cls._client.connect_timeout, read_timeout))
        return response.json().get("message") or ""
