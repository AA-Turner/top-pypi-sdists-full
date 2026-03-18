#! /usr/bin/python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import re
from typing import Any, Dict, List

from sqlalchemy import log, exc, text, sql, schema as sa_schema
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb
from sqlalchemy.dialects.mysql.base import MySQLDDLCompiler, MySQLTypeCompiler
from sqlalchemy.engine import Connection
from sqlalchemy.sql import sqltypes
from pydoris.sqlalchemy import datatype
from sqlalchemy.sql.sqltypes import Unicode

logger = logging.getLogger(__name__)


class DorisTypeCompiler(MySQLTypeCompiler):
    def _extend_numeric(self, type_, spec):
        # Doris doesn't support UNSIGNED or ZEROFILL
        return spec

    def visit_TINYINT(self, type_, **kw):
        return "TINYINT"

    def visit_LARGEINT(self, type_, **kw):
        return "LARGEINT"

    def visit_DOUBLE(self, type_, **kw):
        return "DOUBLE"

    def visit_HLL(self, type_, **kw):
        return "HLL"

    def visit_BITMAP(self, type_, **kw):
        return "BITMAP"

    def visit_QUANTILE_STATE(self, type_, **kw):
        return "QUANTILE_STATE"

    def visit_AGG_STATE(self, type_, **kw):
        return "AGG_STATE"

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY"

    def visit_MAP(self, type_, **kw):
        return "MAP"

    def visit_STRUCT(self, type_, **kw):
        return "STRUCT"

    def visit_IPV4(self, type_, **kw):
        return "IPV4"

    def visit_IPV6(self, type_, **kw):
        return "IPV6"

    def visit_TIME(self, type_, **kw):
        return "TIME"

    def visit_VARIANT(self, type_, **kw):
        return "VARIANT"


class DorisDDLCompiler(MySQLDDLCompiler):

    def get_column_specification(self, column, **kw):
        # Override to suppress AUTO_INCREMENT — Doris uses different semantics
        spec = super().get_column_specification(column, **kw)
        spec = spec.replace(" AUTO_INCREMENT", "")
        return spec

    def visit_primary_key_constraint(self, constraint, **kw):
        # Doris uses KEY model (DUPLICATE/UNIQUE/AGGREGATE) instead of PRIMARY KEY
        return ""

    def visit_foreign_key_constraint(self, constraint, **kw):
        # Doris doesn't support foreign keys
        return ""

    def visit_unique_constraint(self, constraint, **kw):
        # Doris doesn't support UNIQUE constraints in DDL
        return ""

    def post_create_table(self, table):
        opts = table.dialect_options.get("pydoris", {})
        parts = []

        # ENGINE
        engine = opts.get("engine")
        if engine:
            parts.append("ENGINE = %s" % engine)

        # KEY model — auto-detect from primary key columns if not specified
        key_type = opts.get("key_type")
        key_columns = opts.get("key_columns")
        if not key_columns:
            pk_cols = [c.name for c in table.primary_key.columns]
            if pk_cols:
                key_columns = pk_cols
                if not key_type:
                    key_type = "DUPLICATE"
        if key_type and key_columns:
            preparer = self.preparer
            cols = ", ".join(preparer.quote_identifier(c) for c in key_columns)
            parts.append("%s KEY(%s)" % (key_type, cols))

        # COMMENT
        if table.comment:
            comment = table.comment.replace("'", "\\'")
            parts.append("COMMENT '%s'" % comment)

        # PARTITION BY
        partition_by = opts.get("partition_by")
        if partition_by:
            parts.append(partition_by)

        # DISTRIBUTED BY
        distributed_by = opts.get("distributed_by")
        if distributed_by:
            buckets = opts.get("buckets")
            dist = "DISTRIBUTED BY %s" % distributed_by
            if buckets:
                dist += " BUCKETS %s" % buckets
            parts.append(dist)

        # PROPERTIES
        properties = opts.get("properties")
        if properties and isinstance(properties, dict):
            props = ", ".join('"%s" = "%s"' % (k, v) for k, v in properties.items())
            parts.append("PROPERTIES (%s)" % props)

        if parts:
            return "\n" + "\n".join(parts)
        return ""


