from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterable, Mapping, Optional, Union

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pyarrow as pa
    import sqlalchemy as sa
    from sqlalchemy.engine import URL, Connection, Engine

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_csv_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_csv_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.Float,
        sa.Integer,
        sa.String,
        sa.Text,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )

_logger = get_logger(__name__)


_TRINO_HOST_NAME = "TRINO_HOST"
_TRINO_PORT_NAME = "TRINO_PORT"
_TRINO_CATALOG_NAME = "TRINO_CATALOG"
_TRINO_SCHEMA_NAME = "TRINO_SCHEMA"
_TRINO_USER_NAME = "TRINO_USER"
_TRINO_PASSWORD_NAME = "TRINO_PASSWORD"


class TrinoSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.trino

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
    ):
        try:
            import trino
        except ImportError:
            raise missing_dependency_exception("chalkpy[trino]")
        del trino
        self.name = name
        self.host = host or load_integration_variable(
            integration_name=name, name=_TRINO_HOST_NAME, override=integration_variable_override
        )

        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                integration_name=name, name=_TRINO_PORT_NAME, parser=int, override=integration_variable_override
            )
        )
        self.catalog = catalog or load_integration_variable(
            integration_name=name, name=_TRINO_CATALOG_NAME, override=integration_variable_override
        )
        self.schema = schema or load_integration_variable(
            integration_name=name, name=_TRINO_SCHEMA_NAME, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            integration_name=name, name=_TRINO_USER_NAME, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            integration_name=name, name=_TRINO_PASSWORD_NAME, override=integration_variable_override
        )
        self.ingested_tables: Dict[str, Any] = {}

        if engine_args is None:
            engine_args = {}

        if name:
            engine_args_from_ui = self._load_env_engine_args(name, override=integration_variable_override)
            for k, v in engine_args_from_ui.items():
                engine_args.setdefault(k, v)

        chalk_default_engine_args = {
            "session_properties": {"query_max_run_time": "1d"},
        }
        for k, v in chalk_default_engine_args.items():
            engine_args.setdefault(k, v)

        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=None)

    def get_sqlglot_dialect(self) -> str | None:
        return "trino"

    def local_engine_url(self) -> URL:
        import trino.sqlalchemy as ts
        from sqlalchemy.engine import make_url

        if self.host is None:
            raise ValueError("Failed to resolve trino required trino host.")

        return make_url(
            ts.URL(
                user=self.user,
                password=self.password,
                # host is checked for None in the constructor
                host=self.host,
                port=self.port,
                catalog=self.catalog,
                schema=self.schema,
            )
        )

    def get_engine(self) -> Engine:
        from sqlalchemy.engine import create_engine

        if self._engine is None:  # pyright: ignore[reportUnnecessaryComparison]
            self.register_sqlalchemy_compiler_overrides()
            self._check_engine_isolation_level()
            self._engine = create_engine(url=self.local_engine_url(), connect_args=self.engine_args)
        return self._engine

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_TRINO_HOST_NAME, self.name, self.host),
                create_integration_variable(_TRINO_PORT_NAME, self.name, self.port),
                create_integration_variable(_TRINO_CATALOG_NAME, self.name, self.catalog),
                create_integration_variable(_TRINO_SCHEMA_NAME, self.name, self.schema),
                create_integration_variable(_TRINO_USER_NAME, self.name, self.user),
                create_integration_variable(_TRINO_PASSWORD_NAME, self.name, self.password),
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
        """Execute query efficiently for Trino and return raw PyArrow RecordBatches."""
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
