import posixpath
from functools import wraps
from types import TracebackType
from typing import (
    Iterator,
    List,
    Tuple,
    Type,
    Iterable,
    Optional,
    Sequence,
    Any,
    Dict,
    Union,
    Callable,
    cast,
)
from contextlib import contextmanager

from dlt.common import json, pendulum, logger
from dlt.common.exceptions import MissingDependencyException, DltException
from dlt.common.libs.pyarrow import columns_to_arrow, pyarrow as pa
from dlt.common.metrics import LoadJobMetrics
from dlt.common.schema import Schema
from dlt.common.schema.exceptions import SchemaCorruptedException, TableNotFound
from dlt.common.schema.typing import (
    TSchemaTables,
    TPartialTableSchema,
    TWriteDisposition,
    TTableFormat,
    TTableSchemaColumns,
)
from dlt.common.schema.utils import (
    get_columns_names_with_prop,
    get_first_column_name_with_prop,
    is_nested_table,
)
from dlt.common.storages import FileStorage, fsspec_from_config
from dlt.common.storages.load_package import LoadJobInfo, ParsedLoadJobFileName
from dlt.common.destination.capabilities import DestinationCapabilitiesContext
from dlt.common.destination.exceptions import (
    DestinationTransientException,
    DestinationTerminalException,
    OpenTableCatalogNotSupported,
    OpenTableFormatNotSupported,
    DestinationUndefinedEntity,
)
from dlt.common.destination.client import (
    FollowupJobRequest,
    PreparedTableSchema,
    RunnableLoadJob,
    JobClientBase,
    WithStateSync,
    SupportsOpenTables,
    StorageSchemaInfo,
    StateInfo,
    LoadJob,
)
from dlt.common.destination.utils import resolve_merge_strategy
from dlt.common.typing import TFun

from dlt.destinations.job_impl import (
    ReferenceFollowupJobRequest,
    FinalizedLoadJobWithFollowupJobs,
)
from dlt.destinations.sql_client import WithSqlClient, SqlClientBase
from dlt.destinations.sql_jobs import SqlMergeFollowupJob


from dlthub import version
from dlthub.destinations.impl.iceberg.iceberg_adapter import build_iceberg_partition_spec
from dlthub.destinations.utils import get_dedup_sort_order_by_sql

from dlthub.destinations.impl.iceberg.configuration import (
    IcebergClientConfiguration,
    IcebergRESTCatalogCredentials,
    IcebergSqlCatalogCredentials,
    AwsRESTCatalogCredentials,
    AwsGlueCatalogCredentials,
)

try:
    from dlt.common.libs.pyiceberg import (
        ensure_iceberg_compatible_arrow_data,
        ensure_iceberg_compatible_arrow_schema,
        write_iceberg_table,
        get_sql_catalog,
        register_table,
        IcebergTable,
        IcebergCatalog,
    )
    from pyiceberg.table import ALWAYS_TRUE, Transaction
    from pyiceberg.expressions import BooleanExpression
    from pyiceberg.exceptions import NoSuchTableError, NoSuchViewError, NoSuchNamespaceError

    from dlthub.destinations.impl.iceberg.iceberg_adapter import (
        PARTITION_HINT,
        iceberg_partition,
        PartitionSpec as HintPartitionSpec,
    )
    import pyarrow as pa
    import pyarrow.compute as pc
except ImportError:
    raise MissingDependencyException(
        "dlthub iceberg destination",
        [f"{version.PKG_NAME}[iceberg]"],
        "iceberg needs pyiceberg, pyarrow, sqlalchemy and duckdb in order to work",
    )


def pyiceberg_error(f: TFun) -> TFun:
    @wraps(f)
    def _wrap(self: JobClientBase, *args: Any, **kwargs: Any) -> Any:
        try:
            return f(self, *args, **kwargs)
        except (
            FileNotFoundError,
            NoSuchTableError,
            NoSuchViewError,
            NoSuchNamespaceError,
        ) as status_ex:
            raise DestinationUndefinedEntity(status_ex) from status_ex
        except DltException:
            raise
        except ValueError as val_err:
            if "cannot add required column" in str(val_err):
                raise DestinationTerminalException(val_err) from val_err
            raise DestinationTransientException(val_err) from val_err
        except Exception as e:
            raise DestinationTransientException(e) from e

    return _wrap  # type: ignore[return-value]


