"""SQLAlchemy dialect backed by the SDK-owned Athena DBAPI adapter."""

import re
from typing import Any, Dict

from sqlalchemy import types
from sqlalchemy.engine.default import DefaultDialect

_TYPE_PATTERN = re.compile(r"^([a-zA-Z]+)(?:\((\d+)(?:,(\d+))?\))?")
_TYPE_MAP = {
    "boolean": types.BOOLEAN,
    "tinyint": types.SMALLINT,
    "smallint": types.SMALLINT,
    "integer": types.INTEGER,
    "int": types.INTEGER,
    "bigint": types.BIGINT,
    "float": types.FLOAT,
    "real": types.FLOAT,
    "double": types.FLOAT,
    "decimal": types.DECIMAL,
    "char": types.CHAR,
    "varchar": types.VARCHAR,
    "string": types.String,
    "date": types.DATE,
    "timestamp": types.TIMESTAMP,
    "binary": types.LargeBinary,
    "varbinary": types.LargeBinary,
    "array": types.JSON,
    "map": types.JSON,
    "struct": types.JSON,
    "row": types.JSON,
    "json": types.JSON,
}


class AthenaDialect(DefaultDialect):
    name = "awsathena"
    driver = "rest"
    default_paramstyle = "named"
    supports_statement_cache = True
    supports_sane_rowcount = True
    supports_sane_multi_rowcount = False
    supports_native_boolean = True
    supports_native_decimal = True
    supports_multivalues_insert = True
    supports_pk_autoincrement = False
    postfetch_lastrowid = False

    @classmethod
    def import_dbapi(cls):
        from . import dbapi

        return dbapi

    def create_connect_args(self, url):
        options: Dict[str, Any] = {}
        if url.host:
            match = re.match(r"^athena\.([a-z0-9-]+)\.amazonaws\.(?:com|com\.cn)$", url.host)
            if match:
                options["region"] = match.group(1)
        if url.database:
            options["schema_name"] = url.database
        options.update(dict(url.query))
        return [], options

    def do_execute(self, cursor, statement, parameters, context=None):
        cursor.execute(statement, parameters or None)

    def do_executemany(self, cursor, statement, parameters, context=None):
        cursor.executemany(statement, parameters)

    def do_rollback(self, dbapi_connection):
        pass

    def do_commit(self, dbapi_connection):
        dbapi_connection.commit()

    def do_close(self, dbapi_connection):
        dbapi_connection.close()

    def _driver(self, connection):
        raw = connection.connection
        return getattr(raw, "driver_connection", raw)

    def _executor(self, connection):
        return self._driver(connection).executor

    def _get_default_schema_name(self, connection):
        return self._driver(connection).schema_name

    def _get_server_version_info(self, connection):
        return (4, 0)

    def get_schema_names(self, connection, **_kw):
        resources = self._executor(connection).get_resources("DATABASE")
        return [resource.name for resource in resources]

    def _table_metadata(self, connection, schema=None):
        driver = self._driver(connection)
        executor = driver.executor
        request = {
            "CatalogName": executor.catalog or "AwsDataCatalog",
            "DatabaseName": schema or driver.schema_name,
            "WorkGroup": executor.work_group,
        }
        items = []
        while True:
            response = executor.client.list_table_metadata(**request)
            items.extend(response.get("TableMetadataList") or [])
            token = response.get("NextToken")
            if not token:
                return items
            request["NextToken"] = token

    def get_table_names(self, connection, schema=None, **_kw):
        table_types = {"EXTERNAL_TABLE", "MANAGED_TABLE", "EXTERNAL", "customer"}
        return [
            item["Name"]
            for item in self._table_metadata(connection, schema)
            if item.get("TableType") in table_types
        ]

    def get_view_names(self, connection, schema=None, **_kw):
        return [
            item["Name"]
            for item in self._table_metadata(connection, schema)
            if item.get("TableType") == "VIRTUAL_VIEW"
        ]

    def get_columns(self, connection, table_name, schema=None, **_kw):
        driver = self._driver(connection)
        executor = driver.executor
        response = executor.client.get_table_metadata(
            CatalogName=executor.catalog or "AwsDataCatalog",
            DatabaseName=schema or driver.schema_name,
            TableName=table_name,
            WorkGroup=executor.work_group,
        )
        metadata = response.get("TableMetadata") or {}
        columns = [(column, False) for column in metadata.get("Columns") or []] + [
            (column, True) for column in metadata.get("PartitionKeys") or []
        ]
        return [
            {
                "name": column["Name"],
                "type": self._column_type(column.get("Type", "string")),
                "nullable": True,
                "default": None,
                "autoincrement": False,
                "comment": column.get("Comment"),
                "dialect_options": {"awsathena_partition": partition},
            }
            for column, partition in columns
        ]

    def has_table(self, connection, table_name, schema=None, **_kw):
        return table_name in self.get_table_names(connection, schema)

    def get_foreign_keys(self, connection, table_name, schema=None, **_kw):
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **_kw):
        return {"name": None, "constrained_columns": []}

    def get_indexes(self, connection, table_name, schema=None, **_kw):
        return []

    @staticmethod
    def _column_type(type_name: str):
        match = _TYPE_PATTERN.match(type_name.strip())
        if not match:
            return types.NullType()
        base, first, second = match.groups()
        type_class = _TYPE_MAP.get(base.lower(), types.NullType)
        if type_class is types.DECIMAL and first:
            return type_class(int(first), int(second or 0))
        if type_class in (types.CHAR, types.VARCHAR) and first:
            return type_class(int(first))
        return type_class()