@log.class_logger
class DorisDialect(MySQLDialect_mysqldb):
    name = "pydoris"
    supports_statement_cache = True

    type_compiler = DorisTypeCompiler
    ddl_compiler = DorisDDLCompiler

    construct_arguments = [
        (
            sa_schema.Table,
            {
                "engine": None,
                "key_type": None,
                "key_columns": None,
                "distributed_by": None,
                "buckets": None,
                "partition_by": None,
                "properties": None,
            },
        ),
    ]

    def __init__(self, *args, **kw):
        super(DorisDialect, self).__init__(*args, **kw)

    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)

        if schema is None:
            schema = self.default_schema_name

        rs = connection.execute(
            text(
                "SELECT COUNT(*) FROM information_schema.tables WHERE "
                "table_schema = :table_schema AND "
                "table_name = :table_name"
            ).bindparams(
                sql.bindparam("table_schema", type_=Unicode),
                sql.bindparam("table_name", type_=Unicode),
            ),
            {
                "table_schema": str(schema),
                "table_name": str(table_name),
            },
        )
        return bool(rs.scalar())

    def get_schema_names(self, connection, **kw):
        rp = connection.exec_driver_sql("SHOW schemas")
        return [r[0] for r in rp]

    def get_table_names(self, connection, schema=None, **kw):
        """Return a Unicode SHOW TABLES from a given schema."""
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.default_schema_name

        charset = self._connection_charset

        rp = connection.exec_driver_sql(
            "SHOW FULL TABLES FROM %s"
            % self.identifier_preparer.quote_identifier(current_schema)
        )

        return [
            row[0]
            for row in self._compat_fetchall(rp, charset=charset)
            if row[1] == "BASE TABLE"
        ]

    def get_view_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = self.default_schema_name
        charset = self._connection_charset
        rp = connection.exec_driver_sql(
            "SHOW FULL TABLES FROM %s"
            % self.identifier_preparer.quote_identifier(schema)
        )
        return [
            row[0]
            for row in self._compat_fetchall(rp, charset=charset)
            if row[1] in ("VIEW", "SYSTEM VIEW")
        ]

    def get_columns(self, connection: Connection, table_name: str, schema: str = None, **kw) -> List[Dict[str, Any]]:
        if not self.has_table(connection, table_name, schema):
            raise exc.NoSuchTableError(f"schema={schema}, table={table_name}")
        schema = schema or self._get_default_schema_name(connection)

        quote = self.identifier_preparer.quote_identifier
        full_name = quote(table_name)
        if schema:
            full_name = "{}.{}".format(quote(schema), full_name)

        # SHOW COLUMNS returns: Field(0), Type(1), Null(2), Key(3), Default(4), Extra(5)
        res = connection.exec_driver_sql("SHOW COLUMNS FROM %s" % full_name)
        columns = []
        for record in res:
            column = dict(
                name=record[0],
                type=datatype.parse_sqltype(record[1]),
                nullable=record[2] == "YES",
                default=record[4],
            )
            columns.append(column)
        return columns

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return {  # type: ignore  # pep-655 not supported
            "name": None,
            "constrained_columns": [],
        }

    def get_unique_constraints(
            self, connection: Connection, table_name: str, schema: str = None, **kw
    ) -> List[Dict[str, Any]]:
        return []

    def get_check_constraints(
            self, connection: Connection, table_name: str, schema: str = None, **kw
    ) -> List[Dict[str, Any]]:
        return []

    def get_foreign_keys(
            self, connection: Connection, table_name: str, schema: str = None, **kw
    ) -> List[Dict[str, Any]]:
        return []

    def get_primary_keys(self, connection: Connection, table_name: str, schema: str = None, **kw) -> List[str]:
        pk = self.get_pk_constraint(connection, table_name, schema)
        return pk.get("constrained_columns")  # type: ignore

    def get_indexes(self, connection, table_name, schema=None, **kw):
        quote = self.identifier_preparer.quote_identifier
        full_name = quote(table_name)
        if schema:
            full_name = "{}.{}".format(quote(schema), full_name)
        try:
            # SHOW INDEX returns: Table(0), Non_unique(1), Key_name(2),
            # Seq_in_index(3), Column_name(4), ..., Index_type(10), ...
            rs = connection.exec_driver_sql("SHOW INDEX FROM %s" % full_name)
            indexes = {}
            for row in rs:
                index_name = row[2]   # Key_name
                column_name = row[4]  # Column_name
                # Doris may return empty string for Non_unique
                non_unique = row[1]
                is_unique = non_unique == "0" or non_unique == 0
                index_type = row[10] if len(row) > 10 else None
                if index_name not in indexes:
                    indexes[index_name] = {
                        "name": index_name,
                        "column_names": [],
                        "unique": is_unique,
                    }
                    if index_type:
                        indexes[index_name]["type"] = index_type
                indexes[index_name]["column_names"].append(column_name)
            return list(indexes.values())
        except Exception:
            return []

    def has_sequence(self, connection: Connection, sequence_name: str, schema: str = None, **kw) -> bool:
        return False

    def get_sequence_names(self, connection: Connection, schema: str = None, **kw) -> List[str]:
        return []

    def get_temp_view_names(self, connection: Connection, schema: str = None, **kw) -> List[str]:
        return []

    def get_temp_table_names(self, connection: Connection, schema: str = None, **kw) -> List[str]:
        return []

    def get_table_options(self, connection, table_name, schema=None, **kw):
        return {}

    def get_table_comment(self, connection: Connection, table_name: str, schema: str = None, **kw) -> Dict[str, Any]:
        if schema is None:
            schema = self.default_schema_name
        rs = connection.execute(
            text(
                "SELECT table_comment FROM information_schema.tables "
                "WHERE table_schema = :schema AND table_name = :table_name"
            ),
            {"schema": str(schema), "table_name": str(table_name)},
        )
        row = rs.fetchone()
        return {"text": row[0] if row else None}
