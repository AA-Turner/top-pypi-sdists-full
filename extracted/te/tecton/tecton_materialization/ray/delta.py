import dataclasses
import json
import logging
import os
import uuid
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pyarrow
import pyarrow.dataset
import pyarrow.fs
import ray
from deltalake.writer import DeltaJSONEncoder
from deltalake.writer import get_file_stats_from_metadata
from pyarrow._dataset import WrittenFile

from tecton_core import conf
from tecton_core import offline_store
from tecton_core.arrow import PARQUET_WRITE_OPTIONS
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_types import TimestampType
from tecton_core.offline_store import patch_timestamps_in_arrow_schema
from tecton_core.query.dialect import Dialect
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.schema import Schema
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.ray.offline_store_writer import OfflineStoreParams
from tecton_materialization.ray.offline_store_writer import OfflineStoreWriter
from tecton_materialization.ray.offline_store_writer import path_from_uri
from tecton_proto.common import data_type__client_pb2 as data_type_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common.aws_credentials__client_pb2 import AwsIamRole
from tecton_proto.offlinestore.delta import metadata__client_pb2 as metadata_pb2
from tecton_proto.offlinestore.delta import transaction_writer__client_pb2 as transaction_writer_pb2


Z_ORDER_TAG = "optimizationType"
Z_ORDER_TAG_VALUE = "z-order"

logger = logging.getLogger(__name__)


class DeltaConcurrentModificationException(Exception):
    def __init__(self, error_type: transaction_writer_pb2.UpdateResult.ErrorType, error_message: str):
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        error_type_name = transaction_writer_pb2.UpdateResult.ErrorType.Name(self.error_type)
        return (
            f"Delta commit failed due to a transaction conflict. "
            f"Conflict type: {error_type_name}. Message: {self.error_message}"
        )


class JavaActorWrapper:
    """Blocking wrapper around a Java actor."""

    def __init__(self, class_name):
        self.actor = ray.cross_language.java_actor_class(class_name).remote()

    def __getattr__(self, item):
        def f(*args):
            return ray.get(getattr(self.actor, item).remote(*args))

        return f


class TransactionWriter:
    """Wrapper around TransactionWriter actor which handles (de)serialization of parameters and return values."""

    def __init__(self, args: transaction_writer_pb2.InitializeArgs):
        self.actor = JavaActorWrapper("com.tecton.offlinestore.delta.TransactionWriterActor")
        self.actor.initialize(args.SerializeToString())

    def has_commit_with_metadata(self, metadata: metadata_pb2.TectonDeltaMetadata) -> bool:
        return self.actor.hasCommitWithMetadata(metadata.SerializeToString())

    def read_for_update(self, predicate: transaction_writer_pb2.Expression) -> List[str]:
        result_bytes = self.actor.readForUpdate(
            transaction_writer_pb2.ReadForUpdateArgs(read_predicate=predicate).SerializeToString()
        )
        result = transaction_writer_pb2.ReadForUpdateResult()
        result.ParseFromString(result_bytes)
        return result.uris

    def update(self, args: transaction_writer_pb2.UpdateArgs) -> transaction_writer_pb2.UpdateResult:
        result_bytes = self.actor.update(args.SerializeToString())
        result = transaction_writer_pb2.UpdateResult()
        result.ParseFromString(result_bytes)
        if not result.committed_version:
            raise DeltaConcurrentModificationException(error_type=result.error_type, error_message=result.error_message)

        return result

    def get_partitions_not_marked_with(self, tags: Dict[str, str]) -> List[Dict[str, str]]:
        args = transaction_writer_pb2.GetPartitionsArgs(tags=tags)
        result_bytes = self.actor.getPartitionsNotMarkedWith(args.SerializeToString())
        result = transaction_writer_pb2.GetPartitionsResult()
        result.ParseFromString(result_bytes)
        return [partition.values for partition in result.partitions]


