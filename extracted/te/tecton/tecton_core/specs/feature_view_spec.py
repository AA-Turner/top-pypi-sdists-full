import copy
import enum
import logging
from types import MappingProxyType
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
from google.protobuf import duration_pb2
from typeguard import typechecked

import tecton_core.tecton_pendulum as pendulum
from tecton_core import data_types
from tecton_core import data_types as tecton_types
from tecton_core import errors
from tecton_core import feature_view_utils
from tecton_core import id_helper
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.aggregation_utils import get_aggregation_enum_from_string
from tecton_core.aggregation_utils import get_aggregation_function_result_type
from tecton_core.compute_mode import BatchComputeMode
from tecton_core.data_types import DataType
from tecton_core.data_types import data_type_from_proto
from tecton_core.pipeline import pipeline_common
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_core.specs.calculation_node_spec import AbstractSyntaxTreeNodeSpec
from tecton_core.specs.feature_spec import FeatureMetadataSpec
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import TimeWindowSpec
from tecton_core.specs.time_window_spec import create_time_window_spec_from_data_proto
from tecton_core.specs.time_window_spec import window_spec_to_window_data_proto
from tecton_core.specs.utils import get_field_or_none
from tecton_proto.args import feature_view__client_pb2 as feature_view__args_pb2
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2
from tecton_proto.common import aggregation_function__client_pb2 as afpb
from tecton_proto.common import data_source_type__client_pb2 as data_source_type_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.common import secret__client_pb2 as secret_pb2
from tecton_proto.common.id__client_pb2 import Id
from tecton_proto.data import feature_store__client_pb2 as feature_store_pb2
from tecton_proto.data import feature_view__client_pb2 as feature_view__data_pb2
from tecton_proto.modelartifactservice import model_artifact_data__client_pb2 as model_artifact_service_pb2
from tecton_proto.validation import validator__client_pb2 as validator_pb2


logger = logging.getLogger(__name__)

__all__ = [
    "FeatureTableSpec",
    "FeatureViewSpec",
    "FeatureViewSpecArgsSupplement",
    "MaterializedFeatureViewSpec",
    "MaterializedFeatureViewType",
    "OnlineBatchTablePart",
    "OnlineBatchTablePartTile",
    "RealtimeFeatureViewSpec",
    "create_feature_view_spec_from_args_proto",
    "create_feature_view_spec_from_data_proto",
    "get_aggregate_features_from_feature_view_args",
    "get_batch_schedule_from_feature_view_args",
    "get_batch_trigger_from_feature_view_args",
    "get_is_continuous_from_feature_view_args",
    "get_join_keys_from_feature_view_args",
    "get_online_serving_keys_from_feature_view_args",
    "resolve_timestamp_field_for_materialized_feature_view",
]

MIGRATE_TO_FEATURES_GUIDE_LINK = "https://docs.tecton.ai/docs/release-notes/upgrade-process/to-1_0-upgrade-guide"


@utils.frozen_strict
class FeatureViewSpec(tecton_object_spec.TectonObjectSpec):
    """Base class for feature view specs."""

    join_keys: Tuple[str, ...]
    entity_ids: Tuple[str, ...]
    online_serving_keys: Tuple[str, ...]  # Aka the Online Serving Index.
    feature_store_format_version: feature_store_pb2.FeatureStoreFormatVersion.ValueType = attrs.field()
    view_schema: schema.Schema
    materialization_schema: schema.Schema
    prevent_destroy: bool

    # materialization_enabled is True if the feature view has online or online set to True, and the feature view is
    # applied to a live workspace.
    materialization_enabled: bool
    online: bool
    offline: bool
    options: Mapping[str, str]

    url: Optional[str] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    context_parameter_name: Optional[str]
    secrets: Optional[Mapping[str, secret_pb2.SecretReference]]
    resource_providers: Optional[Mapping[str, Id]]

    @feature_store_format_version.validator
    def check_valid_feature_store_format_version(self, _, value):
        if (
            value < feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT
            or value > feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_MAX
        ):
            msg = f"Unsupported feature_store_format_version: {value}"
            raise ValueError(msg)

    @property
    def features(self) -> List[str]:
        """
        Returns the output feature names of this feature view
        """
        raise NotImplementedError

    @property
    def feature_metadata(self) -> List[FeatureMetadataSpec]:
        """
        Returns the output feature + metadata
        """
        raise NotImplementedError

    def join_key_schema(self) -> schema.Schema:
        """
        Return the join key schema which is adjusted by online serving keys.
        """
        spine_schema_dict = self.view_schema.to_dict()
        # If online_serving_keys are specified, spine only needs to contain these keys instead of all join keys.
        retrieval_keys = self.online_serving_keys if len(self.online_serving_keys) > 0 else self.join_keys
        spine_schema_dict = {key: spine_schema_dict[key] for key in retrieval_keys}
        return schema.Schema.from_dict(spine_schema_dict)

    def inferred_join_key_schema(
        self, dependent_fv_specs_and_jk_overrides: List[Tuple["FeatureViewSpec", List[utils.JoinKeyMappingSpec]]]
    ) -> schema.Schema:
        """Returns the combined join key schema from all input FVs which are adjusted by join key overridings.

        This is only relevant to RealtimeFeatureViews and Prompts.
        """
        input_fv_schema = schema.Schema(schema_pb2.Schema())
        for fv_spec, jk_overrides in dependent_fv_specs_and_jk_overrides:
            fv_schema_dict = fv_spec.join_key_schema().to_dict()
            for jk_override_spec in jk_overrides:
                fv_schema_dict[jk_override_spec.spine_column_name] = fv_schema_dict[
                    jk_override_spec.feature_view_column_name
                ]
                # Delete the original feature_view_column_name entry as the data type is assigned to the overriding key.
                del fv_schema_dict[jk_override_spec.feature_view_column_name]
            input_fv_schema += schema.Schema.from_dict(fv_schema_dict)
        return input_fv_schema


@attrs.define
class FeatureViewSpecArgsSupplement:
    """A data class used for supplementing args protos during FeatureViewSpec construction.

    This Python data class can be used to include data that is not included in args protos (e.g. schemas) into the
    FeatureViewSpec constructor.
    """

    view_schema: Optional[schema_pb2.Schema]
    materialization_schema: Optional[schema_pb2.Schema]
    online_batch_table_format: Optional[schema_pb2.OnlineBatchTableFormat]
    model_artifacts: Optional[Dict[str, model_artifact_service_pb2.ModelArtifactInfo]] = None


@utils.frozen_strict
class SecondaryKeyOutputColumn:
    name: str
    time_window: TimeWindowSpec


