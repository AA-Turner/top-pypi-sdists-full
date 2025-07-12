import datetime
import enum
import time
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from functools import reduce
from operator import and_
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from urllib.parse import urlparse

import attrs
import pyarrow
import pyarrow.compute
import pyarrow.dataset
import pyarrow.fs

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import time_utils
from tecton_core.aws_credentials import assume_role_fetcher
from tecton_core.errors import TectonInternalError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.query_consts import anchor_time
from tecton_core.specs import FeatureTableSpec
from tecton_core.specs import MaterializedFeatureViewSpec
from tecton_proto.common.aws_credentials__client_pb2 import AwsIamRole
from tecton_proto.common.id__client_pb2 import Id
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion
from tecton_proto.data.feature_view__client_pb2 import DeltaOfflineStoreVersion
from tecton_proto.data.feature_view__client_pb2 import OfflineStoreParams
from tecton_proto.data.feature_view__client_pb2 import ParquetOfflineStoreVersion
from tecton_proto.data.saved_feature_data_frame__client_pb2 import SavedFeatureDataFrame


TIME_PARTITION = "time_partition"
SECONDS_TO_NANOSECONDS = 1000 * 1000 * 1000
CONTINUOUS_PARTITION_SIZE_SECONDS = 86400
DATASET_PARTITION_SIZE = timedelta(days=1)


class PartitionType(str, enum.Enum):
    NONE = "None"  # no partitioning, use for datasets
    DATE_STR = "DateString"
    EPOCH = "Epoch"
    # RAW_TIMESTAMP is only used for Snowflake
    RAW_TIMESTAMP = "RawTimestamp"
    ENTITY_BUCKET = "EntityBucket"


class OfflineStoreType(str, enum.Enum):
    PARQUET = "parquet"
    DELTA = "delta"
    SNOWFLAKE = "snowflake"
    ICEBERG = "iceberg"


@attrs.frozen
class TimestampFormats:
    spark_format: str
    python_format: str


@attrs.frozen
class OfflineStorePartitionParams:
    partition_by: str
    partition_type: PartitionType
    partition_interval: pendulum.duration


def partition_size_for_parquet(fd: FeatureDefinitionWrapper) -> pendulum.Duration:
    if fd.offline_store_params is not None:
        return pendulum.Duration(
            seconds=fd.offline_store_params.parquet.time_partition_size.ToTimedelta().total_seconds()
        )
    elif fd.is_continuous:
        return pendulum.Duration(seconds=CONTINUOUS_PARTITION_SIZE_SECONDS)
    else:
        return fd.min_scheduling_interval


def partition_col_for_parquet(fd: FeatureDefinitionWrapper) -> str:
    offline_store_version = (
        fd.offline_store_params.parquet.version
        if fd.offline_store_params is not None
        else ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1
    )
    if offline_store_version == ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1:
        return TIME_PARTITION if fd.is_continuous else anchor_time()
    elif offline_store_version == ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_2:
        return TIME_PARTITION
    else:
        msg = "unsupported offline store version"
        raise TectonInternalError(msg)


def partition_size_for_delta(fd: FeatureDefinitionWrapper) -> pendulum.Duration:
    if fd.offline_store_params is not None:
        return pendulum.Duration(
            seconds=fd.offline_store_params.delta.time_partition_size.ToTimedelta().total_seconds()
        )
    else:
        return pendulum.Duration(
            seconds=fd.offline_store_config.delta.time_partition_size.ToTimedelta().total_seconds()
        )


def partition_type_for_delta(offline_store_params: Optional[OfflineStoreParams]) -> PartitionType:
    # TODO(TEC-17350): use this method when reading from the offline store
    if (
        offline_store_params is not None
        and offline_store_params.delta.version == DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_2
    ):
        return PartitionType.EPOCH
    else:
        return PartitionType.DATE_STR


DELTA_SUPPORTED_VERSIONS = [
    DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_1,
    DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_2,
]

PARQUET_SUPPORTED_VERSIONS = [
    ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_1,
    ParquetOfflineStoreVersion.PARQUET_OFFLINE_STORE_VERSION_2,
]