def _pyarrow_literal(table: pyarrow.Table, column: schema_pb2.Column, row: int) -> transaction_writer_pb2.Expression:
    """Returns a Delta literal Expression for the given row and column within table."""
    pa_column = next((c for (name, c) in zip(table.column_names, table.columns) if name == column.name))
    pa_value = pa_column[row]

    def assert_type(t: pyarrow.DataType):
        assert pa_column.type == t, f"Type error for {column.name}. Expected {t}; got {pa_column.type}"

    if column.offline_data_type.type == data_type_pb2.DataTypeEnum.DATA_TYPE_INT64:
        assert_type(pyarrow.int64())
        lit = transaction_writer_pb2.Expression.Literal(int64=pa_value.as_py())
    elif column.offline_data_type.type == data_type_pb2.DataTypeEnum.DATA_TYPE_STRING:
        assert_type(pyarrow.string())
        lit = transaction_writer_pb2.Expression.Literal(str=pa_value.as_py())
    elif column.offline_data_type.type == data_type_pb2.DataTypeEnum.DATA_TYPE_TIMESTAMP:
        assert_type(pyarrow.timestamp("us", "UTC"))
        lit = transaction_writer_pb2.Expression.Literal()
        lit.timestamp.FromDatetime(pa_value.as_py())
    else:
        msg = f"Unsupported type {column.offline_data_type.type} in column {column.name}"
        raise Exception(msg)
    return transaction_writer_pb2.Expression(literal=lit)


def _binary_expr(
    op: transaction_writer_pb2.Expression.Binary.Op,
    left: transaction_writer_pb2.Expression,
    right: transaction_writer_pb2.Expression,
) -> transaction_writer_pb2.Expression:
    return transaction_writer_pb2.Expression(
        binary=transaction_writer_pb2.Expression.Binary(op=op, left=left, right=right)
    )


TRUE = transaction_writer_pb2.Expression(literal=transaction_writer_pb2.Expression.Literal(bool=True))


def _in_range(
    table: pyarrow.Table, column: schema_pb2.Column, end_inclusive: bool
) -> transaction_writer_pb2.Expression:
    """Returns a predicate Expression for values which are within the limits of the given column of the given limits table.

    :param table: The table
    :param: column: The column to test in this expression
    :param: Whether the predicate should include the end value
    """
    start_cond = _binary_expr(
        op=transaction_writer_pb2.Expression.Binary.OP_LE,
        left=_pyarrow_literal(table, column, row=0),
        right=transaction_writer_pb2.Expression(column=column),
    )
    end_cond = _binary_expr(
        op=transaction_writer_pb2.Expression.Binary.OP_LE
        if end_inclusive
        else transaction_writer_pb2.Expression.Binary.OP_LT,
        left=transaction_writer_pb2.Expression(column=column),
        right=_pyarrow_literal(table, column, row=1),
    )
    return _binary_expr(op=transaction_writer_pb2.Expression.Binary.OP_AND, left=start_cond, right=end_cond)


def _get_fs_and_path(table_uri: str) -> Tuple[pyarrow.fs.FileSystem, str]:
    return pyarrow.fs.FileSystem.from_uri(table_uri)