@utils.frozen_strict
class OnlineBatchTablePartTile:
    relative_start_time_inclusive: pendulum.Duration
    relative_end_time_exclusive: pendulum.Duration

    @classmethod
    def from_proto(cls, proto: schema_pb2.OnlineBatchTablePartTile) -> "OnlineBatchTablePartTile":
        return cls(
            relative_start_time_inclusive=time_utils.proto_to_duration(proto.relative_start_time_inclusive),
            relative_end_time_exclusive=time_utils.proto_to_duration(proto.relative_end_time_exclusive),
        )


@utils.frozen_strict
class OnlineBatchTablePart:
    window_index: int
    time_window: TimeWindowSpec
    schema: schema.Schema
    # We allow divergence between local and remote for tiles because we do not compute the tiles for args.
    tiles: Tuple[OnlineBatchTablePartTile, ...] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    def from_proto(cls, proto: schema_pb2.OnlineBatchTablePart) -> "OnlineBatchTablePart":
        part_schema = _remove_deprecated_column_proto_fields(proto.schema)
        return cls(
            window_index=proto.window_index,
            time_window=create_time_window_spec_from_data_proto(proto.time_window),
            schema=schema.Schema(part_schema),
            tiles=tuple(OnlineBatchTablePartTile.from_proto(tile) for tile in proto.tiles),
        )


@utils.frozen_strict
class Attribute:
    name: str
    column_dtype: DataType
    description: Optional[str]
    tags: Optional[Dict[str, str]]

    @classmethod
    def from_data_proto(cls, attribute_proto: feature_view__data_pb2.Attribute) -> "Attribute":
        return cls(
            name=attribute_proto.column.name,
            column_dtype=data_type_from_proto(attribute_proto.column.dtype),
            description=utils.get_field_or_none(attribute_proto, "description"),
            tags=dict(attribute_proto.tags) if attribute_proto.tags else None,
        )

    @classmethod
    def from_args_proto(cls, attribute_proto: feature_view__args_pb2.Attribute) -> "Attribute":
        return cls(
            name=attribute_proto.name,
            column_dtype=data_type_from_proto(attribute_proto.column_dtype),
            description=utils.get_field_or_none(attribute_proto, "description"),
            tags=dict(attribute_proto.tags) if attribute_proto.tags else None,
        )


@utils.frozen_strict
class Calculation:
    name: str
    root: AbstractSyntaxTreeNodeSpec
    description: Optional[str]
    tags: Optional[Dict[str, str]]

    @classmethod
    def from_data_proto(cls, calculation_proto: feature_view__data_pb2.Calculation) -> "Calculation":
        return cls(
            name=calculation_proto.name,
            root=AbstractSyntaxTreeNodeSpec.from_proto(calculation_proto.abstract_syntax_tree_root),
            description=utils.get_field_or_none(calculation_proto, "description"),
            tags=dict(calculation_proto.tags) if calculation_proto.tags else None,
        )

    @classmethod
    def from_args_proto(cls, calculation_proto: feature_view__data_pb2.Calculation) -> "Calculation":
        return cls(
            name=calculation_proto.name,
            root=AbstractSyntaxTreeNodeSpec.from_proto(calculation_proto.abstract_syntax_tree_root),
            description=utils.get_field_or_none(calculation_proto, "description"),
            tags=dict(calculation_proto.tags) if calculation_proto.tags else None,
        )


@utils.frozen_strict
class Inference:
    input_columns: List[schema.Column]
    output_column: schema.Column
    # TODO(jiadong): Make this a data class to wrap the proto
    model_artifact: model_artifact_service_pb2.ModelArtifactInfo
    description: Optional[str]
    tags: Optional[Dict[str, str]]

    @classmethod
    def from_data_proto(cls, inference_proto: feature_view__data_pb2.Inference) -> "Inference":
        return cls(
            input_columns=[schema.Column.from_proto(proto) for proto in inference_proto.input_columns],
            output_column=schema.Column.from_proto(inference_proto.output_column),
            model_artifact=inference_proto.model_artifact,
            description=utils.get_field_or_none(inference_proto, "description"),
            tags=dict(inference_proto.tags) if inference_proto.tags else None,
        )

    @classmethod
    def from_args_proto(
        cls, inference_proto: feature_view__args_pb2.Inference, supplement: FeatureViewSpecArgsSupplement
    ) -> "Inference":
        if inference_proto.model not in supplement.model_artifacts:
            msg = f"Model Artifact {inference_proto.model} was not stored in FeatureViewSpecArgsSupplement"
            raise errors.TectonValidationError(msg)

        artifact = supplement.model_artifacts[inference_proto.model]
        expected_model_data_types = [column.offline_data_type for column in artifact.input_schema.columns]
        defined_model_data_types = [column.dtype for column in inference_proto.input_columns]
        if expected_model_data_types != defined_model_data_types:
            msg = f"The `input_columns` defined in the Feature View does not match the `input_schema` defined in model {inference_proto.model}'s `input_schema`"
            raise errors.TectonValidationError(msg)

        return cls(
            input_columns=[
                schema.Column(name=proto.name, dtype=data_type_from_proto(proto.dtype))
                for proto in inference_proto.input_columns
            ],
            output_column=schema.Column(
                name=inference_proto.name,
                dtype=data_type_from_proto(artifact.output_schema.columns[0].offline_data_type),
            ),
            model_artifact=artifact,
            description=utils.get_field_or_none(inference_proto, "description"),
            tags=dict(inference_proto.tags) if inference_proto.tags else None,
        )


@utils.frozen_strict
class Embedding:
    input_column_name: str
    output_column_name: str
    model: str
    description: Optional[str]
    tags: Optional[Dict[str, str]]

    @classmethod
    def from_args_proto(
        cls,
        embedding_proto: feature_view__args_pb2.Embedding,
    ) -> "Embedding":
        return cls(
            input_column_name=embedding_proto.column,
            output_column_name=embedding_proto.name,
            model=embedding_proto.model,
            description=utils.get_field_or_none(embedding_proto, "description"),
            tags=dict(embedding_proto.tags) if embedding_proto.tags else None,
        )

    @classmethod
    def from_data_proto(
        cls,
        embedding_proto: feature_view__data_pb2.Embedding,
    ) -> "Embedding":
        return cls(
            input_column_name=embedding_proto.input_column_name,
            output_column_name=embedding_proto.output_column_name,
            model=embedding_proto.model,
            description=utils.get_field_or_none(embedding_proto, "description"),
            tags=dict(embedding_proto.tags) if embedding_proto.tags else None,
        )


@utils.frozen_strict
class OnlineBatchTableFormat:
    online_batch_table_parts: Tuple[OnlineBatchTablePart, ...]

    @classmethod
    def from_proto(cls, proto: schema_pb2.OnlineBatchTableFormat) -> "OnlineBatchTableFormat":
        return cls(
            online_batch_table_parts=tuple(
                OnlineBatchTablePart.from_proto(part) for part in proto.online_batch_table_parts
            )
        )


