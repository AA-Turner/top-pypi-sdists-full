#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
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
from typing import Dict, Type

import datetime
import pyarrow
import sqlalchemy
from adbc_driver_flightsql import DatabaseOptions as FlightSQLDatabaseOptions
from adbc_driver_manager import DatabaseOptions as ADBCDatabaseOptions
from sqlalchemy.engine import default, reflection
from sqlalchemy.engine.interfaces import IsolationLevel, DBAPIConnection

import denodo.sqlalchemy.flightsql.context as context
import denodo.sqlalchemy.flightsql.meta as adbc
from denodo.sqlalchemy.flightsql import CONNECT_ARGS_USE_ENCRYPTION
from denodo.sqlalchemy.flightsql import DEFAULT_PORT



_type_map: Dict[int, Type] = {
    pyarrow.lib.Type_BOOL: sqlalchemy.types.BOOLEAN,
    pyarrow.lib.Type_STRING: sqlalchemy.types.VARCHAR,
    pyarrow.lib.Type_INT8: sqlalchemy.types.SMALLINT,
    pyarrow.lib.Type_INT16: sqlalchemy.types.SMALLINT,
    pyarrow.lib.Type_INT32: sqlalchemy.types.INTEGER,
    pyarrow.lib.Type_INT64: sqlalchemy.types.BIGINT,
    pyarrow.lib.Type_FLOAT: sqlalchemy.types.FLOAT,
    pyarrow.lib.Type_DOUBLE: sqlalchemy.types.DOUBLE,
    pyarrow.lib.Type_DECIMAL128: sqlalchemy.types.DECIMAL,
    pyarrow.lib.Type_DECIMAL256: sqlalchemy.types.DECIMAL,
    pyarrow.lib.Type_DATE32: sqlalchemy.types.DATE,
    pyarrow.lib.Type_TIME32: sqlalchemy.types.TIME,
    pyarrow.lib.Type_DATE64: sqlalchemy.types.DATETIME,
    pyarrow.lib.Type_TIMESTAMP: sqlalchemy.types.TIMESTAMP,
    pyarrow.lib.Type_INTERVAL_MONTH_DAY_NANO: sqlalchemy.types.Interval,
    pyarrow.lib.Type_BINARY: sqlalchemy.types.BLOB,
    pyarrow.lib.Type_STRUCT: sqlalchemy.types.VARCHAR,
    pyarrow.lib.Type_LIST: sqlalchemy.types.VARCHAR,
}