def _check_supported_offline_store_version(fd: FeatureDefinitionWrapper) -> None:
    if fd.offline_store_params is None:
        return
    if (
        fd.offline_store_params.HasField("delta")
        and fd.offline_store_params.delta.version not in DELTA_SUPPORTED_VERSIONS
    ):
        msg = (
            f"Unsupported offline store version {fd.offline_store_params.delta.version}. Try upgrading your Tecton SDK."
        )
        raise TectonInternalError(msg)
    if (
        fd.offline_store_params.HasField("parquet")
        and fd.offline_store_params.parquet.version not in PARQUET_SUPPORTED_VERSIONS
    ):
        msg = f"Unsupported offline store version {fd.offline_store_params.parquet.version}. Try upgrading your Tecton SDK."
        raise TectonInternalError(msg)


def get_offline_store_type(fd: FeatureDefinitionWrapper) -> OfflineStoreType:
    # TODO(TEC-15800): Update Snowflake FV protos to have snowflake as their store type
    assert isinstance(fd.fv_spec, (MaterializedFeatureViewSpec, FeatureTableSpec))

    store_type = fd.offline_store_config.WhichOneof("store_type")
    if store_type == OfflineStoreType.PARQUET:
        return OfflineStoreType.PARQUET
    elif store_type == OfflineStoreType.DELTA:
        return OfflineStoreType.DELTA
    elif store_type == OfflineStoreType.ICEBERG:
        return OfflineStoreType.ICEBERG
    else:
        msg = f"Unknown offline store type {store_type}"
        raise TectonInternalError(msg)


def get_time_column_for_offline_reader(fd: FeatureDefinitionWrapper) -> str:
    if (
        get_offline_store_type(fd) == OfflineStoreType.DELTA
        and fd.offline_store_params is not None
        and fd.offline_store_params.delta.version == DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_2
    ):
        return fd.time_key

    if fd.is_temporal_aggregate:
        return anchor_time()

    return fd.time_key


def get_time_column_for_offline_writer(fd: FeatureDefinitionWrapper) -> str:
    if (
        get_offline_store_type(fd) == OfflineStoreType.DELTA
        and fd.offline_store_params is not None
        and fd.offline_store_params.delta.version == DeltaOfflineStoreVersion.DELTA_OFFLINE_STORE_VERSION_2
    ):
        return fd.materialization_job_partition_timestamp

    if fd.is_temporal_aggregate:
        return anchor_time()

    return fd.materialization_job_partition_timestamp


def get_offline_store_partition_params(feature_definition: FeatureDefinitionWrapper) -> OfflineStorePartitionParams:
    # Examples of how our offline store is partitioned
    ### Compaction FV on Delta Version 2
    # Partition Column: time_partition
    # Partition Column Type: Epoch Long
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]
    # Note the timestamp column is always saved here because compaction fvs have an untiled offline store.

    ### FV w/out Aggregations on Delta Version 1
    # Partition Column: time_partition
    # Partition Column Type: Date String
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]

    ### FV w/ Aggregations on Delta Version 1
    # Partition Column: time_partition
    # Partition Column Type: Date String
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]

    ### Continuous Stream FV with Aggregations on Parquet Version 1
    # Partition Column: time_partition
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]
    # Note: Very weird that we have a timestamp parquet column here - redundant with _anchor_time

    ### BFV w/ Aggregations on Parquet Version 1
    # Partition Column: _anchor_time
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]
    # !! In this case we need to drop the partition column from the top level columns

    ### BFV w/out Aggregations on Parquet Version 1
    # Partition Column: _anchor_time
    # Materialized Columns: ts, [join_keys], [feature_columns]

    ### Any FV on Snowflake
    # Partition Column: none
    # Materialized Columns: ts, [join_keys], [feature_columns]

    _check_supported_offline_store_version(feature_definition)
    store_type = get_offline_store_type(feature_definition)

    if store_type == OfflineStoreType.DELTA:
        partition_by = TIME_PARTITION
        partition_type = partition_type_for_delta(feature_definition.offline_store_params)
        partition_interval = partition_size_for_delta(feature_definition)
    elif store_type == OfflineStoreType.PARQUET:
        partition_by = partition_col_for_parquet(feature_definition)
        partition_type = PartitionType.EPOCH
        partition_interval = partition_size_for_parquet(feature_definition)
    elif store_type == OfflineStoreType.ICEBERG:
        partition_by = EntityBucketPartitionParams.partition_by
        partition_type = PartitionType.ENTITY_BUCKET
        partition_interval = pendulum.Duration(seconds=CONTINUOUS_PARTITION_SIZE_SECONDS)
    else:
        msg = f"Unexpected offline store config {store_type}"
        raise ValueError(msg)
    return OfflineStorePartitionParams(partition_by, partition_type, partition_interval)