class MaterializedFeatureViewType(enum.Enum):
    TEMPORAL = 1
    TEMPORAL_AGGREGATE = 2


def build_attribute_metadata(attribute_features: Tuple[Attribute, ...]) -> List[FeatureMetadataSpec]:
    return [
        FeatureMetadataSpec(
            name=attribute.name,
            dtype=attribute.column_dtype,
            description=attribute.description,
            tags=attribute.tags,
        )
        for attribute in attribute_features
    ]


def build_calculation_metadata(calculation_features: Tuple[Calculation, ...]) -> List[FeatureMetadataSpec]:
    return [
        FeatureMetadataSpec(
            name=calculation.name,
            dtype=calculation.root.dtype,
            description=calculation.description,
            tags=calculation.tags,
        )
        for calculation in calculation_features
    ]


def build_inference_metadata(inference_features: Tuple[Inference, ...]) -> List[FeatureMetadataSpec]:
    return [
        FeatureMetadataSpec(
            name=inference.output_column.name,
            dtype=inference.output_column.dtype,
            description=inference.description,
            tags=inference.tags,
        )
        for inference in inference_features
    ]


def build_embedding_metadata(embedding_features: Tuple[Embedding, ...]) -> List[FeatureMetadataSpec]:
    return [
        FeatureMetadataSpec(
            name=embedding.output_column_name,
            dtype=data_types.ArrayType(data_types.Float32Type()),
            description=embedding.description,
            tags=embedding.tags,
        )
        for embedding in embedding_features
    ]


def build_aggregate_metadata(
    aggregate_features: Tuple[feature_view__data_pb2.Aggregate, ...], view_schema: schema.Schema
) -> List[FeatureMetadataSpec]:
    feature_metadata: List[FeatureMetadataSpec] = []

    view_schema_column_name_to_dtype = dict(view_schema.column_name_and_data_types())
    for aggregate_feature in aggregate_features:
        input_column_type = view_schema_column_name_to_dtype.get(aggregate_feature.input_feature_name, None)
        assert input_column_type is not None, (
            f"{aggregate_feature.input_feature_name} is not defined on the view schema"
        )
        aggregate_output_column_type = get_aggregation_function_result_type(
            aggregation=aggregate_feature, feature_type=input_column_type
        )
        feature_metadata.append(
            FeatureMetadataSpec(
                name=aggregate_feature.output_feature_name,
                dtype=aggregate_output_column_type,
                description=get_field_or_none(aggregate_feature, "description"),
                tags=dict(aggregate_feature.tags) if aggregate_feature.tags else None,
            )
        )
    return feature_metadata


def build_secondary_key_metadata(
    aggregation_secondary_key: str,
    secondary_key_rollup_outputs: Optional[Tuple[SecondaryKeyOutputColumn, ...]],
    view_schema: schema.Schema,
) -> List[FeatureMetadataSpec]:
    view_schema_column_name_to_dtype = dict(view_schema.column_name_and_data_types())

    aggregation_secondary_key_type = view_schema_column_name_to_dtype.get(aggregation_secondary_key)
    return [
        FeatureMetadataSpec(
            name=secondary_key_output_column.name,
            dtype=aggregation_secondary_key_type,
            # setting description + tags on secondary key column is not supported
            description=None,
            tags=None,
        )
        for secondary_key_output_column in secondary_key_rollup_outputs
    ]