@dataclasses.dataclass
class DeltaWriter(OfflineStoreWriter):
    def __init__(
        self,
        store_params: OfflineStoreParams,
        table_uri: str,
        join_keys: List[str],
        dynamodb_log_table_name: str,
        dynamodb_log_table_region: str,
        dynamodb_cross_account_role: Optional[AwsIamRole],
        kms_key_arn: str,
        partition_type: Optional[offline_store.PartitionType] = None,
    ):
        super().__init__(store_params, table_uri, join_keys)
        self._fs, self._base_path = _get_fs_and_path(self._table_uri)
        self._adds: List[transaction_writer_pb2.AddFile] = []
        self._delete_uris: List[str] = []
        self._dynamodb_log_table_name = dynamodb_log_table_name
        self._dynamodb_log_table_region = dynamodb_log_table_region
        self._dynamodb_cross_account_role = dynamodb_cross_account_role
        self._current_transaction_writer: Optional[TransactionWriter] = None
        if partition_type == offline_store.PartitionType.NONE:
            self._partitioning = None
        # for compaction jobs, we use delta v2 (epoch nanoseconds) as partition
        elif partition_type == offline_store.PartitionType.EPOCH:
            self._partitioning = pyarrow.dataset.partitioning(
                pyarrow.schema([(offline_store.TIME_PARTITION, pyarrow.int64())]), flavor="hive"
            )
        else:
            self._partitioning = pyarrow.dataset.partitioning(
                pyarrow.schema([(offline_store.TIME_PARTITION, pyarrow.string())]), flavor="hive"
            )
        self._kms_key_arn = kms_key_arn
        self._retry_exceptions = [DeltaConcurrentModificationException]
        self._partition_type = partition_type

    def _transaction_writer(self) -> TransactionWriter:
        if not self._current_transaction_writer:
            # for untiled offline store, we use view schema
            if self._partition_type == offline_store.PartitionType.EPOCH:
                schema = self._feature_params.view_schema
            else:
                schema = self._feature_params.schema

            if self._partition_type == offline_store.PartitionType.NONE:
                partition_columns = []
            else:
                partition_columns = [offline_store.TIME_PARTITION]
                partition_column = schema_pb2.Column(
                    name=offline_store.TIME_PARTITION,
                    offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_STRING),
                )
                schema.columns.append(partition_column)

            init_args = transaction_writer_pb2.InitializeArgs(
                path=self._table_uri,
                id=self._feature_params.feature_view_id,
                name=self._feature_params.feature_view_name,
                description=f"Offline store for FeatureView {self._feature_params.feature_view_id} ({self._feature_params.feature_view_name})",
                schema=schema,
                partition_columns=partition_columns,
                dynamodb_log_table_name=self._dynamodb_log_table_name,
                dynamodb_log_table_region=self._dynamodb_log_table_region,
                kms_key_arn=self._kms_key_arn,
            )
            if self._dynamodb_cross_account_role is not None:
                init_args.cross_account_role_configs.dynamo_cross_account_role.CopyFrom(
                    self._dynamodb_cross_account_role
                )
            self._current_transaction_writer = TransactionWriter(init_args)
        return self._current_transaction_writer

    def _time_limits(self, time_interval: TimeInterval) -> pyarrow.Table:
        """Returns a Table specifying the limits of data affected by a materialization job.

        :param time_interval: The feature time interval
        :returns: A relation with one column for the timestamp key, anchor time, and one with the partition value
            corresponding to the first column. The first row will be the values for feature start time and the second for
            feature end time.
        """
        timestamp_key = self._feature_params.time_spec.timestamp_key
        timestamp_table = pyarrow.table({timestamp_key: [time_interval.start, time_interval.end]})

        if self._feature_params.batch_schedule is None:
            msg = "Batch schedule is required for batch materialization"
            raise Exception(msg)

        tree = AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=AddAnchorTimeNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=ConvertTimestampToUTCNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    input_node=StagedTableScanNode(
                        dialect=Dialect.DUCKDB,
                        compute_mode=ComputeMode.RIFT,
                        staged_schema=Schema.from_dict({timestamp_key: TimestampType()}),
                        staging_table_name="timestamp_table",
                    ).as_ref(),
                    timestamp_key=timestamp_key,
                ).as_ref(),
                feature_store_format_version=self._feature_params.feature_store_format_version,
                batch_schedule=self._feature_params.batch_schedule,
                timestamp_field=timestamp_key,
            ).as_ref(),
            time_spec=self._feature_params.time_spec,
        ).as_ref()
        return self._duckdb_conn.sql(tree.to_sql()).arrow()

    def _time_limit_predicate(self, interval: TimeInterval) -> transaction_writer_pb2.Expression:
        """Returns a predicate Expression matching offline store rows for materialization of the given interval."""
        table = self._time_limits(interval)
        time_spec = self._feature_params.time_spec
        time_column = next((col for col in self._feature_params.schema.columns if col.name == time_spec.time_column))
        partition_column = schema_pb2.Column(
            name=offline_store.TIME_PARTITION,
            offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_STRING),
        )
        predicate = _binary_expr(
            op=transaction_writer_pb2.Expression.Binary.OP_AND,
            left=_in_range(table, time_column, end_inclusive=False),
            right=_in_range(table, partition_column, end_inclusive=True),
        )
        return predicate

    def _filter_files_for_deletion(
        self,
        predicate: transaction_writer_pb2.Expression,
        filter_table: Callable[[pyarrow.dataset.Dataset], pyarrow.Table],
        force_overwrite: bool = False,
        **write_kwargs,
    ):
        paths = self._transaction_writer().read_for_update(predicate)
        deletes = []
        for path in paths:
            input_table = pyarrow.dataset.dataset(
                source=os.path.join(self._base_path, path),
                filesystem=self._fs,
                partitioning=self._partitioning,
            ).to_table()
            output_table = filter_table(input_table)
            if input_table.num_rows != output_table.num_rows or force_overwrite:
                deletes.append(path)
                if output_table.num_rows:
                    self.write(output_table, **write_kwargs)
        self._delete_uris.extend(deletes)

    def transaction_exists(self, metadata: metadata_pb2.TectonDeltaMetadata) -> bool:
        """checks matching transaction metadata, which signals that a previous task attempt already wrote data
        If the task overwrites a previous materialization task interval then we treat it as a new transaction.
        # TODO (vitaly): replace with txnAppId since overwrite tasks might also have multiple attempts (redundant txns)

        :param metadata: transaction metadata
        :return: whether the same transaction has been executed before
        """
        return self._transaction_writer().has_commit_with_metadata(metadata)

    def delete_time_range(self, interval: TimeInterval) -> None:
        """Filters and deletes previously materialized data within the interval.

        :param interval: The feature data time interval to delete

        High level process:
        1. Construct a Delta predicate expression matching the data we want to delete. This includes both a partition
           predicate to limit the files we have to look at, and a predicate on timestamp/anchor time which doesn't limit
           the files we have to consider, but can help with limit transaction conflicts.
        2. Mark files matching the predicate as read in the Delta transaction. This returns a list of files possibly
           matching the predicate.
        3. For each file:
           3a. Open it, filter out all data matching the predicate, and write out remaining data (if any) to a
               new file.
           3b. If any data was filtered out, add the old file to the list of deletes in the transaction. If any data remains,
               add the new file to the transaction.

        Implementation notes:
        1. This is racy if there is another job running at the same time. This behavior is the same as in Spark.
        2. We have corrected a bug that exists in Spark where we're not correctly selecting the data to delete: TEC-16681
        """
        print(f"Clearing prior data in range {interval.start} - {interval.end}")

        time_spec = self._feature_params.time_spec

        def table_filter(input_table: pyarrow.dataset.Dataset) -> pyarrow.Table:
            time_limit_table = self._time_limits(interval)
            # Add timezone to timestamps
            input_table = input_table.cast(patch_timestamps_in_arrow_schema(input_table.schema))
            # Not using pypika because it lacks support for ANTI JOIN
            return self._duckdb_conn.sql(
                f"""
                WITH flattened_limits AS(
                    SELECT MIN("{time_spec.time_column}") AS start, MAX("{time_spec.time_column}") AS end
                    FROM time_limit_table
                )
                SELECT * FROM input_table
                LEFT JOIN flattened_limits
                ON input_table."{time_spec.time_column}" >= flattened_limits.start
                AND input_table."{time_spec.time_column}" < flattened_limits.end
                WHERE flattened_limits.start IS NULL
            """
            ).arrow()

        predicate = self._time_limit_predicate(interval)
        self._filter_files_for_deletion(predicate, table_filter)

    def write(
        self, table: Union[pyarrow.Table, pyarrow.RecordBatchReader], tags: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """Writes a pyarrow Table to the Delta table at base_uri partitioned by the TIME_PARTITION column.

        Returns a list of URIs for the written file(s).

        This does NOT commit to the Delta log. Call commit() after calling this to commit your changes.
        """

        if conf.get_bool("DUCKDB_DEBUG"):
            logger.warning("Beginning write to Delta table")

        adds = write(table, self._base_path, self._table_uri, self._join_keys, self._fs, self._partitioning, tags)

        self._adds.extend(adds)
        return [add.uri for add in adds]

    def add_files(self, adds: List[transaction_writer_pb2.AddFile]):
        self._adds.extend(adds)

    def delete_keys(self, keys: pyarrow.Table):
        def filter_table(input_table: pyarrow.dataset.Dataset) -> pyarrow.Table:
            return self._duckdb_conn.sql(
                f"""
                SELECT * FROM input_table
                ANTI JOIN keys
                USING ({", ".join(keys.column_names)})
                """
            ).arrow()

        # It's necessary to scan the entire table anyway, so we just use True as the predicate.
        #
        # In theory this might be missing out on some optimizations to avoid conflicting queries, but in
        # practice the only types of conflicts we could avoid would be key deletion operations on
        # disjoint sets of keys and also end up only touching disjoint sets of files. This is probably not very likely
        # to occur.
        return self._filter_files_for_deletion(TRUE, filter_table)

    # Collect entity samples for each Parquet file in Delta
    # Each sample is accompanied by weight = (number of rows in file) / (sample size)
    def collect_sample_entities(self, entity_sample_rows: int):
        for add_file in self._adds:
            parquet_path = os.path.join(self._base_path, add_file.uri)
            count_query = f"SELECT COUNT(*) AS total_rows FROM parquet_scan('{parquet_path}')"
            total_rows = self._duckdb_conn.execute(count_query).fetchone()[0]
            sample_size = min(total_rows, entity_sample_rows)

            get_sample_query = f"""
                SELECT {", ".join(self._join_keys)}
                FROM parquet_scan('{parquet_path}')
                TABLESAMPLE RESERVOIR({sample_size} rows)
            """
            try:
                sampled_parquet_df = self._duckdb_conn.execute(get_sample_query).fetchdf()
                sampled_parquet_df["key_tuple"] = sampled_parquet_df[self._join_keys].apply(tuple, axis=1)
                hash_counts = sampled_parquet_df["key_tuple"].value_counts()
                weight = total_rows / sample_size
                weighted_hash_counts = {}
                for k, v in hash_counts.items():
                    key_str = json.dumps(k)
                    value = float(v * weight)
                    weighted_hash_counts[key_str] = value
                serialized_sample_data = json.dumps(weighted_hash_counts, cls=DeltaJSONEncoder)
                # Writing the sample data to Delta metadata tags instead of stats because the Delta API
                # can only read specific types of metadata, such as min/max values and null counts.
                # Custom metadata like sample data is not supported through the Delta API's,
                # so we are storing it in tags for now.
                add_file.tags["sample_entity_weight"] = serialized_sample_data
            except Exception as e:
                print(f"error occurred when sampling parquet data: {e}")

    def run_z_order_optimization(self):
        partitions = self._transaction_writer().get_partitions_not_marked_with({Z_ORDER_TAG: Z_ORDER_TAG_VALUE})
        partition_column = schema_pb2.Column(
            name=offline_store.TIME_PARTITION,
            offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_STRING),
        )

        def table_sorted(input_table: pyarrow.dataset.Dataset) -> pyarrow.Table:
            return self._duckdb_conn.from_arrow(input_table).order(", ".join(self._join_keys)).arrow()

        for partition in partitions:
            partition_predicate = _binary_expr(
                op=transaction_writer_pb2.Expression.Binary.OP_EQ,
                left=transaction_writer_pb2.Expression(column=partition_column),
                right=transaction_writer_pb2.Expression(
                    literal=transaction_writer_pb2.Expression.Literal(str=partition[offline_store.TIME_PARTITION])
                ),
            )
            self._filter_files_for_deletion(
                partition_predicate,
                table_sorted,
                force_overwrite=True,
                tags={Z_ORDER_TAG: Z_ORDER_TAG_VALUE},
            )

    def commit(self, metadata: Optional[metadata_pb2.TectonDeltaMetadata] = None) -> Optional[int]:
        """Returns version of commit if it was successful"""
        if not self._adds and not self._delete_uris:
            # nothing to commit
            return

        args = transaction_writer_pb2.UpdateArgs(
            add_files=self._adds, delete_uris=self._delete_uris, user_metadata=metadata
        )
        try:
            return self._transaction_writer().update(args).committed_version
        except tuple(self._retry_exceptions):
            # Commit should be retried together with new write.
            self.abort()

            raise
        finally:
            self._reset_state()

    def abort(self):
        """
        Abort the transaction by cleaning up any files and state.
        Clean up created parquet files that were not part of a successful commit.
        """
        for add_file in self._adds:
            self._fs.delete_file(path_from_uri(add_file.uri))
        self._reset_state()

    def _reset_state(self):
        self._current_transaction_writer = None
        self._adds = []
        self._delete_uris = []