def timestamp_to_partition_date_str(timestamp: pendulum.DateTime, partition_params: OfflineStorePartitionParams) -> str:
    partition_interval_timedelta = partition_params.partition_interval.as_timedelta()
    aligned_time = time_utils.align_time_downwards(timestamp, partition_interval_timedelta)
    partition_format = timestamp_formats(partition_interval_timedelta).python_format
    return aligned_time.strftime(partition_format)


def timestamp_to_partition_epoch(
    timestamp: pendulum.DateTime,
    partition_params: OfflineStorePartitionParams,
    feature_store_format_version: int,
) -> int:
    aligned_time = time_utils.align_time_downwards(timestamp, partition_params.partition_interval.as_timedelta())
    # align_time_downwards returns the time without tzinfo. convert_timestamp_for_version calls timestamp() which
    # treats naive datetime instances as local time. This can cause an issue if local time is not in UTC.
    aligned_time = aligned_time.replace(tzinfo=datetime.timezone.utc)
    return time_utils.convert_timestamp_for_version(aligned_time, feature_store_format_version)


def window_size_seconds(window: Union[timedelta, pendulum.Duration]) -> int:
    if isinstance(window, pendulum.Duration):
        window = window.as_timedelta()
    if window % timedelta(seconds=1) != timedelta(0):
        msg = f"partition_size is not a round number of seconds: {window}"
        raise AssertionError(msg)
    return int(window.total_seconds())


def timestamp_formats(partition_size: timedelta) -> TimestampFormats:
    if partition_size % timedelta(days=1) == timedelta(0):
        return TimestampFormats(spark_format="yyyy-MM-dd", python_format="%Y-%m-%d")
    else:
        return TimestampFormats(spark_format="yyyy-MM-dd-HH:mm:ss", python_format="%Y-%m-%d-%H:%M:%S")


def datetime_to_partition_str(dt: datetime, partition_size: timedelta) -> str:
    partition_format = timestamp_formats(partition_size).python_format
    return dt.strftime(partition_format)


@dataclass
class OfflineStoreReaderParams:
    delta_table_uri: str
    partition_size: timedelta
    storage_options: Callable[[], Optional["S3Options"]]
    partition_type: Optional[PartitionType] = None
    feature_store_format_version: int = FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT

    @classmethod
    def for_feature_definition(
        cls,
        fd: FeatureDefinitionWrapper,
        delta_table_uri: str,
        options_providers: Iterable["OfflineStoreOptionsProvider"],
    ) -> "OfflineStoreReaderParams":
        def storage_options() -> Optional[S3Options]:
            if delta_table_uri.startswith("s3"):
                return get_s3_options_for_fd(fd, options_providers)

            return None

        return OfflineStoreReaderParams(
            delta_table_uri=delta_table_uri,
            partition_size=partition_size_for_delta(fd).as_timedelta(),
            storage_options=storage_options,
            partition_type=partition_type_for_delta(fd.offline_store_params),
            feature_store_format_version=fd.get_feature_store_format_version,
        )

    @classmethod
    def for_dataset(
        cls,
        dataset: SavedFeatureDataFrame,
        delta_table_uri: str,
        options_providers: Iterable["OfflineStoreOptionsProvider"],
    ) -> "OfflineStoreReaderParams":
        def storage_options() -> Optional[S3Options]:
            if delta_table_uri.startswith("s3"):
                return get_s3_options_for_dataset(dataset, options_providers)

            return None

        return OfflineStoreReaderParams(
            delta_table_uri=delta_table_uri, partition_size=DATASET_PARTITION_SIZE, storage_options=storage_options
        )


@dataclass
class JoinKeyBoundaries:
    min: Union[int, str]
    max: Union[int, str]


class OfflineStoreReader(ABC):
    @abstractmethod
    def read(
        self,
        partition_time_limits: Optional[pendulum.Period] = None,
        join_keys_limits: Optional[Dict[str, JoinKeyBoundaries]] = None,
    ) -> "pyarrow.dataset.Dataset":
        raise NotImplementedError