@utils.frozen_strict
class MaterializedFeatureViewSpec(FeatureViewSpec):
    """Spec for Batch and Stream feature views."""

    is_continuous: bool
    type: MaterializedFeatureViewType
    data_source_type: data_source_type_pb2.DataSourceType.ValueType
    incremental_backfills: bool
    timestamp_field: str
    batch_publish_timestamp: Optional[str]

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]

    batch_schedule: Optional[pendulum.Duration]
    slide_interval: Optional[pendulum.Duration]
    ttl: Optional[pendulum.Duration]
    feature_start_time: Optional[pendulum.DateTime]
    materialization_start_time: Optional[pendulum.DateTime]
    max_source_data_delay: pendulum.Duration
    materialized_data_path: Optional[str]
    published_features_path: Optional[str]
    sink_config: Optional[feature_view__data_pb2.SinkConfig]
    time_range_policy: Optional[feature_view__data_pb2.MaterializationTimeRangePolicy.ValueType]
    materialization_state_transitions: Tuple[feature_view__data_pb2.MaterializationStateTransition, ...] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    offline_store: Optional[feature_view__args_pb2.OfflineFeatureStoreConfig]
    offline_store_params: Optional[feature_view__data_pb2.OfflineStoreParams] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    # Generally, data protos should not be exposed in the "spec". However, we make an exception in this case because
    # (a) there is no equivalent args proto, (b) it's a good data model for this usage, and (c) this proto is used
    # extensively in the query gen code (not worth refactoring).
    aggregate_features: Tuple[feature_view__data_pb2.Aggregate, ...]

    attribute_features: Tuple[Attribute, ...]
    embedding_features: Tuple[Embedding, ...]
    inference_features: Tuple[Inference, ...]

    aggregation_secondary_key: Optional[str]
    secondary_key_rollup_outputs: Optional[Tuple[SecondaryKeyOutputColumn, ...]]

    slide_interval_string: Optional[str]

    # Only relevant for offline-materialized fvs on snowflake compute
    snowflake_view_name: Optional[str] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]
    stream_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    batch_compute_mode: BatchComputeMode

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    # See failure: https://tectonworkspace.slack.com/archives/C04L8M14XGX/p1675279851469019
    batch_trigger: Optional[feature_view__args_pb2.BatchTriggerType.ValueType]
    manual_trigger_backfill_end_time: Optional[pendulum.DateTime]

    online_batch_table_format: Optional[OnlineBatchTableFormat]
    compaction_enabled: bool
    stream_tiling_enabled: bool
    stream_tile_size: Optional[pendulum.Duration]
    output_stream: Optional[feature_view__args_pb2.OutputStream]

    monitor_freshness: bool
    expected_feature_freshness: Optional[pendulum.Duration]
    alert_email: str

    max_backfill_interval: Optional[pendulum.Duration]
    tecton_materialization_runtime: Optional[str]
    cache_config: Optional[feature_view__args_pb2.CacheConfig]
    environment: Optional[str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "MaterializedFeatureViewSpec":
        cache_config_in_seconds = time_utils.proto_to_duration(proto.cache_config.max_age_seconds).in_seconds()

        if proto.HasField("temporal_aggregate"):
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE
            is_continuous = proto.temporal_aggregate.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal_aggregate, "data_source_type")
            incremental_backfills = False
            slide_interval = time_utils.proto_to_duration(proto.temporal_aggregate.slide_interval)
            ttl = None
            # TODO(sanika): add a wrapper for aggregate features spec
            aggregate_features = utils.get_tuple_from_repeated_field(proto.temporal_aggregate.features)
            embedding_features = ()
            inference_features = ()
            attribute_features = ()
            slide_interval_string = utils.get_field_or_none(proto.temporal_aggregate, "slide_interval_string")
            aggregation_secondary_key = utils.get_field_or_none(proto.temporal_aggregate, "aggregation_secondary_key")
            secondary_key_rollup_outputs = None
            if aggregation_secondary_key:
                secondary_key_rollup_outputs = tuple(
                    SecondaryKeyOutputColumn(
                        name=output_col.name,
                        time_window=create_time_window_spec_from_data_proto(output_col.time_window),
                    )
                    for output_col in proto.temporal_aggregate.secondary_key_output_columns
                )
        elif proto.HasField("temporal"):
            fv_type = MaterializedFeatureViewType.TEMPORAL
            is_continuous = proto.temporal.is_continuous
            data_source_type = utils.get_field_or_none(proto.temporal, "data_source_type")
            incremental_backfills = proto.temporal.incremental_backfills
            slide_interval = None
            ttl = utils.get_non_default_duration_field_or_none(proto.temporal, "serving_ttl")
            aggregate_features = ()
            embedding_features = tuple(Embedding.from_data_proto(emb_proto) for emb_proto in proto.temporal.embeddings)
            inference_features = tuple(
                Inference.from_data_proto(inference_proto) for inference_proto in proto.temporal.inferences
            )
            attribute_features = tuple(
                Attribute.from_data_proto(attribute_proto) for attribute_proto in proto.temporal.attributes
            )
            slide_interval_string = None
            aggregation_secondary_key = None
            secondary_key_rollup_outputs = None
        else:
            msg = f"Unexpected feature view type: {proto}"
            raise TypeError(msg)

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            offline_store_params=utils.get_field_or_none(proto.materialization_params, "offline_store_params"),
            is_continuous=is_continuous,
            data_source_type=data_source_type,
            incremental_backfills=incremental_backfills,
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            batch_publish_timestamp=utils.get_field_or_none(proto.materialization_params, "batch_publish_timestamp"),
            type=fv_type,
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.materialization_params.writes_to_online_store,
            offline=proto.materialization_params.writes_to_offline_store,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=utils.get_non_default_duration_field_or_none(
                proto.materialization_params, "schedule_interval"
            ),
            slide_interval=slide_interval,
            ttl=ttl,
            feature_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "feature_start_timestamp"
            ),
            materialization_start_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "materialization_start_timestamp"
            ),
            max_source_data_delay=time_utils.proto_to_duration(proto.materialization_params.max_source_data_delay),
            aggregate_features=aggregate_features,
            aggregation_secondary_key=aggregation_secondary_key,
            secondary_key_rollup_outputs=secondary_key_rollup_outputs,
            embedding_features=embedding_features,
            inference_features=inference_features,
            attribute_features=attribute_features,
            slide_interval_string=slide_interval_string,
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            published_features_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.feature_export_data_location, "path"
            ),
            materialization_state_transitions=utils.get_tuple_from_repeated_field(
                proto.materialization_state_transitions
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            snowflake_view_name=utils.get_field_or_none(proto.snowflake_data, "snowflake_view_name"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            stream_cluster_config=utils.get_field_or_none(proto.materialization_params, "stream_materialization"),
            batch_trigger=utils.get_field_or_none(proto, "batch_trigger"),
            manual_trigger_backfill_end_time=utils.get_timestamp_field_or_none(
                proto.materialization_params, "manual_trigger_backfill_end_timestamp"
            ),
            url=utils.get_field_or_none(proto, "web_url"),
            online_batch_table_format=_get_online_batch_table_format(proto.schemas),
            batch_compute_mode=BatchComputeMode(proto.batch_compute_mode)
            if proto.HasField("batch_compute_mode")
            else None,
            compaction_enabled=proto.materialization_params.compaction_enabled,
            stream_tiling_enabled=proto.materialization_params.stream_tiling_enabled,
            stream_tile_size=utils.get_non_default_duration_field_or_none(
                proto.materialization_params, "stream_tile_size"
            ),
            options=MappingProxyType(proto.options),
            context_parameter_name=proto.context_parameter_name,
            prevent_destroy=proto.validation_args.args.prevent_destroy,
            output_stream=utils.get_field_or_none(proto.materialization_params, "output_stream"),
            monitor_freshness=proto.monitoring_params.monitor_freshness,
            expected_feature_freshness=time_utils.proto_to_duration(proto.monitoring_params.expected_feature_freshness),
            alert_email=proto.monitoring_params.alert_email,
            max_backfill_interval=time_utils.proto_to_duration(proto.materialization_params.max_backfill_interval),
            tecton_materialization_runtime=proto.materialization_params.tecton_materialization_runtime,
            cache_config=feature_view__args_pb2.CacheConfig(max_age_seconds=cache_config_in_seconds)
            if cache_config_in_seconds > 0
            else None,
            environment=proto.materialization_params.environment,
            secrets=MappingProxyType(proto.secrets),
            resource_providers=MappingProxyType(proto.resource_providers),
            sink_config=proto.materialization_params.feature_publish_offline_store_config.sink_config
            if proto.materialization_params.HasField("feature_publish_offline_store_config")
            and proto.materialization_params.feature_publish_offline_store_config.HasField("sink_config")
            else None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "MaterializedFeatureViewSpec":
        feature_start_time = utils.get_timestamp_field_or_none(
            proto.materialized_feature_view_args, "feature_start_time"
        )

        compaction_enabled = proto.materialized_feature_view_args.compaction_enabled
        is_continuous = get_is_continuous_from_feature_view_args(proto)
        data_source_type = utils.get_field_or_none(proto.materialized_feature_view_args, "data_source_type")
        aggregate_features = get_aggregate_features_from_feature_view_args(proto)
        embedding_features = tuple(
            Embedding.from_args_proto(emb_args_proto)
            for emb_args_proto in proto.materialized_feature_view_args.embeddings
        )

        inference_features = tuple(
            Inference.from_args_proto(inference_args_proto, supplement)
            for inference_args_proto in proto.materialized_feature_view_args.inferences
        )

        attribute_features = tuple(
            Attribute.from_args_proto(attribute_args_proto)
            for attribute_args_proto in proto.materialized_feature_view_args.attributes
        )

        is_aggregate = len(proto.materialized_feature_view_args.aggregations) > 0
        if is_aggregate:
            fv_type = MaterializedFeatureViewType.TEMPORAL_AGGREGATE

            slide_interval_proto = _get_aggregation_interval_from_feature_view_args(
                proto, is_continuous, data_source_type
            )
            if slide_interval_proto:
                slide_interval = time_utils.proto_to_duration(slide_interval_proto)
                slide_interval_string = feature_view_utils.construct_aggregation_interval_name(
                    slide_interval_proto, is_continuous
                )
            else:
                slide_interval = None
                slide_interval_string = ""

            lifetime_start_time = utils.get_timestamp_field_or_none(
                proto.materialized_feature_view_args, "lifetime_start_time"
            )
            if lifetime_start_time:
                materialization_start_time = lifetime_start_time
            elif feature_start_time is not None:
                # Logic must be kept in sync with getMaterializationStartTime() in FeatureViewManager.
                earliest_window_start = min(
                    [
                        RelativeTimeWindowSpec.from_args_proto(agg.time_window).window_start
                        for agg in proto.materialized_feature_view_args.aggregations
                    ]
                )
                materialization_start_time = feature_start_time + earliest_window_start
            else:
                materialization_start_time = None

            aggregation_secondary_key = utils.get_field_or_none(
                proto.materialized_feature_view_args, "aggregation_secondary_key"
            )
            secondary_key_rollup_outputs = None
            if aggregation_secondary_key:
                secondary_key_rollup_outputs = tuple(
                    SecondaryKeyOutputColumn(
                        name=output_col.name, time_window=args_oneof_timewindow_to_spec(output_col)
                    )
                    for output_col in proto.materialized_feature_view_args.secondary_key_output_columns
                )
        else:
            fv_type = MaterializedFeatureViewType.TEMPORAL
            slide_interval_string = None
            materialization_start_time = feature_start_time
            slide_interval = None
            aggregation_secondary_key = None
            secondary_key_rollup_outputs = None

        try:
            timestamp_field = resolve_timestamp_field_for_materialized_feature_view(proto, supplement.view_schema)
        except errors.TectonValidationError:
            raise

        batch_publish_timestamp = utils.get_field_or_none(
            proto.materialized_feature_view_args, "batch_publish_timestamp"
        )

        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.feature_view_id, proto.info, proto.version
            ),
            aggregation_secondary_key=aggregation_secondary_key,
            secondary_key_rollup_outputs=secondary_key_rollup_outputs,
            entity_ids=tuple(id_helper.IdHelper.to_string(entity.entity_id) for entity in proto.entities),
            join_keys=get_join_keys_from_feature_view_args(proto),
            online_serving_keys=get_online_serving_keys_from_feature_view_args(proto),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            offline_store=utils.get_field_or_none(
                proto.materialized_feature_view_args.offline_store, "staging_table_format"
            ),
            offline_store_params=None,
            is_continuous=is_continuous,
            data_source_type=data_source_type,
            incremental_backfills=proto.materialized_feature_view_args.incremental_backfills,
            timestamp_field=timestamp_field,
            batch_publish_timestamp=batch_publish_timestamp,
            type=fv_type,
            feature_store_format_version=proto.materialized_feature_view_args.feature_store_format_version
            if proto.materialized_feature_view_args.tecton_materialization_runtime != ""
            else feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=proto.online_enabled,
            offline=proto.offline_enabled,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            batch_schedule=get_batch_schedule_from_feature_view_args(proto),
            slide_interval=slide_interval,
            ttl=utils.get_duration_field_or_none(proto.materialized_feature_view_args, "serving_ttl"),
            feature_start_time=feature_start_time,
            materialization_start_time=materialization_start_time,
            max_source_data_delay=_get_max_schedule_offset(proto.pipeline),
            aggregate_features=aggregate_features,
            embedding_features=embedding_features,
            inference_features=inference_features,
            attribute_features=attribute_features,
            slide_interval_string=slide_interval_string,
            materialized_data_path=None,
            published_features_path=None,
            time_range_policy=feature_view__data_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
            materialization_state_transitions=(),
            snowflake_view_name=None,
            validation_args=None,
            batch_cluster_config=utils.get_field_or_none(proto.materialized_feature_view_args, "batch_compute"),
            stream_cluster_config=utils.get_field_or_none(proto.materialized_feature_view_args, "stream_compute"),
            batch_trigger=get_batch_trigger_from_feature_view_args(proto),
            manual_trigger_backfill_end_time=utils.get_timestamp_field_or_none(
                proto.materialized_feature_view_args, "manual_trigger_backfill_end_time"
            ),
            url=None,
            online_batch_table_format=OnlineBatchTableFormat.from_proto(supplement.online_batch_table_format)
            if supplement.online_batch_table_format
            else None,
            batch_compute_mode=BatchComputeMode(proto.batch_compute_mode)
            if proto.HasField("batch_compute_mode")
            else None,
            compaction_enabled=compaction_enabled,
            stream_tiling_enabled=proto.materialized_feature_view_args.stream_tiling_enabled,
            stream_tile_size=utils.get_duration_field_or_none(proto.materialized_feature_view_args, "stream_tile_size"),
            options=MappingProxyType(proto.options),
            context_parameter_name=proto.context_parameter_name,
            prevent_destroy=proto.prevent_destroy,
            output_stream=utils.get_field_or_none(proto.materialized_feature_view_args, "output_stream"),
            monitor_freshness=proto.materialized_feature_view_args.monitoring.monitor_freshness,
            expected_feature_freshness=time_utils.proto_to_duration(
                proto.materialized_feature_view_args.monitoring.expected_freshness
            ),
            alert_email=proto.materialized_feature_view_args.monitoring.alert_email,
            max_backfill_interval=time_utils.proto_to_duration(
                proto.materialized_feature_view_args.max_backfill_interval
            ),
            tecton_materialization_runtime=proto.materialized_feature_view_args.tecton_materialization_runtime,
            cache_config=utils.get_field_or_none(proto, "cache_config"),
            environment=proto.materialized_feature_view_args.environment,
            secrets=MappingProxyType(proto.secrets),
            resource_providers=MappingProxyType(proto.resource_providers),
            # Only populated from data proto for now because local dev flow is not supported yet.
            sink_config=None,
        )

    @property
    def features(self) -> List[str]:
        if len(self.aggregate_features) > 0:
            # Temporal aggregate feature view.
            secondary_key_output_cols = (
                [col.name for col in self.secondary_key_rollup_outputs] if self.secondary_key_rollup_outputs else []
            )
            aggregate_output_cols = [
                aggregate_feature.output_feature_name for aggregate_feature in self.aggregate_features
            ]
            return secondary_key_output_cols + aggregate_output_cols
        else:
            # Temporal feature view.
            non_feature_cols = {self.timestamp_field, *self.join_keys, "_anchor_time", "_ANCHOR_TIME"}
            if self.batch_publish_timestamp is not None:
                non_feature_cols.add(self.batch_publish_timestamp)
            cols = [col for col in self.materialization_schema.column_names() if col not in non_feature_cols]
            return cols

    @property
    def feature_metadata(self) -> List[Union[FeatureMetadataSpec]]:
        feature_metadata = []
        has_features = bool(self.attribute_features) or bool(self.embedding_features) or bool(self.inference_features)

        if bool(self.aggregate_features):
            feature_metadata.extend(build_aggregate_metadata(self.aggregate_features, self.view_schema))
            if self.aggregation_secondary_key is not None:
                feature_metadata.extend(
                    build_secondary_key_metadata(
                        self.aggregation_secondary_key, self.secondary_key_rollup_outputs, self.view_schema
                    )
                )
            return feature_metadata
        elif has_features:
            feature_metadata.extend(build_attribute_metadata(self.attribute_features))
            feature_metadata.extend(build_inference_metadata(self.inference_features))
            feature_metadata.extend(build_embedding_metadata(self.embedding_features))
            return feature_metadata
        else:
            msg = f"Feature Metadata is only supported when using the Features parameter. Feature View {self.name} is not using the Features parameter - see {MIGRATE_TO_FEATURES_GUIDE_LINK} for migration instructions."
            raise NotImplementedError(msg)


