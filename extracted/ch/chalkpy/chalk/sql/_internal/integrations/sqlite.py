from __future__ import annotations

import os
from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, Optional, TypeVar, Union

from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


T = TypeVar("T")


class SQLiteSourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.sqlite

    def __init__(
        self,
        name: Optional[str] = None,
        filename: Optional[Union[PathLike, str]] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
    ):
        self.ingested_tables: Dict[str, Any] = {}
        self.filename = filename
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    def local_engine_url(self) -> URL:
        try:
            from sqlalchemy.engine.url import URL
        except ImportError:
            raise missing_dependency_exception("chalkpy[sqlite]")
        database = ":memory:" if self.filename is None else str(self.filename)
        return URL.create(drivername="sqlite+pysqlite", database=database, query={"check_same_thread": "true"})

    def async_local_engine_url(self) -> URL:
        try:
            from sqlalchemy.engine.url import URL
        except ImportError:
            raise missing_dependency_exception("chalkpy[sqlite]")
        database = ":memory:" if self.filename is None else str(self.filename)
        return URL.create(drivername="sqlite+aiosqlite", database=database, query={"check_same_thread": "true"})

    def get_sqlglot_dialect(self) -> Union[str, None]:
        return "sqlite"

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {}
