from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

_DATABRICKS_HOST_NAME = "DATABRICKS_HOST"
_DATABRICKS_HTTP_PATH_NAME = "DATABRICKS_HTTP_PATH"
_DATABRICKS_TOKEN_NAME = "DATABRICKS_TOKEN"
_DATABRICKS_DATABASE_NAME = "DATABRICKS_DATABASE"
_DATABRICKS_PORT_NAME = "DATABRICKS_PORT"


class DatabricksSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.databricks

    def __init__(
        self,
        host: Optional[str] = None,
        http_path: Optional[str] = None,
        access_token: Optional[str] = None,
        db: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            from databricks import sql
        except ImportError:
            raise missing_dependency_exception("chalkpy[databricks]")
        del sql
        self.host = host or load_integration_variable(
            name=_DATABRICKS_HOST_NAME, integration_name=name, override=integration_variable_override
        )
        self.http_path = http_path or load_integration_variable(
            name=_DATABRICKS_HTTP_PATH_NAME, integration_name=name, override=integration_variable_override
        )
        self.access_token = access_token or load_integration_variable(
            name=_DATABRICKS_TOKEN_NAME, integration_name=name, override=integration_variable_override
        )
        self.db = db or load_integration_variable(
            name=_DATABRICKS_DATABASE_NAME, integration_name=name, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                name=_DATABRICKS_PORT_NAME, integration_name=name, parser=int, override=integration_variable_override
            )
        )
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    def get_sqlglot_dialect(self) -> str | None:
        return "databricks"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="databricks",
            username="token",
            password=self.access_token,
            host=self.host,
            port=self.port,
            database=self.db,
            query={"http_path": self.http_path or ""},
        )

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_DATABRICKS_HOST_NAME, self.name, self.host),
                create_integration_variable(_DATABRICKS_HTTP_PATH_NAME, self.name, self.http_path),
                create_integration_variable(_DATABRICKS_TOKEN_NAME, self.name, self.access_token),
                create_integration_variable(_DATABRICKS_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_DATABRICKS_PORT_NAME, self.name, self.port),
            ]
            if v is not None
        }
