from __future__ import annotations

import os
from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, Optional, TypeVar, Union

import duckdb
from sqlalchemy.engine import Engine

from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol

if TYPE_CHECKING:
    import pyarrow as pa
    from sqlalchemy.engine.url import URL

T = TypeVar("T")


class DuckDBSourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.duckdb

    def __init__(
        self,
        name: Optional[str] = None,
        filename: Optional[Union[PathLike, str]] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        arrow_tables: dict[str, pa.Table] | None = None,
    ):
        self.ingested_tables: Dict[str, Any] = {}
        self.filename = filename
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        if arrow_tables is None:
            arrow_tables = {}

        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)
        self.connection = duckdb.connect(":memory:")
        for table in arrow_tables:
            # must be defined here to make the duckdb craziness work.
            t = arrow_tables[table]  # pyright: ignore [reportUnusedVariable]
            self.connection.execute(f"create table {table} as select * from t")

    def get_engine(self) -> Engine:
        raise NotImplementedError("DuckDB does not support async connections")

    def local_engine_url(self) -> URL:
        raise NotImplementedError("DuckDB does not support local_engine_url")
        # try:
        #     from sqlalchemy.engine.url import URL
        # except ImportError:
        #     raise missing_dependency_exception("chalkpy[duckdb]")
        # return URL.create(drivername="duckdb", database=self.file, query={"check_same_thread": "true"})

    def async_local_engine_url(self) -> URL:
        raise NotImplementedError("DuckDB does not support async connections")

    def get_sqlglot_dialect(self) -> Union[str, None]:
        return "duckdb"

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {}

    def close(self):
        self.connection.close()
