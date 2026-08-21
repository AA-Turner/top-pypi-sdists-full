from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterable, Dict, Iterable, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import ChalkQueryProtocol, SQLSourceWithTableIngestProtocol, StringChalkQueryProtocol

if TYPE_CHECKING:
    import pyarrow as pa
    from sqlalchemy.engine import Connection

_MSSQL_HOST_NAME = "MSSQL_HOST"
_MSSQL_TCP_PORT_NAME = "MSSQL_TCP_PORT"
_MSSQL_DATABASE_NAME = "MSSQL_DATABASE"
_MSSQL_USER_NAME = "MSSQL_USER"
_MSSQL_PWD_NAME = "MSSQL_PWD"
_MSSQL_CLIENT_ID_NAME = "MSSQL_CLIENT_ID"
_MSSQL_CLIENT_SECRET_NAME = "MSSQL_CLIENT_SECRET"
_MSSQL_TENANT_ID_NAME = "MSSQL_TENANT_ID"


class MSSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    """MSSQL is queried exclusively through Chalk's native (libchalk) driver.

    This class only carries the connection configuration to the engine, which builds the
    native connection from these attributes. There is no Python (SQLAlchemy/pyodbc) query
    path, so every query method raises `NotImplementedError`, mirroring `DynamoDBSourceImpl`.
    """

    kind = SQLSourceKind.mssql

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
        permission_tags: list[str] | None = None,
    ):
        self.name = name
        self.host = host or load_integration_variable(
            integration_name=name, name=_MSSQL_HOST_NAME, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                integration_name=name, name=_MSSQL_TCP_PORT_NAME, parser=int, override=integration_variable_override
            )
        )
        self.db = db or load_integration_variable(
            integration_name=name, name=_MSSQL_DATABASE_NAME, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            integration_name=name,
            name=_MSSQL_USER_NAME,
            override=integration_variable_override,
        )
        self.password = password or load_integration_variable(
            integration_name=name,
            name=_MSSQL_PWD_NAME,
            override=integration_variable_override,
        )
        self.client_id = client_id or load_integration_variable(
            integration_name=name,
            name=_MSSQL_CLIENT_ID_NAME,
            override=integration_variable_override,
        )
        self.client_secret = client_secret or load_integration_variable(
            integration_name=name,
            name=_MSSQL_CLIENT_SECRET_NAME,
            override=integration_variable_override,
        )
        self.tenant_id = tenant_id or load_integration_variable(
            integration_name=name,
            name=_MSSQL_TENANT_ID_NAME,
            override=integration_variable_override,
        )
        self.ingested_tables: Dict[str, Any] = {}

        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}

        if name:
            engine_args_from_ui = self._load_env_engine_args(name, override=integration_variable_override)
            for k, v in engine_args_from_ui.items():
                engine_args.setdefault(k, v)
                async_engine_args.setdefault(k, v)

        BaseSQLSource.__init__(
            self,
            name=name,
            engine_args=engine_args,
            async_engine_args=async_engine_args,
            permission_tags=permission_tags,
        )

    def get_sqlglot_dialect(self) -> str | None:
        return "tsql"

    def query(self, *args: Any, **kwargs: Any) -> ChalkQueryProtocol:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")

    def query_sql_file(self, *args: Any, **kwargs: Any) -> StringChalkQueryProtocol:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")

    def query_string(self, *args: Any, **kwargs: Any) -> StringChalkQueryProtocol:
        raise NotImplementedError(
            "MSSQL sources cannot be queried in python resolvers directly. Create a sql file resolver to query this source through native sql."
        )

    def execute_query(self, *args: Any, **kwargs: Any) -> Iterable[pa.RecordBatch]:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")

    async def async_execute_query(self, *args: Any, **kwargs: Any) -> AsyncIterable[pa.RecordBatch]:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")
        yield  # noqa: unreachable code

    def _execute_query_inefficient(self, *args: Any, **kwargs: Any) -> pa.RecordBatch:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        raise NotImplementedError("MSSQL sources can only be queried through native sql")
        yield  # noqa: unreachable code

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_MSSQL_HOST_NAME, self.name, self.host),
                create_integration_variable(_MSSQL_TCP_PORT_NAME, self.name, self.port),
                create_integration_variable(_MSSQL_DATABASE_NAME, self.name, self.db),
                create_integration_variable(_MSSQL_USER_NAME, self.name, self.user),
                create_integration_variable(_MSSQL_PWD_NAME, self.name, self.password),
                create_integration_variable(_MSSQL_CLIENT_ID_NAME, self.name, self.client_id),
                create_integration_variable(_MSSQL_CLIENT_SECRET_NAME, self.name, self.client_secret),
                create_integration_variable(_MSSQL_TENANT_ID_NAME, self.name, self.tenant_id),
            ]
            if v is not None
        }