@utils.frozen_strict
class RealtimeFeatureViewSpec(FeatureViewSpec):
    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required.
    pipeline: Optional[pipeline_pb2.Pipeline]
    environments: Tuple[str, ...]
    attribute_features: Tuple[Attribute, ...]
    calculation_features: Tuple[Calculation, ...]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "RealtimeFeatureViewSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=False,
            online=False,
            offline=False,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            url=utils.get_field_or_none(proto, "web_url"),
            options=MappingProxyType(proto.options),
            context_parameter_name=proto.context_parameter_name,
            prevent_destroy=proto.validation_args.args.prevent_destroy,
            environments=tuple(e.name for e in proto.realtime_feature_view.supported_environments),
            attribute_features=tuple(
                Attribute.from_data_proto(attribute_data_proto)
                for attribute_data_proto in proto.realtime_feature_view.attributes
            ),
            calculation_features=tuple(
                Calculation.from_data_proto(calculation_data_proto)
                for calculation_data_proto in proto.realtime_feature_view.calculations
            ),
            secrets=MappingProxyType(proto.secrets),
            resource_providers=MappingProxyType(proto.resource_providers),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "RealtimeFeatureViewSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.feature_view_id, proto.info, proto.version
            ),
            entity_ids=(),
            join_keys=(),
            online_serving_keys=(),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=False,
            offline=False,
            pipeline=utils.get_field_or_none(proto, "pipeline"),
            validation_args=None,
            url=None,
            options=MappingProxyType(proto.options),
            context_parameter_name=proto.context_parameter_name,
            prevent_destroy=proto.prevent_destroy,
            environments=utils.get_tuple_from_repeated_field(proto.realtime_args.environments),
            attribute_features=tuple(
                Attribute.from_args_proto(attribute_args_proto)
                for attribute_args_proto in proto.realtime_args.attributes
            ),
            calculation_features=tuple(
                Calculation.from_args_proto(calculation_args_proto)
                for calculation_args_proto in proto.realtime_args.calculations
            ),
            secrets=MappingProxyType(proto.secrets),
            resource_providers=MappingProxyType(proto.resource_providers),
        )

    @property
    def features(self) -> List[str]:
        return list(self.view_schema.column_names())

    @property
    def feature_metadata(self):
        feature_metadata = []
        has_features = bool(self.attribute_features) or bool(self.calculation_features)
        if not has_features:
            msg = f"Feature Metadata is only supported when using the Features parameter. Feature View {self.name} is not using the Features parameter - see {MIGRATE_TO_FEATURES_GUIDE_LINK} for migration instructions."
            raise NotImplementedError(msg)

        feature_metadata.extend(build_attribute_metadata(self.attribute_features))
        feature_metadata.extend(build_calculation_metadata(self.calculation_features))
        return feature_metadata