class FlightSQLDenodoDialect(default.DefaultDialect):
    name = "denodo"
    driver = "flightsql"
    default_paramstyle = "qmark"
    supports_statement_cache = True
    supports_server_side_cursors = False
    execution_ctx_cls = context.FlightSQLDenodoExecutionContext
    default_isolation_level = "AUTOCOMMIT"


    def __init__(self, **kwargs):
        paramstyle = kwargs.pop("paramstyle", FlightSQLDenodoDialect.default_paramstyle)
        if paramstyle != FlightSQLDenodoDialect.default_paramstyle:
            raise ValueError(f"paramstyle values supported by dialect: {FlightSQLDenodoDialect.default_paramstyle} (was: {paramstyle})")
        default.DefaultDialect.__init__(self, **kwargs)


    def create_connect_args(self, url):
        cparams = url.translate_connect_args(
            username=ADBCDatabaseOptions.USERNAME.value, password=ADBCDatabaseOptions.PASSWORD.value,
            database=f"{FlightSQLDatabaseOptions.RPC_CALL_HEADER_PREFIX.value}database")
        host = cparams.pop("host")
        port = cparams.pop("port") if "port" in cparams else DEFAULT_PORT
        cparams[FlightSQLDatabaseOptions.TLS_SKIP_VERIFY.value] = "false"
        cparams[f"{FlightSQLDatabaseOptions.RPC_CALL_HEADER_PREFIX.value}timePrecision"] = "milliseconds"
        # Returns arguments (host, port) and connection params (opts)
        return [host,port], cparams


    @classmethod
    def import_dbapi(cls):
        import adbc_driver_flightsql.dbapi as dbapi
        return dbapi

    def connect(self, *cargs, **cparams):
        host = cargs[0]
        port = cargs[1]
        use_encryption = (cparams.pop(CONNECT_ARGS_USE_ENCRYPTION, "True").casefold() != "false")
        uri = f"grpc{'+tls' if use_encryption else ''}://{host}:{port}"
        # Transactions are not supported, autocommit will be always set to True
        return self.dbapi.connect(uri=uri, db_kwargs=cparams, autocommit=True)

    def set_isolation_level(self, dbapi_connection: DBAPIConnection, level: IsolationLevel) -> None:
        # Transactions are not supported, the only isolation level allowed is "AUTOCOMMIT"
        if level != "AUTOCOMMIT":
            raise RuntimeError(f"AUTOCOMMIT is the only supported isolation level (trying to set: {level})")
        # No need to set autocommit to True because it will have already been set during connect()
        pass

    def reset_isolation_level(self, dbapi_conn):
        pass

    def do_begin(self, dbapi_connection):
        # Transactions are not supported
        pass

    def do_rollback(self, dbapi_connection):
        # Transactions are not supported
        pass

    def do_commit(self, dbapi_connection):
        # Transactions are not supported
        pass

    def do_close(self, dbapi_connection):
        super().do_close(dbapi_connection)

    @reflection.cache
    def get_schema_names(self, connection, schema=None, **kw):
        schema_meta = adbc.get_schema_meta(connection)
        schema_name = schema_meta["db_schema_name"]
        return [schema_name] if schema_name else []

    @reflection.cache
    def get_table_names(self, connection, schema, **kw):
        tables_info = adbc.get_tables_meta(connection)
        return [t["table_name"] for t in tables_info if t["table_type"] == "TABLE"]

    @reflection.cache
    def has_table(self, connection, table_name, schema=None, **kw):
        table_names = self.get_table_names(connection, schema, **kw)
        return table_name in table_names

    @reflection.cache
    def get_table_oid(self, connection, table_name, schema=None, **kw):
        return table_name

    @reflection.cache
    def get_view_names(self, connection, schema, **kwargs):
        tables_info = adbc.get_tables_meta(connection)
        return [t["table_name"] for t in tables_info if t["table_type"] == "VIEW"]

    @reflection.cache
    def get_columns(self, connection, table_name, schema, **kw):
        schema = adbc.get_table_schema(connection, table_name)
        result = []
        for column in schema:
            col_name = column.name
            col_nullable = column.nullable
            col_arrow_type : pyarrow.DataType = column.type
            col_type = _type_map.get(col_arrow_type.id, None)
            if not col_type:
                raise RuntimeError(f"Unrecognized arrow type: {col_arrow_type}")
            column = {
                "name": col_name,
                "type": col_type,
                "default": None,
                "comment": None,
                "nullable": col_nullable
            }
            result.append(column)
        return result

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        # The Arrow ADBC/FlightSQL driver for Python does not support this yet
        # See https://github.com/apache/arrow-adbc/issues/2222
        return []

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema, **kw):
        # The Arrow ADBC/FlightSQL driver for Python does not support this yet
        # See https://github.com/apache/arrow-adbc/issues/2222
        return []

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema, **kw):
        # The Arrow ADBC/FlightSQL driver for Python does not support this yet
        # See https://github.com/apache/arrow-adbc/issues/2222
        return []

    # Parameterized queries are not supported in Denodo via FlightSQL
    def do_execute(self, cursor, statement, parameters, context=...):
        rep = ( lambda st, value: st.replace('?', value, 1) )
        st = statement
        for v in parameters:
            if v is None:
                st = rep(st, "null")
            elif isinstance(v, (int, float, bool)):
                st = rep(st, str(v))
            elif isinstance(v, datetime.datetime):
                if v.tzinfo:
                    st = rep(st, f"TIMESTAMP WITH TIME ZONE '{v.isoformat(timespec='milliseconds', sep=' ')}'")
                else:
                    st = rep(st, f"TIMESTAMP '{v.isoformat(timespec='milliseconds', sep=' ')}'")
            elif isinstance(v, datetime.date):
                st = rep(st, f"DATE '{v.isoformat()}'")
            elif isinstance(v, datetime.time):
                if v.tzinfo:
                    st = rep(st, f"TIME WITH TIME ZONE '{v.isoformat(timespec='milliseconds')}'")
                else:
                    st = rep(st, f"TIME '{v.isoformat(timespec='milliseconds')}'")
            else:
                st = rep(st, "'" + str(v).replace("'", "''") + "'")
        super().do_execute_no_params(cursor, st, context)


dialect = FlightSQLDenodoDialect