class IcebergLoadJob(RunnableLoadJob):
    def __init__(
        self, file_path: str, catalog: IcebergCatalog, table: PreparedTableSchema, table_id: str
    ):
        super().__init__(file_path)
        self._catalog: IcebergCatalog = catalog
        self._table: PreparedTableSchema = table
        self._file_paths = ReferenceFollowupJobRequest.resolve_references(self._file_path)
        self._table_id = table_id
        self._table_location: str = None
        self._job_client: "PyIcebergJobClient" = None

    @pyiceberg_error
    def run(self) -> None:
        iceberg_table = self._catalog.load_table(self._table_id)
        self._table_location = iceberg_table.location()
        if self._table["write_disposition"] != "merge":
            self._run_append(iceberg_table)
        else:
            strategy = self._table["x-merge-strategy"]  # type: ignore[typeddict-item]
            if strategy == "upsert":
                self._run_upsert(iceberg_table)
            elif strategy == "delete-insert":
                primary_keys = get_columns_names_with_prop(self._load_table, "primary_key")
                merge_keys = get_columns_names_with_prop(self._load_table, "merge_key")

                if primary_keys or merge_keys:
                    self._run_delete_insert(iceberg_table, primary_keys, merge_keys)
                else:
                    # If no keys available, fall back to append mode
                    logger.warning(
                        f"Merge operation for table '{self._table['name']}' is falling back to "
                        "append mode because no primary_key or merge_key was found. "
                    )
                    self._run_append(iceberg_table)

    def _run_append(self, iceberg_table: IcebergTable) -> None:
        ds = pa.dataset.dataset(self._file_paths)
        # arrow_schema = ensure_iceberg_compatible_arrow_schema(ds_.schema)
        # iceberg_columns = {f.name for f in iceberg_table.schema().fields}
        # arrow_columns = {f.name for f in arrow_schema}
        # if arrow_columns - iceberg_columns:
        #     with iceberg_table.update_schema() as update:
        #         update.union_by_name(arrow_schema)
        # else:
        #     print("No schema update 🤯")

        batch_size = self._job_client.config.iceberg_write_batch_size

        if batch_size == 0:
            with self._job_client._clock_iceberg(f"write_iceberg_table `{iceberg_table.name()}`"):
                write_iceberg_table(
                    table=iceberg_table,
                    data=ds.to_table(),
                    write_disposition="append",
                )
        else:
            self._write_batches(
                iceberg_table,
                dataset=ds,
                batch_size=batch_size,
                op_description="batch append",
                process_fn=lambda txn, chunk: txn.append(chunk),
            )

    def _run_delete_insert(
        self, iceberg_table: IcebergTable, primary_keys: List[str], merge_keys: List[str]
    ) -> None:
        batch_size = self._job_client.config.iceberg_write_batch_size
        is_deduplicated = self._table.get("x-stage-data-deduplicated", False)

        if not is_deduplicated and batch_size > 0:
            raise ValueError(
                "Batching is not supported for delete-insert merge strategy when data is not "
                "deduplicated. Either set iceberg_write_batch_size=0 or use "
                'write_disposition={"disposition": "merge", "strategy": "delete-insert", '
                '"deduplicated": True}'
            )

        ds = pa.dataset.dataset(self._file_paths)

        # prepare hard delete info
        from dlt.destinations import duckdb as duckdb_destination

        caps = duckdb_destination()._raw_capabilities()
        hard_delete_col, _ = SqlMergeFollowupJob._get_hard_delete_col_and_cond(
            self._load_table,
            caps.escape_identifier,
            caps.escape_literal,
            invert=True,
        )

        if batch_size == 0:
            arrow_table = ensure_iceberg_compatible_arrow_data(ds.to_table())

            # deduplicate if primary key and deduplication is enabled
            if primary_keys:
                import duckdb

                order_by = get_dedup_sort_order_by_sql(self._load_table)
                con = duckdb.connect()
                arrow_table = (
                    con.sql(f"""
                    FROM arrow_table
                    QUALIFY row_number()
                        OVER (PARTITION BY {primary_keys[0]} ORDER BY {order_by}) = 1;
                """)
                    .to_arrow_table()
                    .cast(arrow_table.schema)
                )

            # prepare deletes
            delete_filter = self._get_delete_filter(arrow_table, primary_keys, merge_keys)

            if hard_delete_col is not None:
                arrow_table = self._exclude_hard_deleted_rows(arrow_table, hard_delete_col)

            with (
                iceberg_table.transaction() as txn,
                self._job_client._clock_iceberg(f"delete-insert `{iceberg_table.name()}`"),
            ):
                if delete_filter:
                    txn.delete(delete_filter)
                txn.append(arrow_table)
        else:
            self._write_filtered_batches(
                iceberg_table,
                dataset=ds,
                batch_size=batch_size,
                primary_keys=primary_keys,
                merge_keys=merge_keys,
                hard_delete_col=hard_delete_col,
                op_description="batch delete-insert",
            )

    def _run_upsert(self, iceberg_table: Any) -> None:
        batch_size = self._job_client.config.iceberg_write_batch_size

        ds = pa.dataset.dataset(self._file_paths)

        # we check that unique columns or primary key exists in the verify_schema()
        if is_nested_table(self._table):
            key_column = get_first_column_name_with_prop(self._table, "unique")
        else:
            primary_keys = get_columns_names_with_prop(self._table, "primary_key")
            key_column = primary_keys[0] if primary_keys else None

        hard_delete_col = get_first_column_name_with_prop(self._load_table, "hard_delete")

        if batch_size == 0:
            arrow_table = ensure_iceberg_compatible_arrow_data(ds.to_table())
            delete_filter = self._get_delete_filter(arrow_table, [key_column])
            if hard_delete_col:
                arrow_table = self._exclude_hard_deleted_rows(arrow_table, hard_delete_col)

            with (
                iceberg_table.transaction() as txn,
                self._job_client._clock_iceberg(f"upsert `{iceberg_table.name()}`"),
            ):
                if delete_filter:
                    txn.delete(delete_filter)
                txn.append(arrow_table)
        else:
            self._write_filtered_batches(
                iceberg_table,
                dataset=ds,
                batch_size=batch_size,
                primary_keys=[key_column],
                hard_delete_col=hard_delete_col,
                op_description="batch upsert",
            )

    def _write_filtered_batches(
        self,
        iceberg_table: IcebergTable,
        dataset: pa.dataset.Dataset,
        batch_size: int,
        primary_keys: Optional[List[str]] = None,
        merge_keys: Optional[List[str]] = None,
        hard_delete_col: Optional[str] = None,
        op_description: Optional[str] = None,
    ) -> None:
        """Process PyArrow dataset in batches using delete-then-insert logic for merge operations.

        Args:
            iceberg_table: Target Iceberg table for merge operations.
            dataset: Source PyArrow dataset to merge.
            batch_size: Rows per batch (must be > 0).
            primary_keys: Primary key columns for row deletion.
            merge_keys: Secondary key columns for deletion.
            hard_delete_col: Column marking rows to exclude from insertion.
            op_description: Description for timing/logging.

        Raises:
            ValueError: If neither primary_keys nor merge_keys are provided.
        """

        def _process(transaction: Transaction, chunk: pa.Table) -> None:
            delete_filter = self._get_delete_filter(chunk, primary_keys, merge_keys)
            insert_chunk = (
                self._exclude_hard_deleted_rows(chunk, hard_delete_col)
                if hard_delete_col
                else chunk
            )
            if delete_filter:
                transaction.delete(delete_filter)
            transaction.append(insert_chunk)

        self._write_batches(
            iceberg_table,
            dataset=dataset,
            batch_size=batch_size,
            op_description=op_description,
            process_fn=_process,
        )

    def _write_batches(
        self,
        iceberg_table: IcebergTable,
        dataset: pa.dataset.Dataset,
        batch_size: int,
        op_description: str,
        process_fn: Callable[[Any, pa.Table], None],
    ) -> None:
        with (
            iceberg_table.transaction() as txn,
            self._job_client._clock_iceberg(
                f"{op_description} `{iceberg_table.name()}` (batch={batch_size})"
            ),
        ):
            for batch_num, record_batch in enumerate(dataset.to_batches(batch_size=batch_size), 1):
                with self._job_client._clock_iceberg(
                    f"{op_description} batch {batch_num} `{iceberg_table.name()}`"
                ):
                    table_chunk = pa.Table.from_batches([record_batch])
                    process_fn(txn, table_chunk)

    def _exclude_hard_deleted_rows(self, arrow_table: pa.Table, hard_delete_col: str) -> pa.Table:
        field = pc.field(hard_delete_col)
        if arrow_table.field(hard_delete_col).type == pa.bool_():
            expression = pc.is_null(field) | pc.equal(field, False)
        else:
            expression = pc.is_null(field)
        return arrow_table.filter(expression)

    def _get_delete_filter(
        self,
        deleted_table: pa.Table,
        primary_keys: List[str],
        merge_keys: Optional[List[str]] = None,
    ) -> Optional[BooleanExpression]:
        from pyiceberg.expressions import In, Or
        # we know we have one primary key and/or one merge key, because we have already
        # checked this in `verify_schema` method

        if merge_keys is None:
            merge_keys = []

        assert primary_keys or merge_keys
        assert len(primary_keys) <= 1
        assert len(merge_keys) <= 1

        if deleted_table is None or deleted_table.num_rows == 0:
            return None

        if primary_keys and merge_keys:
            primary_key, merge_key = primary_keys[0], merge_keys[0]
            key_vals = deleted_table.select([primary_key, merge_key]).to_pydict()
            return Or(
                In(primary_key, key_vals[primary_key]),
                In(merge_key, key_vals[merge_key]),
            )
        elif primary_keys:
            primary_key = primary_keys[0]
            key_vals = deleted_table.select([primary_key]).to_pydict()
            return In(primary_key, key_vals[primary_key])
        elif merge_keys:
            merge_key = merge_keys[0]
            key_vals = deleted_table.select([merge_key]).to_pydict()
            return In(merge_key, key_vals[merge_key])
        return None

    def metrics(self) -> Optional[LoadJobMetrics]:
        m = super().metrics()
        return m._replace(remote_url=self._table_location)