@utils.frozen_strict
class FeatureTableSpec(FeatureViewSpec):
    timestamp_field: str
    ttl: Optional[pendulum.Duration]

    offline_store: Optional[feature_view__args_pb2.OfflineFeatureStoreConfig]
    offline_store_params: Optional[feature_view__data_pb2.OfflineStoreParams] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )
    materialized_data_path: Optional[str]
    time_range_policy: Optional[feature_view__data_pb2.MaterializationTimeRangePolicy.ValueType]
    materialization_state_transitions: Tuple[feature_view__data_pb2.MaterializationStateTransition, ...] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    # TODO(TEC-12321): Audit and fix feature view spec fields that should be required. (batch_cluster_config should be.)
    batch_cluster_config: Optional[feature_view__args_pb2.ClusterConfig]

    alert_email: str
    tecton_materialization_runtime: Optional[str]
    attribute_features: Tuple[Attribute, ...]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: feature_view__data_pb2.FeatureView) -> "FeatureTableSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.feature_view_id, proto.fco_metadata
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(id) for id in proto.entity_ids),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            online_serving_keys=utils.get_tuple_from_repeated_field(proto.online_serving_index.join_keys),
            view_schema=_get_view_schema(proto.schemas),
            materialization_schema=_get_materialization_schema(proto.schemas),
            offline_store=utils.get_field_or_none(proto.materialization_params, "offline_store_config"),
            offline_store_params=utils.get_field_or_none(proto.materialization_params, "offline_store_params"),
            timestamp_field=utils.get_field_or_none(proto, "timestamp_key"),
            feature_store_format_version=proto.feature_store_format_version,
            materialization_enabled=proto.materialization_enabled,
            online=proto.feature_table.online_enabled,
            offline=proto.feature_table.offline_enabled,
            ttl=utils.get_non_default_duration_field_or_none(proto.feature_table, "serving_ttl"),
            materialized_data_path=utils.get_field_or_none(
                proto.enrichments.fp_materialization.materialized_data_location, "path"
            ),
            materialization_state_transitions=utils.get_tuple_from_repeated_field(
                proto.materialization_state_transitions
            ),
            time_range_policy=utils.get_field_or_none(proto.materialization_params, "time_range_policy"),
            validation_args=validator_pb2.FcoValidationArgs(feature_view=proto.validation_args),
            batch_cluster_config=utils.get_field_or_none(proto.materialization_params, "batch_materialization"),
            url=utils.get_field_or_none(proto, "web_url"),
            options=MappingProxyType(proto.options),
            context_parameter_name=None,
            prevent_destroy=proto.validation_args.args.prevent_destroy,
            alert_email=proto.monitoring_params.alert_email,
            tecton_materialization_runtime=proto.materialization_params.tecton_materialization_runtime,
            attribute_features=tuple(
                Attribute.from_data_proto(attribute_data_proto)
                for attribute_data_proto in proto.feature_table.attributes
            ),
            secrets=None,
            resource_providers=None,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: feature_view__args_pb2.FeatureViewArgs, supplement: FeatureViewSpecArgsSupplement
    ) -> "FeatureTableSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.feature_view_id, proto.info, proto.version
            ),
            entity_ids=tuple(id_helper.IdHelper.to_string(entity.entity_id) for entity in proto.entities),
            join_keys=get_join_keys_from_feature_view_args(proto),
            online_serving_keys=get_online_serving_keys_from_feature_view_args(proto),
            view_schema=schema.Schema(supplement.view_schema),
            materialization_schema=schema.Schema(supplement.materialization_schema),
            offline_store=utils.get_field_or_none(proto.feature_table_args.offline_store, "staging_table_format"),
            offline_store_params=None,
            timestamp_field=_get_timestamp_column(supplement.view_schema),
            feature_store_format_version=feature_store_pb2.FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS,
            materialization_enabled=False,
            online=proto.online_enabled,
            offline=proto.offline_enabled,
            ttl=utils.get_duration_field_or_none(proto.feature_table_args, "serving_ttl"),
            materialized_data_path=None,
            materialization_state_transitions=(),
            time_range_policy=None,
            validation_args=None,
            batch_cluster_config=utils.get_field_or_none(proto.feature_table_args, "batch_compute"),
            url=None,
            options=MappingProxyType(proto.options),
            context_parameter_name=None,
            prevent_destroy=proto.prevent_destroy,
            alert_email=proto.feature_table_args.monitoring.alert_email,
            tecton_materialization_runtime=proto.feature_table_args.tecton_materialization_runtime,
            attribute_features=tuple(
                Attribute.from_args_proto(attribute_args_proto)
                for attribute_args_proto in proto.feature_table_args.attributes
            ),
            secrets=None,
            resource_providers=None,
        )

    @property
    def features(self) -> List[str]:
        return [
            col for col in self.view_schema.column_names() if col != self.timestamp_field and col not in self.join_keys
        ]

    @property
    def feature_metadata(self):
        has_features = bool(self.attribute_features)
        if not has_features:
            msg = f"Feature Metadata is only supported when using the Features parameter. Feature Table {self.name} is not using the Features parameter - see {MIGRATE_TO_FEATURES_GUIDE_LINK} for migration instructions."
            raise NotImplementedError(msg)

        return build_attribute_metadata(self.attribute_features)


