from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


_CLOUDSQL_INSTANCE_NAME_NAME = "CLOUDSQL_INSTANCE_NAME"
_CLOUDSQL_DATABASE_NAME = "CLOUDSQL_DATABASE"
_CLOUDSQL_USER_NAME = "CLOUDSQL_USER"
_CLOUDSQL_PASSWORD_NAME = "CLOUDSQL_PASSWORD"


class CloudSQLSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.cloudsql

    def __init__(
        self,
        *,
        instance_name: Optional[str] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import psycopg
            import psycopg2
            from sqlalchemy.dialects import registry  # pyright: ignore
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        del psycopg
        if "postgresql.psycopg" not in registry.impls:
            registry.register(
                "postgresql.psycopg", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect"
            )
        if "postgresql.psycopg_async" not in registry.impls:
            registry.register(
                "postgresql.psycopg_async", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect_async"
            )
        self.instance_name = instance_name or load_integration_variable(
            name=_CLOUDSQL_INSTANCE_NAME_NAME, integration_name=name, override=integration_variable_override
        )
        self.db = db or load_integration_variable(
            name=_CLOUDSQL_DATABASE_NAME, integration_name=name, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            name=_CLOUDSQL_USER_NAME, integration_name=name, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            name=_CLOUDSQL_PASSWORD_NAME, integration_name=name, override=integration_variable_override
        )
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        async_engine_args.setdefault("pool_size", 20)
        async_engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    def get_sqlglot_dialect(self) -> str | None:
        return "postgres"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host="",
            query={"host": "{}/{}/.s.PGSQL.5432".format("/cloudsql", self.instance_name)},
            database=self.db,
        )

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_CLOUDSQL_INSTANCE_NAME_NAME, self.name, self.instance_name),
                create_integration_variable(_CLOUDSQL_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_CLOUDSQL_USER_NAME, self.name, self.user),
                create_integration_variable(_CLOUDSQL_PASSWORD_NAME, self.name, self.password),
            ]
            if v is not None
        }