# Create this standalone function to avoid serialization of DeltaWriter. This function is called in the Ray sub-task.
def write(
    table: Union[pyarrow.Table, pyarrow.RecordBatchReader],
    base_path: str,
    table_uri: str,
    join_keys: List[str],
    fs: pyarrow.fs.FileSystem,
    partitioning: Optional[pyarrow.dataset.Partitioning],
    tags: Optional[Dict[str, str]] = None,
) -> List[transaction_writer_pb2.AddFile]:
    """Writes a pyarrow Table to the Delta table at base_uri partitioned by the TIME_PARTITION column.

    Returns a list of URIs for the written file(s).

    This does NOT commit to the Delta log. Call commit() after calling this to commit your changes.
    """

    adds = []
    failed = False
    visited_files_count = 0

    def visit_file(f: WrittenFile):
        if conf.get_bool("DUCKDB_DEBUG"):
            nonlocal visited_files_count
            visited_files_count += 1

            if visited_files_count % 10 == 0:
                logger.warning(f"Processed {visited_files_count} files")

        try:
            path = f.path
            _, prefix, relative = path.partition(base_path)
            assert prefix == base_path, f"Written path is not relative to base path: {path}"
            path_pieces = relative.split("/")
            partition = path_pieces[1]
            k, eq, v = partition.partition("=")
            # if there is a valid partitioning, then v will be non-empty
            if v:
                assert k == offline_store.TIME_PARTITION and eq == "=", (
                    f"path_pieces: {path_pieces}\n Unexpected partition format: {path}"
                )
                partition_values = {k: v}
            else:
                partition_values = {}
            stats = get_file_stats_from_metadata(
                f.metadata,
                num_indexed_cols=-1,  # since we specify columns_to_collect_stats this should be -1
                columns_to_collect_stats=join_keys,
            )
            serialized_stats = json.dumps(stats, cls=DeltaJSONEncoder)
            # somehow Delta Standalone wants this to be double-serialized with all special JSON literals escaped
            serialized_stats = json.dumps(serialized_stats)
            adds.append(
                transaction_writer_pb2.AddFile(
                    uri=table_uri + relative,
                    partition_values=partition_values,
                    tags=tags,
                    stats=serialized_stats,
                )
            )
        except Exception as e:
            # Pyarrow logs and swallows exceptions from this function, so we need some other way of knowing there
            # was a # failure
            nonlocal failed
            failed = True
            raise e

    max_rows_per_file = conf.get_or_none("PARQUET_MAX_ROWS_PER_FILE")
    max_rows_per_group = conf.get_or_none("PARQUET_MAX_ROWS_PER_GROUP")
    pyarrow.dataset.write_dataset(
        data=table,
        filesystem=fs,
        base_dir=base_path,
        format=pyarrow.dataset.ParquetFileFormat(),
        file_options=PARQUET_WRITE_OPTIONS,
        basename_template=f"{uuid.uuid4()}-part-{{i}}.parquet",
        partitioning=partitioning,
        file_visitor=visit_file,
        existing_data_behavior="overwrite_or_ignore",
        max_partitions=365 * 100,
        max_rows_per_file=int(max_rows_per_file) if max_rows_per_file else 0,
        max_rows_per_group=int(max_rows_per_group) if max_rows_per_group else 1_000_000,
    )

    if failed:
        msg = "file visitor failed"
        raise Exception(msg)

    return adds
