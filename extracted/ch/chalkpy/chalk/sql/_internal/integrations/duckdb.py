from __future__ import annotations

import os
from os import PathLike
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, TypeVar, Union

import duckdb
import pyarrow as pa
from sqlalchemy.engine import Engine

from chalk.features import Feature
from chalk.sql import FinalizedChalkQuery
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL

T = TypeVar("T")


class DuckDBSourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.duckdb

    def __init__(
        self,
        name: Optional[str] = None,
        filename: Optional[Union[PathLike, str]] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        arrow_tables: dict[str, pa.Table] | None = None,
    ):
        self.ingested_tables: Dict[str, Any] = {}
        self.filename = filename
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        if arrow_tables is None:
            arrow_tables = {}

        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args=async_engine_args)
        self.connection = duckdb.connect(":memory:")
        for table in arrow_tables:
            # must be defined here to make the duckdb craziness work.
            t = arrow_tables[table]  # pyright: ignore [reportUnusedVariable]
            self.connection.execute(f"create table {table} as select * from t")

    def get_engine(self) -> Engine:
        try:
            from sqlalchemy import create_engine
        except ImportError:
            raise missing_dependency_exception("chalkpy[duckdb]")
        return create_engine(self.local_engine_url(), **self.engine_args)

    def local_engine_url(self) -> URL:
        try:
            from sqlalchemy.engine.url import URL
        except ImportError:
            raise missing_dependency_exception("chalkpy[duckdb]")
        return URL.create(drivername="duckdb", database=str(self.filename) if self.filename else None)

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Any],  # sqlalchemy.ext.asyncio.AsyncConnection
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        reader = self.connection.query(self.compile_query(finalized_query)[0]).fetch_arrow_reader()

        while True:
            try:
                batch = reader.read_next_batch()
                yield batch
            except StopIteration:
                return

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Any],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for DuckDB and return raw PyArrow RecordBatches."""
        import pyarrow.compute as pc

        query_str, _, _ = self.compile_query(finalized_query)
        reader = self.connection.query(query_str).fetch_arrow_reader()

        while True:
            try:
                batch = reader.read_next_batch()
                # Map columns to expected schema
                if batch.schema != expected_output_schema:
                    # Create mapping from result columns to expected columns
                    arrays: list[pa.Array] = []
                    for field in expected_output_schema:
                        if field.name in batch.schema.names:
                            col = batch.column(field.name)
                            # Cast to expected type if needed
                            if col.type != field.type:
                                col = pc.cast(col, field.type)
                            arrays.append(col)
                        else:
                            # Column not found, create null array
                            arrays.append(pa.nulls(len(batch), field.type))
                    batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
                yield batch
            except StopIteration:
                return

    def supports_inefficient_fallback(self) -> bool:
        return False

    def async_local_engine_url(self) -> URL:
        raise NotImplementedError("DuckDB does not support async connections")

    def get_sqlglot_dialect(self) -> Union[str, None]:
        return "duckdb"

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {}

    def close(self):
        self.connection.close()