def _remove_deprecated_column_proto_fields(schema: schema_pb2.Schema) -> schema_pb2.Schema:
    """Clear out deprecated fields from the column proto

    The deprecated fields are still served in data proto for backwards compatibility with old SDKs.
    Clear the field here so that:
        1) Developers don't depend on this field being set.
        2) Local specs are equivalent to the remote specs.
    """

    # Copy the schema so the `ClearField` doesn't change the proto passed into this fuction such as the schema in the MaterializationTaskParam.
    schema_copy = copy.deepcopy(schema)
    for column in schema_copy.columns:
        column.ClearField("feature_server_type")
        column.ClearField("raw_spark_type")
        column.ClearField("raw_snowflake_type")
    return schema_copy


def _get_view_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    if not schemas.HasField("view_schema"):
        return None

    view_schema = _remove_deprecated_column_proto_fields(schemas.view_schema)
    return schema.Schema(view_schema)


def _get_materialization_schema(schemas: feature_view__data_pb2.FeatureViewSchemas) -> Optional[schema.Schema]:
    if not schemas.HasField("materialization_schema"):
        return None

    materialization_schema = _remove_deprecated_column_proto_fields(schemas.materialization_schema)
    return schema.Schema(materialization_schema)


def _get_online_batch_table_format(
    schemas: feature_view__data_pb2.FeatureViewSchemas,
) -> Optional[OnlineBatchTableFormat]:
    if not schemas.HasField("online_batch_table_format"):
        return None

    return OnlineBatchTableFormat.from_proto(schemas.online_batch_table_format)


