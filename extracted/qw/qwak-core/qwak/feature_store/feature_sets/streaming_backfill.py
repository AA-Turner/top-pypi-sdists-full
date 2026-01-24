from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Set, Union

from _qwak_proto.qwak.feature_store.features.execution_pb2 import (
    ExecutionSpec as ProtoExecutionSpec,
)
from _qwak_proto.qwak.execution.v1.streaming_aggregation_pb2 import (
    StreamingAggregationBackfillIngestion as ProtoStreamingAggregationBackfillIngestion,
    BackfillDataSource as ProtoBackfillDataSource,
    TimeRange as ProtoTimeRange,
)
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp
from qwak.exceptions import QwakException
from qwak.feature_store._common.artifact_utils import ArtifactSpec, ArtifactsUploader
from qwak.feature_store.feature_sets.execution_spec import ClusterTemplate
from qwak.feature_store.feature_sets.transformations import SparkSqlTransformation

_BACKFILL_ = "_qwak_backfill_specification"


@dataclass
class BackfillDataSource:
    data_source_name: str
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _to_proto(self) -> ProtoBackfillDataSource:
        start_timestamp: Optional[ProtoTimestamp] = None
        end_timestamp: Optional[ProtoTimestamp] = None

        if self.end_datetime:
            end_timestamp = ProtoTimestamp()
            end_timestamp.FromDatetime(self.end_datetime.astimezone(timezone.utc))

        if self.start_datetime:
            start_timestamp = ProtoTimestamp()
            start_timestamp.FromDatetime(self.start_datetime.astimezone(timezone.utc))

        time_range = ProtoTimeRange(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

        return ProtoBackfillDataSource(
            data_source_name=self.data_source_name,
            time_range=time_range,
        )

    @classmethod
    def _from_proto(cls, proto: ProtoBackfillDataSource) -> "BackfillDataSource":
        start_datetime: Optional[datetime] = None
        end_datetime: Optional[datetime] = None

        time_range: ProtoTimeRange = proto.time_range

        proto_start_timestamp: Optional[ProtoTimestamp] = (
            time_range.start_timestamp if time_range.start_timestamp else None
        )
        proto_end_timestamp: Optional[ProtoTimestamp] = (
            time_range.end_timestamp if time_range.end_timestamp else None
        )

        start_datetime = (
            datetime.fromtimestamp(
                proto_start_timestamp.seconds + proto_start_timestamp.nanos / 1e9
            )
            if proto_start_timestamp
            else None
        )

        end_datetime = (
            datetime.fromtimestamp(
                proto_end_timestamp.seconds + proto_end_timestamp.nanos / 1e9
            )
            if proto_end_timestamp
            else None
        )

        return cls(
            data_source_name=proto.data_source_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

    def _validate(self):
        if self.start_datetime and self.end_datetime:
            if self.start_datetime >= self.end_datetime:
                raise QwakException(
                    f"Backfill data source {self.data_source_name} has invalid time range: "
                    f"start_datetime {self.start_datetime} is after or equal end_datetime {self.end_datetime}."
                )

        if not self.data_source_name:
            raise QwakException(
                "Backfill data source must have a valid data source name."
            )


@dataclass
class StreamingBackfill:
    featureset_name: str
    start_datetime: datetime
    end_datetime: datetime
    data_sources: List[BackfillDataSource]
    transform: "SparkSqlTransformation"
    cluster_template: Optional[ClusterTemplate] = ClusterTemplate.SMALL

    def __post_init__(self):
        if not self.featureset_name:
            raise QwakException("featureset_name must be provided for backfill.")

        if not self.start_datetime or not self.end_datetime:
            raise QwakException(
                "For Streaming backfill, start_datetime and end_datetime are mandatory fields."
            )

        if self.start_datetime >= self.end_datetime:
            raise QwakException(
                f"Backfill has invalid time range: "
                f"start_datetime {self.start_datetime} is after or equal end_datetime {self.end_datetime}."
            )

        if not self.data_sources:
            raise QwakException(
                "Trying to create a streaming backfill with no data sources. "
                "At least one data source has to be provided when trying to create a streaming backfill."
            )

        if type(self.transform) is not SparkSqlTransformation:
            raise QwakException(
                "For backfill, only Spark SQL transformation type is currently supported"
            )

        self._validate_unique_sources()

    def _validate_unique_sources(self):
        source_names: List[str] = [
            data_source.data_source_name for data_source in self.data_sources
        ]
        duplicates: Set[str] = {
            item for item in source_names if source_names.count(item) > 1
        }
        if duplicates:
            raise QwakException(
                f"A specific data source can only appear once per backfill definition. "
                f"Found these duplicates: {', '.join(set(duplicates))}"
            )

    def _to_proto(
        self,
        original_instance_module_path: str,
    ) -> ProtoStreamingAggregationBackfillIngestion:
        artifact_url: Optional[str] = None
        artifact_spec: Optional[ArtifactSpec] = ArtifactsUploader.get_artifact_spec(
            transformation=self.transform,
            featureset_name=f"{self.featureset_name}-backfill",
            __instance_module_path__=original_instance_module_path,
        )

        if artifact_spec:
            artifact_url = ArtifactsUploader.upload(artifact_spec)

        end_timestamp = ProtoTimestamp()
        end_timestamp.FromDatetime(self.end_datetime.astimezone(timezone.utc))

        start_timestamp = ProtoTimestamp()
        start_timestamp.FromDatetime(self.start_datetime.astimezone(timezone.utc))

        return ProtoStreamingAggregationBackfillIngestion(
            featureset_name=self.featureset_name,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            execution_spec=ProtoExecutionSpec(
                cluster_template=ClusterTemplate.to_proto(self.cluster_template)
            ),
            transformation=self.transform._to_proto(artifact_path=artifact_url),
            data_source_specs=[
                data_source._to_proto() for data_source in self.data_sources
            ],
        )

    @classmethod
    def _from_proto(cls, proto: ProtoStreamingAggregationBackfillIngestion):
        backfill_data_sources = [
            BackfillDataSource._from_proto(ds) for ds in proto.data_source_specs
        ]

        return cls(
            featureset_name=proto.featureset_name,
            start_datetime=datetime.fromtimestamp(
                proto.start_timestamp.seconds + proto.start_timestamp.nanos / 1e9
            ),
            end_datetime=datetime.fromtimestamp(
                proto.end_timestamp.seconds + proto.end_timestamp.nanos / 1e9
            ),
            data_sources=backfill_data_sources,
            transform=SparkSqlTransformation._from_proto(
                proto.transformation.sql_transformation
            ),
            cluster_template=(
                ClusterTemplate.from_proto(proto.execution_spec.cluster_template)
                if proto.execution_spec.cluster_template
                else None
            ),
        )

    @staticmethod
    def _get_normalized_backfill_sources_spec(
        data_sources: Union[List[str], List[BackfillDataSource]],
    ) -> List[BackfillDataSource]:
        # reformat all data source names to 'BackfillDataSource'
        return [
            (
                BackfillDataSource(data_source_name=data_source)
                if isinstance(data_source, str)
                else data_source
            )
            for data_source in data_sources
        ]
