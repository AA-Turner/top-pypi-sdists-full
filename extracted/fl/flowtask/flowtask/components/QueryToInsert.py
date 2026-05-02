# -*- coding: utf-8 -*-
from typing import Any
from collections.abc import Callable
import asyncio
from datetime import datetime
from pathlib import PosixPath
from tqdm import tqdm
import orjson
from datamodel.parsers.json import json_encoder
from asyncdb.drivers.postgres import postgres
from asyncdb.exceptions import ProviderError
from ..exceptions import ComponentError
from ..utils import SafeDict
from ..conf import default_dsn
from .flow import FlowComponent


class QueryToInsert(FlowComponent):
    """
    QueryToInsert.


    Overview

        This component allows me to insert data into a database schema

       :widths: auto


    | schema       |   Yes    | Name of the schema where is to the table                          |
    | tablename    |   Yes    | Name of the table in the database                                 |
    | action       |   Yes    | Sets the action to execute in this case an insert                 |
    | pk           |   Yes    | Primary key to the table in the database                          |
    | directory    |   Yes    | Source directory where the file is located                        |
    | filter       |   Yes    | This attribute allows me to apply a filter to the data            |



    Return the list of arbitrary days



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          QueryToInsert:
          schema: public
          tablename: queries
          action: insert
          pk:
          - query_slug
          directory: /home/ubuntu/symbits/
          filter:
          query_slug: walmart_stores
        ```
    """
    _version = "1.0.0"
    """
    QueryToInsert

    Overview

        This component generates SQL INSERT or UPDATE statements from a query and saves them to a file.

    .. table:: Properties
    :widths: auto


    +------------------------+----------+-----------+-------------------------------------------------------+
    | Name                   | Required | Summary                                                           |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | schema                 |   Yes    | The schema of the table to insert or update data in.              |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | tablename              |   Yes    | The name of the table to insert or update data in.                |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | action                 |   Yes    | The action to perform, either "insert" or "update".               |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | pk                     |   Yes    | The primary key(s) of the table.                                  |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | filter                 |   No     | Filters to apply to the query.                                    |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | directory              |   Yes    | The directory to save the SQL file.                               |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | fields                 |   No     | Specific fields to select in the query.                           |
    +------------------------+----------+-----------+-------------------------------------------------------+

    Returns

    This component returns True if the SQL file is successfully created, otherwise raises a ComponentError.
    """
    where = ""
    query = "SELECT {fields} FROM {schema}.{table} {where} order by ctid;"
    insert = "INSERT INTO {}.{} ({}) VALUES({}) {};\n"
    conflict = "ON CONFLICT ({}) DO UPDATE SET {}"
    conflict_update = "{} = EXCLUDED.{}"
    update = "UPDATE {}.{} SET {} {};\n"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.action: str = None
        self.schema: str = ""
        self.tablename: str = ""
        self.pk: Any = None
        self.filter: Any = None
        self._connection: Callable = None
        self._fields = kwargs.pop('fields', [])
        super(QueryToInsert, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def _escapeString(self, value):
        v = value if value != "None" or value is not None else ""
        v = str(v).replace("'", "''") if type(v) == str else v
        v = "'{}'".format(v) if type(v) == str else v
        v = "array{}".format(v) if type(v) == list else v
        return v

    async def start(self, **kwargs):
        """Start."""
        if not hasattr(self, "schema"):
            raise ComponentError("Schema not defined:")
        if not hasattr(self, "tablename"):
            raise ComponentError("Tablename not defined:")
        if not hasattr(self, "action"):
            raise ComponentError("Action not defined:")
        if not hasattr(self, "pk"):
            raise ComponentError("Primary keys not defined:")
        else:
            if isinstance(self.pk, str):
                try:
                    self.pk = orjson.loads(self.pk)
                except Exception:
                    self.pk = self.pk
        if not hasattr(self, "directory"):
            raise ComponentError("Directory not defined:")
        if hasattr(self, "filter"):
            filter = []
            if isinstance(self.filter, str):
                self.filter = orjson.loads(self.filter)
            for key, value in self.filter.items():
                filter.append(
                    "{} = {}".format(
                        key, ("'{}'".format(value) if type(value) == str else value)
                    )
                )
            if len(filter) > 0:
                self.where = "WHERE {}".format(" AND ".join(filter))
        today = datetime.today().strftime("%Y-%m-%d")
        # Create directory if not exists
        try:
            PosixPath(self.directory).mkdir(parents=True, exist_ok=True)
        except Exception as err:
            self.logger.error(f"Error creating directory {self.directory}: {err}")
            raise ComponentError(
                f"Error creating directory {self.directory}: {err}"
            ) from err
        self.filename = PosixPath(
            self.directory,
            "{}_{}_{}.{}.sql".format(today, self.action, self.schema, self.tablename),
        )
        if not self._fields:
            fields = '*'
        else:
            fields = ', '.join(self._fields)
        self.query = self.query.format_map(
            SafeDict(fields=fields)
        )
        self.query = self.query.format(
            schema=self.schema,
            table=self.tablename,
            where=self.where
        )
        self._logger.notice(
            f"Query: {self.query}"
        )
        return True

    async def get_connection(self):
        try:
            self._connection = postgres(dsn=default_dsn, loop=self._loop)
            await self._connection.connection()
        except Exception as err:
            raise ProviderError(f"Error configuring pg Connection: {err!s}") from err
        return self._connection

    async def run(self):
        """Async Method."""
        # get connection
        self._connection = await self.get_connection()
        res, err = await self._connection.query(self.query)
        if err:
            raise ComponentError(
                'Query Error "{}": {}'.format(self.query, err)
            )
        colinfo = self.column_info("{}.{}".format(self.schema, self.tablename))
        if res:
            query = []
            if self.action == "insert":
                total = len(res)
                with tqdm(total=total) as pbar:
                    for row in res:
                        columns_update = row.keys()
                        columns = row.keys()
                        values = []
                        for col in row.keys():
                            values.append(self.get_values(col, colinfo[col], row[col]))
                        update = ", ".join(
                            [self.conflict_update.format(c, c) for c in columns_update]
                        )
                        conflict = self.conflict.format(",\n".join(self.pk), update)
                        query.append(
                            self.insert.format(
                                self.schema,
                                self.tablename,
                                ", ".join(columns),
                                ", ".join(values),
                                conflict,
                            )
                        )
                        pbar.update(1)
            elif self.action == "update":
                for row in res:
                    columns = row.keys()
                    values = []
                    for col in row.keys():
                        values.append(self.get_values(col, colinfo[col], row[col]))
                    vals = dict(zip(list(columns), values))
                    pkwhere = "AND".join(["{}={}".format(v, vals[v]) for v in self.pk])
                    where = (
                        "{} AND {}".format(self.where, pkwhere)
                        if self.where != ""
                        else "WHERE {}".format(pkwhere)
                    )
                    update_list = ["{}={}".format(k, v) for k, v in vals.items()]
                    query.append(
                        self.update.format(
                            self.schema, self.tablename, ", ".join(update_list), where
                        )
                    )

            f = open(self.filename, "w")
            f.write("".join(query))
            f.close()
            self._result = "".join(query)
            self.add_metric('NUM_ROWS', len(query))
            self.add_metric('QUERY', self.query)
            # return self._result
            return True
        else:
            raise ComponentError(
                "Error creating Query File: Empty Result."
            )

    def close(self):
        """Method."""
        pass

    def column_info(self, table):
        result = None
        sql = f"""
        SELECT attname AS column_name, atttypid::regtype AS data_type, attnotnull::boolean as notnull
        FROM pg_attribute WHERE attrelid = '{table}'::regclass AND attnum > 0 AND NOT attisdropped
        ORDER  BY attnum"""
        db = postgres(dsn=default_dsn)
        conn = db.connect()
        result, error = conn.fetchall(sql)
        if error:
            raise ComponentError(f"Error executing query: {error}")
        if result:
            return {item["column_name"]: item["data_type"] for item in result}
        else:
            print(f"The table {self.schema}.{self.tablename} does not exist")
            return None

    def get_values(self, column, type, value):
        if value is None or value == "None":
            return "NULL"
        elif type in [
            "text",
            "character varying",
            "timestamp with time zone",
            "timestamp without time zone",
            "date",
            "uuid",
            "inet",
        ]:
            return "'{}'".format(str(value).replace("'", "''"))
        elif type in ["hstore"]:
            return "'{}'".format(
                ", ".join(
                    [
                        '"{}"=>"{}"'.format(k, v).replace("'", "''")
                        for k, v in value.items()
                    ]
                )
            )
        elif type in ["jsonb"]:
            return "'{}'".format(json_encoder(value).replace("'", "''"))
        elif type in ["character varying[]"]:
            return "'{{{}}}'".format(
                ", ".join(['"{}"'.format(v) for v in value]).replace("'", "''")
            )
        elif type in ["integer[]"]:
            return "'{{{}}}'".format(
                ", ".join([str(v) for v in value]).replace("'", "''")
            )
        else:
            return str(value)
