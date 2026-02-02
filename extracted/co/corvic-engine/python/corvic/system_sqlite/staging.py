"""Sqlite backed staging system."""

import functools
import uuid
from collections.abc import Callable, Iterable, Mapping
from typing import Final

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import sqlglot
import sqlglot._version
import sqlglot.expressions

from corvic.result import InternalError, Ok
from corvic.system import (
    DataKindManager,
    StagingDB,
    StorageManager,
    TableSliceArgs,
    VectorSimilarityMetric,
)

_CORVIC_SIMILARTITY_TO_DUCKDB_SIMILARITY: Final[dict[VectorSimilarityMetric, str]] = {
    "cosine": "cosine",
    "euclidean": "l2sq",
}


def _patch_schema_for_storage(
    new_schema: pa.Schema, old_schema: pa.Schema
) -> pa.Schema:
    """Merge new arrow Schema with an old schema to cast data before storage.

    This merge explicitly avoids casting a non-null column to null,
    which is never a valid cast.
    """
    # TODO(Patrick): handle maps, etc
    patched_schema: list[pa.Field] = []
    for field in new_schema:
        old_field = old_schema.field(field.name)
        if pa.types.is_struct(field.type):
            patched_schema.append(_patch_struct_field(field, old_field))
        elif (
            pa.types.is_list(field.type)
            or pa.types.is_large_list(field.type)
            or pa.types.is_fixed_size_list(field.type)
        ):
            patched_schema.append(_patch_list_field(field, old_field))
        elif not pa.types.is_null(field.type):
            patched_schema.append(field)
        elif old_field and not pa.types.is_null(old_field.type):
            patched_schema.append(field.with_type(old_field.type))
        else:
            patched_schema.append(field)
    return pa.schema(patched_schema, new_schema.metadata)


def _wrap_list_type(
    list_type: pa.ListType | pa.LargeListType | pa.FixedSizeListType,
    list_value_field: pa.Field,
) -> pa.DataType:
    if isinstance(list_type, pa.ListType):
        return pa.list_(value_type=list_value_field)
    if isinstance(list_type, pa.FixedSizeListType):
        return pa.list_(value_type=list_value_field, list_size=list_type.list_size)
    return pa.large_list(value_type=list_value_field)


def _patch_list_field(
    new_field: pa.Field,
    old_field: pa.Field,
) -> pa.Field:
    new_field_type = new_field.type
    old_field_type = old_field.type
    if (
        not old_field
        or not isinstance(
            new_field_type,
            pa.ListType | pa.LargeListType | pa.FixedSizeListType,
        )
        or not isinstance(
            old_field_type,
            pa.ListType | pa.LargeListType | pa.FixedSizeListType,
        )
    ):
        return new_field
    new_list_field = new_field_type.value_field
    old_list_type = old_field_type.value_field.type

    if pa.types.is_struct(new_list_field.type):
        return new_field.with_type(
            _wrap_list_type(
                new_field_type,
                new_field_type.value_field.with_type(
                    _patch_struct_field(
                        new_list_field, new_list_field.with_type(old_list_type)
                    ).type
                ),
            )
        )
    if (
        pa.types.is_list(new_list_field.type)
        or pa.types.is_large_list(new_list_field.type)
        or pa.types.is_fixed_size_list(new_list_field.type)
    ):
        return new_field.with_type(
            _wrap_list_type(
                new_field_type,
                new_field_type.value_field.with_type(
                    _patch_list_field(
                        new_list_field, new_list_field.with_type(old_list_type)
                    ).type
                ),
            )
        )
    if not pa.types.is_null(new_list_field.type):
        return new_field
    return new_field.with_type(
        _wrap_list_type(new_field_type, old_field_type.value_field)
    )


def _patch_struct_field(
    new_field: pa.Field,
    old_field: pa.Field,
) -> pa.Field:
    new_field_type = new_field.type
    if not old_field or not isinstance(new_field_type, pa.StructType):
        return new_field
    old_struct = old_field.type
    if not isinstance(old_struct, pa.StructType):
        return new_field

    patched_nested_fields: list[pa.Field] = []
    for field_index in range(old_struct.num_fields):
        old_nested_field = old_struct.field(field_index)
        field = new_field_type.field(
            new_field_type.get_field_index(old_nested_field.name)
        )
        if pa.types.is_struct(field.type):
            patched_nested_fields.append(
                _patch_struct_field(field, field.with_type(old_nested_field.type))
            )
        elif (
            pa.types.is_list(field.type)
            or pa.types.is_large_list(field.type)
            or pa.types.is_fixed_size_list(field.type)
        ):
            patched_nested_fields.append(
                _patch_list_field(field, field.with_type(old_nested_field.type))
            )
        elif not pa.types.is_null(field.type):
            patched_nested_fields.append(field)
        elif old_nested_field.type and not pa.types.is_null(old_nested_field.type):
            patched_nested_fields.append(field.with_type(old_nested_field.type))
        else:
            patched_nested_fields.append(field)
    return new_field.with_type(pa.struct(patched_nested_fields))


