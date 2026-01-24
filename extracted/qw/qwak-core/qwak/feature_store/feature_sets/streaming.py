import collections
import functools
import inspect
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from _qwak_proto.qwak.feature_store.features.execution_pb2 import (
    StreamingExecutionSpec as ProtoStreamingExecutionSpec,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import (
    FeatureSetSpec as ProtoFeatureSetSpec,
)
from _qwak_proto.qwak.feature_store.features.feature_set_types_pb2 import (
    AggregationSpec as ProtoAggregationSpec,
    FeatureSetType as ProtoFeatureSetType,
    StreamingAggregationFeatureSet as ProtoStreamingAggregationFeatureSet,
    StreamingFeatureSetV1 as ProtoStreamingFeatureSetV1,
)
from _qwak_proto.qwak.feature_store.sources.streaming_pb2 import (
    StreamingSource,
    StreamingSource as ProtoStreamingSource,
)
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.exceptions import QwakException
from qwak.feature_store._common.artifact_utils import ArtifactSpec, ArtifactsUploader
from qwak.feature_store.entities.entity import Entity
from qwak.feature_store.feature_sets._utils._featureset_utils import FeaturesetUtils
from qwak.feature_store.feature_sets.base_feature_set import BaseFeatureSet
from qwak.feature_store.feature_sets.execution_spec import ClusterTemplate
from qwak.feature_store.feature_sets.metadata import (
    Metadata,
    get_metadata_from_function,
    set_metadata_on_function,
)
from qwak.feature_store.feature_sets.streaming_backfill import (
    BackfillDataSource,
    StreamingBackfill,
)
from qwak.feature_store.feature_sets.transformations import (
    BaseTransformation,
    PySparkTransformation,
    SparkSqlTransformation,
    Window,
)
from qwak.feature_store.sinks.base import BaseSink
from qwak.feature_store.sinks.streaming.factory import StreamingSinkFactory
from qwak.feature_store.validations.validation_options import (
    FeatureSetValidationOptions,
)
from typeguard import typechecked

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass

_OFFLINE_SCHEDULING_ATTRIBUTE = "_qwak_offline_scheduling"
_OFFLINE_CLUSTER_SPEC = "_qwak_offline_cluster_specification"
_ONLINE_TRIGGER_INTERVAL = "_qwak_online_trigger_interval"
_ONLINE_CLUSTER_SPEC = "_qwak_online_cluster_specification"
_METADATA_ = "_qwak_online_cluster_specification"


@typechecked
def feature_set(
    *,
    data_sources: List[str],
    timestamp_column_name: str,
    offline_scheduling_policy: Optional[str] = "*/30 * * * *",
    online_trigger_interval: Optional[int] = 5,
    name: Optional[str] = None,
    entity: Optional[str] = None,
    key: Optional[str] = None,
    auxiliary_sinks: List[BaseSink] = [],
    repository: Optional[str] = None,
    backfill_max_timestamp: Optional[datetime] = None,
):
    """
    Creates a streaming feature set for the specified entity using the given streaming data sources.

    A streaming feature set allows for real-time updates of features from live data sources, letting ML models access
    the most recent values without waiting for batch updates.

    :param entity: The name of the entity for which the feature set is being created. An entity typically represents a
                   unique object or concept, like 'user', 'product', etc. Entity and key are mutually exclusive.
    :param key: a column name in the feature set which is the key. Entity and key are mutually exclusive.
    :param data_sources: A list of references to the data sources from which the feature values will be streamed.
                                Each data source should be capable of providing data in a streaming manner.
    :param timestamp_column_name: The name of the column in the data source that contains timestamp information. This
                                  is used to order the data chronologically and ensure that the feature values are
                                  updated in the correct order.
    :param offline_scheduling_policy: Defines the offline ingestion policy - which affects the data freshness of
                                      the offline store. defaults to */30 * * * * (every 30 minutes)
    :param online_trigger_interval: Defines the online ingestion policy  - which affects the data freshness of
                                      the online store. defaults to 5 seconds
    :param name: An optional name for the feature set. If not provided, the name of the function will be used.
    :param  auxiliary_sinks: list of auxiliary sinks. Not supported with Aggregations
    Example:

    ... code-block:: python

        @streaming.feature_set(
            entity="users",
            data_sources=["users_registration_stream"],
            timestamp_column_name="reg_date"
        )
        def user_streaming_features():
            return SparkSqlTransformation("SELECT user_id, reg_country, reg_date FROM data_source")
    """

    def decorator(function):
        if isinstance(function, StreamingBackfill):
            raise QwakException(
                "Backfill can no longer be defined as a decorator on the feature set, it must be triggered after feature set creation."
            )

        user_transformation = function()
        FeaturesetUtils.validate_base_featureset_decorator(
            user_transformation=user_transformation, entity=entity, key=key
        )

        FeaturesetUtils.validate_streaming_featureset_decorator(
            online_trigger_interval=online_trigger_interval,
            offline_scheduling_policy=offline_scheduling_policy,
        )

        fs_name = name or function.__name__
        streaming_feature_set = StreamingFeatureSet(
            name=fs_name,
            entity=entity if entity else None,
            key=key if key else None,
            repository=repository,
            data_sources=data_sources,
            timestamp_column_name=timestamp_column_name,
            transformation=user_transformation,
            metadata=get_metadata_from_function(
                function, description=fs_name, display_name=fs_name
            ),
            online_trigger_interval=(
                online_trigger_interval if online_trigger_interval else 5
            ),
            offline_scheduling_policy=(
                offline_scheduling_policy
                if offline_scheduling_policy
                else "*/30 * * * *"
            ),
            offline_cluster_template=getattr(
                function, _OFFLINE_CLUSTER_SPEC, ClusterTemplate.SMALL
            ),
            online_cluster_template=getattr(
                function, _ONLINE_CLUSTER_SPEC, ClusterTemplate.SMALL
            ),
            backfill_max_timestamp=backfill_max_timestamp,
            __instance_module_path__=inspect.stack()[1].filename,
            auxiliary_sinks=auxiliary_sinks,
        )

        functools.update_wrapper(streaming_feature_set, user_transformation)
        return streaming_feature_set

    return decorator


@typechecked
def execution_specification(
    *,
    online_cluster_template: Optional[ClusterTemplate] = None,
    offline_cluster_template: Optional[ClusterTemplate] = None,
):
    """
    Set the execution specification of the cluster running the feature set

    :param online_cluster_template: Predefined template sizes
    :param offline_cluster_template: Predefined template sizes

    Cluster template example:

    ... code-block:: python
        @streaming.feature_set(entity="users", data_sources=["streaming_users_source"])
        @streaming.execution_specification(
                offline_cluster_template=ClusterTemplate.MEDIUM,
                online_cluster_template=ClusterTemplate.MEDIUM)
        def user_streaming_features():
            return SparkSqlTransformation("SELECT user_id, age, timestamp FROM streaming_users_source"
    """

    def decorator(user_transformation):
        setattr(user_transformation, _ONLINE_CLUSTER_SPEC, online_cluster_template)

        setattr(user_transformation, _OFFLINE_CLUSTER_SPEC, offline_cluster_template)

        return user_transformation

    return decorator


@typechecked
def backfill(
    *,
    feature_set_name: str,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    data_sources: Union[List[str], List[BackfillDataSource]],
    backfill_cluster_template: Optional[ClusterTemplate] = ClusterTemplate.SMALL,
):
    """
    Triggers a backfill execution for an existing streaming featureset. Currently available for streaming
    aggregation featuresets only.

    Args:
        feature_set_name (str): Name of the FeatureSet to trigger a backfill for.
        start_date (datetime): Backfill start date, on Streaming Aggregation Feature Sets,
            needs to align with the FeatureSet tiles.
        end_date (datetime): Backfill end date, on Streaming Aggregation Feature Sets,
            needs to align with the FeatureSet tiles and be smaller than the Feature Set's backfill_max_timestamp.
        data_sources (list[BackfillDataSource] | list[str]): A list of BackfillDataSource objects containing
            batch source name and optional time range, or a list of batch source names (with no time range limits).
        backfill_cluster_template (ClusterTemplate, optional): An optional cluster specification for the backfill job.
            Defaults to SMALL.

    Examples:
        @streaming.backfill(
            feature_set_name="user_streaming_agg_features",
            start_date=datetime(2022,1,1,0,0,0),
            end_date=datetime(2023,9,1,0,0,0),
            data_sources=[BackfillDataSource(data_source_name="backfill_data_source",
                                             start_datetime=datetime(2023,1,1,0,0,0),
                                             end_datetime=datetime(2023,8,1,0,0,0))],
            backfill_cluster_template=ClusterTemplate.SMALL
        )
        def backfill_transformation():
            return SparkSqlTransformation("SELECT user_id, reg_country, reg_date FROM backfill_data_source")
    """

    def decorator(function):
        if isinstance(function, StreamingFeatureSet):
            raise QwakException(
                "Backfill can no longer be defined as a decorator on the feature set, it must be triggered after feature set creation."
            )

        backfill_transformation: SparkSqlTransformation = function()

        if not isinstance(backfill_transformation, SparkSqlTransformation):
            raise QwakException(
                "Backfill must defined on a method returning a SparkSqlTransformation"
            )

        streaming_backfill = StreamingBackfill(
            featureset_name=feature_set_name,
            start_datetime=start_date,
            end_datetime=end_date,
            data_sources=StreamingBackfill._get_normalized_backfill_sources_spec(
                data_sources
            ),
            transform=backfill_transformation,
            cluster_template=backfill_cluster_template,
        )

        functools.update_wrapper(streaming_backfill, backfill_transformation)

        return streaming_backfill

    return decorator


@typechecked
def metadata(
    *,
    owner: Optional[str] = None,
    description: Optional[str] = None,
    display_name: Optional[str] = None,
    version_comment: Optional[str] = None,
):
    """
    Sets additional user provided metadata

    :param owner: feature set owner
    :param description: General description of the feature set
    :param display_name: Human readable name of the feature set
    :param version_comment: Comment which describes the version

    Example:

    ... code-block:: python

        @streaming.feature_set(
            entity="users",
            data_sources=["users_registration_stream"],
            timestamp_column_name="reg_date"
        )
        @streaming.metadata(
            owner="datainfra@qwak.com",
            display_name="User Streaming Features",
            description="Users feature from the Kafka topic of users registration stream",
        )
        def user_streaming_features():
            return SparkSqlTransformation("SELECT user_id, reg_country, reg_date FROM data_source")

    """

    def decorator(function):
        _validate_decorator_ordering(function)
        set_metadata_on_function(
            function=function,
            owner=owner,
            description=description,
            display_name=display_name,
            version_comment=version_comment,
        )

        return function

    return decorator


def _validate_decorator_ordering(function):
    if isinstance(function, StreamingFeatureSet):
        raise ValueError(
            "Wrong decorator ordering - @streaming.feature_set should be the top most decorator"
        )


@dataclass
class StreamingFeatureSet(BaseFeatureSet):
    timestamp_column_name: str = str()
    online_trigger_interval: int = int()
    offline_scheduling_policy: str = str()
    transformation: Optional[BaseTransformation] = None
    offline_cluster_template: Optional[ClusterTemplate] = None
    online_cluster_template: Optional[ClusterTemplate] = None
    metadata: Optional[Metadata] = None
    backfill_max_timestamp: Optional[datetime] = None
    auxiliary_sinks: List[BaseSink] = field(default_factory=lambda: [])

    def __post_init__(self):
        self._validate()

    @classmethod
    def _from_proto(cls, proto: ProtoFeatureSetSpec):
        streaming_def: ProtoStreamingFeatureSetV1 = (
            proto.feature_set_type.streaming_feature_set_v1
        )

        return cls(
            name=proto.name,
            repository=proto.featureset_repository_name,
            entity=Entity._from_proto(proto.entity).name,
            data_sources=[ds.name for ds in streaming_def.data_sources],
            timestamp_column_name=streaming_def.timestamp_column_name,
            online_trigger_interval=streaming_def.online_trigger_interval,
            offline_scheduling_policy=streaming_def.offline_scheduling_policy,
            transformation=BaseTransformation._from_proto(streaming_def.transformation),
            offline_cluster_template=ClusterTemplate.from_cluster_template_number(
                streaming_def.execution_spec.offline_cluster_template
            ),
            online_cluster_template=ClusterTemplate.from_cluster_template_number(
                streaming_def.execution_spec.online_cluster_template
            ),
            metadata=Metadata.from_proto(proto.metadata),
            auxiliary_sinks=[
                StreamingSinkFactory.get_streaming_sink(proto)
                for proto in streaming_def.auxiliary_sinks
            ],
        )

    def _get_data_sources(
        self, feature_registry: FeatureRegistryClient
    ) -> List[ProtoStreamingSource]:
        sources: List[ProtoStreamingSource] = list()

        for name in self.data_sources:
            ds = feature_registry.get_data_source_by_name(name)
            if not ds:
                raise QwakException(
                    f"Trying to register a featureset with a non existing data source {name}"
                )
            else:
                sources.append(
                    ds.data_source.data_source_definition.data_source_spec.stream_source
                )
        return sources

    def _to_proto(
        self,
        git_commit,
        features,
        feature_registry: FeatureRegistryClient,
        artifact_url: Optional[str] = None,
        **kwargs,
    ) -> Tuple[ProtoFeatureSetSpec, Optional[str]]:
        maybe_initial_tile_size: Optional[int] = self._validate_streaming_aggregation()

        data_sources: List[StreamingSource] = self._get_data_sources(feature_registry)

        if not artifact_url:
            artifact: Optional[ArtifactSpec] = ArtifactsUploader.get_artifact_spec(
                transformation=self.transformation,
                featureset_name=self.name,
                __instance_module_path__=self.__instance_module_path__,
            )
            if artifact:
                artifact_url = ArtifactsUploader.upload(artifact)

        proto_featureset_type: ProtoFeatureSetType
        if maybe_initial_tile_size is None:
            # row-level streaming
            proto_featureset_type = self._get_streaming_featureset_proto(
                artifact_url=artifact_url, streaming_sources=data_sources
            )
        else:
            # streaming aggregation
            proto_featureset_type = self._get_streaming_aggregation_featureset_proto(
                artifact_url=artifact_url,
                streaming_sources=data_sources,
                initial_tile_size=maybe_initial_tile_size,
            )

        return (
            ProtoFeatureSetSpec(
                name=self.name,
                metadata=self.metadata.to_proto(),
                git_commit=git_commit,
                features=features,
                entity=self._get_entity_definition(feature_registry),
                feature_set_type=proto_featureset_type,
                featureset_repository_name=self.repository,
            ),
            artifact_url,
        )

    def _validate(self):
        import croniter

        super()._validate()

        # verify offline_scheduling_policy was set
        if not self.offline_scheduling_policy:
            raise QwakException("'offline_scheduling_policy' field must be set")

        # verify the cron expression is valid
        if not croniter.croniter.is_valid(self.offline_scheduling_policy):
            raise QwakException(
                f"offline scheduling policy "
                f"'{self.offline_scheduling_policy}'"
                f" is not a valid cron expression"
            )

        # verify the online scheduling policy is valid
        if self.online_trigger_interval < 0:
            raise QwakException(
                f"Value '{self.online_trigger_interval}'"
                f" is not a legal online scheduling policy, "
                f"only non-negative integers are allowed"
            )

        # verify timestamp_col_name was set
        if not self.timestamp_column_name:
            raise QwakException("'timestamp_col_name' field must be set")

        is_streaming_agg = bool(self._validate_streaming_aggregation())

        # if sinks were configured, make sure it's not streaming-agg
        if len(self.auxiliary_sinks) > 0 and is_streaming_agg:
            raise QwakException(
                "Auxiliary Sinks Are not supported in Streaming Aggregation Feature Sets"
            )

        if self.backfill_max_timestamp and not is_streaming_agg:
            raise QwakException(
                "backfill_max_timestamp can only be set for Streaming Aggregation FeatureSet."
            )

        # Validate transformation is PySpark when multiple data sources are used
        if len(self.data_sources) > 1 and not isinstance(
            self.transformation, PySparkTransformation
        ):
            raise QwakException(
                "When using multiple data sources, only `PySparkTransformation` is allowed."
            )

    def _validate_streaming_aggregation(self) -> Optional[int]:
        if not (self.transformation.windows or self.transformation.aggregations):
            # definitely not streaming aggregation
            return None

        # at least 1 window and/or at least 1 aggregate - so we need to verify
        # it's a valid streaming aggregation definition
        if not self.transformation.windows:
            raise QwakException(
                "When specifying aggregations, at least one time window must be defined"
            )

        if not self.transformation.aggregations:
            raise QwakException(
                "When specifying time windows, at least one aggregation must be defined"
            )

        (
            initial_tile_size,
            min_window,
        ) = StreamingFeatureSet._get_default_slide_period(self.transformation.windows)

        if initial_tile_size > max(10.0, (min_window / 10)):
            raise QwakException(
                "Windows with such different cardinality (For example years vs days) can't be in "
                "the same feature set. Please separate to different feature sets."
            )

        # Validate no feature duplications exist

        # Get feature names, with or without aliases
        final_feature_names = self.transformation.get_features_names()

        # Look for duplicated feature names
        group_by_feature_name_to_count = collections.Counter(final_feature_names)
        features_with_duplicates = [
            feature
            for feature, count in group_by_feature_name_to_count.items()
            if count > 1
        ]
        if features_with_duplicates:
            error_message_str = ""
            for dup in features_with_duplicates:
                error_message_str += (
                    f"{repr(dup)} feature, appears more than once in Aggregations.\n"
                )
            raise QwakException(error_message_str)

        if not self.backfill_max_timestamp:
            raise QwakException(
                """
                backfill_max_timestamp must be set for Streaming Aggregation FeatureSet.
                 Events earlier than this timestamp can only be processed by triggering backfill,
                 the Streaming job will not process events that are earlier than this timestamp.
            """
            )

        self._validate_streaming_aggregation_backfill_max_timestamp()

        return initial_tile_size

    def _validate_streaming_aggregation_backfill_max_timestamp(self):
        initial_tile_size, _ = StreamingFeatureSet._get_default_slide_period(
            self.transformation.windows
        )

        if self.backfill_max_timestamp.timestamp() % initial_tile_size != 0:
            raise QwakException(
                f"Chosen backfill max timestamp is invalid,"
                f" it has to be exactly dividable by slice size of {initial_tile_size} seconds."
            )

    @staticmethod
    def _get_default_slide_period(
        windows: List[Window], minimum_time_window_seconds: int = 10
    ):
        """
        Tile size is the max between the `minimum_time_window_seconds`,
        and the round down of the max window size divided by 2048.
        By dividing by 2048 we promise that the max aggregation time contains
        up to 2048 different tiles, which limit the amount of keys that exists in the Online Store.
        :param windows:
        :param minimum_time_window_seconds:
        :return: tuple of tile size and the minimum window size seconds
        """
        time_windows_in_seconds = [w.length * w.seconds_in_time_unit for w in windows]
        max_window = max(time_windows_in_seconds)
        min_window = min(time_windows_in_seconds)

        if min_window < minimum_time_window_seconds:
            raise QwakException(
                f"The minimum time window is {minimum_time_window_seconds} seconds"
            )

        def round(k):
            return k - (k % minimum_time_window_seconds)

        initial_tile_size = round(max((max_window / 2048), minimum_time_window_seconds))

        return int(initial_tile_size), min_window

    def get_sample(
        self,
        number_of_rows: int = 10,
        validation_options: Optional[FeatureSetValidationOptions] = None,
    ) -> "pd.DataFrame":
        return super().get_sample(
            number_of_rows=number_of_rows, validation_options=validation_options
        )

    def _get_streaming_featureset_proto(
        self, artifact_url: Optional[str], streaming_sources: List[StreamingSource]
    ) -> ProtoFeatureSetType:
        return ProtoFeatureSetType(
            streaming_feature_set_v1=ProtoStreamingFeatureSetV1(
                transformation=self.transformation._to_proto(
                    artifact_path=artifact_url
                ),
                data_sources=streaming_sources,
                execution_spec=ProtoStreamingExecutionSpec(
                    online_cluster_template=ClusterTemplate.to_proto(
                        self.online_cluster_template
                    ),
                    offline_cluster_template=ClusterTemplate.to_proto(
                        self.offline_cluster_template
                    ),
                ),
                timestamp_column_name=self.timestamp_column_name,
                online_trigger_interval=self.online_trigger_interval,
                offline_scheduling_policy=self.offline_scheduling_policy,
                auxiliary_sinks=[
                    s.to_proto_streaming_sink() for s in self.auxiliary_sinks
                ],
            )
        )

    def _get_streaming_aggregation_featureset_proto(
        self,
        artifact_url: Optional[str],
        streaming_sources: List[StreamingSource],
        initial_tile_size: int,
    ) -> ProtoFeatureSetType:
        backfill_max_timestamp = ProtoTimestamp()
        backfill_max_timestamp.FromDatetime(
            self.backfill_max_timestamp.astimezone(timezone.utc)
        )
        return ProtoFeatureSetType(
            streaming_aggregation_feature_set=ProtoStreamingAggregationFeatureSet(
                transformation=self.transformation._to_proto(
                    artifact_path=artifact_url
                ),
                data_sources=streaming_sources,
                execution_spec=ProtoStreamingExecutionSpec(
                    online_cluster_template=ClusterTemplate.to_proto(
                        self.online_cluster_template
                    ),
                    offline_cluster_template=ClusterTemplate.to_proto(
                        self.offline_cluster_template
                    ),
                ),
                timestamp_column_name=self.timestamp_column_name,
                online_trigger_interval=self.online_trigger_interval,
                compaction_scheduling_policy=self.offline_scheduling_policy,
                aggregation_spec=ProtoAggregationSpec(
                    slide_seconds=initial_tile_size,
                    allowed_late_arrival_seconds=60 * 10,
                    aggregations=self.transformation._get_aggregations_proto(),
                ),
                backfill_spec=None,
                backfill_max_timestamp=backfill_max_timestamp,
            )
        )
