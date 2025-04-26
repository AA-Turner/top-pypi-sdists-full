from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


_MYSQL_HOST_NAME = "MYSQL_HOST"
_MYSQL_TCP_PORT_NAME = "MYSQL_TCP_PORT"
_MYSQL_DATABASE_NAME = "MYSQL_DATABASE"
_MYSQL_USER_NAME = "MYSQL_USER"
_MYSQL_PWD_NAME = "MYSQL_PWD"


class MySQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import pymysql
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[mysql]")
        del pymysql
        self.name = name
        self.host = host or load_integration_variable(
            name=_MYSQL_HOST_NAME, integration_name=name, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                name=_MYSQL_TCP_PORT_NAME, integration_name=name, parser=int, override=integration_variable_override
            )
        )
        self.db = db or load_integration_variable(
            name=_MYSQL_DATABASE_NAME, integration_name=name, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            name=_MYSQL_USER_NAME, integration_name=name, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            name=_MYSQL_PWD_NAME, integration_name=name, override=integration_variable_override
        )
        self.ingested_tables: Dict[str, Any] = {}
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault("pool_size", 20)
        async_engine_args.setdefault("max_overflow", 60)
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    kind = SQLSourceKind.mysql

    def get_sqlglot_dialect(self) -> str | None:
        return "mysql"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="mysql+pymysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="mysql+aiomysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def _recreate_integration_variables(self) -> Dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_MYSQL_HOST_NAME, self.name, self.host),
                create_integration_variable(_MYSQL_TCP_PORT_NAME, self.name, self.port),
                create_integration_variable(_MYSQL_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_MYSQL_USER_NAME, self.name, self.user),
                create_integration_variable(_MYSQL_PWD_NAME, self.name, self.password),
            ]
            if v is not None
        }
