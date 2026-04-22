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

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot._compat import String
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
        SQL/data type name (e.g. ``INTEGER``, ``VARCHAR``).
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


class JdbcPreview(APIObject):
    """
    JDBC data preview API: run SQL against a JDBC URL and get a row-limited preview
    without creating a data store.

    Entry-point class with :meth:`preview` returning a :class:`JdbcPreviewData`.
    """

    _path = "jdbcDataPreview/"

    @classmethod
    def preview(
        cls,
        jdbc_url: str,
        sql: str,
        max_rows: int = 1000,
        parameters: Optional[Dict[str, str]] = None,
    ) -> JdbcPreviewData:
        """
        Preview data from a JDBC URL by executing SQL without creating a data store.

        Executes the given SQL against the JDBC URL and returns a row-limited preview.
        Connection credentials and parameters may be specified in the JDBC URL and/or
        in the ``parameters`` dict (e.g. ``user``, ``password``, ``ssl``, ``timeout``).

        Parameters
        ----------
        jdbc_url : str
            The JDBC URL (e.g. ``jdbc:postgresql://host:5432/dbname``).
        sql : str
            The SQL to execute (e.g. ``SELECT * FROM my_table LIMIT 10``).
        max_rows : int, optional
            Row limit for the preview. Default is 1,000; maximum is 10,000.
        parameters : dict, optional
            Optional connection parameters and credentials as key-value pairs
            (e.g. ``{"user": "u", "password": "p"}``).

        Returns
        -------
        JdbcPreviewData
            Object with ``columns`` (list of column names), ``records`` (list of rows),
            and ``result_schema`` (list of :class:`JdbcResultSchemaEntry`), if returned by the server.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> preview = dr.JdbcPreview.preview(
            ...     jdbc_url='jdbc:postgresql://localhost:5432/mydb',
            ...     sql='SELECT * FROM public.users',
            ...     max_rows=5,
            ...     parameters={'user': 'dbuser', 'password': 'secret'},
            ... )
            >>> preview.columns
            ['id', 'name', 'email']
            >>> len(preview.records)
            5
        """
        payload: Dict[str, Union[str, int, Dict[str, str]]] = {
            "jdbc_url": jdbc_url,
            "sql": sql,
            "max_rows": max_rows,
        }
        if parameters is not None:
            payload["parameters"] = rawdict(parameters)
        response = cls._client.post(
            cls._path,
            data=to_api(payload),
        )
        return JdbcPreviewData.from_server_data(response.json())
