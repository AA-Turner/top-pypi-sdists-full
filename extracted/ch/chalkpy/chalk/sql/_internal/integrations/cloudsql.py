from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Iterable, Mapping, Optional

from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pyarrow as pa
    from sqlalchemy.engine import Connection
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

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for CloudSQL and return raw PyArrow RecordBatches."""
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
