import datetime
import itertools
import time
from functools import reduce
from operator import and_
from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pandas
import pyarrow
import pyarrow.parquet as pq

from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.errors import AccessError
from tecton_core.offline_store import BotoOfflineStoreOptionsProvider
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.errors import UserCodeError
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.node_interface import SinglePartition
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.pandas.node import ArrowExecNode
from tecton_core.schema import Schema
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.skew_config import SkewConfig
from tecton_core.specs import DatetimePartitionColumnSpec
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.args.pipeline__client_pb2 import DataSourceNode
from tecton_proto.data import batch_data_source__client_pb2 as batch_data_source_pb2


@attrs.frozen
class RedshiftDataSourceScanNode(ArrowExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    skew_config: Optional[SkewConfig] = None

    @classmethod
    def from_node_input(cls, query_node: DataSourceScanNode) -> "RedshiftDataSourceScanNode":
        assert isinstance(query_node.ds.batch_source, specs.RedshiftSourceSpec)
        return cls.from_node_inputs(query_node, input_node=NodeRef(query_node))

    def as_str(self):
        return f"RedshiftDataSourceScanNode for {self.ds.name}"

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        try:
            import redshift_connector
        except ImportError:
            msg = "Please install `redshift-connector` package to connect to Redshift."
            raise ImportError(msg)
        batch_source = self.ds.batch_source
        assert isinstance(batch_source, specs.RedshiftSourceSpec)

        host, port, database = self._parse_redshift_endpoint(batch_source.endpoint)
        # Note: keeping use of conf for secrets for parity with the Spark connector
        # TODO: add secrets support to RedshiftConfig
        user = conf.get_or_none("REDSHIFT_USER")
        password = conf.get_or_none("REDSHIFT_PASSWORD")

        # assuming IAM role is authenticated if pw not setup
        if not password:
            is_iam_auth = True
            # db_user is the user required for IAM role to use; 'awsuser' is the default user.
            db_user = user or "awsuser"
            cluster_identifier = host.split(".")[0]
        else:
            is_iam_auth = False
            db_user = None
            cluster_identifier = None

        chunk_size = 100_000
        execute_sql = self.input_node.to_sql()
        try:
            with redshift_connector.connect(
                host=host,
                port=int(port),
                database=database,
                user=user,
                password=password,
                iam=is_iam_auth,
                db_user=db_user,
                cluster_identifier=cluster_identifier,
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(execute_sql)
                    batches = []
                    while True:
                        df_chunk = cursor.fetch_dataframe(num=chunk_size)
                        # Note: if we stop supporting pandas post_processor we can improve the memory redundancy here
                        if batch_source.post_processor:
                            try:
                                df_chunk = batch_source.post_processor(df_chunk)
                            except Exception as e:
                                msg = f"Post processor function of data source `{self.ds.name}` failed with exception: {e}"
                                raise UserCodeError(msg) from e
                        if df_chunk.empty:
                            break
                        record_batch = pyarrow.RecordBatch.from_pandas(df_chunk, preserve_index=False)
                        batches.append(record_batch)
        except redshift_connector.InterfaceError as ie:
            msg = f"Unable to establish a connection with Redshift.\n{ie}"
            raise AccessError(msg) from ie
        except redshift_connector.ProgrammingError as pe:
            raise SQLCompilationError(str(pe), execute_sql) from pe

        if batches:
            return pyarrow.RecordBatchReader.from_batches(batches[0].schema, batches)
        else:
            # Note: may be neater to infer schema from cursor.descriptor (name, type_code)
            empty_batch = pyarrow.RecordBatch.from_pandas(df_chunk, preserve_index=False)
            return pyarrow.RecordBatchReader.from_batches(empty_batch.schema, [empty_batch])

    def _parse_redshift_endpoint(self, endpoint: str) -> Tuple[str, str, str]:
        """
        split endpoint in to separate host, port, database fields
        Example:
        'cluster-name.abc123xyz.us-west-2.redshift.amazonaws.com:5439/my_db'
        cluster-name, 5439, my_db
        """
        host_and_port, database = endpoint.rsplit("/", 1)
        host, port = host_and_port.rsplit(":", 1)
        return host, port, database


@attrs.define
class FileDataSourceScanNode(ArrowExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    skew_config: Optional[SkewConfig] = None

    @classmethod
    def from_node_input(cls, query_node: DataSourceScanNode) -> "FileDataSourceScanNode":
        assert isinstance(query_node.ds.batch_source, specs.FileSourceSpec)
        return cls.from_node_inputs(query_node, input_node=None)

    @property
    def spec(self) -> specs.FileSourceSpec:
        return self.ds.batch_source

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        import duckdb

        file_uri = self.spec.uri
        timestamp_field = self.spec.timestamp_field

        proto_format = self.spec.file_format
        if proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_CSV:
            arrow_format = "csv"
        elif proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_JSON:
            arrow_format = "json"
        elif proto_format == batch_data_source_pb2.FILE_DATA_SOURCE_FORMAT_PARQUET:
            arrow_format = "parquet"
        else:
            raise ValueError(batch_data_source_pb2.FileDataSourceFormat.Name(self.spec.file_format))

        fs, path = pyarrow.fs.FileSystem.from_uri(file_uri)
        if isinstance(fs, pyarrow.fs.S3FileSystem):
            options = BotoOfflineStoreOptionsProvider.static_options()
            if options is not None:
                fs = pyarrow.fs.S3FileSystem(
                    access_key=options.access_key_id,
                    secret_key=options.secret_access_key,
                    session_token=options.session_token,
                    # When created via Filesystem.from_uri, the bucket region will be autodetected. This constructor
                    # does not have a bucket from which it can detect the region, so we need to copy it over from the
                    # previous instance.
                    region=fs.region,
                )

        if self.spec.schema_uri and self.spec.schema_uri.endswith(".parquet"):
            _, schema_path = pyarrow.fs.FileSystem.from_uri(self.spec.schema_uri)
            arrow_schema = pq.read_schema(schema_path, filesystem=fs)

        # There seems to be a bug in Arrow related to the explicit schema:
        # when we pass an explicit schema to `dataset` and both resolution and timezone in the timestamp column
        # don't match the schema in parquet files - filters that are pushed down by DuckDB will not work.
        # It is very likely that we will not guess both resolution and timezone correctly.
        # So we won't pass schema for now.
        elif self.ds.schema and arrow_format != "parquet":
            schema = Schema(self.ds.schema.tecton_schema)
            arrow_schema = tecton_schema_to_arrow_schema(schema)
            if self.spec.timestamp_format:
                # replace timestamp column type with string,
                # we will convert timestamp with DuckDB (see below)
                timestamp_pos = arrow_schema.names.index(timestamp_field)
                arrow_schema = arrow_schema.set(timestamp_pos, pyarrow.field(timestamp_field, pyarrow.string()))
        else:
            arrow_schema = None

        partitioning = None
        partition_filter = None
        # If source supports partitions then only read the relevant partitions
        if (self.start_time or self.end_time) and self.spec.datetime_partition_columns:
            partition_fields = []
            filter_conditions = []
            for i, partition in enumerate(self.spec.datetime_partition_columns):
                partition_col = partition.column_name if partition.column_name else f"_dir_partition_{i}"
                partition_type = None
                partition_value_at_start = None
                partition_value_at_end = None

                if self.start_time:
                    partition_value_at_start, partition_type = _partition_value_and_type_for_time(
                        partition, self.start_time
                    )
                if self.end_time:
                    partition_value_at_end, partition_type = _partition_value_and_type_for_time(
                        partition, self.end_time
                    )

                if partition_value_at_start == partition_value_at_end:
                    # Use the partition path to reduce scanning for metadata when initializing the dataset
                    hive_key = f"{partition.column_name}=" if partition.column_name else ""
                    partition_value = self.start_time.strftime(partition.format_string)
                    path = path.rstrip("/") + f"/{hive_key}{self.start_time.strftime(partition_value)}"
                else:
                    # Otherwise we use a range filter and break so we don't combine hierarchical partition filters
                    partition_fields.append(pyarrow.field(partition_col, partition_type))
                    filter_conditions.append((pyarrow.dataset.field(partition_col) >= partition_value_at_start))
                    filter_conditions.append((pyarrow.dataset.field(partition_col) <= partition_value_at_end))
                    # TODO: combine range filters on hierarchical partitions using nested 'Or' filters
                    break

            # Setup dataset partitioning if we used partition range filters
            if partition_fields:
                partitioning = pyarrow.dataset.partitioning(
                    pyarrow.schema(partition_fields),
                    # default is a directory partition
                    flavor="hive" if self.spec.datetime_partition_columns[0].column_name else None,
                )
                partition_filter = reduce(and_, filter_conditions)

                if arrow_schema:
                    for field in partition_fields:
                        arrow_schema = arrow_schema.append(field)

        file_dataset = pyarrow.dataset.dataset(
            source=path, schema=arrow_schema, filesystem=fs, format=arrow_format, partitioning=partitioning
        )
        fragment_readahead = int(conf.get_or_raise("DUCKDB_FILE_DATA_SOURCE_READ_PARALLEL_FRAGMENTS"))
        reader = pyarrow.RecordBatchReader.from_batches(
            file_dataset.schema, file_dataset.to_batches(filter=partition_filter, fragment_readahead=fragment_readahead)
        )
        if self.spec.post_processor:

            def _map(input_df: pandas.DataFrame) -> pandas.DataFrame:
                try:
                    return self.spec.post_processor(input_df)
                except Exception as exc:
                    msg = f"Post processor function of data source ('{self.spec.name}') failed with exception"
                    raise UserCodeError(msg) from exc

            reader = map_batches(reader, _map)

        # ToDo: consider using pyarrow compute instead
        duckdb_session = duckdb_factory.create_connection()
        relation = duckdb_session.from_arrow(reader)
        column_types = dict(zip(relation.columns, relation.dtypes))

        if column_types[timestamp_field] == duckdb.typing.VARCHAR:
            if self.spec.timestamp_format:
                conversion_exp = f"strptime(\"{timestamp_field}\", '{self.spec.timestamp_format}')"
            else:
                conversion_exp = f'CAST("{timestamp_field}" AS TIMESTAMP)'
            relation = relation.select(f'* REPLACE({conversion_exp} AS "{timestamp_field}")')

        if self.start_time:
            if column_types[timestamp_field] == duckdb.typing.TIMESTAMP_TZ:
                start_time = get_timezone_aware_datetime(self.start_time)
            else:
                start_time = self.start_time.replace(tzinfo=None)
            relation = relation.filter(f"\"{timestamp_field}\" >= '{start_time}'")
        if self.end_time:
            if column_types[timestamp_field] == duckdb.typing.TIMESTAMP_TZ:
                end_time = get_timezone_aware_datetime(self.end_time)
            else:
                end_time = self.end_time.replace(tzinfo=None)
            relation = relation.filter(f"\"{timestamp_field}\" < '{end_time}'")

        return relation.fetch_arrow_reader()

    def as_str(self):
        return f"FileDataSourceScanNode for {self.ds.name}"


@attrs.define
class PushTableSourceScanNode(ArrowExecNode):
    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    skew_config: Optional[SkewConfig] = None

    @classmethod
    def from_node_input(cls, query_node: DataSourceScanNode) -> "PushTableSourceScanNode":
        assert isinstance(query_node.ds.batch_source, specs.PushTableSourceSpec)
        return cls.from_node_inputs(query_node, input_node=None)

    @property
    def spec(self) -> specs.PushTableSourceSpec:
        return self.ds.batch_source

    @property
    def output_partitioning(self):
        return SinglePartition()

    def to_arrow_reader(
        self, context: ExecutionContext, partition_selector: Optional["PartitionSelector"] = None
    ) -> pyarrow.RecordBatchReader:
        from deltalake import DeltaTable

        ds_id = id_helper.IdHelper.from_string(self.ds.id)
        creds = next(
            filter(
                lambda o: o is not None,
                (p.get_s3_options_for_data_source(ds_id) for p in context.offline_store_options_providers),
            ),
            None,
        )
        if not creds:
            msg = f"Unable to retrieve S3 store credentials for data source {self.ds.name}"
            raise Exception(msg)
        storage_options = {
            "AWS_ACCESS_KEY_ID": creds.access_key_id,
            "AWS_SECRET_ACCESS_KEY": creds.secret_access_key,
            "AWS_SESSION_TOKEN": creds.session_token,
            "AWS_S3_LOCKING_PROVIDER": "dynamodb",
            "AWS_REGION": conf.get_or_raise("CLUSTER_REGION"),
        }
        saved_error = None
        for _ in range(20):
            try:
                table = DeltaTable(table_uri=self.spec.ingested_data_location, storage_options=storage_options)
                break
            except OSError as e:
                saved_error = e
                time.sleep(0.1)
        else:
            msg = "Failed to read from S3"
            raise TimeoutError(msg) from saved_error
        ds = table.to_pyarrow_dataset()
        return pyarrow.RecordBatchReader.from_batches(ds.schema, ds.to_batches())

    def as_str(self):
        return f"PushTableSourceScanNode for {self.ds.name}"


def _partition_value_and_type_for_time(
    partition: DatetimePartitionColumnSpec, dt: datetime
) -> Tuple[Union[int, datetime.date], pyarrow.DataType]:
    fmt = partition.format_string
    if fmt == "%-Y" or fmt == "%Y":
        return dt.year, pyarrow.int32()
    elif fmt == "%-m" or fmt == "%m":
        return dt.month, pyarrow.int32()
    elif fmt == "%-d" or fmt == "%d":
        return dt.day, pyarrow.int32()
    elif fmt == "%-H" or fmt == "%H":
        return dt.hour, pyarrow.int32()
    elif fmt == "%Y-%m-%d":
        return dt.date(), pyarrow.date32()
    elif _preserves_lexicographic_order(fmt):
        return dt.strftime(fmt), pyarrow.string()
    else:
        msg = f"Datetime format `{fmt}` not supported for partition column {partition.column_name}"
        raise ValueError(msg)


def _preserves_lexicographic_order(fmt: str) -> bool:
    """
    Heuristic function to check if a datetime format preserves lexicographic order.
    - Ensures components appear in descending significance (`%Y`, `%m`, `%d`, `%H`, `%M`, `%S`).
    """
    ordered_components = ["%Y", "%m", "%d", "%H", "%M", "%S"]
    found_components = [comp for comp in ordered_components if comp in fmt]
    return found_components == sorted(found_components, key=ordered_components.index)


def map_batches(
    input_: pyarrow.RecordBatchReader, map_: Callable[[pandas.DataFrame], pandas.DataFrame]
) -> pyarrow.RecordBatchReader:
    def gen():
        while True:
            try:
                batch = input_.read_next_batch()
            except StopIteration:
                return
            processed = map_(batch.to_pandas())
            yield pyarrow.RecordBatch.from_pandas(processed)

    batches = gen()
    first_batch = next(batches)
    return pyarrow.RecordBatchReader.from_batches(first_batch.schema, itertools.chain([first_batch], batches))