class S3OptionsSource(enum.Enum):
    LOCAL = 1
    MDS = 2


@dataclass
class S3Options:
    access_key_id: str
    secret_access_key: str
    session_token: Optional[str]
    options_source: S3OptionsSource
    region: Optional[str] = None

    def to_dict(self):
        opts = {
            "AWS_ACCESS_KEY_ID": self.access_key_id,
            "AWS_SECRET_ACCESS_KEY": self.secret_access_key,
        }
        if self.session_token:
            opts["AWS_SESSION_TOKEN"] = self.session_token
        if self.region:
            opts["AWS_REGION"] = self.region
        return opts


class OfflineStoreOptionsProvider:
    def get_s3_options_for_feature_view(self, feature_view_id: Id) -> Optional[S3Options]:
        return

    def get_s3_options_for_data_source(self, data_source_id: Id) -> Optional[S3Options]:
        return

    def get_s3_options_for_dataset(self, dataset_id: Id) -> Optional[S3Options]:
        return


class BotoOfflineStoreOptionsProvider(OfflineStoreOptionsProvider):
    """deltalake's built-in S3 auth is implemented by a Rust library which doesn't support the full range of AWS
    auth configurations supported by boto, which can be surprising to users used to boto's options. This class
    following does a fully-featured auth using boto instead of depending on Rust.

    See also https://github.com/delta-io/delta-rs/issues/855
    """

    @staticmethod
    def static_options(assume_role: Optional[AwsIamRole] = None) -> Optional[S3Options]:
        import boto3

        if assume_role:
            return BotoOfflineStoreOptionsProvider._cross_account_options(assume_role)

        # Sometimes we receive None credentials. The reason is still unclear, so we retry 3 times for now.
        session = boto3.Session()
        credentials = None
        for _ in range(3):
            credentials = session.get_credentials()
            if credentials is not None:
                break
            if conf.get_bool("TECTON_DEBUG"):
                print("Failed to fetch offline store credentials. Retrying...")
            # Short sleep because for some notebook cases, the credentials are supposed to be None.
            time.sleep(0.1)
        if credentials is None:
            return None
        current_credentials = credentials.get_frozen_credentials()
        return S3Options(
            access_key_id=current_credentials.access_key,
            secret_access_key=current_credentials.secret_key,
            session_token=current_credentials.token,
            options_source=S3OptionsSource.LOCAL,
            region=conf.get_or_none("CLUSTER_REGION"),
        )

    @staticmethod
    def _cross_account_options(assume_role: AwsIamRole) -> Optional[S3Options]:
        credentials = assume_role_fetcher(
            assume_role, session_name=f"CrossAccountSession-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        ).fetch_credentials()
        return S3Options(
            access_key_id=credentials["access_key"],
            secret_access_key=credentials["secret_key"],
            session_token=credentials["token"],
            options_source=S3OptionsSource.LOCAL,
            region=conf.get_or_none("CLUSTER_REGION"),
        )

    def get_s3_options_for_feature_view(self, feature_view_id: Id) -> Optional[S3Options]:
        return BotoOfflineStoreOptionsProvider.static_options()

    def get_s3_options_for_data_source(self, data_source_id: Id) -> Optional[S3Options]:
        return BotoOfflineStoreOptionsProvider.static_options()

    def get_s3_options_for_dataset(self, dataset_id: Id) -> Optional[S3Options]:
        return BotoOfflineStoreOptionsProvider.static_options()


DEFAULT_OPTIONS_PROVIDERS = [BotoOfflineStoreOptionsProvider()]


def get_s3_options_for_fd(
    fd: FeatureDefinitionWrapper, options_providers: Iterable[OfflineStoreOptionsProvider]
) -> S3Options:
    fvid = id_helper.IdHelper.from_string(fd.id)
    options = next(
        filter(lambda o: o is not None, (p.get_s3_options_for_feature_view(fvid) for p in options_providers)), None
    )
    if options is None:
        msg = f"Unable to retrieve S3 store credentials for feature view {fd.name}."
        raise ValueError(msg)

    return options


def get_s3_options_for_dataset(
    ds: SavedFeatureDataFrame, options_providers: Iterable[OfflineStoreOptionsProvider]
) -> S3Options:
    dsid = ds.saved_feature_dataframe_id
    options = next(
        filter(lambda o: o is not None, (p.get_s3_options_for_dataset(dsid) for p in options_providers)), None
    )
    if options is None:
        msg = f"Unable to retrieve S3 store credentials for dataset {ds.info.name}."
        raise ValueError(msg)

    return options


def patch_timestamps_in_arrow_schema(schema: pyarrow.Schema) -> pyarrow.Schema:
    """Patches schema to replace tz-naive columns with UTC timestamps"""
    for idx, field in enumerate(schema):
        if isinstance(field.type, pyarrow.TimestampType) and field.type.tz is None:
            schema = schema.set(idx, pyarrow.field(field.name, pyarrow.timestamp(field.type.unit, "UTC")))
    return schema


class DeltaReader(OfflineStoreReader):
    def __init__(
        self,
        params: OfflineStoreReaderParams,
    ) -> None:
        self._params = params

    @property
    def _table(self):
        # TODO(TEC-16757): Move import to top of file.
        try:
            from deltalake import DeltaTable
        except ImportError:
            msg = (
                "Couldn't initialize Rift compute. "
                "To use Rift install all Rift dependencies first by executing `pip install tecton[rift]`."
            )
            raise RuntimeError(msg)

        options = self._params.storage_options()
        options_dict = {}
        if options:
            options_dict = options.to_dict()

        # Sometimes the backend credentials we receive are not considered valid by S3 for some time. We want to silently
        # retry until they become valid when this happens.
        #
        # This is done in a rather crude way here. It would be better to test the credentials out using boto3 which is
        # faster/gives us more granular errors, but inexplicably there are at least some cases where the credentials
        # work with boto3 but then later fail when passed to Delta.
        saved_error = None
        for _ in range(20):
            try:
                return DeltaTable(table_uri=self._params.delta_table_uri, storage_options=options_dict)
            except OSError as e:
                saved_error = e
                time.sleep(0.1)
        msg = "Failed to read from S3"
        if not options or S3OptionsSource.LOCAL == options.options_source:
            msg = "Failed to read from S3 using user-provided AWS credentials"
        elif S3OptionsSource.MDS == options.options_source:
            msg = "Failed to read from S3 using Tecton-provided temporary credentials"
        raise TimeoutError(msg) from saved_error

    def _partition_filter(
        self, partition_time_limits: Optional[pendulum.Period] = None
    ) -> Optional[List[Tuple[str, str, str]]]:
        partition_size = self._params.partition_size
        if partition_time_limits is None or not partition_size:
            return

        filters = []
        aligned_start_time = time_utils.align_time_downwards(partition_time_limits.start, partition_size)
        aligned_end_time = time_utils.align_time_downwards(partition_time_limits.end, partition_size)
        if self._params.partition_type == PartitionType.EPOCH:
            start_partition = str(
                time_utils.convert_timestamp_for_version(aligned_start_time, self._params.feature_store_format_version)
            )
            end_partition = str(
                time_utils.convert_timestamp_for_version(aligned_end_time, self._params.feature_store_format_version)
            )
        else:
            start_partition = datetime_to_partition_str(aligned_start_time, partition_size)
            end_partition = datetime_to_partition_str(aligned_end_time, partition_size)
        filters.append((TIME_PARTITION, ">=", start_partition))
        filters.append((TIME_PARTITION, "<=", end_partition))
        return filters

    def _join_keys_filter(
        self, join_keys_limits: Optional[Dict[str, JoinKeyBoundaries]] = None
    ) -> Optional[pyarrow.dataset.Expression]:
        if not join_keys_limits:
            return

        conditions = []
        for join_key, boundaries in join_keys_limits.items():
            if boundaries.min is not None:
                conditions.append(pyarrow.compute.field(join_key) >= boundaries.min)

            if boundaries.max is not None:
                conditions.append(pyarrow.compute.field(join_key) <= boundaries.max)

        return reduce(and_, conditions)

    def read(
        self,
        partition_time_limits: Optional[pendulum.Period] = None,
        join_keys_limits: Optional[Dict[str, JoinKeyBoundaries]] = None,
    ) -> "pyarrow.dataset.Dataset":
        fs = None
        if conf.get_bool("DUCKDB_USE_PYARROW_FILESYSTEM"):
            fs, path = pyarrow.fs.FileSystem.from_uri(self._params.delta_table_uri)

            if isinstance(fs, pyarrow.fs.S3FileSystem):
                options = self._params.storage_options()
                fs = pyarrow.fs.S3FileSystem(
                    access_key=options.access_key_id,
                    secret_key=options.secret_access_key,
                    session_token=options.session_token,
                )
            fs = pyarrow.fs.SubTreeFileSystem(path, fs)

        ds = self._table.to_pyarrow_dataset(partitions=self._partition_filter(partition_time_limits), filesystem=fs)
        fragments = ds.get_fragments(filter=self._join_keys_filter(join_keys_limits))
        schema = patch_timestamps_in_arrow_schema(ds.schema)
        return pyarrow.dataset.FileSystemDataset(fragments, schema, ds.format, ds.filesystem)


class ParquetReader(OfflineStoreReader):
    def __init__(
        self,
        fd: FeatureDefinitionWrapper,
        options_providers: Iterable[OfflineStoreOptionsProvider],
    ) -> None:
        self._fd = fd
        self._options_providers = options_providers
        self._partition_params = get_offline_store_partition_params(self._fd)

    def _partition_column_type(self):
        return pyarrow.int64() if self._partition_params.partition_type == PartitionType.EPOCH else pyarrow.string()

    def _filesystem_and_uri(self) -> Tuple[pyarrow.fs.FileSystem, str]:
        uri = self._fd.materialized_data_path
        fs, path = pyarrow.fs.FileSystem.from_uri(uri)

        if isinstance(fs, pyarrow.fs.S3FileSystem):
            options = get_s3_options_for_fd(self._fd, self._options_providers)

            return (
                pyarrow.fs.S3FileSystem(
                    access_key=options.access_key_id,
                    secret_key=options.secret_access_key,
                    session_token=options.session_token,
                ),
                path,
            )

        return fs, path

    def _filter(self, partition_time_limits: Optional[pendulum.Period]) -> pyarrow.dataset.Expression:
        if not partition_time_limits:
            return

        start_partition = timestamp_to_partition_epoch(
            partition_time_limits.start,
            self._partition_params,
            self._fd.get_feature_store_format_version,
        )
        end_partition = timestamp_to_partition_epoch(
            partition_time_limits.end,
            self._partition_params,
            self._fd.get_feature_store_format_version,
        )
        column = pyarrow.compute.field(self._partition_params.partition_by)
        return (column >= start_partition) & (column <= end_partition)

    def read(
        self,
        partition_time_limits: Optional[pendulum.Period] = None,
        join_keys_limits: Optional[Dict[str, JoinKeyBoundaries]] = None,
    ) -> "pyarrow.dataset.Dataset":
        partitioning = pyarrow.dataset.partitioning(
            pyarrow.schema([(self._partition_params.partition_by, self._partition_column_type())]), flavor="hive"
        )
        fs, uri = self._filesystem_and_uri()

        # to match DeltaReader output we use SubTreeFileSystem,
        # so that fragments will have local path relative to offline store root
        sub_fs = pyarrow.fs.SubTreeFileSystem(uri, fs)

        # We had to use an explicit dataset creation (via FileSystemDatasetFactory)
        # to override default `selector_ignore_prefixes` parameter.
        # The default behaviour is to ignore directories/files starting with ["_", "."],
        # and we use column `_anchor_time` as a partition column.
        selector = pyarrow.fs.FileSelector("", recursive=True)
        file_format = pyarrow.dataset.ParquetFileFormat()
        options = pyarrow.dataset.FileSystemFactoryOptions(
            partitioning=partitioning,
            selector_ignore_prefixes=[".", "_SUCCESS", "_committed", "_started"],
        )
        factory = pyarrow.dataset.FileSystemDatasetFactory(sub_fs, selector, file_format, options)
        # probe for schema inference (read it from the first file)
        schema = factory.finish().schema
        # now actually create dataset with patched schema
        return factory.finish(schema=patch_timestamps_in_arrow_schema(schema))


class EntityBucketPartitionParams(OfflineStorePartitionParams):
    partition_by: str = "entity_bucket"
    partition_type: PartitionType = PartitionType.ENTITY_BUCKET
    partition_interval: pendulum.duration = None  # not relevant for entity bucket partitioning


class IcebergReader(OfflineStoreReader):
    def __init__(
        self,
        fdw: FeatureDefinitionWrapper,
        s3_options: Optional[S3Options] = None,
    ) -> None:
        # TODO: move these out to file scope once pyiceberg is a `tecton` dependency
        from pyiceberg.io import S3_ACCESS_KEY_ID
        from pyiceberg.io import S3_REGION
        from pyiceberg.io import S3_SECRET_ACCESS_KEY
        from pyiceberg.io import S3_SESSION_TOKEN

        from tecton_core.iceberg_catalog import MetadataCatalog

        assert fdw.has_iceberg_offline_store, (
            f"Feature view `{fdw.name}` must be configured to use Iceberg offline store."
        )
        self._fdw = fdw
        self._s3_options = s3_options
        catalog_properties = {}
        if s3_options:
            catalog_properties = {
                S3_ACCESS_KEY_ID: s3_options.access_key_id,
                S3_SECRET_ACCESS_KEY: s3_options.secret_access_key,
                S3_SESSION_TOKEN: s3_options.session_token,
                S3_REGION: s3_options.region,
            }

        self._catalog = MetadataCatalog(name="object_store_catalog", properties=catalog_properties)

    def read(
        self,
        time_limits: Optional[pendulum.Period] = None,
        join_keys_buckets: Optional[List[int]] = None,
    ) -> "pyarrow.dataset.Dataset":
        fs, _ = pyarrow.fs.FileSystem.from_uri(self._fdw.materialized_data_path)

        if isinstance(fs, pyarrow.fs.S3FileSystem) and self._s3_options:
            fs = pyarrow.fs.S3FileSystem(
                access_key=self._s3_options.access_key_id,
                secret_key=self._s3_options.secret_access_key,
                session_token=self._s3_options.session_token,
            )

        files_to_read = [path_from_uri(uri) for uri in self.get_files_to_read(time_limits, join_keys_buckets)]
        tbl = self._catalog.load_table(self._fdw.materialized_data_path)
        schema = tbl.schema().as_arrow()
        file_format = pyarrow.dataset.ParquetFileFormat()
        factory = pyarrow.dataset.FileSystemDatasetFactory(fs, files_to_read, file_format)

        return factory.finish(schema)

    def get_files_to_read(
        self,
        time_limits: Optional[pendulum.Period] = None,
        join_keys_buckets: Optional[List[int]] = None,
    ) -> List[str]:
        from pyiceberg.expressions import And
        from pyiceberg.expressions import GreaterThanOrEqual
        from pyiceberg.expressions import In
        from pyiceberg.expressions import LessThan
        from pyiceberg.expressions.literals import TimestampLiteral
        from pyiceberg.table import ALWAYS_TRUE
        from pyiceberg.utils.datetime import timestamptz_to_micros

        tbl = self._catalog.load_table(self._fdw.materialized_data_path)

        predicate = ALWAYS_TRUE
        if time_limits:
            if self._fdw.is_temporal_aggregate:
                start_time = time_utils.convert_timestamp_for_version(
                    time_limits.start, self._fdw.get_batch_schedule_for_version
                )
                end_time = time_utils.convert_timestamp_for_version(
                    time_limits.end, self._fdw.get_batch_schedule_for_version
                )
                predicate = And(GreaterThanOrEqual(anchor_time(), start_time), LessThan(anchor_time(), end_time))
            else:
                start_time_str = time_limits.start.isoformat()
                end_time_str = time_limits.end.isoformat()
                start_time_lit = TimestampLiteral(timestamptz_to_micros(start_time_str))
                end_time_lit = TimestampLiteral(timestamptz_to_micros(end_time_str))
                predicate = And(
                    GreaterThanOrEqual(self._fdw.timestamp_key, start_time_lit),
                    LessThan(self._fdw.timestamp_key, end_time_lit),
                )

        if join_keys_buckets:
            predicate = And(predicate, In(EntityBucketPartitionParams.partition_by, join_keys_buckets))

        plan_files = tbl.scan(
            row_filter=predicate,
        ).plan_files()
        paths = [file_scan.file.file_path for file_scan in plan_files]
        return paths


def path_from_uri(uri):
    parts = urlparse(uri)
    return parts.netloc + parts.path
