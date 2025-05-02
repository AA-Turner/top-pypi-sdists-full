from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

_CLICKHOUSE_HOST_NAME = "CLICKHOUSE_HOST"
_CLICKHOUSE_TCP_PORT_NAME = "CLICKHOUSE_TCP_PORT"
_CLICKHOUSE_DATABASE_NAME = "CLICKHOUSE_DATABASE"
_CLICKHOUSE_USER_NAME = "CLICKHOUSE_USER"
_CLICKHOUSE_PWD_NAME = "CLICKHOUSE_PWD"
_CLICKHOUSE_USE_TLS = "CLICKHOUSE_USE_TLS"

# For parsing the USE_TLS flag
_TRUTHY_VALUES = {"1", "true", "yes", "t", "y"}


class ClickhouseSourceImpl(BaseSQLSource, TableIngestMixIn):
    def __init__(
        self,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: Optional[Union[bool, str]] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import clickhouse_driver
            import clickhouse_sqlalchemy
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[clickhouse]")
        del clickhouse_driver
        del clickhouse_sqlalchemy
        self.name = name
        self.host = host or load_integration_variable(
            name=_CLICKHOUSE_HOST_NAME, integration_name=name, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                name=_CLICKHOUSE_TCP_PORT_NAME,
                integration_name=name,
                parser=int,
                override=integration_variable_override,
            )
        )
        self.db = db or load_integration_variable(
            name=_CLICKHOUSE_DATABASE_NAME, integration_name=name, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            name=_CLICKHOUSE_USER_NAME, integration_name=name, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            name=_CLICKHOUSE_PWD_NAME, integration_name=name, override=integration_variable_override
        )
        self.use_tls = (
            use_tls
            if isinstance(use_tls, bool)
            else use_tls in _TRUTHY_VALUES
            if isinstance(use_tls, str)
            else load_integration_variable(
                name=_CLICKHOUSE_USE_TLS,
                integration_name=name,
                override=integration_variable_override,
                parser=lambda x: x in _TRUTHY_VALUES,
            )
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
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)

    kind = SQLSourceKind.clickhouse

    def get_sqlglot_dialect(self) -> str | None:
        return "clickhouse"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="clickhouse+native",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
            query={"secure": "True"} if self.use_tls is not False else {},
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="clickhouse+asynch",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
            query={"secure": "True"} if self.use_tls is not False else {},
        )

    def _recreate_integration_variables(self) -> Dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_CLICKHOUSE_HOST_NAME, self.name, self.host),
                create_integration_variable(_CLICKHOUSE_TCP_PORT_NAME, self.name, self.port),
                create_integration_variable(_CLICKHOUSE_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_CLICKHOUSE_USER_NAME, self.name, self.user),
                create_integration_variable(_CLICKHOUSE_PWD_NAME, self.name, self.password),
            ]
            if v is not None
        }
