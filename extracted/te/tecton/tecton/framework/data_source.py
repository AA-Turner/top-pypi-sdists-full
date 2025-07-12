from __future__ import annotations

import datetime
import json
import logging
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union

import attrs
import pandas
from pyspark.sql import dataframe as pyspark_dataframe
from pyspark.sql import streaming as pyspark_streaming
from typeguard import typechecked

from tecton import types
from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import querytree_api
from tecton._internals import sdk_decorators
from tecton._internals import spark_api
from tecton._internals import type_utils
from tecton._internals import validations_api
from tecton._internals.ingestion import IngestionClient
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework import data_frame
from tecton.framework import repo_config
from tecton_core import conf
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.compute_mode import offline_retrieval_compute_mode
from tecton_core.filter_utils import FilterDateTime
from tecton_core.filter_utils import TectonTimeConstant
from tecton_core.repo_file_handler import construct_fco_source_info
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import fco_args__client_pb2 as fco_args_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type__client_pb2 as data_source_type_pb2
from tecton_proto.common import fco_locator__client_pb2 as fco_locator_pb2
from tecton_proto.common import schema_container__client_pb2 as schema_container_pb2
from tecton_proto.common import spark_schema__client_pb2 as spark_schema_pb2
from tecton_proto.common.spark_schema__client_pb2 import SparkSchema
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2
from tecton_spark import spark_schema_wrapper


BatchConfigType = Union[
    configs.FileConfig,
    configs.HiveConfig,
    configs.RedshiftConfig,
    configs.SnowflakeConfig,
    configs.SparkBatchConfig,
    configs.UnityConfig,
    configs.PandasBatchConfig,
    configs.BigQueryConfig,
    configs.PyArrowBatchConfig,
]

StreamConfigType = Union[configs.KinesisConfig, configs.KafkaConfig, configs.SparkStreamConfig, configs.PushConfig]

logger = logging.getLogger(__name__)


