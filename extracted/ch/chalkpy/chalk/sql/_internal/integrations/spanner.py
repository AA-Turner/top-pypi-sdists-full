from __future__ import annotations

import base64
import json
import os
from typing import TYPE_CHECKING, Any, Dict, Iterable, Mapping, Optional

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pyarrow as pa
    from sqlalchemy.engine import Connection, Engine
    from sqlalchemy.engine.url import URL


_logger = get_logger(__name__)


_SPANNER_PROJECT_NAME = "SPANNER_PROJECT"
_SPANNER_INSTANCE_NAME = "SPANNER_INSTANCE"
_SPANNER_DATABASE_NAME = "SPANNER_DATABASE"
_SPANNER_CREDENTIALS_BASE64_NAME = "SPANNER_CREDENTIALS_BASE64"
_SPANNER_EMULATOR_HOST_NAME = "SPANNER_EMULATOR_HOST"
_SPANNER_ENGINE_ARGUMENTS_NAME = "SPANNER_ENGINE_ARGUMENTS"


class SpannerSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.spanner

    def __init__(
        self,
        name: str | None = None,
        project: str | None = None,
        instance: str | None = None,
        database: str | None = None,
        credentials_base64: str | None = None,
        emulator_host: str | None = None,
        engine_args: Dict[str, Any] | None = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            from google.cloud import sqlalchemy_spanner
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[spanner]")
        del sqlalchemy_spanner  # unused

        self.ingested_tables: Dict[str, Any] = {}
        self.project_id = project or load_integration_variable(
            integration_name=name, name=_SPANNER_PROJECT_NAME, override=integration_variable_override
        )
        self.instance_id = instance or load_integration_variable(
            integration_name=name, name=_SPANNER_INSTANCE_NAME, override=integration_variable_override
        )
        self.database_id = database or load_integration_variable(
            integration_name=name, name=_SPANNER_DATABASE_NAME, override=integration_variable_override
        )
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name=_SPANNER_CREDENTIALS_BASE64_NAME, override=integration_variable_override
        )
        self.emulator_host = emulator_host or load_integration_variable(
            integration_name=name, name=_SPANNER_EMULATOR_HOST_NAME, override=integration_variable_override
        )

        eargs = {}
        if engine_args is not None:
            eargs = engine_args
        else:
            found = load_integration_variable(
                integration_name=name,
                name=_SPANNER_ENGINE_ARGUMENTS_NAME,
                parser=json.loads,
                override=integration_variable_override,
            )
            if found is not None:
                eargs = found

        # The SQL sources are read-only, so transactions are not needed.
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool.
        eargs.setdefault(
            "isolation_level",
            os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"),
        )

        # Spanner defaults to ReadWrite, but Chalk only reads data from spanner.
        eargs.setdefault("read_only", True)

        BaseSQLSource.__init__(self, name=name, engine_args=eargs, async_engine_args={})

    # Spanner does not support using URL, so we need to create the engine directly (rather than using URL)
    def get_engine(self) -> "Engine":
        try:
            from google.auth.credentials import AnonymousCredentials
            from google.cloud import spanner
            from google.oauth2 import service_account
            from sqlalchemy.engine import create_engine
        except ImportError:
            raise missing_dependency_exception("chalkpy[spanner]")

        if self._engine is None:  # pyright: ignore[reportUnnecessaryComparison]
            connect_args = {}

            # Uses workload identity if credentials are not provided
            if self.credentials_base64:
                decoded_credentials = base64.b64decode(self.credentials_base64).decode("utf-8")
                json_acct_info: Dict = json.loads(decoded_credentials)
                credentials = (
                    service_account.Credentials.from_service_account_info(json_acct_info)
                    if not self.emulator_host
                    else AnonymousCredentials()
                )
                connect_args = dict(
                    client=spanner.Client(
                        project=self.project_id,
                        client_options={"api_endpoint": self.emulator_host} if self.emulator_host else None,
                        credentials=credentials,
                    ),
                )
            elif self.emulator_host:
                connect_args = dict(
                    client=spanner.Client(
                        project=self.project_id,
                        client_options={"api_endpoint": self.emulator_host},
                        credentials=AnonymousCredentials(),
                    )
                )

            self._engine = create_engine(
                self.local_engine_url().render_as_string(),  # Spanner adapter does not support URL
                connect_args=connect_args,
            ).execution_options(**self.engine_args)

        return self._engine

    def local_engine_url(self) -> "URL":
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="spanner+spanner",
            host=f"/projects/{self.project_id}/instances/{self.instance_id}",
            database=f"databases/{self.database_id}",
        )

    def get_sqlglot_dialect(self) -> str | None:
        # BigQuery and Spanner have very similar dialects (but not identical)
        return "bigquery"

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_SPANNER_PROJECT_NAME, self.name, self.project_id),
                create_integration_variable(_SPANNER_INSTANCE_NAME, self.name, self.instance_id),
                create_integration_variable(_SPANNER_DATABASE_NAME, self.name, self.database_id),
                create_integration_variable(_SPANNER_CREDENTIALS_BASE64_NAME, self.name, self.credentials_base64),
                create_integration_variable(_SPANNER_EMULATOR_HOST_NAME, self.name, self.emulator_host),
            ]
            if v is not None
        }

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for Spanner and return raw PyArrow RecordBatches."""
        import contextlib

        import pyarrow as pa
        import pyarrow.compute as pc

        # Use existing connection or create new one
        with (self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)) as cnx:
            with cnx.begin():
                # Handle temp tables
                with contextlib.ExitStack() as exit_stack:
                    for (
                        _,
                        temp_value,
                        create_temp_table,
                        temp_table,
                        drop_temp_table,
                    ) in finalized_query.temp_tables.values():
                        exit_stack.enter_context(
                            self._create_temp_table(create_temp_table, temp_table, drop_temp_table, cnx, temp_value)
                        )

                    # Execute query
                    result = cnx.execute(finalized_query.query, finalized_query.params)

                    # Convert result to PyArrow
                    rows = result.fetchall()
                    column_names = result.keys()

                    if not rows:
                        # Return empty batch with expected schema
                        arrays = [pa.nulls(0, field.type) for field in expected_output_schema]
                        batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
                        if query_execution_parameters.yield_empty_batches:
                            yield batch
                        return

                    # Convert rows to column arrays
                    data: dict[str, list[Any]] = {}
                    for i, col_name in enumerate(column_names):
                        col_data = [row[i] for row in rows]
                        data[col_name] = col_data

                    # Create PyArrow table
                    table = pa.table(data)

                    # Map columns to expected schema
                    arrays: list[pa.Array] = []
                    for field in expected_output_schema:
                        if field.name in table.column_names:
                            col = table.column(field.name)
                            # Cast to expected type if needed
                            if col.type != field.type:
                                col = pc.cast(col, field.type)
                            arrays.append(col)
                        else:
                            # Column not found, create null array
                            arrays.append(pa.nulls(len(table), field.type))

                    batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
                    yield batch