class DuckDBStaging(StagingDB):
    """Access to data staged in a local database like sqlite."""

    _storage_manager: StorageManager
    _db_conn: duckdb.DuckDBPyConnection
    _vector_column_names_to_widths: dict[str, int]

    # Known tables and known row counts. As a DuckDBStaging instance is just
    # one client of possibly many clients of the underlying StorageManager
    # and duckdb instance, these counts are treated as invalidatable state
    # snapshots.
    _table_counts: dict[str, int | None]

    def __init__(
        self,
        storage_manager: StorageManager,
        db_conn: duckdb.DuckDBPyConnection,
        vector_column_names_to_sizes: dict[str, int],
    ):
        self._storage_manager = storage_manager
        self._db_conn = db_conn
        self._vector_column_names_to_widths = vector_column_names_to_sizes
        self._table_counts = {}

    def _get_tables(self) -> set[str]:
        """Returns tables known by duckdb."""
        with self._db_conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name FROM information_schema.tables
                """
            )
            result = cur.fetchall()
        return {r[0] for r in result}

    def _add_vector_indexes(self, table_name: str, raw_table_data: pa.Table):
        table_column_names = raw_table_data.column_names
        for column_name in self.vector_column_names_to_widths:
            if column_name not in table_column_names:
                continue
            for sim_metric in _CORVIC_SIMILARTITY_TO_DUCKDB_SIMILARITY.values():
                self._db_conn.execute(
                    f"""
                    CREATE INDEX '{sim_metric}_idx_{column_name}' ON {table_name}
                        USING HNSW ('{column_name}') WITH (metric = '{sim_metric}')
                    """
                )

    def _setup_vss_extensions(self):
        with self._db_conn.cursor() as cur:
            cur.install_extension("vss")
            cur.load_extension("vss")

    @staticmethod
    def _select_from_union(column_names: list[str], vector_blob_names: list[str]):
        return functools.reduce(
            lambda x, y: x.union(y, distinct=False),
            (
                sqlglot.select(*column_names).from_(
                    sqlglot.table(sqlglot.to_identifier(blob_name, quoted=True))
                )
                for blob_name in vector_blob_names
            ),
        )

    @staticmethod
    def _order_by_func_for_metric(
        vector_column: sqlglot.exp.Column,
        similarity_metric: VectorSimilarityMetric,
        input_vector: list[float],
    ):
        distance_metric = "array_distance"
        descending = False
        if similarity_metric == "cosine":
            # note that this metric will return -1 if the norm of
            # either array is 0
            distance_metric = "array_cosine_similarity"
            descending = True
        fixed_vector_column = sqlglot.exp.TryCast(
            this=vector_column, to=f"FLOAT[{len(input_vector)}]"
        )
        similarity_func = sqlglot.exp.func(
            distance_metric,
            fixed_vector_column,
            # TODO(Hunterlige): Replace column per something more accurate
            # The FLOAT[N] casting is not currently supported by sqlglot
            sqlglot.column(f"{input_vector}::FLOAT[{len(input_vector)}]", quoted=False),
            dialect="duckdb",
        )
        if descending:
            similarity_func = similarity_func.desc()
        return similarity_func

    def _update_blobs_for_prefix(
        self,
        manager: DataKindManager,
        next_count: dict[str, int | None],
        transform_table: Callable[[str, pa.Table], None] | None = None,
    ):
        bucket = self._storage_manager.bucket
        blobs = bucket.list_blobs()
        prefix = manager.prefix
        table_blobs = [
            (
                blob,
                manager.blob_name_from_url(url=blob.url).unwrap_or_raise(),
            )
            for blob in blobs
            if blob.name.startswith(prefix)
        ]

        tables = self._get_tables()
        for blob, table_name in table_blobs:
            if table_name in tables:
                next_count[table_name] = self._table_counts.get(table_name)
                continue
            with blob.open("rb") as stream:
                table = pq.read_table(stream)
                self._db_conn.from_arrow(table).create(f'"{table_name}"')
                next_count[table_name] = table.num_rows
                if transform_table:
                    transform_table(table_name, table)

    def _update_blobs(self) -> None:
        """Adds any blobs not yet known by duckdb to duckdb as tables.

        As a side-effect, update _table_counts.
        """
        next_count: dict[str, int | None] = {}
        self._update_blobs_for_prefix(self._storage_manager.tabular, next_count)
        self._update_blobs_for_prefix(
            self._storage_manager.vector, next_count, self._add_vector_indexes
        )
        self._table_counts = next_count

    def _update_counts(self, blobs: Iterable[str]) -> None:
        """Try to update row counts for given blob tables.

        If the blob tables are not known by duckdb, no counts can be updated. Thus,
        callers should not assume that counts for the given will be known after this
        call returns.
        """
        blobs = [blob for blob in blobs if blob in self._table_counts]
        table_queries = [f"SELECT COUNT(*) FROM '{name}'" for name in blobs]
        if not table_queries:
            return

        with self._db_conn.cursor() as cur:
            cur.execute(" UNION_ALL ".join(table_queries))
            result = cur.fetchall()

        for table_name, count in zip(blobs, [r[0] for r in result], strict=True):
            self._table_counts[table_name] = int(count)

    def count_ingested_rows(self, blob_name: str, *other_blob_names: str) -> int:
        # Callers expect this function to be cheap, so reuse data where possible
        blobs = (blob_name, *other_blob_names)
        blobs_to_query = [
            blob for blob in blobs if self._table_counts.get(blob, None) is None
        ]
        if blobs_to_query:
            # This will only execute in the unlikely situation that another client
            # is adding blobs that the current client is asking for the counts of.
            self._update_blobs()
            self._update_counts(blobs_to_query)
        return sum([self._table_counts.get(blob, None) or 0 for blob in blobs])

    def query_for_blobs(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Query:
        columns = [
            sqlglot.column(sqlglot.exp.to_identifier(name, quoted=True))
            for name in column_names
        ]
        tables = [
            sqlglot.to_identifier(blob_name, quoted=True) for blob_name in blob_names
        ]
        query = sqlglot.select(*columns)

        if len(tables) == 1:
            return query.from_(tables[0])

        staging_union_table = sqlglot.to_identifier(
            f"staging-{uuid.uuid4().hex}", quoted=True
        )

        union = self._select_from_union(column_names, blob_names)
        return (
            sqlglot.select(*column_names)
            .from_(staging_union_table)
            .with_(staging_union_table, as_=union)
        )

    @property
    def vector_column_names_to_widths(self) -> Mapping[str, int]:
        return self._vector_column_names_to_widths

    def query_for_vector_search(
        self,
        input_vector: list[float],
        vector_blob_names: list[str],
        vector_column_name: str,
        column_names: list[str],
        similarity_metric: VectorSimilarityMetric,
    ) -> sqlglot.exp.Query:
        """Creates a SQL query for vector search."""
        self._setup_vss_extensions()

        columns = [
            sqlglot.column(sqlglot.exp.to_identifier(name, quoted=True))
            for name in column_names
        ]
        vector_column = sqlglot.column(
            sqlglot.exp.to_identifier(vector_column_name, quoted=True)
        )

        vector_union_table = sqlglot.to_identifier(
            f"vector-union-{uuid.uuid4().hex}", quoted=True
        )

        union = self._select_from_union(column_names, vector_blob_names)
        similarity_func = self._order_by_func_for_metric(
            vector_column, similarity_metric, input_vector
        )

        vector_search_query = (
            sqlglot.select(*columns).from_(vector_union_table).order_by(similarity_func)
        )
        return vector_search_query.with_(vector_union_table, as_=union)

    def run_select_query(
        self,
        query: sqlglot.exp.Query,
        expected_schema: pa.Schema,
        slice_args: TableSliceArgs | None = None,
    ) -> Ok[pa.RecordBatchReader] | InternalError:
        """Run a select query to extract and transform staging data.

        N.B. this behaves a little differently than rockset would.
        Rockset has one super-wide table, so it would silently omit data. This
        implementation will complain loudly if the query references an unstaged blob.
        That tradeoff is somewhat reasonable since if data isn't staged in this case it
        means the caller is doing something wrong (in Rockset's case there's some
        asynchrony which could lead to the data not being staged).
        """
        self._update_blobs()

        # This is slightly stronger than the property we would get from SQL backends
        # that cache query results different slices would be taken from the same cached
        # query result. Imitated here by enforcing that the result order is always
        # deterministic.
        order_exp: sqlglot.exp.Expression | None = query.args.get("order")
        if not order_exp:
            query.set(
                "order",
                sqlglot.parse_one(
                    "ORDER BY ALL",
                    into=sqlglot.exp.Order,
                    dialect="duckdb",
                ),
            )
        else:
            for named_select in query.named_selects:
                order_exp.append(
                    "expressions",
                    sqlglot.exp.Identifier(this=named_select, quoted=True),
                )

        with self._db_conn.cursor() as cur:
            cur.execute(query.sql(dialect="duckdb"))
            result = cur.fetch_arrow_table()

        if slice_args:
            if slice_args.offset >= result.num_rows:
                result = pa.schema([]).empty_table()
            elif slice_args.offset + slice_args.length > result.num_rows:
                result = result.slice(offset=slice_args.offset)
            else:
                result = result.slice(
                    offset=slice_args.offset,
                    length=slice_args.length,
                )

        batches = result.to_batches()
        if batches:
            storage_schema = _patch_schema_for_storage(
                new_schema=expected_schema,
                old_schema=batches[0].select(expected_schema.names).schema,
            )
            cast_batches = [
                batch.select(expected_schema.names).cast(storage_schema, safe=True)
                for batch in batches
            ]
            return Ok(
                pa.RecordBatchReader.from_batches(
                    schema=storage_schema, batches=cast_batches
                )
            )

        return Ok(result.to_reader())
