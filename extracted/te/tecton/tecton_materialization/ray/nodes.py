import dataclasses
import datetime
from typing import Optional
from typing import Tuple

import attrs
import pypika

from tecton_core import offline_store
from tecton_core import query_consts
from tecton_core import time_utils as core_time_utils
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_types import StringType
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import PartitionType
from tecton_core.offline_store import partition_type_for_delta
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.node_interface import QueryNode
from tecton_core.schema import Schema
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion


@dataclasses.dataclass
class TimeSpec:
    timestamp_key: str
    # Can be either the anchor time or timestamp column depending on FeatureView type
    time_column: str
    partition_size: datetime.timedelta
    partition_is_anchor: bool

    @staticmethod
    def for_feature_definition(fd: FeatureDefinitionWrapper) -> "TimeSpec":
        use_anchor_time = fd.is_temporal_aggregate and not fd.compaction_enabled
        return TimeSpec(
            timestamp_key=fd.timestamp_key,
            partition_size=offline_store.partition_size_for_delta(fd).as_timedelta()
            if fd.has_delta_offline_store
            else None,
            time_column=query_consts.anchor_time() if use_anchor_time else fd.timestamp_key,
            partition_is_anchor=fd.is_temporal_aggregate,
        )


@attrs.frozen
class AddTimePartitionNode(QueryNode):
    input_node: NodeRef
    time_spec: TimeSpec
    feature_store_version: FeatureStoreFormatVersion = FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT
    partition_type: Optional[PartitionType] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        return (*self.input_node.columns, offline_store.TIME_PARTITION)

    @property
    def output_schema(self) -> Optional[Schema]:
        schema = self.input_node.output_schema.to_dict()
        schema[offline_store.TIME_PARTITION] = StringType()
        return Schema.from_dict(schema)

    @property
    def inputs(self) -> Tuple[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Partition by {self.time_spec.time_column} in buckets of {self.time_spec.partition_size}"

    def _to_query(self, partition_selector: Optional[PartitionSelector] = None) -> pypika.queries.QueryBuilder:
        # For compaction, we use delta v2 format (epoch nano second partition)
        if self.partition_type == PartitionType.EPOCH:
            partition_size_nanoseconds = core_time_utils.convert_timedelta_for_version(
                self.time_spec.partition_size, self.feature_store_version
            )
            assert partition_size_nanoseconds != 0, "Can't partition by 0-width buckets"
            # we are not using anchor time for compaction jobs
            assert self.time_spec.time_column != query_consts.anchor_time()
            epoch_nanoseconds = self.func.convert_epoch_seconds_to_feature_store_format_version(
                self.func.to_unixtime(pypika.Field(self.time_spec.time_column)), self.feature_store_version
            )
            partition_epoch = epoch_nanoseconds - (epoch_nanoseconds % partition_size_nanoseconds)
            partition_col = partition_epoch.as_(offline_store.TIME_PARTITION)
            return pypika.Query().from_(self.input_node._to_query(partition_selector)).select("*", partition_col)
        else:
            partition_size_seconds = offline_store.window_size_seconds(self.time_spec.partition_size)
            assert partition_size_seconds != 0, "Can't partition by 0-width buckets"
            if self.time_spec.partition_is_anchor:
                # Anchor time is ns
                epoch_seconds = self.func.int_div(pypika.Field(self.time_spec.time_column), 1_000_000_000)
            else:
                epoch_seconds = self.func.to_unixtime(pypika.Field(self.time_spec.time_column))
            partition_epoch = epoch_seconds - (epoch_seconds % partition_size_seconds)
            ts_format = offline_store.timestamp_formats(self.time_spec.partition_size).python_format
            partition_col = self.func.strftime(self.func.from_unixtime(partition_epoch), ts_format).as_(
                offline_store.TIME_PARTITION
            )
            return pypika.Query().from_(self.input_node._to_query(partition_selector)).select("*", partition_col)

    @staticmethod
    def for_feature_definition(fd: FeatureDefinitionWrapper, input_node: NodeRef) -> NodeRef:
        assert (
            fd.get_feature_store_format_version
            >= FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS
        ), f"FeatureStoreFormateVersion {fd.get_feature_store_format_version} is not supported"
        return AddTimePartitionNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=input_node,
            time_spec=TimeSpec.for_feature_definition(fd),
            feature_store_version=fd.get_feature_store_format_version,
            partition_type=partition_type_for_delta(fd.offline_store_params),
        ).as_ref()
