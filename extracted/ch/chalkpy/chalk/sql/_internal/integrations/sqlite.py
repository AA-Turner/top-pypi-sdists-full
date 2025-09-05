from __future__ import annotations

import os
from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, TypeVar, Union

from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pyarrow as pa
    from sqlalchemy.engine import Connection
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

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for SQLite and return raw PyArrow RecordBatches."""
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

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {}