class PyIcebergJobClient(JobClientBase, WithStateSync, WithSqlClient, SupportsOpenTables):
    def __init__(
        self,
        schema: Schema,
        config: IcebergClientConfiguration,
        capabilities: DestinationCapabilitiesContext,
    ):
        super().__init__(schema, config, capabilities)
        self.config: IcebergClientConfiguration = config
        self.dataset_name = config.normalize_dataset_name(schema)
        # TODO: pass catalog name via config. this will allow pyiceberg yaml to be used
        #  to configure catalogs
        self._catalog = self._create_catalog(config.catalog_name)
        self._sql_client: SqlClientBase[Any] = None

    def initialize_storage(self, truncate_tables: Optional[Iterable[str]] = None) -> None:
        """Prepares storage to be used ie. creates database schema or file system folder. Truncates"
        requested tables.
        """
        if not self.is_storage_initialized():
            self._catalog.create_namespace(self.dataset_name)
        # TODO: implement staging dataset replace via followup job
        if truncate_tables:
            for table_name in truncate_tables:
                table_identifier = self.make_qualified_table_name(table_name)
                if self._catalog.table_exists(table_identifier):
                    self._catalog.load_table(table_identifier).delete()

    def is_storage_initialized(self) -> bool:
        """Returns if storage is ready to be read/written."""
        try:
            if self.config.catalog_type == "s3tables-rest":
                self._catalog.list_tables(self.dataset_name)
            else:
                self._catalog.load_namespace_properties(self.dataset_name)
            return True
        except NoSuchNamespaceError:
            return False

    def drop_storage(self) -> None:
        """Deletes all tables from catalog and purges data location, then deletes namespace.
        Note that purging of actual data may be delayed as this is done by a catalog.
        """
        # purges all known (in schema) tables in the namespace
        for table_name in self.schema.tables.keys():
            table_id = self.make_qualified_table_name(table_name)
            if self._catalog.table_exists(table_id):
                self._catalog.purge_table(table_id)
        # purge remaining tables
        for table_ident in self._catalog.list_tables(self.dataset_name):
            self._catalog.purge_table(table_ident)
        # remove namespace (will raise if still containing tables)
        self._catalog.drop_namespace(self.dataset_name)

    def drop_tables(self, *tables: str, delete_schema: bool = True) -> None:
        """Deletes and purges selected tables and optionally deletes schemas. Non existing tables
        are ignored
        Note that purging of actual data may be delayed as this is done by a catalog.
        """
        for table_name in tables:
            table_id = self.make_qualified_table_name(table_name)
            if self._catalog.table_exists(table_id):
                self._catalog.purge_table(table_id)
        if delete_schema:
            self._delete_schema_in_storage(self.schema)

    def update_stored_schema(
        self,
        only_tables: Iterable[str] = None,
        expected_update: TSchemaTables = None,
    ) -> Optional[TSchemaTables]:
        applied_update: TSchemaTables = {}
        if self.get_stored_schema_by_hash(self.schema.stored_version_hash) is None:
            logger.info(
                f"Schema with hash {self.schema.stored_version_hash} not found in the storage."
                " upgrading"
            )
            for table_name in only_tables or self.schema.tables.keys():
                partial_table = self._create_or_evolve_table(table_name)
                if partial_table:
                    applied_update[table_name] = partial_table
            self._update_schema_in_storage(self.schema)
        return applied_update

    def verify_schema(
        self, only_tables: Iterable[str] = None, new_jobs: Iterable[ParsedLoadJobFileName] = None
    ) -> List[PreparedTableSchema]:
        tables = super().verify_schema(only_tables, new_jobs)
        # verify merge strategy and replace options

        for table in tables:
            if table.get("table_format") == "iceberg" and table["write_disposition"] == "merge":
                primary_key = get_columns_names_with_prop(table, "primary_key")
                merge_key = get_columns_names_with_prop(table, "merge_key")

                for key in [primary_key, merge_key]:
                    key_type = "primary_key" if key == primary_key else "merge_key"
                    if len(key) > 1:
                        raise SchemaCorruptedException(
                            self.schema.name,
                            f"Found multiple `{key_type}` columns for table"
                            f""" "{table["name"]}" while only one is allowed when using `iceberg`"""
                            " table format:"
                            f""" {", ".join([f'"{k}"' for k in key])}.""",
                        )

                merge_strategy = resolve_merge_strategy(
                    self.schema.tables, table, self.capabilities
                )

                if merge_strategy == "delete-insert":
                    if is_nested_table(table):
                        raise SchemaCorruptedException(
                            self.schema.name,
                            f'Found nested table "{table["name"]}". Nested tables are not '
                            "supported when using `iceberg` table format and `delete-insert` "
                            "merge strategy.",
                        )
                elif merge_strategy == "upsert":
                    if is_nested_table(table):
                        # For nested tables, require a unique column
                        if get_first_column_name_with_prop(table, "unique") is None:
                            raise SchemaCorruptedException(
                                self.schema.name,
                                f"Could not determine row key for nested table {table['name']} "
                                f"when using `upsert` merge strategy. Nested tables require "
                                f"a column with 'unique' property.",
                            )
                    else:
                        # For regular tables, require primary keys
                        if not primary_key:
                            raise SchemaCorruptedException(
                                self.schema.name,
                                f'Upsert requires primary keys but table "{table["name"]}" '
                                "does not define any when using `iceberg` table format "
                                "and `upsert` merge strategy.",
                            )

        return tables

    def prepare_load_table(self, table_name: str) -> PreparedTableSchema:
        load_table = super().prepare_load_table(table_name)
        if load_table["write_disposition"] == "merge":
            merge_strategy = resolve_merge_strategy(
                self.schema.tables, load_table, self.capabilities
            )
            load_table["x-merge-strategy"] = merge_strategy  # type: ignore[typeddict-unknown-key]
        return load_table

    def create_load_job(
        self, table: PreparedTableSchema, file_path: str, load_id: str, restore: bool = False
    ) -> LoadJob:
        """Creates a load job for a particular `table` with content in `file_path`.
        Table is already prepared to be loaded.
        """
        # TODO: significant performance improvements may be achieved here
        # - execute append/replace jobs immediately, do not chain. also upsert should work without
        #   chaining
        # - implement staging-replace via followup job where we truncate table and then append
        #   batches

        table_format = table.get("table_format")
        assert table_format == "iceberg", f"Only iceberg table format supported, got {table_format}"
        if ReferenceFollowupJobRequest.is_reference_job(file_path):
            with self:
                return IcebergLoadJob(
                    file_path, self._catalog, table, self.make_qualified_table_name(table["name"])
                )

        # otherwise just continue to collect jobs and to create a full table chain
        return FinalizedLoadJobWithFollowupJobs(file_path)

    def create_table_chain_completed_followup_jobs(
        self,
        table_chain: Sequence[PreparedTableSchema],
        completed_table_chain_jobs: Optional[Sequence[LoadJobInfo]] = None,
    ) -> List[FollowupJobRequest]:
        """Creates a list of followup jobs that should be executed after a table chain is
        completed. Tables are already prepared to be loaded.
        """
        assert completed_table_chain_jobs is not None
        jobs = super().create_table_chain_completed_followup_jobs(
            table_chain, completed_table_chain_jobs
        )
        for table in table_chain:
            table_job_paths = [
                job.file_path
                for job in completed_table_chain_jobs
                if job.job_file_info.table_name == table["name"]
            ]
            if table_job_paths:
                file_name = FileStorage.get_file_name_from_file_path(table_job_paths[0])
                jobs.append(ReferenceFollowupJobRequest(file_name, table_job_paths))

        return jobs

    def get_storage_tables(
        self, table_names: Iterable[str]
    ) -> Iterable[Tuple[str, TTableSchemaColumns]]:
        """Yields tables that have files in storage, does not return column schemas"""
        # print(self._catalog.list_tables(self.dataset_name))
        catalog_tables = [t[-1] for t in self._catalog.list_tables(self.dataset_name)]
        for table_name in table_names:
            if table_name in catalog_tables:
                yield (table_name, {"_column": {}})
            else:
                # if no columns we assume that table does not exist
                yield (table_name, {})

    def get_storage_table(self, table_name: str) -> Tuple[bool, TTableSchemaColumns]:
        _, storage_table = list(self.get_storage_tables([table_name]))[0]
        has_table = len(storage_table) > 0
        if has_table:
            from dlt.common.libs.pyarrow import py_arrow_to_table_schema_columns

            iceberg_Table = self.load_open_table("iceberg", table_name)
            return True, py_arrow_to_table_schema_columns(iceberg_Table.schema().as_arrow())
        else:
            return has_table, storage_table

    def _update_schema_in_storage(self, schema: Schema) -> None:
        records = [
            {
                schema.naming.normalize_identifier("version"): schema.version,
                schema.naming.normalize_identifier("engine_version"): schema.ENGINE_VERSION,
                schema.naming.normalize_identifier("inserted_at"): pendulum.now(),
                schema.naming.normalize_identifier("schema_name"): schema.name,
                schema.naming.normalize_identifier("version_hash"): schema.stored_version_hash,
                schema.naming.normalize_identifier("schema"): json.dumps(schema.to_dict()),
            }
        ]
        self.write_records(records, table_name=schema.version_table_name)

    @pyiceberg_error
    def _delete_schema_in_storage(self, schema: Schema) -> None:
        """
        Delete all stored versions with the same name as given schema.
        Fails silently if versions table does not exist
        """
        p_schema_name = self.schema.naming.normalize_identifier("schema_name")

        try:
            version_table = self.load_open_table("iceberg", self.schema.version_table_name)
            version_table.delete(delete_filter=f"{p_schema_name} = '{schema.name}'")
        except DestinationUndefinedEntity:
            pass

    def complete_load(self, load_id: str) -> None:
        records = [
            {
                self.schema.naming.normalize_identifier("load_id"): load_id,
                self.schema.naming.normalize_identifier("schema_name"): self.schema.name,
                self.schema.naming.normalize_identifier("status"): 0,
                self.schema.naming.normalize_identifier("inserted_at"): pendulum.now(),
                self.schema.naming.normalize_identifier(
                    "schema_version_hash"
                ): self.schema.version_hash,
            }
        ]
        self.write_records(
            records,
            table_name=self.schema.loads_table_name,
        )

    def __enter__(self) -> "JobClientBase":
        return self

    def __exit__(
        self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType
    ) -> None:
        pass

    @property
    def sql_client_class(self) -> Type[SqlClientBase[Any]]:
        from dlthub.destinations.impl.iceberg.sql_client import IcebergSqlClient

        return IcebergSqlClient

    @property
    def sql_client(self) -> SqlClientBase[Any]:
        # we use an inner import here, since the sql client depends on duckdb and will
        # only be used for read access on data, some users will not need the dependency
        from dlthub.destinations.impl.iceberg.sql_client import IcebergSqlClient

        if not self._sql_client:
            self._sql_client = IcebergSqlClient(self, dataset_name=self.dataset_name)
        return self._sql_client

    # state sync
    @pyiceberg_error
    def get_stored_schema(self, schema_name: str = None) -> Optional[StorageSchemaInfo]:
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")
        p_inserted_at = self.schema.naming.normalize_identifier("inserted_at")
        p_schema_name = self.schema.naming.normalize_identifier("schema_name")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_schema = self.schema.naming.normalize_identifier("schema")

        try:
            version_table = self.load_open_table("iceberg", self.schema.version_table_name)
            row_filter = f"{p_schema_name} = '{schema_name}'" if schema_name else None
            schemas_table: pa.Table = (
                version_table.scan(row_filter=row_filter or ALWAYS_TRUE)
                .to_arrow()
                .sort_by([(p_inserted_at, "descending")])
            )

            if schemas_table.num_rows == 0:
                return None

            most_recent_schema = schemas_table.take([0]).to_pylist()[0]

            return StorageSchemaInfo(
                version_hash=most_recent_schema[p_version_hash],
                schema_name=most_recent_schema[p_schema_name],
                version=most_recent_schema[p_version],
                engine_version=most_recent_schema[p_engine_version],
                inserted_at=most_recent_schema[p_inserted_at],
                schema=most_recent_schema[p_schema],
            )
        except DestinationUndefinedEntity:
            return None

    @pyiceberg_error
    def get_stored_schema_by_hash(self, version_hash: str) -> StorageSchemaInfo:
        """Retrieves newest schema from destination storage."""
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")
        p_inserted_at = self.schema.naming.normalize_identifier("inserted_at")
        p_schema_name = self.schema.naming.normalize_identifier("schema_name")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_schema = self.schema.naming.normalize_identifier("schema")

        try:
            version_table = self.load_open_table("iceberg", self.schema.version_table_name)

            schemas_table: pa.Table = (
                (version_table.scan(row_filter=f"{p_version_hash} = '{version_hash}'"))
                .to_arrow()
                .sort_by([(p_inserted_at, "descending")])
            )

            if schemas_table.num_rows == 0:
                return None

            most_recent_schema = schemas_table.take([0]).to_pylist()[0]

            return StorageSchemaInfo(
                version_hash=most_recent_schema[p_version_hash],
                schema_name=most_recent_schema[p_schema_name],
                version=most_recent_schema[p_version],
                engine_version=most_recent_schema[p_engine_version],
                inserted_at=most_recent_schema[p_inserted_at],
                schema=most_recent_schema[p_schema],
            )
        except DestinationUndefinedEntity:
            return None

    @pyiceberg_error
    def get_stored_state(self, pipeline_name: str) -> Optional[StateInfo]:
        """Retrieves the latest completed state for a pipeline."""
        state_table_ = self.load_open_table("iceberg", self.schema.state_table_name)
        loads_table_ = self.load_open_table("iceberg", self.schema.loads_table_name)

        # normalize property names
        p_load_id = self.schema.naming.normalize_identifier("load_id")
        p_dlt_load_id = self.schema.naming.normalize_identifier(
            self.schema.data_item_normalizer.c_dlt_load_id  # type: ignore[attr-defined]
        )
        p_pipeline_name = self.schema.naming.normalize_identifier("pipeline_name")
        p_status = self.schema.naming.normalize_identifier("status")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_state = self.schema.naming.normalize_identifier("state")
        p_created_at = self.schema.naming.normalize_identifier("created_at")
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")

        # Read the tables into memory as Arrow tables, with pushdown predicates,
        # so we pull as little
        # data into memory as possible.
        state_table = state_table_.scan(
            row_filter=f"{p_pipeline_name} = '{pipeline_name}'"
        ).to_arrow()
        loads_table = loads_table_.scan(row_filter=f"{p_status} = 0").to_arrow()

        # Join arrow tables in-memory.
        joined_table: pa.Table = state_table.join(
            loads_table, keys=p_dlt_load_id, right_keys=p_load_id, join_type="inner"
        ).sort_by([(p_dlt_load_id, "descending")])

        if joined_table.num_rows == 0:
            return None

        state = joined_table.take([0]).to_pylist()[0]
        return StateInfo(
            version=state[p_version],
            engine_version=state[p_engine_version],
            pipeline_name=state[p_pipeline_name],
            state=state[p_state],
            created_at=pendulum.instance(state[p_created_at]),
            version_hash=state[p_version_hash],
            _dlt_load_id=state[p_dlt_load_id],
        )

    @pyiceberg_error
    def write_records(
        self,
        records: List[Dict[str, Any]],
        table_name: str,
        write_disposition: TWriteDisposition = "append",
    ) -> None:
        table_schema = self.prepare_load_table(table_name)
        arrow_schema = columns_to_arrow(table_schema["columns"], self.capabilities)
        # Convert records to Arrow table
        arrays = {col: [record.get(col, None) for record in records] for col in arrow_schema.names}
        table_data = pa.Table.from_pydict(arrays, schema=arrow_schema)
        iceberg_table = self._catalog.load_table(self.make_qualified_table_name(table_name))

        write_iceberg_table(iceberg_table, table_data, write_disposition=write_disposition)

    def _sanitize_table_name(self, table_name: str) -> str:
        if self.config.is_aws_rest_catalog:
            table_name = table_name.lstrip("_")
        return table_name

    def make_qualified_table_name(self, table_name: str) -> str:
        return f"{self.dataset_name}.{self._sanitize_table_name(table_name)}"

    def export_aws_creds_to_env(
        self, credentials: Union[AwsRESTCatalogCredentials, AwsGlueCatalogCredentials]
    ) -> None:
        import os
        import logging

        # TODO: refactor when https://github.com/apache/iceberg-python/pull/2071 is merged
        os.environ.setdefault("AWS_ACCESS_KEY_ID", credentials.aws_access_key_id)
        os.environ.setdefault("AWS_SECRET_ACCESS_KEY", credentials.aws_secret_access_key)
        if credentials.aws_session_token:
            os.environ.setdefault("AWS_SESSION_TOKEN", credentials.aws_session_token)
        if credentials.region_name:
            os.environ.setdefault("AWS_DEFAULT_REGION", credentials.region_name)

        # silence - INFO botocore.credentials: Found credentials in environment variables.
        logging.getLogger("botocore.credentials").setLevel(logging.ERROR)

    def _create_catalog(self, catalog_name: str) -> IcebergCatalog:
        # TODO: move to the configuration?
        if isinstance(self.config.credentials, IcebergSqlCatalogCredentials):
            return get_sql_catalog(
                catalog_name,
                self.config.credentials.to_native_representation(),
                self.config.filesystem.credentials,
                self.config.credentials.properties,
            )
        elif isinstance(self.config.credentials, IcebergRESTCatalogCredentials):
            from pyiceberg.catalog.rest import RestCatalog

            rest_credentials = self.config.credentials
            properties = dict(self.config.credentials.properties or {})
            if self.config.credentials.headers:
                headers = {"header." + k: v for k, v in self.config.credentials.headers.items()}
                properties.update(headers)
            if self.config.credentials.warehouse:
                properties["warehouse"] = self.config.credentials.warehouse
            if self.config.credentials.credential:
                properties["credential"] = self.config.credentials.credential
            return RestCatalog(catalog_name, uri=rest_credentials.uri, **properties)
        elif isinstance(self.config.credentials, AwsRESTCatalogCredentials):
            from pyiceberg.catalog.rest import RestCatalog

            properties = self.config.catalog_props
            aws_rest_credentials: AwsRESTCatalogCredentials = self.config.credentials

            if self.config.credentials.warehouse:
                properties["warehouse"] = self.config.credentials.warehouse
            if self.config.credentials.uri:
                properties["uri"] = self.config.credentials.uri

            # TODO: fix upstream pyiceberg issue
            self.export_aws_creds_to_env(aws_rest_credentials)

            return RestCatalog(catalog_name, **properties)
        elif isinstance(self.config.credentials, AwsGlueCatalogCredentials):
            from pyiceberg.catalog.glue import GlueCatalog

            properties = self.config.catalog_props
            aws_glue_credentials: AwsGlueCatalogCredentials = self.config.credentials

            # glue.* is used to create glue session but to access files you need to create
            # fileio secrets. (client.* works for both)
            properties.update({
                "client.access-key-id": aws_glue_credentials.aws_access_key_id,
                "client.secret-access-key": aws_glue_credentials.aws_secret_access_key,
                "glue.connect-timeout": 300,
            })
            if aws_glue_credentials.aws_session_token:
                properties["client.session-token"] = aws_glue_credentials.aws_session_token
            if aws_glue_credentials.region_name:
                properties["client.region"] = aws_glue_credentials.region_name
            if aws_glue_credentials.endpoint_url:
                properties["glue.endpoint"] = aws_glue_credentials.endpoint_url

            return GlueCatalog(catalog_name, **properties)
        else:
            raise NotImplementedError(
                f"Iceberg catalog of type {self.config.catalog_type} with credentials "
                f"{type(self.config.credentials)} is not yet implemented."
            )

    @pyiceberg_error
    def _create_or_evolve_table(
        self,
        table_name: str,
    ) -> Optional[TPartialTableSchema]:
        """Creates or evolves schema of Iceberg table using configured catalog. Returns partial
        table with only new columns present to compute applied schema update.
        """
        prepared_table = self.prepare_load_table(table_name)
        # table with empty columns will not be created
        if not prepared_table["columns"]:
            return None

        table_name = self._sanitize_table_name(table_name)
        table_id = self.make_qualified_table_name(table_name)
        columns_no_nested = prepared_table["columns"]
        arrow_schema = ensure_iceberg_compatible_arrow_schema(
            # NOTE: we have nested types passed via arrow-ipc serialization via dlt schema
            #   final version should use human readable form
            columns_to_arrow(columns_no_nested, self.capabilities)
        )
        try:
            iceberg_table = self.load_open_table("iceberg", table_name)
            # table was found or registered
            new_columns = set(prepared_table["columns"].keys()).difference(
                iceberg_table.schema().column_names
            )
            # evolve schema
            # TODO: we may want to set table properties here as well ie. current snapshot.
            # then you cannot skip like below
            if new_columns:
                with self._clock_iceberg(f"update_schema `{iceberg_table.name()}`"):
                    with iceberg_table.update_schema() as update:
                        update.union_by_name(arrow_schema)
                prepared_table["columns"] = {
                    k: v for k, v in prepared_table["columns"].items() if k in new_columns
                }
            else:
                prepared_table = None
        except DestinationUndefinedEntity:
            # found no metadata; create new table
            location = self.get_open_table_location("iceberg", table_name)
            partition_specs = self._get_partition_specs(prepared_table)
            self._create_table_with_partitions(table_id, arrow_schema, location, partition_specs)

        # return prepared table with only new columns present
        return prepared_table

    def _get_partition_specs(self, prepared_table: TPartialTableSchema) -> List[HintPartitionSpec]:
        """Returns partition specs both from table partition hints and from column properties."""
        columns_with_partition = get_columns_names_with_prop(prepared_table, "partition")
        partition_hints = cast(List[Dict[str, Any]], prepared_table.get(PARTITION_HINT, []))

        hints_specs = []
        for spec_data in partition_hints:
            spec = HintPartitionSpec.from_dict(spec_data)
            if spec.transform == "identity" and spec.source_column in columns_with_partition:
                raise SchemaCorruptedException(
                    self.schema.name,
                    f"Column '{spec.source_column}' is defined both as a partition column "
                    "and in partition hints.",
                )
            hints_specs.append(spec)

        identity_specs = [
            iceberg_partition.identity(column_name) for column_name in columns_with_partition
        ]
        return identity_specs + hints_specs

    def _create_table_with_partitions(
        self,
        table_id: str,
        arrow_schema: pa.Schema,
        location: str,
        helper_specs: List[HintPartitionSpec],
    ) -> None:
        partition_spec, iceberg_schema = build_iceberg_partition_spec(arrow_schema, helper_specs)
        with self._clock_iceberg(f"create_table `{table_id}`"):
            self._catalog.create_table(
                identifier=table_id,
                schema=iceberg_schema,  # must be an IcebergSchema, not pa.Schema
                location=location,
                partition_spec=partition_spec,
                properties={},
            )

    def get_open_table_catalog(
        self, table_format: TTableFormat, catalog_name: str = None
    ) -> IcebergCatalog:
        if table_format != "iceberg":
            raise OpenTableCatalogNotSupported(table_format, "iceberg")
        return self._catalog

    def get_open_table_location(self, table_format: TTableFormat, table_name: str) -> str:
        """Computes table location without loading table from a catalog. This requires
        absolute `table_location_layout` or `bucket_url` defined in `config.filesystem`.
        """
        if table_format != "iceberg":
            raise OpenTableFormatNotSupported(table_format, table_name, "iceberg")
        location = self.config.table_location_layout()
        # if location is set try to add namespace and table name to it
        if location:
            location = location.format(dataset_name=self.dataset_name, table_name=table_name)
        # assert location is not None
        logger.info(
            f"will use location: {location or '<catalog controlled>'} for table {table_name}"
        )
        return location

    @pyiceberg_error
    def load_open_table(
        self, table_format: TTableFormat, table_name: str, **kwargs: Any
    ) -> IcebergTable:
        """Loads table with `table_name` from catalog. If table does not exist and configuration
        allows to register new tables ('register_new_tables'), `filesystem` configuration will
        be used to find the newest metadata and add this table to the catalog.
        Note: we do not return static pyiceberg table if table is not in the catalog.
        """
        if table_format != "iceberg":
            raise OpenTableFormatNotSupported(table_format, table_name, "iceberg")
        table_id = self.make_qualified_table_name(table_name)
        try:
            with self._clock_iceberg(f"load_table '{table_id}'"):
                return self._catalog.load_table(table_id)
        except NoSuchTableError:
            # try to register existing table
            if self.config.capabilities.register_new_tables:
                if self.config.filesystem is None or not self.config.filesystem.is_resolved():
                    raise DestinationTerminalException(
                        "Cannot register table without filesystem configuration. dlt needs location"
                        " and access to table storage to look for the newest metadata file"
                    )
                # TODO: metadata location may also be present in the dlt schema ie.
                # x-loader/iceberg/metadata_location
                # TODO: use similar search as duckdb (hints.txt, glob with metadata)
                fs_client = fsspec_from_config(self.config.filesystem)[0]
                location = self.get_open_table_location("iceberg", table_name)
                if location:
                    metadata_location = posixpath.join(
                        location,
                        self.config.capabilities.table_metadata_layout,
                    )
                    if fs_client.exists(metadata_location):
                        logger.info(
                            f"Registering table {table_id} at metadata location {metadata_location}"
                        )
                        try:
                            return register_table(
                                table_id,
                                metadata_path=metadata_location,
                                catalog=self._catalog,
                                fs_client=fs_client,
                                config=self.config.filesystem,
                            )
                        except NoSuchNamespaceError:
                            # create namespace and try again
                            self.initialize_storage()
                            return self.load_open_table("iceberg", table_name)
                    else:
                        logger.info(
                            f"Table metadata at {metadata_location} could not be found and "
                            "registered."
                        )
                else:
                    logger.info(
                        f"Table {table_name} not exists and could not be registered because "
                        "location could not be computed from destination config."
                    )
            # unable to register
            raise

    def is_open_table(self, table_format: TTableFormat, table_name: str) -> bool:
        try:
            table = self.prepare_load_table(table_name)
            return table["table_format"] == "iceberg" == table_format
        except TableNotFound:
            return False

    @staticmethod
    @contextmanager
    def _clock_iceberg(op: str) -> Iterator[None]:
        import time
        import humanize
        import threading

        st = time.time()

        yield

        # uncomment to enable iceberg timing
        clocked = humanize.naturaldelta(time.time() - st, minimum_unit="milliseconds")
        logger.debug(
            f"ICEBERG {op} took {clocked} on thread {threading.current_thread().native_id}"
        )
        # print(f"ICEBERG {op} took {clocked} on thread {threading.currentThread().native_id}")