@attrs.define(eq=False)
class DataSource(base_tecton_object.BaseTectonObject):
    """Base class for Data Source classes."""

    # A data source spec, i.e. a dataclass representation of the Tecton object that is used in most functional use
    # cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e. applied
    # objects fetched from the backend, are assumed valid.
    _spec: Optional[specs.DataSourceSpec] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and
    # fetched from the Tecton backend.
    _args: Optional[virtual_data_source__args_pb2.VirtualDataSourceArgs] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    # A supplement to the _args proto that is needed to create the Data Source spec.
    _args_supplement: Optional[specs.DataSourceSpecArgsSupplement] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    @sdk_decorators.assert_local_object
    def _build_and_resolve_args(self, objects) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(virtual_data_source=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                virtual_data_source=validator_pb2.VirtualDataSourceValidationArgs(
                    args=self._args,
                    batch_schema=self._args_supplement.batch_schema,
                    stream_schema=self._args_supplement.stream_schema,
                )
            )
        else:
            return self._spec.validation_args

    def _validate(self) -> None:
        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
        )

    def _populate_spec(self):
        # TODO(TEC-19869): Remove dependencies on this field, either switching to lazy-evaluation
        # if relevant or removing. We no longer eagerly derive the schema for datasources, so it
        # is not usable.
        self._args_supplement.batch_schema = spark_schema_pb2.SparkSchema()
        self._args_supplement.stream_schema = spark_schema_pb2.SparkSchema()
        self._spec = specs.DataSourceSpec.from_args_proto(self._args, self._args_supplement)

    @sdk_decorators.assert_local_object
    def _create_unvalidated_spec(
        self, mock_data: Union[pandas.DataFrame, pyspark_dataframe.DataFrame]
    ) -> specs.DataSourceSpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        if is_pyspark_df(mock_data):
            schema = spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(mock_data.schema)
        elif isinstance(mock_data, pandas.DataFrame):
            # Using a empty schema for Rift, since Rift does not use the schema for batch sources.
            schema = SparkSchema()
        else:
            msg = f"Unexpected mock source type {type(mock_data)}"
            raise TypeError(msg)
        # Use the mock schema as both the batch and stream schema because StreamSource specs expect a non-nil stream
        # schema.
        supplement = attrs.evolve(self._args_supplement, batch_schema=schema, stream_schema=schema)
        return specs.DataSourceSpec.from_args_proto(self._args, supplement)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human-readable summary."""
        request = metadata_service_pb2.GetVirtualDataSourceSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetVirtualDataSourceSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.sdk_public_method
    def get_dataframe(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        *,
        apply_translator: bool = True,
        compute_mode: Optional[Union[ComputeMode, str]] = None,
    ) -> data_frame.TectonDataFrame:
        """Returns the data in this Data Source as a Tecton DataFrame.

        :param start_time: The interval start time from when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param end_time: The interval end time until when we want to retrieve source data.
            If no timezone is specified, will default to using UTC.
            Can only be defined if ``apply_translator`` is True.
        :param apply_translator: If True, the transformation specified by ``post_processor``
            will be applied to the dataframe for the data source. ``apply_translator`` is not applicable
            to batch sources configured with ``spark_batch_config`` because it does not have a
            ``post_processor``.
        :param compute_mode: Compute mode to use to produce the data frame.

        :return: A Tecton DataFrame containing the data source's raw or translated source data.

        :raises TectonValidationError: If ``apply_translator`` is False, but ``start_time`` or
            ``end_time`` filters are passed in.
        """
        compute_mode = offline_retrieval_compute_mode(compute_mode)
        _apply_translator = apply_translator
        if self._spec.type == data_source_type_pb2.DataSourceType.PUSH_NO_BATCH:
            if self._args is not None:
                # Object defined locally, and we can't really call get_dataframe on that.
                raise errors.DATA_SOURCE_HAS_NO_BATCH_CONFIG(self.name)
            else:
                _apply_translator = False

        return querytree_api.get_dataframe_for_data_source(
            compute_mode.default_dialect(), compute_mode, self._spec, start_time, end_time, _apply_translator
        )

    @property
    def data_source_type(self) -> data_source_type_pb2.DataSourceType.ValueType:
        return self._spec.type

    @property
    def data_delay(self) -> Optional[datetime.timedelta]:
        """Returns the duration that materialization jobs wait after the ``batch_schedule`` before starting, typically to ensure that all data has landed."""
        return self._spec.batch_source.data_delay if self._spec.batch_source is not None else None

    @property
    def prevent_destroy(self) -> bool:
        """Return whether entity has prevent_destroy flagged"""
        return self._spec.prevent_destroy

    @property
    def _options(self) -> Mapping[str, str]:
        """Return options set on initialization used for configuration. Advanced use cases and beta features."""
        return self._spec.options

    def select_range(
        self,
        start_time: Union[datetime.datetime, FilterDateTime, TectonTimeConstant],
        end_time: Union[datetime.datetime, FilterDateTime, TectonTimeConstant],
    ) -> FilteredSource:
        """
        Returns this DataSource object wrapped as a FilteredSource. FilteredSources will automatically pre-filter sources in Feature View definitions and can reduce compute costs.

        Calling select_range() with no arguments returns an unfiltered source and is equivalent to
        source.unfiltered().

        ```python
        #  The following example demonstrates how to use select_range to filter a source to only include data from
        #  7 days before MATERIALIZATION_END_TIME.
        @batch_feature_view(
            ...
            sources=[
                transactions_source.select_range(
                    start_time=TectonTimeConstant.MATERIALIZATION_END_TIME - timedelta(days=7),
                    end_time=TectonTimeConstant.MATERIALIZATION_END_TIME
                )
            ]
            ...
        )
        ```

        ```python
        # The following example filters all source data from 2020/1/1
        @batch_feature_view(
            ...
            sources=[
                transactions_source.select_range(
                    start_time=datetime.datetime(2020, 1, 1),
                    end_time=TectonTimeConstant.UNBOUNDED_FUTURE
                )
            ]
            ...
        )
        ```

        :param start_time: The start time of the filter. Can be a datetime or TectonTimeConstant optionally offset by a timedelta.
        :param end_time: The end time of the filter. Can be a datetime or TectonTimeConstant optionally offset by a timedelta.

        :return: A FilteredSource object that can be passed into a Feature View.
        """
        if isinstance(start_time, datetime.datetime) and isinstance(end_time, datetime.datetime):
            if start_time > end_time:
                msg = "start_time must be less than or equal to end_time"
                raise ValueError(msg)

        if isinstance(start_time, datetime.datetime):
            start_time = FilterDateTime(timestamp=start_time)
        elif isinstance(start_time, TectonTimeConstant):
            if start_time == TectonTimeConstant.UNBOUNDED_FUTURE:
                msg = "start_time cannot be UNBOUNDED_FUTURE"
                raise ValueError(msg)
            start_time = FilterDateTime(time_reference=start_time)

        if isinstance(end_time, datetime.datetime):
            end_time = FilterDateTime(timestamp=end_time)
        elif isinstance(end_time, TectonTimeConstant):
            if end_time == TectonTimeConstant.UNBOUNDED_PAST:
                msg = "end_time cannot be UNBOUNDED_PAST"
                raise ValueError(msg)
            end_time = FilterDateTime(time_reference=end_time)

        return FilteredSource(self, start_time=start_time, end_time=end_time)

    def unfiltered(self) -> FilteredSource:
        """
        Return an unfiltered DataSource. This scope will make an entire source available to a Feature View, but can increase compute costs as a result.
        """
        start_time = FilterDateTime(time_reference=TectonTimeConstant.UNBOUNDED_PAST)
        end_time = FilterDateTime(time_reference=TectonTimeConstant.UNBOUNDED_FUTURE)
        return FilteredSource(self, start_time=start_time, end_time=end_time)


@attrs.define(eq=False)
class BatchSource(DataSource):
    """A Tecton BatchSource, used to read batch data into Tecton for use in a BatchFeatureView.

    Example of a BatchSource declaration:

    ```python
    # Declare a BatchSource with a HiveConfig instance as its batch_config parameter.
    # Refer to the "Configs Classes and Helpers" section for other batch_config types.
    from tecton import HiveConfig, BatchSource

    credit_scores_batch = BatchSource(
        name='credit_scores_batch',
        batch_config=HiveConfig(
            database='demo_fraud',
            table='credit_scores',
            timestamp_field='timestamp'
        ),
        owner='matt@tecton.ai',
        tags={'release': 'production'}
    )
    ```
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: BatchConfigType,
        options: Optional[Dict[str, str]] = None,
    ):
        """Creates a new BatchSource.

        :param name: A unique name of the DataSource.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Data Source (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent
            accidental changes such as inadvertantly deleting a Feature Service used in production or recreating a Feature
            View that triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton
            objects that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param batch_config: BatchConfig object containing the configuration of the Batch Data Source to be included
            in this Data Source.
        :param options: Additional options to configure the Source. Used for advanced use cases and beta features.
        """
        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=self._framework_version.value,
            type=data_source_type_pb2.DataSourceType.BATCH,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        batch_config._merge_batch_args(ds_args)

        info = base_tecton_object.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "BatchSource":
        """Create a BatchSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        # override the framework version class attribute to be the framework version set by the spec
        class BatchSourceFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = BatchSourceFromSpec.__new__(BatchSourceFromSpec)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj


@attrs.define(eq=False)
class StreamSource(DataSource):
    """A Tecton StreamSource, used to unify stream and batch data into Tecton for use in a StreamFeatureView.

    ```python
        import pyspark
        from tecton import KinesisConfig, HiveConfig, StreamSource
        from datetime import timedelta


        # Define our deserialization raw stream translator
        def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
            from pyspark.sql.functions import col, from_json, from_utc_timestamp
            from pyspark.sql.types import StructType, StringType

            payload_schema = (
              StructType()
                    .add('amount', StringType(), False)
                    .add('isFraud', StringType(), False)
                    .add('timestamp', StringType(), False)
            )
            return (
                df.selectExpr('cast (data as STRING) jsonData')
                .select(from_json('jsonData', payload_schema).alias('payload'))
                .select(
                    col('payload.amount').cast('long').alias('amount'),
                    col('payload.isFraud').cast('long').alias('isFraud'),
                    from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                )
            )

        # Declare a StreamSource with both a batch_config and a stream_config as parameters
        # See the API documentation for both BatchConfig and StreamConfig
        transactions_stream = StreamSource(
            name='transactions_stream',
            stream_config=KinesisConfig(
                stream_name='transaction_events',
                region='us-west-2',
                initial_stream_position='latest',
                watermark_delay_threshold=timedelta(minutes=30),
                timestamp_field='timestamp',
                post_processor=raw_data_deserialization, # deserialization function defined above
                options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
            ),
            batch_config=HiveConfig(
                database='demo_fraud',
                table='transactions',
                timestamp_field='timestamp',
            ),
            owner='user@tecton.ai',
            tags={'release': 'staging'}
        )
    ```
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        batch_config: Optional[BatchConfigType] = None,
        stream_config: StreamConfigType,
        options: Optional[Dict[str, str]] = None,
        schema: Optional[List[types.Field]] = None,
    ):
        """Creates a new StreamSource.

        :param name: A unique name of the DataSource.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param batch_config: BatchConfig object containing the configuration of the Batch Data Source that backs this
            Tecton Stream Source. This field is optional only if `stream_config` is a PushConfig.
        :param stream_config: StreamConfig object containing the configuration of the
            Stream Data Source that backs this Tecton Stream Source.
        :param options: Additional options to configure the Source. Used for advanced use cases and beta features.
        :param schema: A schema for the StreamSource. If not provided, the schema will be inferred from the underlying batch source.
            Right now, schemas can only be specified for StreamSources with a PushConfig, and that's also why the schema must be a list of Tecton types.
        """
        schema_container = (
            schema_container_pb2.SchemaContainer(tecton_schema=type_utils.to_tecton_schema(schema)) if schema else None
        )

        data_source_type: data_source_type_pb2.DataSourceType
        if isinstance(stream_config, configs.PushConfig):
            if batch_config:
                data_source_type = data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH
            else:
                data_source_type = data_source_type_pb2.DataSourceType.PUSH_NO_BATCH
        else:
            assert batch_config is not None, f"batch_config must be provided for stream source {name}"
            data_source_type = data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH

        ds_args = virtual_data_source__args_pb2.VirtualDataSourceArgs(
            virtual_data_source_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            version=self._framework_version.value,
            type=data_source_type,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        if schema_container:
            ds_args.schema.CopyFrom(schema_container)
        if batch_config:
            batch_config._merge_batch_args(ds_args)

        # Apply defaults for PushConfig from repo.yaml
        if isinstance(stream_config, configs.PushConfig):
            stream_source_defaults = repo_config.get_stream_source_defaults()
            if stream_source_defaults.push_config:
                # Apply ingest_server_group default if not specified
                if (
                    stream_config._args.ingest_server_group is None
                    and stream_source_defaults.push_config.ingest_server_group is not None
                ):
                    stream_config._args.ingest_server_group = stream_source_defaults.push_config.ingest_server_group
                # Apply transform_server_group default if not specified
                if (
                    stream_config._args.transform_server_group is None
                    and stream_source_defaults.push_config.transform_server_group is not None
                ):
                    stream_config._args.transform_server_group = (
                        stream_source_defaults.push_config.transform_server_group
                    )

        stream_config._merge_stream_args(ds_args)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)
        source_info = construct_fco_source_info(ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, stream_config),
        )

        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._populate_spec()

        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.DataSourceSpec) -> "StreamSource":
        """Create a StreamSource from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)

        # override the framework version class attribute to be the framework version set by the spec
        class StreamSourceFromSpec(cls):
            _framework_version = spec.metadata.framework_version

        obj = StreamSourceFromSpec.__new__(StreamSourceFromSpec)  # pylint: disable=no-value-for-parameter
        obj.__attrs_init__(
            info=info,
            spec=spec,
            args=None,
            source_info=None,
            args_supplement=None,
        )
        return obj

    @sdk_decorators.sdk_public_method
    def start_stream_preview(
        self,
        table_name: str,
        *,
        apply_translator: bool = True,
        option_overrides: Optional[Dict[str, str]] = None,
        checkpoint_dir: Optional[str] = None,
    ) -> pyspark_streaming.StreamingQuery:
        """
        Starts a streaming job to write incoming records from this DS's stream to a temporary table with a given name.

        After records have been written to the table, they can be queried using ``spark.sql()``. If ran in a Databricks
        notebook, Databricks will also automatically visualize the number of incoming records.

        This is a testing method, most commonly used to verify a StreamDataSource is correctly receiving streaming events.
        Note that the table will grow infinitely large, so this is only really useful for debugging in notebooks.

        :param table_name: The name of the temporary table that this method will write to.
        :param apply_translator: Whether to apply this data source's ``raw_stream_translator``.
            When True, the translated data will be written to the table. When False, the
            raw, untranslated data will be written. ``apply_translator`` is not applicable to stream sources configured
            with ``spark_stream_config`` because it does not have a ``post_processor``.
        :param option_overrides: A dictionary of Spark readStream options that will override any readStream options set
            by the data source. Can be used to configure behavior only for the preview, e.g. setting
            ``startingOffsets:latest`` to preview only the most recent events in a Kafka stream.
        :param checkpoint_dir: A root directory where a temporary folder will be created and used by the streaming job
            for checkpointing. Primarily intended for use with Databricks Unity Catalog Shared Access Mode Clusters.
            If specified, the environment should have write permission for the specified directory. If not provided, a
            temporary directory will be created using the default file system.
        """
        if is_stream_ingest_data_source(self._spec.type):
            msg = "Cannot preview stream ingest data sources"
            raise ValueError(msg)
        return spark_api.start_stream_preview(
            self._spec, table_name, apply_translator, option_overrides, checkpoint_dir
        )

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def ingest(self, events: Union[Dict[str, Any], Sequence[Dict[str, Any]]], dry_run: bool = False) -> Dict[str, Any]:
        """Ingests a list of events, or a single event, into the Tecton Stream Ingest API.

        :param events: A list of dictionaries representing a sequence of events to be ingested. Also accepts a
            single dictionary.
        :param dry_run: If True, the ingest request will be validated, but the event will not be materialized to the online store.
            If False, the event will be materialized.
        """
        if not is_stream_ingest_data_source(self._spec.type):
            msg = "Can only ingest events for stream sources with push configs"
            raise ValueError(msg)
        if not self._spec:
            msg = "Cannot ingest events for a stream source that has not been applied"
            raise ValueError(msg)

        if isinstance(events, dict):
            events = [events]

        status_code, reason, response = IngestionClient().ingest(
            workspace_name=self._spec.workspace,
            push_source_name=self._spec.name,
            ingestion_records=events,
            dry_run=dry_run,
        )
        if status_code >= 500:
            raise errors.INTERNAL_ERROR(message=json.dumps(response))
        elif status_code >= 400:
            raise errors.INGESTAPI_USER_ERROR(
                status_code=status_code, reason=reason, error_message=json.dumps(response)
            )
        else:
            return response


@attrs.define()
class FilteredSource:
    """
    FilteredSource is an internal utility for pre-filtering ``sources`` in materialized Feature View definitions.
    Do not use FilteredSource directly, use DataSource.select_range() instead.

    Attributes:
        source: Data Source that this FilteredSource class wraps.
        start_time: FilterDateTime object representing the start time of the filter.
        end_time: FilterDateTime object representing the end time of the filter.
        start_time_offset: Deprecated. Do not use Filtered Source directly, use DataSource.select_range() instead.
    """

    source: DataSource

    # Deprecated in favor of start_time and end_time
    start_time_offset: Optional[timedelta] = None

    start_time: Optional[FilterDateTime] = None
    end_time: Optional[FilterDateTime] = None


def data_source_from_spec(data_source_spec: specs.DataSourceSpec):
    """Create a Data Source (of the correct type) from the provided spec."""
    if data_source_spec.type in (
        data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
    ):
        return StreamSource._from_spec(data_source_spec)
    elif data_source_spec.type == data_source_type_pb2.DataSourceType.BATCH:
        return BatchSource._from_spec(data_source_spec)
    else:
        msg = f"Unexpected Data Source Type. Spec: {data_source_spec}"
        raise ValueError(msg)


def _build_args_supplement(
    batch_config: Optional[BatchConfigType], stream_config: Optional[StreamConfigType]
) -> specs.DataSourceSpecArgsSupplement:
    supplement = specs.DataSourceSpecArgsSupplement()
    if isinstance(
        batch_config,
        (
            configs.FileConfig,
            configs.HiveConfig,
            configs.RedshiftConfig,
            configs.SnowflakeConfig,
            configs.UnityConfig,
            configs.BigQueryConfig,
        ),
    ):
        supplement.batch_post_processor = batch_config.post_processor
    elif isinstance(batch_config, (configs.PandasBatchConfig, configs.SparkBatchConfig, configs.PyArrowBatchConfig)):
        supplement.batch_data_source_function = batch_config.data_source_function
    elif batch_config is not None:
        msg = f"Unexpected batch_config type: {batch_config}"
        raise TypeError(msg)
    if isinstance(stream_config, (configs.KinesisConfig, configs.KafkaConfig)):
        supplement.stream_post_processor = stream_config.post_processor
    elif isinstance(stream_config, configs.SparkStreamConfig):
        supplement.stream_data_source_function = stream_config.data_source_function
    elif isinstance(stream_config, configs.PushConfig):
        pass
    elif stream_config is not None:
        msg = f"Unexpected stream_config type: {stream_config}"
        raise TypeError(msg)
    return supplement


def is_stream_ingest_data_source(data_source_type: data_source_type_pb2.DataSourceType) -> bool:
    return data_source_type in {
        data_source_type_pb2.DataSourceType.PUSH_WITH_BATCH,
        data_source_type_pb2.DataSourceType.PUSH_NO_BATCH,
    }