@typechecked
def create_feature_view_spec_from_data_proto(
    proto: feature_view__data_pb2.FeatureView,
) -> Optional[Union[MaterializedFeatureViewSpec, RealtimeFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("temporal_aggregate") or proto.HasField("temporal"):
        return MaterializedFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("realtime_feature_view"):
        return RealtimeFeatureViewSpec.from_data_proto(proto)
    elif proto.HasField("feature_table"):
        return FeatureTableSpec.from_data_proto(proto)
    else:
        msg = f"Unexpected feature view type: {proto}"
        raise ValueError(msg)


@typechecked
def create_feature_view_spec_from_args_proto(
    proto: feature_view__args_pb2.FeatureViewArgs,
    supplement: Optional[FeatureViewSpecArgsSupplement],
) -> Optional[Union[MaterializedFeatureViewSpec, RealtimeFeatureViewSpec, FeatureTableSpec]]:
    if proto.HasField("materialized_feature_view_args"):
        return MaterializedFeatureViewSpec.from_args_proto(proto, supplement)
    elif proto.HasField("realtime_args"):
        return RealtimeFeatureViewSpec.from_args_proto(proto, supplement)
    elif proto.HasField("feature_table_args"):
        return FeatureTableSpec.from_args_proto(proto, supplement)
    else:
        msg = f"Unexpect feature view type: {proto}"
        raise ValueError(msg)


def _get_timestamp_column(schema_proto: schema_pb2.Schema) -> str:
    schema_ = schema.Schema(schema_proto)
    timestamp_columns = [
        column[0] for column in schema_.column_name_and_data_types() if column[1] == tecton_types.TimestampType()
    ]
    if len(timestamp_columns) != 1:
        msg = f"Attempted to infer timestamp. Expected exactly one timestamp column in schema {schema_}"
        raise errors.TectonValidationError(msg)
    return timestamp_columns[0]


def _get_max_schedule_offset(pipeline: pipeline_pb2.Pipeline) -> pendulum.Duration:
    ds_nodes = pipeline_common.get_all_data_source_nodes(pipeline)
    assert len(ds_nodes) > 0
    return max([time_utils.proto_to_duration(ds_node.data_source_node.schedule_offset) for ds_node in ds_nodes])


@typechecked
def get_batch_schedule_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Optional[pendulum.Duration]:
    is_aggregate = len(proto.materialized_feature_view_args.aggregations) > 0
    if is_aggregate:
        slide_interval = utils.get_duration_field_or_none(proto.materialized_feature_view_args, "aggregation_interval")
        is_continuous = (
            proto.materialized_feature_view_args.stream_processing_mode
            == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )

        if is_continuous:
            # Default is set in Kotlin to one day per CONTINUOUS_MODE_TILE_DURATION.
            return pendulum.Duration(days=1)
        else:
            return (
                utils.get_duration_field_or_none(proto.materialized_feature_view_args, "batch_schedule")
                or slide_interval
            )
    else:
        return utils.get_duration_field_or_none(proto.materialized_feature_view_args, "batch_schedule")


# TODO: fix/cleanup
def args_oneof_timewindow_to_spec(proto: Any) -> TimeWindowSpec:  # noqa: ANN401
    if proto.HasField("time_window"):
        return RelativeTimeWindowSpec.from_args_proto(proto.time_window)
    elif proto.HasField("time_window_series"):
        return TimeWindowSeriesSpec.from_args_proto(proto.time_window_series)
    elif proto.HasField("lifetime_window"):
        return LifetimeWindowSpec()
    else:
        msg = f"Unexpected time window type in agg args proto: {proto}"
        raise ValueError(msg)


@typechecked
def get_aggregate_features_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Tuple[feature_view__data_pb2.Aggregate, ...]:
    is_continuous = (
        proto.materialized_feature_view_args.stream_processing_mode
        == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
    )
    aggregate_features = []
    for agg_args_proto in proto.materialized_feature_view_args.aggregations:
        window_spec = args_oneof_timewindow_to_spec(agg_args_proto)

        agg_data_proto = create_aggregate_features(
            agg_args_proto, proto.materialized_feature_view_args.aggregation_interval, is_continuous, window_spec
        )
        aggregate_features.append(agg_data_proto)
    return tuple(aggregate_features)


@typechecked
def _get_aggregation_interval_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
    is_continuous: bool,
    data_source_type: Optional[data_source_type_pb2.DataSourceType.ValueType],
) -> Optional[duration_pb2.Duration]:
    if proto.materialized_feature_view_args.compaction_enabled:
        is_stream = (
            data_source_type == data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH if data_source_type else False
        )
        # Default set in Kotlin for batch fvs with compaction is the batch schedule. Batch schedule is required for fvs with compaction_enabled=True
        # Default set in Kotlin for non-continuous stream fvs with compaction is the stream compaction tile size.
        if not is_stream:
            return utils.get_field_or_none(proto.materialized_feature_view_args, "batch_schedule")
        elif not is_continuous:
            return utils.get_field_or_none(proto.materialized_feature_view_args, "stream_tile_size")

    return utils.get_field_or_none(proto.materialized_feature_view_args, "aggregation_interval")


@typechecked
def get_is_continuous_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> bool:
    data_source_type = utils.get_field_or_none(proto.materialized_feature_view_args, "data_source_type")
    if not data_source_type or data_source_type == data_source_type_pb2.DataSourceType.BATCH:
        return False

    if proto.materialized_feature_view_args.compaction_enabled:
        return proto.materialized_feature_view_args.stream_tiling_enabled == False

    return (
        proto.materialized_feature_view_args.stream_processing_mode
        == feature_view__args_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
    )


@typechecked
def get_batch_trigger_from_feature_view_args(
    proto: feature_view__args_pb2.FeatureViewArgs,
) -> Optional[feature_view__args_pb2.BatchTriggerType.ValueType]:
    if proto.materialized_feature_view_args.HasField("batch_trigger"):
        return proto.materialized_feature_view_args.batch_trigger
    else:
        return feature_view__args_pb2.BatchTriggerType.BATCH_TRIGGER_TYPE_SCHEDULED


@typechecked
def get_join_keys_from_feature_view_args(proto: feature_view__args_pb2.FeatureViewArgs) -> Tuple[str, ...]:
    join_keys = []
    for entity in proto.entities:
        join_keys.extend(entity.join_keys)
    return tuple(join_keys)


@typechecked
def resolve_timestamp_field_for_materialized_feature_view(
    feature_view_args: feature_view__args_pb2.FeatureViewArgs,
    view_schema: schema_pb2.Schema,
) -> str:
    if feature_view_args.materialized_feature_view_args.HasField("timestamp_field"):
        return feature_view_args.materialized_feature_view_args.timestamp_field
    return _get_timestamp_column(view_schema)


@typechecked
def get_online_serving_keys_from_feature_view_args(proto: feature_view__args_pb2.FeatureViewArgs) -> Tuple[str, ...]:
    return (
        tuple(proto.online_serving_index) if proto.online_serving_index else get_join_keys_from_feature_view_args(proto)
    )


@typechecked
def create_aggregate_features(
    feature_aggregation: feature_view__args_pb2.FeatureAggregation,
    aggregation_interval_seconds: duration_pb2.Duration,
    is_continuous: bool,
    time_window: TimeWindowSpec,
) -> feature_view__data_pb2.Aggregate:
    """Build a AggregateFeature data proto from the input FeatureAggregation args proto."""
    feature_function = get_aggregation_enum_from_string(feature_aggregation.function.lower())
    assert feature_function, f"Unknown aggregation name: {feature_aggregation.function}"

    if feature_function in {
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    }:
        function_params = afpb.AggregationFunctionParams(
            last_n=afpb.LastNParams(n=feature_aggregation.function_params["n"].int64_value)
        )
    elif feature_function in {
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
        afpb.AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
    }:
        function_params = afpb.AggregationFunctionParams(
            first_n=afpb.FirstNParams(n=feature_aggregation.function_params["n"].int64_value)
        )
    elif feature_function == afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT:
        function_params = afpb.AggregationFunctionParams(
            approx_count_distinct=afpb.ApproxCountDistinctParams(
                precision=feature_aggregation.function_params["precision"].int64_value
            )
        )
    elif feature_function == afpb.AggregationFunction.AGGREGATION_FUNCTION_APPROX_PERCENTILE:
        function_params = afpb.AggregationFunctionParams(
            approx_percentile=afpb.ApproxPercentileParams(
                precision=feature_aggregation.function_params["precision"].int64_value,
                percentile=feature_aggregation.function_params["percentile"].double_value,
            )
        )
    else:
        function_params = None

    if len(feature_aggregation.function_params) > 0:
        assert function_params is not None, (
            "function_params in the data proto should not be None since it is a non-empty dictionary in the args proto"
        )
    return feature_view__data_pb2.Aggregate(
        input_feature_name=feature_aggregation.column,
        output_feature_name=feature_aggregation.name,
        function=feature_function,
        time_window=window_spec_to_window_data_proto(time_window),
        function_params=function_params,
        batch_sawtooth_tile_size=feature_aggregation.batch_sawtooth_tile_size
        if feature_aggregation.HasField("batch_sawtooth_tile_size")
        else None,
        description=get_field_or_none(feature_aggregation, "description"),
        tags=dict(feature_aggregation.tags) if feature_aggregation.tags else None,
    )
