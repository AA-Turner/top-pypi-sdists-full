from __future__ import annotations

import collections.abc
import dataclasses
import datetime as dt
import enum
import json
import os
import random
import shutil
import tempfile
import types
import typing
import warnings
from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Mapping, Optional, Sequence, Tuple, TypeVar, Union
from urllib.parse import urlparse

import grpc
import grpc.experimental
import requests
from google.protobuf import empty_pb2, timestamp_pb2
from rich.console import Console
from rich.style import Style
from rich.text import Text

from chalk import DataFrame, EnvironmentId, chalk_logger
from chalk._gen.chalk.aggregate.v1.service_pb2 import (
    AGGREGATE_BACKFILL_MODE_CREATE,
    AGGREGATE_BACKFILL_MODE_PLAN,
    CreateAggregateBackfillJobResponse,
    CreateAggregateBackfillV2Request,
    CreateAggregateBackfillV2Response,
)
from chalk._gen.chalk.aggregate.v1.service_pb2_grpc import AggregateServiceStub
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import offline_query_pb2, online_query_pb2, resources_pb2, upload_features_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery, UploadFeaturesBulkRequest
from chalk._gen.chalk.common.v1.script_task_pb2 import ScriptTaskKind, ScriptTaskRequest, TrainingRunArgs
from chalk._gen.chalk.common.v2.execute_plan_pb2 import ExecutePlanRequest, ExecutePlanResponse
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.bloom_filter_pb2 import InspectBloomFiltersRequest
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.engine.v2.dataframe_service_pb2_grpc import DataFrameServiceStub
from chalk._gen.chalk.engine.v2.offline_store_service_pb2_grpc import OfflineStoreServiceStub
from chalk._gen.chalk.engine.v2.query_values_pb2 import GetQueryValuesRequest, OperationIdTableIdentifier
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk._gen.chalk.graph.v1.graph_pb2 import Graph
from chalk._gen.chalk.modeldeployment.v1.service_pb2_grpc import ModelDeploymentServiceStub
from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
from chalk._gen.chalk.protosql.v1.sql_service_pb2 import (
    ExecuteSqlQueryRequest,
    ExecuteSqlResultPersistenceSettings,
    GetDbCatalogsRequest,
    GetDbSchemasRequest,
    GetTablesRequest,
    PlanSqlQueryRequest,
)
from chalk._gen.chalk.protosql.v1.sql_service_pb2_grpc import SqlServiceStub
from chalk._gen.chalk.scalinggroup.v1 import service_pb2 as scalinggroup_service_pb2
from chalk._gen.chalk.scalinggroup.v1.service_pb2_grpc import ScalingGroupManagerServiceStub
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.builder_pb2 import (
    ActivateDeploymentRequest,
    DeployKubeComponentsRequest,
    IndexDeploymentRequest,
    RebuildDeploymentRequest,
    RedeployDeploymentRequest,
    ResumeEnvironmentRequest,
    StartBranchResponse,
    StartShadowBuildFromDeploymentRequest,
    SuspendEnvironmentRequest,
)
from chalk._gen.chalk.server.v1.builder_pb2_grpc import BuilderServiceStub
from chalk._gen.chalk.server.v1.dataframe_pb2_grpc import DataFrameServiceStub as ApiDataFrameServiceStub
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import (
    GetJobQueueOperationSummaryRequest,
    GetJobQueueOperationSummaryResponse,
)
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import JobQueueKind as ProtoJobQueueKind
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import JobQueueState as ProtoJobQueueState
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import ListDataPlaneJobQueueRequest
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2_grpc import DataPlaneJobQueueServiceStub
from chalk._gen.chalk.server.v1.dataplaneworkflows_pb2_grpc import DataPlaneWorkflowsServiceStub
from chalk._gen.chalk.server.v1.datasets_pb2 import ListDatasetsRequest
from chalk._gen.chalk.server.v1.datasets_pb2_grpc import DatasetMetadataServiceStub
from chalk._gen.chalk.server.v1.deploy_pb2 import (
    CreateBranchFromSourceDeploymentRequest,
    CreateBranchFromSourceDeploymentResponse,
    GetActiveDeploymentsRequest,
)
from chalk._gen.chalk.server.v1.deploy_pb2_grpc import DeployServiceStub
from chalk._gen.chalk.server.v1.environment_pb2 import DeploymentBuildProfile
from chalk._gen.chalk.server.v1.graph_pb2 import (
    GetAllOfflineStoreTablesRequest,
    GetCodegenFeaturesFromGraphRequest,
    GetCodegenFeaturesFromGraphResponse,
    GetGraphRequest,
    GetGraphResponse,
    GetOfflineStoreTableRequest,
    PythonVersion,
)
from chalk._gen.chalk.server.v1.graph_pb2_grpc import GraphServiceStub
from chalk._gen.chalk.server.v1.integrations_pb2_grpc import IntegrationsServiceStub
from chalk._gen.chalk.server.v1.log_pb2_grpc import LogSearchServiceStub
from chalk._gen.chalk.server.v1.model_registry_pb2 import (
    CreateModelArtifactRequest,
    CreateModelArtifactResponse,
    CreateModelRequest,
    CreateModelResponse,
    CreateModelVersionFromArtifactRequest,
    CreateModelVersionFromArtifactResponse,
    CreateModelVersionRequest,
    CreateModelVersionResponse,
    DeleteModelRequest,
    DeleteModelResponse,
    DeleteModelVersionRequest,
    DeleteModelVersionResponse,
    DownloadModelArtifactRequest,
    DownloadModelArtifactResponse,
    GetModelArtifactUploadUrlsRequest,
    GetModelArtifactUploadUrlsResponse,
    GetModelRequest,
    GetModelResponse,
    GetModelVersionRequest,
    GetModelVersionResponse,
    ModelVersionKey,
)
from chalk._gen.chalk.server.v1.model_registry_pb2_grpc import ModelRegistryServiceStub
from chalk._gen.chalk.server.v1.named_query_pb2 import GetNamedQueryByNameRequest
from chalk._gen.chalk.server.v1.named_query_pb2_grpc import NamedQueryServiceStub
from chalk._gen.chalk.server.v1.offline_queries_pb2 import (
    CancelAsyncOfflineQueryRequest,
    GetBatchReportRequest,
    GetOfflineQueryProfileSummaryRequest,
    GetOfflineQueryRequest,
)
from chalk._gen.chalk.server.v1.offline_queries_pb2_grpc import OfflineQueryMetadataServiceStub
from chalk._gen.chalk.server.v1.offline_wide_tables_pb2_grpc import OfflineWideTablesServiceStub
from chalk._gen.chalk.server.v1.queries_pb2 import GetMetaQueryRequest, GetQueryRunRequest
from chalk._gen.chalk.server.v1.queries_pb2_grpc import QueriesServiceStub
from chalk._gen.chalk.server.v1.scheduled_query_pb2_grpc import ScheduledQueryServiceStub
from chalk._gen.chalk.server.v1.scheduled_query_run_pb2 import GetScheduledQueryRunsRequest
from chalk._gen.chalk.server.v1.scheduler_pb2 import ManualTriggerScheduledQueryRequest
from chalk._gen.chalk.server.v1.scheduler_pb2_grpc import SchedulerServiceStub
from chalk._gen.chalk.server.v1.script_tasks_pb2 import CreateScriptTaskRequest, CreateScriptTaskResponse
from chalk._gen.chalk.server.v1.script_tasks_pb2_grpc import ScriptTaskServiceStub
from chalk._gen.chalk.server.v1.team_pb2 import (
    CreateServiceTokenRequest,
    CreateServiceTokenResponse,
    ListServiceTokensRequest,
    ListServiceTokensResponse,
)
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk._gen.chalk.streaming.v1.simple_streaming_service_pb2_grpc import SimpleStreamingServiceStub
from chalk._reporting.rich.color import CHALK_WEBSITE_GREEN
from chalk.client import ChalkAuthException, ChalkError, FeatureReference
from chalk.client.client_headers import (
    CHALK_BRANCH_ID_HEADER,
    CHALK_DEPLOYMENT_TAG_HEADER_LOWERCASE,
    CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE,
    CHALK_ENV_ID_HEADER_LOWERCASE,
    CHALK_GRPC_TRACE_ID_HEADER,
)
from chalk.client.client_impl import _validate_context_dict  # pyright: ignore[reportPrivateUsage]
from chalk.client.exc import ChalkCustomException
from chalk.client.model_image import (
    build_image_from_spec_bytes,
    build_image_from_spec_with_files,
    build_inferred_image,
    chalk_handler_volume_name,
    generate_volume_name,
    image_local_files,
    image_spec_bakes_handler_shim,
    model_artifact_volume_name,
    serialize_image_spec,
    stage_chalk_model_handler_image,
    upload_chalk_handler_artifacts,
)
from chalk.client.models import (
    AggregateBackfillResponse,
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    CreateBranchResponse,
    DeployedModelVersion,
    DownloadModelArtifactResult,
    JobQueueItem,
)
from chalk.client.models import ListDatasetsResponse as ListDatasetsResponseDataclass
from chalk.client.models import ManualTriggerScheduledQueryResponse as ManualTriggerScheduledQueryResponseDataclass
from chalk.client.models import (
    ModelArtifactSpec,
    ModelNamespaceResponse,
    ModelUploadUrlResponse,
    ModelVersionResponse,
    NamedQueryMetadata,
    OfflineQueryInfo,
    OfflineQueryProfileSummary,
    OfflineQueryReport,
    OfflineStoreTable,
    OnlineQuery,
    OnlineQueryResponse,
    RedeployResponse,
    RegisteredModelVersion,
    RegisterModelArtifactResponse,
    RegisterModelResponse,
    RegisterModelVersionResponse,
    ResourceRequests,
    ScheduledQueryRun,
    StreamResolverTestResponse,
    StreamResolverTestStatus,
    UploadFeaturesResponse,
    WorkflowExecutionInfo,
    resolve_multi_query_query_name,
)
from chalk.client.serialization.model_serialization import ModelSerializer
from chalk.client.serialization.protos import (
    AggregateBackfillConverter,
    ChalkErrorConverter,
    OnlineQueryConverter,
    UploadFeaturesBulkConverter,
)
from chalk.config.auth_config import TokenConfig, load_token
from chalk.features import live_updates
from chalk.features._encoding.inputs import (
    GRPC_ENCODE_OPTIONS,
    InputEncodeOptions,
    InputSchemaHint,
    recursive_encode_bulk_inputs,
)
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.resolver import Resolver
from chalk.features.tag import DeploymentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.ml import LocalSourceConfig, ModelEncoding, ModelRunCriterion, ModelType, SourceConfig
from chalk.ml.model_file_transfer import ModelFileUploader
from chalk.ml.model_handler import CHALK_HANDLER_ARTIFACT_PATH, is_model_handler
from chalk.ml.utils import ModelClass, model_class_from_proto, model_encoding_from_proto, model_type_from_proto
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.scalinggroup.spec import (
    DeleteScalingGroupResponse,
    GrpcReadinessProbe,
    GrpcStartupProbe,
    ListScalingGroupsResponse,
    ScalingGroup,
    proto_to_scaling_group,
)
from chalk.utils import df_utils
from chalk.utils.cached_member_fn import cached_member_fn
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor
from chalk.utils.tracing import (
    TraceContext,
    current_or_new_trace_context,
    current_trace_context,
    inject_trace_context,
    safe_trace,
)

if TYPE_CHECKING:
    from pyarrow import RecordBatch, Table
    from pydantic import BaseModel

    from chalk._gen.chalk.aggregate.v1.service_pb2 import (
        CreateAggregateBackfillJobResponse,
        CreateAggregateBackfillV2Request,
        CreateAggregateBackfillV2Response,
    )
    from chalk._gen.chalk.aggregate.v1.service_pb2_grpc import AggregateServiceStub
    from chalk._gen.chalk.dataframe.v1.dataframe_pb2 import DataFramePlan
    from chalk._gen.chalk.server.v1.builder_pb2 import StartBranchResponse
    from chalk._gen.chalk.server.v1.builder_pb2_grpc import BuilderServiceStub
    from chalk._gen.chalk.server.v1.dataframe_pb2 import GetDataFrameRunResponse
    from chalk.client import ChalkError
    from chalk.client.response import OnlineQueryResult


_JOB_STATE_MAP = {
    "scheduled": ProtoJobQueueState.JOB_QUEUE_STATE_SCHEDULED,
    "running": ProtoJobQueueState.JOB_QUEUE_STATE_RUNNING,
    "completed": ProtoJobQueueState.JOB_QUEUE_STATE_COMPLETED,
    "failed": ProtoJobQueueState.JOB_QUEUE_STATE_FAILED,
    "canceled": ProtoJobQueueState.JOB_QUEUE_STATE_CANCELED,
    "not_ready": ProtoJobQueueState.JOB_QUEUE_STATE_NOT_READY,
    "waiting": ProtoJobQueueState.JOB_QUEUE_STATE_WAITING,
}

_JOB_KIND_MAP = {
    "async_offline_query": ProtoJobQueueKind.JOB_QUEUE_KIND_ASYNC_OFFLINE_QUERY,
    "scheduled_query": ProtoJobQueueKind.JOB_QUEUE_KIND_SCHEDULED_QUERY,
    "script_task": ProtoJobQueueKind.JOB_QUEUE_KIND_SCRIPT_TASK,
    "chalksql_run": ProtoJobQueueKind.JOB_QUEUE_KIND_CHALKSQL_RUN,
    "dataframe_run": ProtoJobQueueKind.JOB_QUEUE_KIND_DATAFRAME_RUN,
}

_BUILD_PROFILE_MAP = {
    "o3_no_profiling": DeploymentBuildProfile.DEPLOYMENT_BUILD_PROFILE_O3_NO_PROFILING,
    "o3_profiling": DeploymentBuildProfile.DEPLOYMENT_BUILD_PROFILE_O3_PROFILING,
    "o2_no_profiling": DeploymentBuildProfile.DEPLOYMENT_BUILD_PROFILE_O2_NO_PROFILING,
    "o2_profiling": DeploymentBuildProfile.DEPLOYMENT_BUILD_PROFILE_O2_PROFILING,
}


@dataclasses.dataclass
class ParsedUri:
    uri_without_scheme: str
    use_tls: bool


@dataclasses.dataclass(frozen=True)
class _CachedQueueClient:
    """A function-queue client alongside the metadata baked into it at construction."""

    metadata: List[Tuple[str, str]]
    client: Any
    """``chalkcompute.RemoteCallClient``; untyped here since chalkcompute is an optional dependency."""

    def is_stale(self, current_metadata: Sequence[Tuple[str, str]]) -> bool:
        """True once the baked-in metadata no longer matches what a fresh call would send."""
        return self.metadata != list(current_metadata)


def get_trace_id_from_response(call: grpc.Call) -> Optional[str]:
    for k, v in call.trailing_metadata() or []:
        if k == CHALK_GRPC_TRACE_ID_HEADER:
            if isinstance(v, bytes):
                v = v.decode("utf-8")
            assert isinstance(v, str)  # for pyright
            return v
    return None


def _merge_headers(
    headers: None | Sequence[tuple[str, str | bytes]] | Mapping[str, str | bytes],
    extra_headers: None | Sequence[tuple[str, str | bytes]] | Mapping[str, str | bytes],
) -> tuple[tuple[str, str | bytes], ...]:
    headers = _canonicalize_headers(headers)
    extra_headers = _canonicalize_headers(extra_headers)
    all_headers: list[tuple[str, str | bytes]] = []
    for h in headers:
        all_headers.append(h)
    for h in extra_headers:
        all_headers.append(h)
    return tuple(all_headers)


def _canonicalize_headers(
    headers: None | Sequence[tuple[str, str | bytes]] | Mapping[str, str | bytes],
) -> tuple[tuple[str, str | bytes], ...]:
    if headers is None:
        return ()
    # NOTE: metadata _keys_ must be lowercase
    if isinstance(headers, collections.abc.Mapping):
        return tuple((k.lower(), v) for (k, v) in headers.items())
    return tuple((k.lower(), v) for (k, v) in headers)


def _inject_trace_context_metadata(
    headers: None | Sequence[tuple[str, str | bytes]] | Mapping[str, str | bytes],
    trace_context: TraceContext | None = None,
) -> tuple[tuple[str, str | bytes], ...]:
    canonical_headers = dict(_canonicalize_headers(headers))
    if trace_context is None:
        return tuple(inject_trace_context(canonical_headers).items())
    return tuple(inject_trace_context(canonical_headers, trace_context).items())


def get_features_feather_bytes(
    inputs: "Mapping[FeatureReference, Sequence[Any]] | DataFrame | Table | RecordBatch",
    options: InputEncodeOptions,
    compression: Literal["lz4", "zstd", "uncompressed"] = "lz4",
    input_schema_hint: Optional[InputSchemaHint] = None,
) -> bytes:
    import pyarrow as pa

    if isinstance(inputs, Mapping):
        inputs, _ = recursive_encode_bulk_inputs(inputs, options=options, input_schema_hint=input_schema_hint)
    elif input_schema_hint is not None:
        raise ValueError(
            "input_schema_hint is only supported when inputs are provided as a mapping; "
            + "tabular inputs (DataFrame/Table/RecordBatch) already carry an explicit schema"
        )

    if isinstance(inputs, DataFrame):
        inputs_table: pa.Table = inputs.to_pyarrow()
        input_batch = df_utils.pa_table_to_recordbatch(inputs_table)
    elif isinstance(inputs, pa.Table):
        input_batch = df_utils.pa_table_to_recordbatch(inputs)
    elif isinstance(inputs, pa.RecordBatch):
        input_batch = inputs
    else:
        encoded_inputs = {str(k): v for k, v in inputs.items()}
        input_batch = pa.RecordBatch.from_pydict(encoded_inputs)
    inputs_bytes = record_batch_to_arrow_ipc(input_batch, compression=compression)
    return inputs_bytes


def _parse_uri_for_engine(query_server_uri: str) -> ParsedUri:
    """
    If the scheme is provided, base TLS off of that (http = no tls, https = tls)
    If there is no scheme, default to TLS EXCEPT for localhost/private-vpc uris.
    """
    url_parsed = urlparse(query_server_uri)
    if url_parsed.scheme == "http":
        use_tls = False
    elif url_parsed.scheme == "https":
        use_tls = True
    elif url_parsed.scheme == "" and any(query_server_uri.startswith(pfx) for pfx in ["localhost", "127.0.0.1", "10."]):
        use_tls = False
    else:
        use_tls = True
    uri_without_scheme = query_server_uri.removeprefix(url_parsed.scheme + "://")
    return ParsedUri(uri_without_scheme=uri_without_scheme, use_tls=use_tls)


_DEFAULT_CHANNEL_OPTIONS: Dict[str, str | int] = {
    "grpc.max_send_message_length": 1024 * 1024 * 100,  # 100MB
    "grpc.max_receive_message_length": 1024 * 1024 * 100,  # 100MB
    # https://grpc.io/docs/guides/performance/#python
    grpc.experimental.ChannelOptions.SingleThreadedUnaryStream: 1,
    "grpc.keepalive_time_ms": 60_000,
    "grpc.keepalive_timeout_ms": 5_000,
    "grpc.keepalive_permit_without_calls": 1,
    "grpc.http2.max_pings_without_data": 0,
    "grpc.service_config": json.dumps(
        {
            "methodConfig": [
                {
                    "name": [{}],
                    "retryPolicy": {
                        "maxAttempts": 5,
                        "initialBackoff": "0.1s",
                        "maxBackoff": "1s",
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": ["UNAVAILABLE"],
                    },
                }
            ]
        }
    ),
}


T = TypeVar("T")
U = TypeVar("U")


class _EngineTarget(enum.Enum):
    GRPC_ENGINE = enum.auto()
    API_SERVER = enum.auto()


class StubProvider:
    @property
    def server_channel(self) -> Optional[grpc.Channel]:
        """Return the server channel."""
        return self._server_channel

    def close(self):
        if self._server_channel is not None:
            self._server_channel.close()
        if self._engine_channel is not None:
            self._engine_channel.close()

    def _get_engine_channel_for_target(self, target: _EngineTarget) -> grpc.Channel:
        if target == _EngineTarget.GRPC_ENGINE:
            channel = self._engine_channel
            if channel is None:
                raise ValueError(
                    "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
                )
            return channel
        elif target == _EngineTarget.API_SERVER:
            channel = self._server_channel
            if channel is None:
                raise ValueError(
                    "The GRPC API-Server service is not available. Are you running against a local client?"
                )
            return channel
        else:
            raise ValueError(f"Unsupported target: {target}")

    @cached_property
    def deploy_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return DeployServiceStub(self._server_channel)

    @cached_property
    def graph_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return GraphServiceStub(self._server_channel)

    @cached_property
    def team_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return TeamServiceStub(self._server_channel)

    @cached_member_fn
    def query_stub(self, engine_target: _EngineTarget) -> QueryServiceStub:
        channel = self._get_engine_channel_for_target(engine_target)
        return QueryServiceStub(channel)

    @cached_property
    def offline_query_stub(self) -> OfflineQueryMetadataServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return OfflineQueryMetadataServiceStub(self._server_channel)

    @cached_property
    def offline_store_stub(self) -> OfflineStoreServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return OfflineStoreServiceStub(self._server_channel)

    @cached_property
    def offline_wide_tables_stub(self) -> OfflineWideTablesServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return OfflineWideTablesServiceStub(self._server_channel)

    @cached_property
    def queries_stub(self) -> QueriesServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return QueriesServiceStub(self._server_channel)

    @cached_property
    def scheduled_query_stub(self) -> SchedulerServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return SchedulerServiceStub(self._server_channel)

    @cached_property
    def scheduled_query_run_stub(self) -> ScheduledQueryServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return ScheduledQueryServiceStub(self._server_channel)

    @cached_property
    def dataplane_workflows_stub(self) -> DataPlaneWorkflowsServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return DataPlaneWorkflowsServiceStub(self._server_channel)

    @cached_property
    def dataset_metadata_stub(self) -> DatasetMetadataServiceStub:
        if self._server_channel is None:
            raise ValueError("The GRPC API-Server service is not available. Are you running against a local client?")
        return DatasetMetadataServiceStub(self._server_channel)

    @cached_property
    def named_query_stub(self) -> NamedQueryServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return NamedQueryServiceStub(self._server_channel)

    @cached_member_fn
    def sql_stub(self, engine_target: _EngineTarget) -> SqlServiceStub:
        channel = self._get_engine_channel_for_target(engine_target)
        return SqlServiceStub(channel)

    @cached_member_fn
    def dataframe_stub(self, engine_target: _EngineTarget) -> DataFrameServiceStub:
        channel = self._get_engine_channel_for_target(engine_target)
        return DataFrameServiceStub(channel)

    @cached_member_fn
    def streaming_stub(self, engine_target: _EngineTarget) -> SimpleStreamingServiceStub:
        channel = self._get_engine_channel_for_target(engine_target)
        return SimpleStreamingServiceStub(channel)

    @cached_property
    def model_stub(self) -> ModelRegistryServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ModelRegistryServiceStub(self._server_channel)

    @cached_property
    def task_stub(self) -> ScriptTaskServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ScriptTaskServiceStub(self._server_channel)

    @cached_property
    def builder_stub(self) -> "BuilderServiceStub":
        from chalk._gen.chalk.server.v1.builder_pb2_grpc import BuilderServiceStub

        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return BuilderServiceStub(self._server_channel)

    @cached_property
    def log_stub(self) -> LogSearchServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return LogSearchServiceStub(self._server_channel)

    @cached_property
    def job_queue_stub(self) -> DataPlaneJobQueueServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return DataPlaneJobQueueServiceStub(self._server_channel)

    @cached_property
    def integrations_stub(self) -> IntegrationsServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return IntegrationsServiceStub(self._server_channel)

    @cached_property
    def aggregate_stub(self) -> "AggregateServiceStub":
        from chalk._gen.chalk.aggregate.v1.service_pb2_grpc import AggregateServiceStub

        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return AggregateServiceStub(self._server_channel)

    @cached_property
    def api_dataframe_stub(self) -> ApiDataFrameServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ApiDataFrameServiceStub(self._server_channel)

    @cached_property
    def model_deployment_stub(self) -> "ModelDeploymentServiceStub":
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ModelDeploymentServiceStub(self._server_channel)

    @cached_property
    def scaling_group_stub(self) -> "ScalingGroupManagerServiceStub":
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ScalingGroupManagerServiceStub(self._server_channel)

    def __init__(
        self,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
        channel_options: List[tuple[str, str | int]] | None = None,
    ):
        super().__init__()
        additional_headers_nonempty: List[tuple[str, str]] = [] if additional_headers is None else additional_headers
        token_refresher: TokenRefresher | None = None
        channel_options_merged: Dict[str, str | int] = _DEFAULT_CHANNEL_OPTIONS.copy()
        if channel_options:
            channel_options_merged.update(dict(channel_options))
        if skip_api_server:
            # Omits the auth handshake with the API server. Primarily for internal use/testing -- if used in production,
            # this client will simply fail to connect. If `True` then query_server must be provided & point to
            # `localhost/127.0.0.1`.
            if query_server is None:
                raise ValueError("If skipping API server auth, query_server URI must be provided.")
            parsed_uri = _parse_uri_for_engine(query_server)
            if not (
                parsed_uri.uri_without_scheme.startswith("localhost")
                or parsed_uri.uri_without_scheme.startswith("127.0.0.1")
            ):
                warnings.warn(
                    "Skipping API server auth should only be enabled if query_server URI is localhost. It will fail to authenticate against a production engine."
                )
            self.environment_id = token_config.activeEnvironment
            if self.environment_id is None or self.environment_id == "":
                raise ValueError("No environment specified")
            self._server_channel: Optional[grpc.Channel] = None
        else:
            server_host: str = token_config.apiServer or "api.chalk.ai"
            for pfx in ("https://", "http://", "www."):
                server_host = server_host.removeprefix(pfx)

            _unauthenticated_server_channel: grpc.Channel = (
                grpc.insecure_channel(
                    target=server_host,
                    options=list(channel_options_merged.items()),
                )
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=list(channel_options_merged.items()),
                )
            )

            self._auth_stub: AuthServiceStub = AuthServiceStub(
                grpc.intercept_channel(
                    _unauthenticated_server_channel,
                    UnauthenticatedChalkClientInterceptor(
                        server="go-api",
                        additional_headers=additional_headers_nonempty,
                    ),
                )
            )

            token_refresher = TokenRefresher(
                auth_stub=self._auth_stub,
                client_id=token_config.clientId,
                client_secret=token_config.clientSecret,
            )

            t = token_refresher.get_token()

            self.environment_id = token_config.activeEnvironment or t.primary_environment
            if not self.environment_id:
                raise ValueError("No environment specified")

            if self.environment_id not in t.environment_id_to_name:
                lower_env_id = self.environment_id.lower()
                valid = [eid for eid, ename in t.environment_id_to_name.items() if ename.lower() == lower_env_id]
                if len(valid) > 1:
                    raise ValueError(f"Multiple environments with name {self.environment_id}: {valid}")
                elif len(valid) == 0:
                    raise ValueError(f"No environment with name {self.environment_id}: {t.environment_id_to_name}")
                else:
                    self.environment_id = valid[0]

            self._server_channel: Optional[grpc.Channel] = grpc.intercept_channel(
                _unauthenticated_server_channel,
                AuthenticatedChalkClientInterceptor(
                    refresher=token_refresher,
                    server="go-api",
                    environment_id=self.environment_id,
                    additional_headers=additional_headers_nonempty,
                ),
            )

            query_server = query_server or t.grpc_engines.get(self.environment_id, None)
        engine_headers = additional_headers_nonempty + [(CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE, "engine-grpc")]
        if deployment_tag is not None:
            engine_headers += [(CHALK_DEPLOYMENT_TAG_HEADER_LOWERCASE, deployment_tag)]
        interceptors: List[grpc.UnaryUnaryClientInterceptor] = [
            (
                AuthenticatedChalkClientInterceptor(
                    refresher=token_refresher,
                    environment_id=self.environment_id,
                    server="engine",
                    additional_headers=engine_headers,
                )
                if token_refresher is not None
                else UnauthenticatedChalkClientInterceptor(
                    server="engine",
                    additional_headers=engine_headers + [(CHALK_ENV_ID_HEADER_LOWERCASE, self.environment_id)],
                )
            )
        ]

        self._engine_channel: Optional[grpc.Channel] = None
        # Retained so direct/queue calls can dial the engine ingress without re-parsing.
        self._engine_grpc_target: Optional[tuple[str, bool]] = None
        if query_server is not None:
            parsed_uri = _parse_uri_for_engine(query_server_uri=query_server)
            self._engine_grpc_target = (parsed_uri.uri_without_scheme, parsed_uri.use_tls)
            self._engine_channel = grpc.intercept_channel(
                (
                    grpc.secure_channel(
                        target=parsed_uri.uri_without_scheme,
                        credentials=grpc.ssl_channel_credentials(),
                        options=list(channel_options_merged.items()),
                    )
                    if parsed_uri.use_tls
                    else grpc.insecure_channel(
                        target=parsed_uri.uri_without_scheme,
                        options=list(channel_options_merged.items()),
                    )
                ),
                *interceptors,
            )

        # Retained to mint Bearer tokens for direct (non-proxied) calls; None when skipping auth.
        self._token_refresher: TokenRefresher | None = token_refresher

    def get_remote_call_metadata(self) -> List[tuple[str, str]]:
        """Bearer token + env id for a direct scaling-group call."""
        metadata: List[tuple[str, str]] = []
        if self._token_refresher is not None:
            metadata.append(("authorization", f"Bearer {self._token_refresher.get_token().access_token}"))
        if self.environment_id:
            metadata.append((CHALK_ENV_ID_HEADER_LOWERCASE, self.environment_id))
        return metadata

    def get_queue_call_metadata(self) -> List[tuple[str, str]]:
        """Direct-call metadata plus the header that routes to the function-queue server."""
        return [*self.get_remote_call_metadata(), (CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE, "function-queue")]

    def get_engine_grpc_target(self) -> tuple[str, bool]:
        """``(target, use_tls)`` of the environment's grpc-engine ingress."""
        if self._engine_grpc_target is None:
            raise ValueError("No query server is configured for this environment")
        return self._engine_grpc_target


class StubRefresher:
    def __init__(
        self,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
        channel_options: List[tuple[str, str | int]] | None = None,
    ):
        super().__init__()
        self._token_config = token_config
        self._query_server = query_server
        self._deployment_tag = deployment_tag
        self._skip_api_server = skip_api_server
        self._additional_headers = additional_headers
        self._channel_options = channel_options
        self._stub = self._refresh_stub()

    def _refresh_stub(self) -> StubProvider:
        self._stub = StubProvider(
            token_config=self._token_config,
            query_server=self._query_server,
            deployment_tag=self._deployment_tag,
            skip_api_server=self._skip_api_server,
            additional_headers=self._additional_headers,
            channel_options=self._channel_options,
        )
        return self._stub

    def close(self):
        self._stub.close()

    def _retry_callable(self, fn: Callable[[T], U], get_service: Callable[[], T]) -> U:
        try:
            return fn(get_service())
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                details = (e.details() or "").lower()
                # capitalization seems to vary - original capitalization: "FD Shutdown" and "GOAWAY"
                if "fd shutdown" in details or "goaway" in details:
                    chalk_logger.info("Detected FD shutdown; retrying connection: %s", details)
                    old_stub = self._stub
                    self._refresh_stub()
                    old_stub.close()
                    return fn(get_service())
            raise

    def call_deploy_stub(self, fn: Callable[[DeployServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.deploy_stub)

    def call_graph_stub(self, fn: Callable[[GraphServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.graph_stub)

    def call_team_stub(self, fn: Callable[[TeamServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.team_stub)

    def call_query_stub(self, fn: Callable[[QueryServiceStub], T], target: _EngineTarget) -> T:
        return self._retry_callable(fn, lambda: self._stub.query_stub(target))

    def call_offline_query_stub(self, fn: Callable[[OfflineQueryMetadataServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.offline_query_stub)

    def call_offline_store_stub(self, fn: Callable[[OfflineStoreServiceStub], T]):
        return self._retry_callable(fn, lambda: self._stub.offline_store_stub)

    def call_offline_wide_tables_stub(self, fn: Callable[[OfflineWideTablesServiceStub], T]):
        return self._retry_callable(fn, lambda: self._stub.offline_wide_tables_stub)

    def call_queries_stub(self, fn: Callable[[QueriesServiceStub], T]):
        return self._retry_callable(fn, lambda: self._stub.queries_stub)

    def call_scheduled_query_stub(self, fn: Callable[[SchedulerServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.scheduled_query_stub)

    def call_scheduled_query_run_stub(self, fn: Callable[[ScheduledQueryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.scheduled_query_run_stub)

    def call_dataplane_workflows_stub(self, fn: Callable[[DataPlaneWorkflowsServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.dataplane_workflows_stub)

    def call_dataset_metadata_stub(self, fn: Callable[[DatasetMetadataServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.dataset_metadata_stub)

    def call_get_named_query_metadata(self, fn: Callable[[NamedQueryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.named_query_stub)

    def call_sql_stub(self, fn: Callable[[SqlServiceStub], T], target: _EngineTarget) -> T:
        return self._retry_callable(fn, lambda: self._stub.sql_stub(target))

    def call_dataframe_stub(self, fn: Callable[[DataFrameServiceStub], T], target: _EngineTarget) -> T:
        return self._retry_callable(fn, lambda: self._stub.dataframe_stub(target))

    def call_api_dataframe_stub(self, fn: Callable[[ApiDataFrameServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.api_dataframe_stub)

    def call_model_stub(self, fn: Callable[[ModelRegistryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.model_stub)

    def call_task_stub(self, fn: Callable[[ScriptTaskServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.task_stub)

    def call_model_deployment_stub(self, fn: Callable[["ModelDeploymentServiceStub"], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.model_deployment_stub)

    def call_scaling_group_stub(self, fn: Callable[["ScalingGroupManagerServiceStub"], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.scaling_group_stub)

    def call_builder_stub(self, fn: Callable[["BuilderServiceStub"], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.builder_stub)

    def call_log_stub(self, fn: Callable[[LogSearchServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.log_stub)

    def call_job_queue_stub(self, fn: Callable[[DataPlaneJobQueueServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.job_queue_stub)

    def call_streaming_stub(self, fn: Callable[[SimpleStreamingServiceStub], T], target: _EngineTarget) -> T:
        return self._retry_callable(fn, lambda: self._stub.streaming_stub(target))

    def get_server_channel(self) -> Optional[grpc.Channel]:
        """Get the server gRPC channel."""
        return self._stub.server_channel

    def call_integrations_stub(self, fn: Callable[[IntegrationsServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.integrations_stub)

    def call_aggregate_stub(self, fn: Callable[[AggregateServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.aggregate_stub)

    @property
    def log_stub(self) -> LogSearchServiceStub:
        return self._stub.log_stub

    @property
    def environment_id(self) -> str | None:
        return self._stub.environment_id

    def get_remote_call_metadata(self) -> List[tuple[str, str]]:
        return self._stub.get_remote_call_metadata()

    def get_queue_call_metadata(self) -> List[tuple[str, str]]:
        return self._stub.get_queue_call_metadata()

    def get_engine_grpc_target(self) -> tuple[str, bool]:
        return self._stub.get_engine_grpc_target()


def _model_artifact_spec_from_proto(artifact: Any) -> ModelArtifactSpec:
    spec = artifact.spec
    return ModelArtifactSpec(
        # type/encoding are unset (0) for image-only models, which have no serialized artifact.
        model_type=model_type_from_proto(spec.model_type) if spec.model_type else None,
        model_class=model_class_from_proto(spec.model_class),
        model_encoding=model_encoding_from_proto(spec.model_encoding) if spec.model_encoding else None,
        model_files=[f.name for f in spec.model_files],
        additional_files=[f.name for f in spec.additional_files],
        input_schema=ModelSerializer.convert_schema_from_protobuf(spec.model_signature.inputs),
        output_schema=ModelSerializer.convert_schema_from_protobuf(spec.model_signature.outputs),
        metadata=ModelSerializer.convert_metadata_from_protobuf(artifact.metadata),
        input_features=list(spec.input_features),
        output_features=list(spec.output_features),
        dependencies=list(spec.python_dependencies),
    )


class ChalkGRPCClient:
    """The `ChalkGRPCClient` is the primary Python interface for interacting with Chalk gRPC servers.

    You can use it to run online and offline queries targeted at the gRPC server, get data about the graph of
    features and resolvers deployed, and more."""

    def __init__(
        self,
        environment: EnvironmentId | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        api_server: str | None = None,
        deployment_tag: str | None = None,
        additional_headers: List[tuple[str, str]] | None = None,
        query_server: str | None = None,
        input_compression: typing.Literal["lz4", "zstd", "uncompressed"] = "lz4",
        channel_options: List[Tuple[str, str | int]] | None = None,
        branch: str | None = None,
        **kwargs: Any,
    ):
        """Create a `ChalkGRPCClient` with the given credentials.

        Parameters
        ----------
        environment
            ID of the Chalk environment to connect to. If omitted, this is pulled from the current Chalk project config.
        client_id
            Client ID used to authenticate. If omitted, this is pulled from the current Chalk project config.
        client_secret
            Client secret used to authenticate. If omitted, this is pulled from the current Chalk project config.
        api_server
            URI of the Chalk API server used for authentication/metadata.
        additional_headers
            Additional client metadata to send with GRPC requests.
        query_server
            Hardcoded URI for Chalk query server, if available.
        deployment_tag
            Tag of the deployment to query. If omitted, the active deployment is used.
        """
        super().__init__()
        self._input_compression: typing.Literal["lz4", "zstd", "uncompressed"] = input_compression
        environment_id = kwargs.get("environment_id", None)
        if environment is not None and environment_id is not None:
            raise ValueError("Both environment and environment_id specified; only pass environment.")

        if environment_id is not None:
            environment = EnvironmentId(environment_id)

        # deprecating this.
        del environment_id

        if CHALK_IMPORT_FLAG.get() is True:
            raise RuntimeError(
                "Attempting to instantiate a Chalk client while importing source modules is forbidden. "
                + "Please exclude this file from import using your `.chalkignore` file "
                + "(see https://docs.chalk.ai/cli/apply), or wrap this query in a function that is not called upon import."
            )
        token_config = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=False,
        )
        if token_config is None:
            raise ChalkAuthException()

        # using for instantiation of ChalkClient(). Can remove if we exclusively start using GRPC client
        self._client_id = token_config.clientId
        self._client_secret = token_config.clientSecret
        self._environment = token_config.activeEnvironment
        self._branch = branch
        self._api_server = token_config.apiServer

        self._stub_refresher = StubRefresher(
            token_config=token_config,
            query_server=query_server,
            deployment_tag=deployment_tag,
            additional_headers=additional_headers,
            skip_api_server=kwargs.get("_skip_api_server", False),
            channel_options=channel_options,
        )
        self._queue_client_cache: Optional[_CachedQueueClient] = None
        """Lazily built by _get_queue_client; rebuilt when its metadata goes stale."""

    _INPUT_ENCODE_OPTIONS = GRPC_ENCODE_OPTIONS

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if self._queue_client_cache is not None:
            self._queue_client_cache.client.close()
            self._queue_client_cache = None
        self._stub_refresher.close()

    def ping_engine(self, num: Optional[int] = None) -> int:
        """
        Ping the engine to check if it is alive.

        Parameters
        ----------
        num
            A random number to send to the engine. If not provided, a random number is generated.
            This number will be returned as the response.

        Returns
        -------
        int
            The number sent to the engine.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> client.ping_engine(3)
        3
        """
        return self._stub_refresher.call_query_stub(
            lambda x: x.Ping(query_server_pb2.PingRequest(num=num if num is not None else random.randint(0, 999))),
            _EngineTarget.GRPC_ENGINE,
        ).num

    def online_query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: List[str] | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        trace: bool = False,
        branch: str | None | types.EllipsisType = ...,
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> OnlineQueryResponse:
        """Compute features values using online resolvers.

        See https://docs.chalk.ai/docs/query-basics for more information.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
            For example, `{User.id: 1234}`. Features can also be expressed as snakecased strings,
            e.g. `{"user.id": 1234}`
        output
            Outputs are the features that you'd like to compute from the inputs.
            For example, `[User.age, User.name, User.email]`.

            If an empty sequence, the output will be set to all features on the namespace
            of the query. For example, if you pass as input `{"user.id": 1234}`, then the query
            is defined on the `User` namespace, and all features on the `User` namespace
            (excluding has-one and has-many relationships) will be used as outputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        tags
            The tags used to scope the resolvers.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        required_resolver_tags
            If specified, *all* required_resolver_tags must be present on a resolver for it to be
            considered eligible to execute.
            See https://docs.chalk.ai/docs/resolver-tags for more information.
        query_name
            The semantic name for the query you're making, for example, `"loan_application_model"`.
            Typically, each query that you make from your application should have a name.
            Chalk will present metrics and dashboard functionality grouped by 'query_name'.
        include_meta
            Returns metadata about the query execution under `OnlineQueryResult.meta`.
            This could make the query slightly slower.
            For more information, see https://docs.chalk.ai/docs/query-basics.
        explain
            Log the query execution plan. Requests using `explain=True` will be slower
            than requests using `explain=False`.

            If `True`, 'include_meta' will be set to `True` as well.
        store_plan_stages
            If `True`, the output of each of the query plan stages will be stored.
            This option dramatically impacts the performance of the query,
            so it should only be used for debugging.
        value_metrics_tag_by_features
            If your environment has feature value metrics enabled, this parameter specifies a list of features by which
            to tag these metrics. For example, if `value_metrics_tag_by_features=["user.category_id"]`, then the feature
             value metrics stored for this query will be tagged with the corresponding user's category_id.
        correlation_id
            You can specify a correlation ID to be used in logs and web interfaces.
            This should be globally unique, i.e. a `uuid` or similar. Logs generated
            during the execution of your query will be tagged with this correlation id.
        now
            The time at which to evaluate the query. If not specified, the current time will be used.
            This parameter is complex in the context of online_query since the online store
            only stores the most recent value of an entity's features. If `now` is in the past,
            it is extremely likely that `None` will be returned for cache-only features.

            This parameter is primarily provided to support:
                - controlling the time window for aggregations over cached has-many relationships
                - controlling the time wnidow for aggregations over has-many relationships loaded from an
                  external database

            If you are trying to perform an exploratory analysis of past feature values, prefer `offline_query`.
        query_context
            An immutable context that can be accessed from Python resolvers.
            This context wraps a JSON-compatible dictionary or JSON string with type restrictions.
            See https://docs.chalk.ai/api-docs#ChalkContext for more information.

        branch
            Sends this query to a branch with the given name. If omitted, uses the client's current branch. If explicitly None,
            runs this query on the mainline deployment (i.e. no branch)
        input_schema_hint
            Specifies the intended wire schema of has-many inputs e.g.
            ```{User.transactions: [Transaction.id, Transaction.amount]}```
            If no hint is provided, the schema will be inferred from the provided row data, which
            is ambiguous when the row list is empty.
            This ambiguity can cause query plan cache misses, since the shape of input data may
            affect the inferred input schema, which may change which resolvers are needed to compute
            the requested output.

        Other Parameters
        ----------------
        meta
            Arbitrary `key:value` pairs to associate with a query.
        headers
            Additional headers to send with the request.
        planner_options
            Dictionary of additional options to pass to the Chalk query engine.
            Values may be provided as part of conversations with Chalk support
            to enable or disable specific functionality.
        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.

        Returns
        -------
        OnlineQueryResponse
            Wrapper around the output features and any query metadata
            and errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> result = ChalkGRPCClient().online_query(
        ...     input={
        ...         User.name: "Katherine Johnson"
        ...     },
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        branch = self._branch if branch is ... else branch
        bulk_response = self._online_query_grpc_request(
            input=input,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            request_timeout=request_timeout,
            headers=headers,
            query_context=_validate_context_dict(query_context),
            trace=trace,
            branch=branch,
            input_schema_hint=input_schema_hint,
        )
        return OnlineQueryConverter.online_query_bulk_response_decode_to_single(bulk_response)

    def query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: List[str] | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        trace: bool = False,
        branch: str | None | types.EllipsisType = ...,
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> OnlineQueryResponse:
        """A synonym for :meth:`online_query`.

        See :meth:`online_query` for the full documentation.
        """
        return self.online_query(
            input=input,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            request_timeout=request_timeout,
            headers=headers,
            query_context=query_context,
            trace=trace,
            branch=branch,
            input_schema_hint=input_schema_hint,
        )

    @classmethod
    def _engine_target(cls, branch: str | None) -> _EngineTarget:
        return _EngineTarget.GRPC_ENGINE if branch is None else _EngineTarget.API_SERVER

    def _online_query_grpc_request(
        self,
        *,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: List[str] | None = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | None = None,
        trace: bool = False,
        branch: str | None = None,
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> online_query_pb2.OnlineQueryBulkResponse:
        trace_context = current_or_new_trace_context() if trace else current_trace_context()
        with safe_trace("_online_query_grpc_request"):
            request = self._make_query_bulk_request(
                input={k: [v] for k, v in input.items()},
                input_schema_hint=input_schema_hint,
                output=output,
                now=[now] if now is not None else [],
                staleness=staleness or {},
                tags=tags or (),
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                include_meta=include_meta,
                meta=meta or {},
                explain=explain,
                store_plan_stages=store_plan_stages,
                value_metrics_tag_by_features=value_metrics_tag_by_features,
                encoding_options=encoding_options,
                required_resolver_tags=required_resolver_tags or (),
                planner_options=planner_options or {},
                query_context=query_context,
            )
            if trace_context is not None:
                headers = _inject_trace_context_metadata(headers, trace_context)

            if branch:
                headers = _merge_headers(headers, {CHALK_BRANCH_ID_HEADER: branch})
            metadata = _canonicalize_headers(headers)
            return self._stub_refresher.call_query_stub(
                lambda x: x.OnlineQueryBulk(
                    request,
                    timeout=request_timeout,
                    metadata=metadata,
                ),
                self._engine_target(branch),
            )

    def online_query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, None] = None,
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str | bytes] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        branch: str | None | types.EllipsisType = ...,
        *,
        input_sql: str | None = None,
        input_schema_hint: Optional[InputSchemaHint] = None,
        trace: bool = False,
    ) -> BulkOnlineQueryResult:
        if input is None and input_sql is None:
            raise TypeError("One of `input` or `input_sql` is required")
        if input is not None and input_sql is not None:
            raise TypeError("`input` and `input_sql` are mutually exclusive")
        if input_sql is not None and now is not None:
            raise TypeError(
                "When using `input_sql`, `now` is not allowed: instead, to provide a query time, you can have the SQL query output a column named `__ts__`"
            )
        branch = self._branch if branch is ... else branch

        response, call = self._online_query_bulk_grpc_request(
            input=input,
            input_sql=input_sql,
            input_schema_hint=input_schema_hint,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
            request_timeout=request_timeout,
            headers=headers,
            query_context=_validate_context_dict(query_context),
            branch=branch,
            trace=trace,
        )
        return OnlineQueryConverter.online_query_bulk_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def _online_query_bulk_grpc_request(
        self,
        *,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, None] = None,
        input_sql: str | None = None,
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str | bytes] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | None = None,
        branch: Optional[str] = None,
        input_schema_hint: Optional[InputSchemaHint] = None,
        trace: bool = False,
    ) -> Tuple[online_query_pb2.OnlineQueryBulkResponse, grpc.Call]:
        """Returns the raw GRPC response and metadata"""

        request = self._make_query_bulk_request(
            input=input,
            input_sql=input_sql,
            input_schema_hint=input_schema_hint,
            output=output,
            now=now or (),
            staleness=staleness or {},
            tags=tags or (),
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta or {},
            explain=explain,
            store_plan_stages=store_plan_stages,
            value_metrics_tag_by_features=value_metrics_tag_by_features,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags or (),
            planner_options=planner_options or {},
            query_context=query_context,
        )
        trace_context = current_or_new_trace_context() if trace else current_trace_context()
        if trace_context is not None:
            headers = _inject_trace_context_metadata(headers, trace_context)
        headers = _merge_headers(headers, {CHALK_BRANCH_ID_HEADER: branch} if branch is not None else {})
        return self._stub_refresher.call_query_stub(
            lambda x: x.OnlineQueryBulk.with_call(
                request,
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            ),
            self._engine_target(branch),
        )

    def upload_features_bulk(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> BulkUploadFeaturesResult:
        request = UploadFeaturesBulkRequest(
            inputs_feather=get_features_feather_bytes(inputs, self._INPUT_ENCODE_OPTIONS),
        )
        response, call = self._stub_refresher.call_query_stub(
            lambda x: x.UploadFeaturesBulk.with_call(
                request,
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            ),
            _EngineTarget.GRPC_ENGINE,
        )
        return UploadFeaturesBulkConverter.upload_features_bulk_response_decode(
            response,
            trace_id=get_trace_id_from_response(call),
        )

    def upload_features(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        update_mataggs: bool = False,
        write_offline: bool = False,
        write_online: Optional[bool] = None,
        branch: None | str | types.EllipsisType = ...,
    ) -> UploadFeaturesResponse:
        """Upload data to Chalk to be inserted into the online & offline stores.

        Parameters
        ----------
        inputs
            Input data can be in one of two formats:
            1. A mapping from a feature or feature name to a list of values:
               `{Transaction.id: ["a", "b", "c"], Transaction.amount: [100.0,200.0,300.0]}`
            2. A tabular format such as arrow Table/RecordBatch, polars Dataframe, chalk.DataFrame
               where each column corresponds to a feature.
        headers
            Additional headers to send with the request.
        request_timeout
            Float value indicating number of seconds that the request should wait before timing out
            at the network level. May not cancel resources on the server processing the query.
        update_mataggs
            Whether to update materialized aggregations (streaming aggs). Defaults to False.
        write_offline
            Whether to write features to the offline store. Defaults to False.
        write_online
            Whether to write features to the online store. Defaults to True when not set.
        branch
            The branch to upload features to. Defaults to the mainline deployment.

        Returns
        -------
        UploadFeaturesResponse
            which contains a list of errors if any occurred.
        """
        options = upload_features_pb2.UploadFeaturesOptions()
        if update_mataggs:
            options.update_mataggs = update_mataggs
        if write_offline:
            options.write_offline = write_offline
        if write_online is not None:
            options.write_online = write_online
        request = upload_features_pb2.UploadFeaturesRequest(
            inputs_table=get_features_feather_bytes(inputs, self._INPUT_ENCODE_OPTIONS),
            options=options,
        )
        if branch is ...:
            branch = self._branch
        merged_headers = _merge_headers(headers, {CHALK_BRANCH_ID_HEADER: branch} if branch is not None else None)
        response, call = self._stub_refresher.call_query_stub(
            lambda x: x.UploadFeatures.with_call(request, timeout=request_timeout, metadata=merged_headers),
            self._engine_target(branch),
        )
        trace_id = get_trace_id_from_response(call)
        py_errors = [ChalkErrorConverter.chalk_error_decode(err) for err in response.errors]
        return UploadFeaturesResponse(errors=py_errors, trace_id=trace_id)

    def multi_query(
        self,
        queries: List[OnlineQuery],
        correlation_id: str | None = None,
        query_name: str | None = None,
        query_name_version: str | None = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: bool = False,
        store_plan_stages: bool = False,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]] = None,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[Sequence[str]] = None,
        planner_options: Optional[Mapping[str, Any]] = None,
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        branch: str | None | types.EllipsisType = ...,
    ) -> BulkOnlineQueryResponse:
        """Execute a series of independent requests in parallel."""
        requests: List[GenericSingleQuery] = []
        for query in queries:
            # NOTE: This assumed every request is a 'bulk' request.
            if value_metrics_tag_by_features is not None:
                query_vmtbf = value_metrics_tag_by_features
            else:
                query_vmtbf = query.value_metrics_tag_by_features
            resolved_query_name, resolved_query_name_version = resolve_multi_query_query_name(
                query, query_name, query_name_version
            )
            request = self._make_query_bulk_request(
                input=query.input,
                output=query.output,
                now=(),
                staleness=query.staleness or {},
                tags=query.tags or (),
                correlation_id=correlation_id,
                query_name=resolved_query_name,
                query_name_version=resolved_query_name_version,
                include_meta=include_meta,
                meta=meta or {},
                explain=explain,
                store_plan_stages=store_plan_stages,
                value_metrics_tag_by_features=query_vmtbf,
                encoding_options=encoding_options,
                required_resolver_tags=required_resolver_tags or (),
                planner_options=query.planner_options or planner_options or {},
                query_context=query_context,
            )
            requests.append(GenericSingleQuery(bulk_request=request))
        if branch is ...:
            branch = self._branch
        headers = _merge_headers(headers, {CHALK_BRANCH_ID_HEADER: branch} if branch is not None else branch)
        response, call = self._stub_refresher.call_query_stub(
            lambda x: x.OnlineQueryMulti.with_call(
                online_query_pb2.OnlineQueryMultiRequest(
                    queries=requests,
                ),
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            ),
            self._engine_target(branch),
        )
        return OnlineQueryConverter.online_query_multi_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def _get_python_codegen(
        self, branch: str | None = None, deployment_id: str | None = None
    ) -> GetCodegenFeaturesFromGraphResponse:
        """Execute a series of independent requests in parallel."""
        import sys

        python_verison = sys.version_info

        resp: GetCodegenFeaturesFromGraphResponse = self._stub_refresher.call_graph_stub(
            lambda x: x.GetCodegenFeaturesFromGraph(
                GetCodegenFeaturesFromGraphRequest(
                    branch=branch,
                    deployment_id=deployment_id,
                    python_version=PythonVersion(
                        major=python_verison.major, minor=python_verison.minor, patch=python_verison.micro
                    ),
                )
            )
        )
        return resp

    def _create_branch(
        self, branch_name: str, source_branch_name: str | None = None, source_deployment_id: str | None = None
    ) -> CreateBranchResponse:
        """Create a branch from either a source deployment id, a source branch name, or the mainline deployment."""
        resp: CreateBranchFromSourceDeploymentResponse = self._stub_refresher.call_deploy_stub(
            lambda x: x.CreateBranchFromSourceDeployment(
                CreateBranchFromSourceDeploymentRequest(
                    branch_name=branch_name,
                    source_branch_name=source_branch_name,
                    source_deployment_id=source_deployment_id,
                    current_mainline_deployment=(
                        empty_pb2.Empty() if source_branch_name is None and source_deployment_id is None else None
                    ),
                )
            )
        )
        return CreateBranchResponse(
            branch_already_exists=resp.branch_already_exists,
            errors=[ChalkErrorConverter.chalk_error_decode(err) for err in resp.deployment_errors],
        )

    def _make_query_bulk_request(
        self,
        *,
        input: Mapping[FeatureReference, Sequence[Any]] | DataFrame | None = None,
        input_sql: str | None = None,
        output: Sequence[FeatureReference],
        now: Sequence[dt.datetime],
        staleness: Mapping[FeatureReference, str],
        tags: Sequence[str],
        correlation_id: str | None,
        query_name: str | None,
        query_name_version: str | None,
        include_meta: bool,
        meta: Mapping[str, str],
        explain: bool,
        store_plan_stages: bool,
        value_metrics_tag_by_features: Optional[Sequence[FeatureReference]],
        encoding_options: FeatureEncodingOptions | None,
        required_resolver_tags: Sequence[str],
        planner_options: Mapping[str, str | int | bool],
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None,
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> online_query_pb2.OnlineQueryBulkRequest:
        if input is None and input_sql is None:
            raise TypeError("One of `input` or `input_sql` is required")
        if input is not None and input_sql is not None:
            raise TypeError("`input` and `input_sql` are mutually exclusive")

        inputs_feather: bytes | None
        if input is None:
            inputs_feather = None
        else:
            inputs_feather = get_features_feather_bytes(
                input,
                self._INPUT_ENCODE_OPTIONS,
                compression=self._input_compression,
                input_schema_hint=input_schema_hint,
            )

        encoded_outputs = encode_outputs(output)
        outputs = encoded_outputs.string_outputs
        # Currently assume every feature tag is just a fqn instead of a more complex expr.
        value_metrics_tags_encoded = encode_outputs(value_metrics_tag_by_features or []).string_outputs
        value_metrics_tags_proto = [online_query_pb2.OutputExpr(feature_fqn=o) for o in value_metrics_tags_encoded]

        now_proto: List[timestamp_pb2.Timestamp] = []
        for ts in now:
            if ts.tzinfo is None:
                ts = ts.astimezone(tz=dt.timezone.utc)
            now_proto.append(datetime_to_proto_timestamp(ts))

        staleness_encoded: dict[str, str] = {}
        for k, v in staleness.items():
            if is_feature_set_class(k):
                for f in k.features:
                    staleness_encoded[f.root_fqn] = v
            else:
                staleness_encoded[str(k)] = v

        context_options_dict: dict[str, Any] = {
            "store_plan_stages": store_plan_stages,
        }
        context_options_dict.update(**(planner_options or {}))
        context_options_proto = {k: value_to_proto(v) for k, v in context_options_dict.items()}
        query_context = _validate_context_dict(query_context)
        query_context_proto = {k: value_to_proto(v) for k, v in query_context.items()} if query_context else None
        return online_query_pb2.OnlineQueryBulkRequest(
            inputs_feather=inputs_feather,
            inputs_sql=input_sql,
            outputs=[online_query_pb2.OutputExpr(feature_fqn=o) for o in outputs]
            + [online_query_pb2.OutputExpr(feature_expression=o) for o in encoded_outputs.feature_expressions_proto],
            now=now_proto,
            staleness=staleness_encoded,
            context=online_query_pb2.OnlineQueryContext(
                environment=self._stub_refresher.environment_id,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                options=context_options_proto,
                query_context=query_context_proto,
                value_metrics_tag_by_features=value_metrics_tags_proto,
                overlay_graph=live_updates.build_overlay_graph(),
            ),
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=include_meta,
                explain=online_query_pb2.ExplainOptions() if explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=encoding_options.encode_structs_as_objects if encoding_options else False
                ),
                metadata=meta,
            ),
            body_type=online_query_pb2.FEATHER_BODY_TYPE_RECORD_BATCHES,
        )

    def get_online_query_input_values(
        self,
        query: "Union[OnlineQueryResult, str]",
        query_timestamp: Optional[dt.datetime] = None,
    ) -> list[dict[str, Any]]:
        """Fetch the stored inputs of a past online query as a list of row dicts.

        `query` is either the operation id of the online query (a string), or the
        `OnlineQueryResult` returned by a prior `query(...)` call. When a result is passed, both the
        operation id and the query timestamp are read from `result.meta`, so the query must have
        been run with `include_meta=True`.

        `query_timestamp` is the approximate time the query ran. Without it the query run is only
        looked up within the last 24 hours; pass it to fetch inputs for queries older than that. It
        is taken automatically from `result.meta.query_timestamp` when a result is passed.

        Inputs are only available when online-query value persistence is enabled for the
        environment:

        - `CHALK_PLANNER_PERSIST_VALUES_OFFLINE_STORE=1` is required for online queries to persist
          their inputs/outputs to the value tables. It is off by default; without it this returns
          an empty list.
        - `CHALK_PERSIST_TO_OFFLINE_STORE_QUERY_LOG` controls whether the run is written to the
          query log at all; without it the query run cannot be found.

        (Offline queries always persist their inputs; this method is for online queries.)
        """
        import io

        import pyarrow as pa
        import pyarrow.parquet as pq

        # Resolve the operation id (and, for a result object, the query timestamp) from `query`.
        if isinstance(query, str):
            query_id = query
        else:
            meta = getattr(query, "meta", None)
            query_id = getattr(meta, "query_id", None) if meta is not None else None
            if not query_id:
                raise ValueError(
                    "Could not read the query id from the provided online query result. Run the "
                    + "query with `include_meta=True` so `result.meta.query_id` is populated, or pass "
                    + "the query id string directly."
                )
            if query_timestamp is None:
                query_timestamp = getattr(meta, "query_timestamp", None)

        # 1) Resolve the query run -> creation time (for the value-table scan window) and the meta
        #    query id (to know which columns are inputs). Without an approximate timestamp the
        #    server only searches the last 24h, so pass one through to locate older queries.
        run_request = GetQueryRunRequest(operation_id=query_id)
        if query_timestamp is not None:
            approximate_timestamp = timestamp_pb2.Timestamp()
            approximate_timestamp.FromDatetime(query_timestamp)
            run_request = GetQueryRunRequest(operation_id=query_id, approximate_timestamp=approximate_timestamp)
        try:
            run_resp = self._stub_refresher.call_queries_stub(lambda x: x.GetQueryRun(run_request))
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ValueError(
                    f"Online query '{query_id}' was not found. If the query is new it may take a few "
                    + "seconds to appear. If it ran more than 24h ago, pass `query_timestamp` (its "
                    + "approximate run time) so it can be located."
                ) from e
            raise
        query_run = run_resp.query_run
        created_at = query_run.created_at.ToDatetime()

        meta_resp = self._stub_refresher.call_queries_stub(
            lambda x: x.GetMetaQuery(GetMetaQueryRequest(meta_query_id=query_run.meta_query_id))
        )
        meta_query = meta_resp.meta_query
        # Value-table columns use dunder-separated fqns (e.g. the feature ``bank_account.id`` is
        # stored in the column ``bank_account__id``), so map each input feature fqn to its column
        # name. We key the returned rows by the original dot-separated fqn.
        column_to_fqn: dict[str, str] = {}
        for fqn in set(meta_query.input_features) | set(meta_query.input_feature_root_fqns):
            column = fqn.replace(".", "__")
            column_to_fqn[column] = fqn
            # Tolerate versioned/unversioned mismatches between the meta query and the value table.
            column_to_fqn.setdefault(column.split("@", 1)[0], fqn)

        # 2) The value table is partitioned by query timestamp, so the scan must be bounded to a
        #    window around the run's creation time (mirrors the dashboard's inputs pane).
        window = dt.timedelta(minutes=5)
        lower = timestamp_pb2.Timestamp()
        lower.FromDatetime(created_at - window)
        upper = timestamp_pb2.Timestamp()
        upper.FromDatetime(created_at + window)

        # 3) Page through the stored values for this operation.
        tables: list[pa.Table] = []
        FIRST_RUN = "FIRST_RUN_SENTINEL"
        page_token = FIRST_RUN
        while page_token:
            request = GetQueryValuesRequest(
                operation_id_identifier=OperationIdTableIdentifier(operation_id=query_id),
                query_timestamp_lower_bound_inclusive=lower,
                query_timestamp_upper_bound_exclusive=upper,
                page_token="" if page_token == FIRST_RUN else page_token,
            )
            resp = self._stub_refresher.call_offline_store_stub(lambda x: x.GetQueryValues(request))

            if resp.parquet:
                tables.append(pq.read_table(io.BytesIO(resp.parquet)))

            page_token = resp.next_page_token

        if not tables:
            return []

        table = tables[0] if len(tables) == 1 else pa.concat_tables(tables)

        # 4) Keep only the input columns (dropping outputs and internal __chalk_* columns) and key
        #    each row by the feature fqn rather than the raw value-table column name.
        selected = [name for name in table.column_names if name in column_to_fqn]
        return [
            {column_to_fqn[column]: value for column, value in row.items()}
            for row in table.select(selected).to_pylist()
        ]

    def run_scheduled_query(
        self,
        name: str,
        planner_options: Optional[Mapping[str, Any]],
        incremental_resolvers: Optional[Sequence[str]],
        max_samples: Optional[int],
        env_overrides: Optional[Mapping[str, str]],
        unload_resolvers: Optional[list[dict]] = None,
    ) -> ManualTriggerScheduledQueryResponseDataclass:
        """
        Manually trigger a scheduled query request.

        Parameters
        ----------
        name
            The name of the scheduled query to be triggered.
        incremental_resolvers
            If set to None, Chalk will incrementalize resolvers in the query's root namespaces.
            If set to a list of resolvers, this set will be used for incrementalization.
            Incremental resolvers must return a feature time in its output, and must return a `DataFrame`.
            Most commonly, this will be the name of a SQL file resolver. Chalk will ingest all new data
            from these resolvers and propagate changes to values in the root namespace.
        max_samples
            The maximum number of samples to compute.
        env_overrides:
            A dictionary of environment values to override during this specific triggered query.

        Other Parameters
        ----------------
        planner_options
            A dictionary of options to pass to the planner.
            These are typically provided by Chalk Support for specific use cases.

        Returns
        -------
        ManualTriggerScheduledQueryResponse
            A response message containing metadata around the triggered run.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().run_scheduled_query(
        ...     name="my_scheduled_query",
        ... )
        """
        proto_resp = self._stub_refresher.call_scheduled_query_stub(
            lambda x: x.ManualTriggerScheduledQuery(
                request=ManualTriggerScheduledQueryRequest(
                    cron_query_name=name,
                    planner_options=planner_options or {},
                    incremental_resolvers=incremental_resolvers or (),
                    max_samples=max_samples,
                    env_overrides=env_overrides or {},
                    unload_resolvers=[
                        offline_query_pb2.UnloadResolverSpec(
                            fqn="all" if "any" in spec else spec["fqn"],
                            partition_by=[] if "any" in spec else spec.get("partition_by", []),
                        )
                        for spec in (unload_resolvers or [])
                    ],
                ),
            )
        )
        return ManualTriggerScheduledQueryResponseDataclass.from_proto(proto_resp)

    def get_scheduled_query_run_history(
        self, name: str, limit: int = 10, include_run_details: bool = False
    ) -> List[ScheduledQueryRun]:
        """
        Get the run history for a scheduled query.

        Parameters
        ----------
        name
            The name of the scheduled query.
        limit
            The maximum number of runs to return. Defaults to 10.
        include_run_details
            Whether or not to populate the metadata fields of each run.

        Returns
        -------
        list[ScheduledQueryRun]
            A response message containing the list of scheduled query runs.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().get_scheduled_query_run_history(
        ...     name="my_scheduled_query",
        ...     limit=20,
        ... )
        """
        proto_resp = self._stub_refresher.call_scheduled_query_run_stub(
            lambda x: x.GetScheduledQueryRuns(
                GetScheduledQueryRunsRequest(
                    cron_name=name,
                    limit=limit,
                )
            )
        )

        processed_runs = [ScheduledQueryRun.from_proto(run) for run in proto_resp.runs]

        if include_run_details:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            def _enrich(run: ScheduledQueryRun) -> None:
                meta = self.get_scheduled_query_run_details(run)
                if isinstance(meta, OfflineQueryInfo):
                    run.offline_query_meta = meta
                elif isinstance(meta, WorkflowExecutionInfo):
                    run.workflow_execution = meta

            with ThreadPoolExecutor(max_workers=min(len(processed_runs), 10)) as pool:
                futures = [pool.submit(_enrich, run) for run in processed_runs]
                for future in as_completed(futures):
                    future.result()  # raise if any enrichment failed

        return processed_runs

    def get_scheduled_query_run_details(
        self, scheduled_run: ScheduledQueryRun
    ) -> Union[WorkflowExecutionInfo, OfflineQueryInfo, None]:
        from chalk._gen.chalk.server.v1.dataplaneworkflows_pb2 import GetDataPlaneWorkflowRequest

        if scheduled_run.workflow_execution_id:
            wfe_resp = self._stub_refresher.call_dataplane_workflows_stub(
                lambda x: x.GetDataPlaneWorkflow(GetDataPlaneWorkflowRequest(id=scheduled_run.workflow_execution_id))
            )
            if wfe_resp.HasField("workflow"):
                return WorkflowExecutionInfo.from_proto(wfe_resp.workflow)

        elif scheduled_run.offline_query_id:
            oq_resp = self._stub_refresher.call_offline_query_stub(
                lambda x: x.GetOfflineQuery(GetOfflineQueryRequest(offline_query_id=scheduled_run.offline_query_id))
            )
            if oq_resp.HasField("offline_query"):
                return OfflineQueryInfo.from_proto(oq_resp.offline_query)

        return None

    def list_jobs(
        self,
        state: Optional[
            Literal["scheduled", "running", "completed", "failed", "canceled", "not_ready", "waiting"]
        ] = None,
        kind: Optional[
            Literal["async_offline_query", "scheduled_query", "script_task", "chalksql_run", "dataframe_run"]
        ] = None,
        operation_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[JobQueueItem]:
        """
        List jobs in the data plane job queue.

        Parameters
        ----------
        state
            Filter by job state.
        kind
            Filter by job kind.
        operation_id
            Filter by operation ID.
        limit
            Maximum number of jobs to return. Defaults to 50.
        offset
            Offset for pagination. Defaults to 0.

        Returns
        -------
        List[JobQueueItem]
            The list of jobs.
        """
        request = ListDataPlaneJobQueueRequest(limit=limit, offset=offset)
        if state is not None:
            if state not in _JOB_STATE_MAP:
                raise ValueError(f"Invalid state: {state}. Valid states: {', '.join(_JOB_STATE_MAP)}")
            request.state = _JOB_STATE_MAP[state]
        if kind is not None:
            if kind not in _JOB_KIND_MAP:
                raise ValueError(f"Invalid kind: {kind}. Valid kinds: {', '.join(_JOB_KIND_MAP)}")
            request.kind = _JOB_KIND_MAP[kind]
        if operation_id:
            request.operation_id = operation_id

        try:
            proto_resp = self._stub_refresher.call_job_queue_stub(lambda x: x.ListDataPlaneJobQueue(request))
        except Exception as e:
            raise RuntimeError(f"Could not list jobs. {e}") from e
        return [JobQueueItem.from_proto(job) for job in proto_resp.jobs]

    def get_offline_query_report(self, offline_query_id: str) -> Optional[OfflineQueryReport]:
        """
        Get the batch report associated with the offline query in environment.

        Parameters
        ----------
        offline_query_id
            Offline query's ID.

        environment_id
            Environment ID of offline query.

        Returns
        -------
        Optional[OfflineQueryReport]
            The OfflineQueryReport object if it exists.
        """
        from chalk._reporting.models import BatchOpKind, BatchOpStatus

        _BATCH_OP_KIND_MAP = {
            0: BatchOpKind.OFFLINE_QUERY,  # UNSPECIFIED -> default
            1: BatchOpKind.OFFLINE_QUERY,
            2: BatchOpKind.RECOMPUTE,
            3: BatchOpKind.CRON,
            4: BatchOpKind.AGGREGATION_BACKFILL,
        }

        _BATCH_OP_STATUS_MAP = {
            0: BatchOpStatus.INIT,  # UNSPECIFIED -> default
            1: BatchOpStatus.INIT,
            2: BatchOpStatus.COMPUTE_STARTED,
            3: BatchOpStatus.COMPUTE_ENDED,
            4: BatchOpStatus.COMPLETED,
            5: BatchOpStatus.FAILED,
        }

        try:
            batch_report_resp = self._stub_refresher.call_offline_query_stub(
                lambda x: x.GetBatchReport(GetBatchReportRequest(report_id=offline_query_id))
            )
        except Exception:
            warnings.warn(f"No batch report for offline query {offline_query_id}")
            return None

        return OfflineQueryReport(
            operation_kind=_BATCH_OP_KIND_MAP.get(
                int(batch_report_resp.batch_report.operation_kind), BatchOpKind.OFFLINE_QUERY
            ),
            status=_BATCH_OP_STATUS_MAP.get(int(batch_report_resp.batch_report.status), BatchOpStatus.INIT),
            environment_id=batch_report_resp.batch_report.environment_id,
            deployment_id=batch_report_resp.batch_report.deployment_id,
            started_at=batch_report_resp.batch_report.started_at.ToDatetime(),
            ended_at=(
                batch_report_resp.batch_report.ended_at.ToDatetime()
                if batch_report_resp.batch_report.HasField("ended_at")
                else None
            ),
            all_errors=[ChalkError.from_proto(err) for err in batch_report_resp.batch_report.all_errors],
        )

    def get_offline_query_profile_summary(self, offline_query_id: str) -> OfflineQueryProfileSummary:
        """
        Get the profile metrics summary for an offline query.

        Parameters
        ----------
        offline_query_id
            Offline query's ID.

        Returns
        -------
        OfflineQueryProfileSummary
            Aggregated profile metrics and warnings for the offline query.
        """
        resp = self._stub_refresher.call_offline_query_stub(
            lambda x: x.GetOfflineQueryProfileSummary(
                GetOfflineQueryProfileSummaryRequest(offline_query_id=offline_query_id)
            )
        )
        return OfflineQueryProfileSummary.from_proto(resp)

    def _get_active_deployment_id(self) -> str:
        resp = self._stub_refresher.call_deploy_stub(lambda x: x.GetActiveDeployments(GetActiveDeploymentsRequest()))
        env_id = self._stub_refresher.environment_id
        matching = [d for d in resp.deployments if d.environment_id == env_id]
        if not matching:
            raise RuntimeError("No active deployment found for this environment.")
        return matching[0].id

    def redeploy(
        self,
        deployment_id: Optional[str] = None,
        build_profile: Optional[Literal["o3_no_profiling", "o3_profiling", "o2_no_profiling", "o2_profiling"]] = None,
        deployment_tags: Optional[List[str]] = None,
        base_image_override: Optional[str] = None,
        force_rebuild_dockerfile: bool = False,
        display_description: Optional[str] = None,
    ) -> RedeployResponse:
        """Full rebuild and deploy using this deployment's source."""
        if deployment_id is None:
            deployment_id = self._get_active_deployment_id()
        resolved_build_profile = self._resolve_build_profile(build_profile)
        try:
            req = RedeployDeploymentRequest(
                existing_deployment_id=deployment_id,
                deployment_tags=deployment_tags or [],
                base_image_override=base_image_override or "",
                build_profile=resolved_build_profile,
                force_rebuild_dockerfile=force_rebuild_dockerfile,
                display_description=display_description or "",
            )
            resp = self._stub_refresher.call_builder_stub(lambda x: x.RedeployDeployment(req))
            return RedeployResponse(
                kind="redeploy", deployment_id=resp.deployment_id or None, build_id=resp.build_id or None
            )
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not redeploy deployment '{deployment_id}'. {e}") from e

    def rollback_deployment(self, deployment_id: str) -> RedeployResponse:
        """Instantly redeploy using this deployment's pre-built image."""
        try:
            req = ActivateDeploymentRequest(existing_deployment_id=deployment_id)
            self._stub_refresher.call_builder_stub(lambda x: x.ActivateDeployment(req))
            return RedeployResponse(kind="rollback")
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not rollback deployment '{deployment_id}'. {e}") from e

    def suspend_environment(self, environment_id: str) -> None:
        """Suspend the environment this client is bound to, spinning down its cloud resources."""
        bound_environment_id = self._stub_refresher.environment_id
        if bound_environment_id != environment_id:
            raise ValueError(f"Refusing to suspend '{environment_id}': client is bound to '{bound_environment_id}'.")
        try:
            self._stub_refresher.call_builder_stub(lambda x: x.SuspendEnvironment(SuspendEnvironmentRequest()))
        except Exception as e:
            raise RuntimeError(f"Could not suspend environment '{environment_id}'. {e}") from e

    def resume_environment(self, environment_id: str) -> None:
        """Resume the suspended environment this client is bound to, spinning its cloud resources back up."""
        bound_environment_id = self._stub_refresher.environment_id
        if bound_environment_id != environment_id:
            raise ValueError(f"Refusing to resume '{environment_id}': client is bound to '{bound_environment_id}'.")
        try:
            self._stub_refresher.call_builder_stub(lambda x: x.ResumeEnvironment(ResumeEnvironmentRequest()))
        except Exception as e:
            raise RuntimeError(f"Could not resume environment '{environment_id}'. {e}") from e

    def rebuild_deployment(
        self,
        deployment_id: str,
        new_image_tag: str,
        build_profile: Optional[Literal["o3_no_profiling", "o3_profiling", "o2_no_profiling", "o2_profiling"]] = None,
        base_image_override: Optional[str] = None,
        force_rebuild_dockerfile: bool = False,
    ) -> RedeployResponse:
        """Build a new image from this deployment's source without deploying."""
        resolved_build_profile = self._resolve_build_profile(build_profile)
        try:
            req = RebuildDeploymentRequest(
                existing_deployment_id=deployment_id,
                new_image_tag=new_image_tag,
                base_image_override=base_image_override or "",
                build_profile=resolved_build_profile,
                force_rebuild_dockerfile=force_rebuild_dockerfile,
            )
            resp = self._stub_refresher.call_builder_stub(lambda x: x.RebuildDeployment(req))
            return RedeployResponse(kind="rebuild", build_id=resp.build_id or None)
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not rebuild deployment '{deployment_id}'. {e}") from e

    def patch_deployment(self, deployment_id: Optional[str] = None) -> RedeployResponse:
        """Patch deployment config and restart pods without a new build."""
        if deployment_id is None:
            deployment_id = self._get_active_deployment_id()
        try:
            req = DeployKubeComponentsRequest(existing_deployment_id=deployment_id)
            resp = self._stub_refresher.call_builder_stub(lambda x: x.DeployKubeComponents(req))
            return RedeployResponse(kind="patch", nonfatal_errors=list(resp.nonfatal_errors) or None)
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not patch deployment '{deployment_id}'. {e}") from e

    def _reindex(self, deployment_id: str) -> RedeployResponse:
        try:
            req = IndexDeploymentRequest(existing_deployment_id=deployment_id, shadow=False)
            resp = self._stub_refresher.call_builder_stub(lambda x: x.IndexDeployment(req))
            return RedeployResponse(kind="reindex", build_id=resp.build_id or None)
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not reindex deployment '{deployment_id}'. {e}") from e

    def _shadow_build(self, deployment_id: str) -> RedeployResponse:
        try:
            req = StartShadowBuildFromDeploymentRequest(existing_deployment_id=deployment_id)
            resp = self._stub_refresher.call_builder_stub(lambda x: x.StartShadowBuildFromDeployment(req))
            return RedeployResponse(kind="shadow_build", build_id=resp.build_id or None)
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Could not start shadow build from deployment '{deployment_id}'. {e}") from e

    @staticmethod
    def _resolve_build_profile(
        build_profile: Optional[str],
    ):
        if build_profile is None:
            return None
        if build_profile not in _BUILD_PROFILE_MAP:
            raise ValueError(f"Invalid build_profile: {build_profile!r}. Valid values: {', '.join(_BUILD_PROFILE_MAP)}")
        return _BUILD_PROFILE_MAP[build_profile]

    def get_named_query_metadata(
        self,
        name: str,
        query_version: str | None = None,
        branch: str | None = None,
    ) -> List[NamedQueryMetadata]:
        """
        Get the metadata associated with named queries.

        Parameters
        ----------
        name
            The name of the named query.
        query_version
            The query version of the named query. Returns all versions of the named query by default.
        branch
            The branch name to get the named query from. By default will use the mainline deployment.

        Returns
        -------
        list[ScheduledQueryRun]
            A response message containing the list of metadata of named queries.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().get_named_query_metadata(
        ...     name="my_named_query",
        ...     query_version="1.1.0",
        ... )
        """
        # TODO update underlying logic to be done server side and/or not split between GRPC and python client.
        if branch:
            from chalk.client import ChalkClient

            client = ChalkClient(
                client_id=self._client_id,
                client_secret=self._client_secret,
                environment=self._environment,
                api_server=self._api_server,
            )

            return client.get_named_query_metadata(
                name=name,
                query_version=query_version,
                branch=branch,
            )

        proto_resp = self._stub_refresher.call_get_named_query_metadata(
            lambda x: x.GetNamedQueryByName(
                request=GetNamedQueryByNameRequest(
                    name=name,
                    query_version=query_version,
                )
            )
        )

        return [NamedQueryMetadata.from_proto(nq) for nq in proto_resp.named_queries]

    def get_graph(self, deployment: DeploymentId | None = None) -> Graph:
        """Get the graph for a given deployment.

        Parameters
        ----------
        deployment
            The id of the Chalk deployment, or `None` to use the latest deployment.

        Returns
        -------
        Graph
            The graph for the given deployment.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().get_graph()
        """
        resp: GetGraphResponse = self._stub_refresher.call_graph_stub(
            lambda x: x.GetGraph(GetGraphRequest(deployment_id=deployment))
        )
        return resp.graph

    def get_offline_store_table_name(
        self,
        feature: Any,
        include_historical: bool = False,
    ) -> "str | list[str]":
        """Get the offline store table name(s) for a feature.

        Parameters
        ----------
        feature
            The feature to look up. Can be a feature class attribute (e.g. ``User.fico_score``)
            or a string FQN (e.g. ``"user.fico_score"``).
        include_historical
            If ``False`` (default), returns the current active table name as a string.
            If ``True``, returns all historical table names ordered by internal version
            (oldest to newest).

        Returns
        -------
        str | list[str]
            The table name string, or a list of table name strings if ``include_historical=True``.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().get_offline_store_table_name(User.fico_score)
        >>> ChalkGRPCClient().get_offline_store_table_name("user.fico_score", include_historical=True)
        """
        from chalk.features.feature_wrapper import ensure_feature

        if self._environment is None:
            chalk_logger.error(
                "No environment set on ChalkGRPCClient. Please specify an environment when initializing the client."
            )
            raise ValueError("environment is required to look up offline store table names")

        fqn = feature if isinstance(feature, str) else ensure_feature(feature).root_fqn

        resp = self._stub_refresher.call_graph_stub(
            lambda x: x.GetOfflineStoreTable(GetOfflineStoreTableRequest(fqn=fqn))
        )

        table_names = [t.table_name for t in resp.tables]

        if include_historical:
            return table_names
        return table_names[-1]

    def _iter_offline_store_tables(self, deployment_id: "str | None" = None):
        if self._environment is None:
            chalk_logger.error(
                "No environment set on ChalkGRPCClient. Please specify an environment when initializing the client."
            )
            raise ValueError("environment is required to look up offline store table names")
        page_token = ""
        while True:
            resp = self._stub_refresher.call_graph_stub(
                lambda x: x.GetAllOfflineStoreTables(
                    GetAllOfflineStoreTablesRequest(deployment_id=deployment_id or "", page_token=page_token)
                )
            )

            for table in resp.tables:
                yield OfflineStoreTable(
                    fqn=table.fqn,
                    internal_version=table.internal_version,
                    table_name=table.table_name,
                )
            page_token = resp.next_page_token
            if page_token == "":
                break

    def get_all_offline_store_table_names(
        self,
        deployment_id: "str | None" = None,
    ) -> "list[OfflineStoreTable]":
        """Get the offline store table name for every feature and internal version in a deployment.

        Useful for reverse-mapping a ``feat_<hash>`` offline store table name back to its feature.

        Parameters
        ----------
        deployment_id
            The deployment to look up. If ``None``, uses the environment's active deployment.

        Returns
        -------
        list[OfflineStoreTable]
            One entry per feature and internal version, each with ``fqn``, ``internal_version``, and ``table_name``.
        """
        return list(self._iter_offline_store_tables(deployment_id))

    def get_feature_from_offline_store_table_name(
        self,
        table_name: str,
        deployment_id: "str | None" = None,
    ) -> "OfflineStoreTable | None":
        """Find the feature for a given offline store table name (reverse lookup).

        Parameters
        ----------
        table_name
            The ``feat_<hash>`` offline store table name to look up.
        deployment_id
            The deployment to search. If ``None``, uses the environment's active deployment.

        Returns
        -------
        OfflineStoreTable | None
            The matching table (with ``fqn`` and ``internal_version``), or ``None`` if no feature maps to that table name.
        """
        for table in self._iter_offline_store_tables(deployment_id):
            if table.table_name == table_name:
                return table
        return None

    def cancel_offline_query(
        self,
        offline_query_id: str,
    ) -> None:
        """Cancel an in-progress async offline query by its ID.

        Parameters
        ----------
        offline_query_id
            The ID of the offline query to cancel. Returns an error if the query
            is not found or is not in a cancellable state (i.e. not WORKING or QUEUED).

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> ChalkGRPCClient().cancel_offline_query(
        ...     offline_query_id="oq_1234567890abcdef",
        ... )
        """
        self._stub_refresher.call_offline_query_stub(
            lambda x: x.CancelAsyncOfflineQuery(
                request=CancelAsyncOfflineQueryRequest(offline_query_id=offline_query_id)
            )
        )

    def create_service_token(
        self,
        name: str,
        permissions: List[Permission],
        customer_claims: Mapping[str, List[str]] | None = None,
    ) -> CreateServiceTokenResponse:
        """Create a service token with a given set of permissions and claims.

        Parameters
        ----------
        name
            The name of your service token.
        permissions
            The permissions that you want your token to have.
        customer_claims
            The customer claims that you want your token to have.

        Returns
        -------
        CreateServiceTokenResponse
            A service token response, including a `client_id` and `client_secret` with
            the specified permissions and customer claims.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient(client_id='test', client_secret='test_secret')
        >>> client.create_service_token(permissions=[Permission.PERMISSION_QUERY_ONLINE])
        """
        return self._stub_refresher.call_team_stub(
            lambda x: x.CreateServiceToken(
                CreateServiceTokenRequest(
                    name=name,
                    permissions=permissions,
                    customer_claims=(
                        None
                        if customer_claims is None
                        else [CustomClaim(key=key, values=values) for key, values in customer_claims.items()]
                    ),
                )
            )
        )

    def list_service_tokens(self) -> ListServiceTokensResponse:
        """Get all service tokens for the current environment.

        Returns
        -------
        ListServiceTokensResponse
            A list of service tokens for the current environment.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient()
        >>> client.list_service_tokens()
        """
        return self._stub_refresher.call_team_stub(lambda x: x.ListServiceTokens(ListServiceTokensRequest()))

    def list_datasets(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        search: str | None = None,
    ) -> ListDatasetsResponseDataclass:
        """
        List datasets in the current environment.

        Returns a single page of datasets ordered by creation time, along
        with a cursor for fetching the next page if more results are
        available. Datasets are scoped to the active environment.

        cursor
            Opaque pagination token returned in the ``cursor`` field of a
            previous ``list_datasets`` response. Pass it back verbatim to
            fetch the next page. On the first call, leave as ``None``.
        limit
            Maximum number of datasets to return in this page. Defaults to
            ``100`` on the server when not provided.
        search
            Case-insensitive substring filter applied to dataset names.

        Returns
        -------
        ListDatasetsResponseDataclass
            A page of dataset metadata. The ``cursor`` field on the response
            will be empty when there are no further pages to fetch.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()

        List the most recent datasets:

        >>> response = client.list_datasets()
        >>> for dataset in response.datasets:
        ...     print(dataset.dataset_name, dataset.latest_status)

        Paginate through all datasets in pages of 10:

        >>> response = client.list_datasets(limit=10)
        >>> while response.cursor:
        ...     response = client.list_datasets(cursor=response.cursor, limit=10)
        """
        proto_resp = self._stub_refresher.call_dataset_metadata_stub(
            lambda x: x.ListDatasets(
                request=ListDatasetsRequest(
                    cursor=cursor,
                    limit=limit,
                    search=search,
                )
            )
        )
        return ListDatasetsResponseDataclass.from_proto(proto_resp)

    def get_active_bloom_filters(self):
        """
        Gets bloom filters loaded on an engine, if any have been configured.
        Note: This request is unicast to a single engine, so if multiple engine pods are running
        only the information for one of them will be returned.
        """
        request = InspectBloomFiltersRequest()
        return self._stub_refresher.call_query_stub(lambda x: x.InspectBloomFilters(request), _EngineTarget.GRPC_ENGINE)

    def run_sql(self, sql: str, persistence_settings: Optional[Dict[str, Any]] = None):
        request = ExecuteSqlQueryRequest(query=sql)

        if persistence_settings is not None:
            # Convert dict to proto message
            enabled = persistence_settings.get("enabled", False)
            request.persistence_settings.CopyFrom(ExecuteSqlResultPersistenceSettings(enabled=enabled))

        return self._stub_refresher.call_sql_stub(lambda x: x.ExecuteSqlQuery(request), _EngineTarget.GRPC_ENGINE)

    def execute_dataframe_plan(
        self,
        plan: "DataFramePlan",
        resource_group: Optional[str] = None,
        correlation_id: Optional[str] = None,
        update_performance_summary_interval_secs: Optional[float] = None,
    ) -> str:
        """Submit a DataFramePlan for remote async execution.

        Args:
            plan: The serialized DataFramePlan to execute.
            resource_group: Optional resource group to run the job on.
            correlation_id: Optional correlation id for tracking.
            update_performance_summary_interval_secs: Seconds between periodic
                performance-summary writes during execution, powering the live
                performance summary in the dashboard. ``None`` (default) leaves the
                server default; ``0`` disables the live summary.

        Returns the operation_id string.
        """
        from chalk._gen.chalk.server.v1.dataframe_pb2 import ExecuteDataFramePlanRequest

        request = ExecuteDataFramePlanRequest(plan=plan)
        if correlation_id is not None:
            request.correlation_id = correlation_id
        if resource_group is not None:
            request.resource_group = resource_group
        if update_performance_summary_interval_secs is not None:
            request.update_performance_summary_interval_secs = update_performance_summary_interval_secs

        response = self._stub_refresher.call_api_dataframe_stub(lambda x: x.ExecuteDataFramePlan(request))
        return response.operation_id

    def get_dataframe_job_status(self, operation_id: str) -> "GetDataFrameRunResponse":
        """Poll the status of a DataFrame run.

        Returns a GetDataFrameRunResponse proto with a ``run`` field (DataFrameRun) containing
        status, output_uri_prefix, and other metadata.
        """
        from chalk._gen.chalk.server.v1.dataframe_pb2 import GetDataFrameRunRequest

        request = GetDataFrameRunRequest(operation_id=operation_id)
        return self._stub_refresher.call_api_dataframe_stub(lambda x: x.GetDataFrameRun(request))

    def get_dataframe_job_result(self, operation_id: str) -> str:
        """Return the output URI prefix for a completed DataFrame run.

        The run must be in COMPLETED status; raises RuntimeError otherwise.
        Callers are responsible for reading the parquet files at the returned prefix.
        """
        from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRunStatus
        from chalk.client._dataframe_status import derive_dataframe_run_status

        resp = self.get_dataframe_job_status(operation_id)
        status = derive_dataframe_run_status(resp.run)
        if status != DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED:
            raise RuntimeError(
                f"DataFrame run {operation_id} is not completed (status={status}); cannot fetch results."
            )
        if not resp.run.output_uri_prefix:
            raise RuntimeError(f"DataFrame run {operation_id} has no output_uri_prefix.")
        return resp.run.output_uri_prefix

    def get_dataframe_run_download_urls(self, operation_id: str) -> list[str]:
        """Return presigned download URLs for all parquet output files of a completed run.

        Uses the Chalk API to generate short-lived presigned URLs — no cloud credentials needed.
        """
        from chalk._gen.chalk.server.v1.dataframe_pb2 import GetDataFrameRunDownloadUrlsRequest

        req = GetDataFrameRunDownloadUrlsRequest(operation_id=operation_id)
        resp = self._stub_refresher.call_api_dataframe_stub(lambda x: x.GetDataFrameRunDownloadUrls(req))
        return [u.download_url for u in resp.download_urls]

    def remote_execute_plan(
        self,
        plan: "DataFramePlan",
        resource_group: Optional[str] = None,
        correlation_id: Optional[str] = None,
        poll_interval: float = 2.0,
        update_performance_summary_interval_secs: Optional[float] = None,
    ) -> str:
        """Submit a DataFramePlan for remote execution and wait for it to complete.

        In a Jupyter notebook, displays a live progress UI while waiting.
        Outside a notebook, polls silently until the run reaches a terminal state.
        Returns the operation_id string.
        """
        operation_id = self.execute_dataframe_plan(
            plan=plan,
            resource_group=resource_group,
            correlation_id=correlation_id,
            update_performance_summary_interval_secs=update_performance_summary_interval_secs,
        )
        self.follow_dataframe_run(operation_id, poll_interval=poll_interval)
        return operation_id

    def wait_dataframe_run(self, operation_id: str, poll_interval: float = 2.0) -> None:
        """Poll a DataFrame run until it reaches a terminal state, printing status changes."""
        import time

        from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRunStatus
        from chalk.client._dataframe_status import derive_dataframe_run_status, latest_attempt

        _TERMINAL_CODES = {
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED,
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED,
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED,
        }

        last_status = None
        last_attempt_idx = -1
        while True:
            resp = self.get_dataframe_job_status(operation_id)
            run = resp.run
            status = derive_dataframe_run_status(run)
            attempt = latest_attempt(run)
            # When the queue rolls onto a new attempt after a failure, surface
            # it so the user knows the run is retrying rather than fresh.
            if attempt is not None and attempt.attempt_idx > last_attempt_idx:
                if last_attempt_idx >= 0:
                    print(f"[DataFrame Run] Retrying (attempt {attempt.attempt_idx + 1})")
                last_attempt_idx = attempt.attempt_idx

            if status != last_status:
                pod = attempt.worker_pod_name if attempt and attempt.worker_pod_name else None
                pod_str = f" (pod: {pod})" if pod else ""
                if status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_STARTING:
                    print(f"[DataFrame Run] Starting{pod_str}")
                elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING:
                    print(f"[DataFrame Run] Working{pod_str}")
                elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED:
                    print("[DataFrame Run] Completed")
                elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED:
                    err = attempt.error_message if attempt and attempt.error_message else (run.error_message or None)
                    err_str = f": {err}" if err else ""
                    print(f"[DataFrame Run] Failed{err_str}")
                elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED:
                    print("[DataFrame Run] Canceled")
                last_status = status
            if status in _TERMINAL_CODES:
                if run.dashboard_url:
                    print(f"[DataFrame Run] View: {run.dashboard_url}")
                break
            time.sleep(poll_interval)

    def follow_dataframe_run(self, operation_id: str, poll_interval: float = 2.0) -> Any:
        """Poll a DataFrame run until it reaches a terminal state.

        In a Jupyter notebook, displays a live Rich progress UI.
        Outside a notebook, polls silently.
        Returns the final ``GetDataFrameRunResponse``.
        """
        from chalk.utils import notebook

        if not notebook.is_notebook():
            return self.wait_dataframe_run(operation_id, poll_interval=poll_interval)

        import time

        from rich.columns import Columns
        from rich.console import Console, Group
        from rich.live import Live
        from rich.spinner import Spinner
        from rich.style import Style
        from rich.table import Table
        from rich.text import Text

        from chalk._gen.chalk.server.v1.dataframe_pb2 import DataFrameRun, DataFrameRunStatus, JobAttemptState
        from chalk._reporting.rich.color import CITRUSY_YELLOW, GRASSY_GREEN, SHADOWY_LAVENDER, SHY_RED, UNDERLYING_CYAN
        from chalk.client._dataframe_status import derive_dataframe_run_status, latest_attempt

        _TERMINAL_CODES = {
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED,
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED,
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED,
        }

        _ATTEMPT_STATE_NAMES = {
            JobAttemptState.JOB_ATTEMPT_STATE_UNSPECIFIED: "Unspecified",
            JobAttemptState.JOB_ATTEMPT_STATE_QUEUED: "Queued",
            JobAttemptState.JOB_ATTEMPT_STATE_RUNNING: "Running",
            JobAttemptState.JOB_ATTEMPT_STATE_COMPLETED: "Completed",
            JobAttemptState.JOB_ATTEMPT_STATE_FAILED: "Failed",
            JobAttemptState.JOB_ATTEMPT_STATE_CANCELED: "Canceled",
        }

        _STATUS_NAMES = {
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_UNSPECIFIED: "Unspecified",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_QUEUED: "Queued",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_STARTING: "Starting",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING: "Working",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED: "Completed",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED: "Failed",
            DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED: "Canceled",
        }

        def _status_renderable(status: DataFrameRunStatus):
            name = _STATUS_NAMES.get(status, str(status))
            if status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED:
                return Text(f"✓ {name}", style=Style(color=GRASSY_GREEN, bold=True))
            elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED:
                return Text(f"✗ {name}", style=Style(color=SHY_RED, bold=True))
            elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_CANCELED:
                return Text(f"⊗ {name}", style=Style(color=SHADOWY_LAVENDER))
            elif status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_WORKING:
                return Columns(
                    [
                        Spinner("dots", style=Style(color=UNDERLYING_CYAN)),
                        Text(name, style=Style(color=UNDERLYING_CYAN, bold=True)),
                    ],
                    expand=False,
                )
            else:  # QUEUED, STARTING, or UNSPECIFIED
                return Columns(
                    [
                        Spinner("dots2", style=Style(color=CITRUSY_YELLOW)),
                        Text(name, style=Style(color=CITRUSY_YELLOW)),
                    ],
                    expand=False,
                )

        def _build_display(run: DataFrameRun, elapsed: float) -> Group:
            minutes, seconds = divmod(int(elapsed), 60)
            hours, minutes = divmod(minutes, 60)
            elapsed_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"

            title_text = Text("DataFrame Run", style=Style(color=UNDERLYING_CYAN, bold=True))
            title_text.append(f" [{elapsed_str}]", style=Style(color=SHADOWY_LAVENDER, dim=True))

            table = Table(
                title=title_text,
                title_justify="left",
                box=None,
                show_header=False,
            )
            table.add_column("Label", style=Style(color=SHADOWY_LAVENDER))
            table.add_column("Value")

            status = derive_dataframe_run_status(run)
            attempt = latest_attempt(run)
            table.add_row("Status", _status_renderable(status))
            table.add_row("Operation", Text(operation_id, style=Style(color=SHADOWY_LAVENDER, dim=True)))
            if run.dashboard_url:
                table.add_row("View", Text(run.dashboard_url, style=Style(color=UNDERLYING_CYAN, underline=True)))

            if attempt and attempt.worker_pod_name:
                table.add_row("Worker", Text(attempt.worker_pod_name, style=Style(color=SHADOWY_LAVENDER)))

            if status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED:
                # Per-attempt first, then run-level (deprecated but still populated
                # by go-api-server from dataframe_runs.meta_data as a final fallback).
                err_text = attempt.error_message if attempt and attempt.error_message else (run.error_message or "")
                if err_text:
                    msg = err_text if len(err_text) <= 200 else err_text[:197] + "…"
                    table.add_row("Error", Text(msg, style=Style(color=SHY_RED)))

            # Surface retry history. Only show when there is more than one attempt
            # so the common single-attempt path stays uncluttered.
            total_attempts = sum(len(s.attempts) for s in run.shards)
            if total_attempts > 1:
                attempts_table = Table(
                    box=None, show_header=True, header_style=Style(color=SHADOWY_LAVENDER, bold=True)
                )
                attempts_table.add_column("#")
                attempts_table.add_column("State")
                attempts_table.add_column("Pod")
                attempts_table.add_column("Started")
                for shard in run.shards:
                    for a in shard.attempts:
                        started = (
                            a.started_at.ToDatetime().isoformat(timespec="seconds") if a.HasField("started_at") else ""
                        )
                        pod = a.worker_pod_name if a.worker_pod_name else ""
                        state_name = _ATTEMPT_STATE_NAMES.get(a.state, str(a.state))
                        attempts_table.add_row(str(a.attempt_idx), state_name, pod, started)
                return Group(table, Text(""), attempts_table)

            return Group(table)

        console = Console()
        start = time.time()
        last_resp = None

        with Live(console=console, refresh_per_second=8) as live:
            while True:
                try:
                    last_resp = self.get_dataframe_job_status(operation_id)
                except Exception as e:
                    live.update(Text(f"[error polling status] {e}", style=Style(color=SHY_RED)))
                    time.sleep(poll_interval)
                    continue

                live.update(_build_display(last_resp.run, time.time() - start))

                if derive_dataframe_run_status(last_resp.run) in _TERMINAL_CODES:
                    break

                time.sleep(poll_interval)

        # Print final summary outside the Live context
        final_status = derive_dataframe_run_status(last_resp.run)
        if final_status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_COMPLETED:
            console.print(Text("✓ DataFrame run completed successfully", style=Style(color=GRASSY_GREEN, bold=True)))
        elif final_status == DataFrameRunStatus.DATA_FRAME_RUN_STATUS_FAILED:
            console.print(Text("✗ DataFrame run failed", style=Style(color=SHY_RED, bold=True)))
        else:
            status_name = _STATUS_NAMES.get(final_status, str(final_status))
            console.print(
                Text(f"✗ DataFrame run ended with status: {status_name}", style=Style(color=SHY_RED, bold=True))
            )

        return last_resp

    def explain_sql(self, sql: str):
        return self._stub_refresher.call_sql_stub(
            lambda x: x.PlanSqlQuery(PlanSqlQueryRequest(query=sql)), _EngineTarget.GRPC_ENGINE
        )

    def get_sql_catalogs(self):
        return self._stub_refresher.call_sql_stub(
            lambda x: x.GetDbCatalogs(GetDbCatalogsRequest()), _EngineTarget.GRPC_ENGINE
        )

    def get_sql_schemas(self, catalog: str | None = None, db_schema_filter_pattern: str | None = None):
        return self._stub_refresher.call_sql_stub(
            lambda x: x.GetDbSchemas(
                GetDbSchemasRequest(catalog=catalog, db_schema_filter_pattern=db_schema_filter_pattern)
            ),
            _EngineTarget.GRPC_ENGINE,
        )

    def get_sql_tables(
        self,
        catalog: str | None = None,
        db_schema_filter_pattern: str | None = None,
        table_name_filter_pattern: str | None = None,
        include_schemas: bool = False,
    ):
        return self._stub_refresher.call_sql_stub(
            lambda x: x.GetTables(
                GetTablesRequest(
                    catalog=catalog,
                    db_schema_filter_pattern=db_schema_filter_pattern,
                    table_name_filter_pattern=table_name_filter_pattern,
                    include_schemas=include_schemas,
                )
            ),
            _EngineTarget.GRPC_ENGINE,
        )

    def execute_plan(self, *, lazy_frame_calls: expr_pb.LogicalExprNode) -> ExecutePlanResponse:
        return self._stub_refresher.call_dataframe_stub(
            lambda x: x.ExecutePlan(ExecutePlanRequest(lazy_frame_calls=lazy_frame_calls)), _EngineTarget.GRPC_ENGINE
        )

    def get_model(
        self,
        name: str,
        version: Optional[int] = None,
    ) -> Union[ModelNamespaceResponse, ModelVersionResponse]:
        """Retrieve a model from the Chalk model registry.

        .. deprecated::
            Use `get_model_namespace` for namespace-level info or `get_model_version`
            to retrieve a version (only a version exposes ``.remote()``).
        """
        if version is None:
            warnings.warn(
                "`get_model` is deprecated. Use `get_model_namespace` for namespace-level info.",
                DeprecationWarning,
                stacklevel=2,
            )
            return self.get_model_namespace(name)
        warnings.warn(
            "`get_model` is deprecated. Use `get_model_version` to retrieve a model version.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_model_version(name, version)

    def get_model_namespace(self, name: str) -> ModelNamespaceResponse:
        """Retrieve namespace-level info for a model.

        Returns a `ModelNamespaceResponse`. This does not expose ``.remote()`` —
        use `get_model_version` to invoke a deployed model.
        """
        try:
            model_resp: GetModelResponse = self._stub_refresher.call_model_stub(
                lambda x: x.GetModel(GetModelRequest(model_name=name))
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not get model. {e.details()}")
        m = model_resp.model
        return ModelNamespaceResponse(
            model_id=m.id,
            model_name=m.model_name,
            description=m.description,
            metadata=ModelSerializer.convert_metadata_from_protobuf(m.metadata),
            created_by=m.created_by,
            created_at=m.created_at.ToDatetime(),
            updated_at=m.updated_at.ToDatetime(),
            archived_at=m.archived_at.ToDatetime(),
            latest_model_version=m.latest_model_version,
        )

    def get_model_version(self, name: str, version: Optional[int] = None) -> ModelVersionResponse:
        """Retrieve a single model version. `version=None` resolves the model's latest version.

        Returns a `DeployedModelVersion` if the version has a scaling
        group, otherwise a `RegisteredModelVersion`.

        ``.remote()`` is available on a DeployedModelVersion.
        """
        from chalk.client._model_remote import ModelNotDeployedError, resolve_scaling_group_web_url

        try:
            if version is None:
                model_resp: GetModelResponse = self._stub_refresher.call_model_stub(
                    lambda x: x.GetModel(GetModelRequest(model_name=name))
                )
                version = model_resp.model.latest_model_version.version
                if not version:
                    raise RuntimeError(f"Model {name!r} has no published versions.")
            model_version_resp: GetModelVersionResponse = self._stub_refresher.call_model_stub(
                lambda x: x.GetModelVersion(GetModelVersionRequest(model_name=name, version=version))
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not get model version. {e.details()}")

        mv = model_version_resp.model_version
        artifact = _model_artifact_spec_from_proto(mv.model_artifact)
        input_features = list(mv.model_artifact.spec.input_features)
        if not input_features and isinstance(artifact.input_schema, dict):
            # Image-only models declare their inputs via the schema, not input_features.
            input_features = list(artifact.input_schema.keys())
        common: Dict[str, Any] = dict(
            model_id=mv.id,
            model_name=mv.model_name,
            version=mv.version,
            created_by=mv.created_by,
            created_at=mv.created_at.ToDatetime(),
            model_artifact=artifact,
            input_features=input_features,
            output_features=list(mv.model_artifact.spec.output_features),
        )
        try:
            web_url = resolve_scaling_group_web_url(self, name, version=mv.version)
        except ModelNotDeployedError:
            return RegisteredModelVersion(**common)
        return DeployedModelVersion(_client=self, _web_url=web_url, **common)

    def register_model_namespace(
        self,
        name: str,
        description: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> RegisterModelResponse:
        """
        Register a model namespace in the Chalk model registry.

        Parameters
        ----------
        name : str
            Unique name for the model
        description : str
            Description of the model's purpose and functionality
        metadata : Mapping[str, Any], optional
            Additional metadata dictionary containing framework info,
            training details, performance metrics, etc.

        Returns
        -------
        RegisterModelResponse
            The response object from the model registration

        Examples
        --------
        Register a new model:

        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> client.register_model_namespace(
        ...     name="RiskModel",
        ...     description="Credit risk assessment model using transaction history",
        ...     metadata={
        ...         "accuracy": 0.94,
        ...         "training_date": "2024-01-15"
        ...     }
        ... )
        """

        metadata_converted = ModelSerializer.convert_metadata_to_protobuf(metadata)

        try:
            resp: CreateModelResponse = self._stub_refresher.call_model_stub(
                lambda x: x.CreateModel(
                    CreateModelRequest(
                        model_name=name,
                        description=description,
                        metadata=metadata_converted,
                    )
                )
            )
            return RegisterModelResponse(
                model_id=resp.model.id,
                model_name=resp.model.model_name,
                description=resp.model.description,
                metadata=dict(resp.model.metadata),
                created_by=resp.model.created_by,
                created_at=resp.model.created_at.ToDatetime(),
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not register model. {e.details()}")

    def delete_model_namespace(
        self,
        name: str,
    ) -> ModelNamespaceResponse:
        """Delete a model namespace (and all its versions) from the registry.

        Artifact data for those versions is permanently deleted from storage
        (unless still referenced by another version). Returns the archived namespace.

        >>> from chalk.client import ChalkClient
        >>> ChalkClient().delete_model_namespace(name="RiskModel")
        """

        try:
            resp: DeleteModelResponse = self._stub_refresher.call_model_stub(
                lambda x: x.DeleteModel(
                    DeleteModelRequest(
                        model_name=name,
                    )
                )
            )
            return ModelNamespaceResponse(
                model_id=resp.model.id,
                model_name=resp.model.model_name,
                description=resp.model.description,
                metadata=ModelSerializer.convert_metadata_from_protobuf(resp.model.metadata),
                created_by=resp.model.created_by,
                created_at=resp.model.created_at.ToDatetime(),
                updated_at=resp.model.updated_at.ToDatetime(),
                archived_at=resp.model.archived_at.ToDatetime(),
                latest_model_version=resp.model.latest_model_version,
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not delete model. {e.details()}")

    def delete_model_version(
        self,
        name: str,
        version: int,
    ) -> RegisteredModelVersion:
        """Delete a single model version from the registry.

        Artifact data is permanently deleted from storage (unless still referenced
        by another version). Returns the archived version (not callable).

        >>> from chalk.client import ChalkClient
        >>> ChalkClient().delete_model_version(name="RiskModel", version=1)
        """

        try:
            resp: DeleteModelVersionResponse = self._stub_refresher.call_model_stub(
                lambda x: x.DeleteModelVersion(
                    DeleteModelVersionRequest(
                        model_version_key=ModelVersionKey(
                            model_name=name,
                            version=version,
                        )
                    )
                )
            )
            mv = resp.model_version
            return RegisteredModelVersion(
                model_id=mv.id,
                model_name=mv.model_name,
                version=mv.version,
                created_by=mv.created_by,
                created_at=mv.created_at.ToDatetime(),
                model_artifact=_model_artifact_spec_from_proto(mv.model_artifact),
                input_features=list(mv.model_artifact.spec.input_features),
                output_features=list(mv.model_artifact.spec.output_features),
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not delete model version. {e.details()}")

    def _get_model_artifact_presigned(self, model_paths: List[str]) -> ModelUploadUrlResponse:
        try:
            resp: GetModelArtifactUploadUrlsResponse = self._stub_refresher.call_model_stub(
                lambda x: x.GetModelArtifactUploadUrls(GetModelArtifactUploadUrlsRequest(file_names=model_paths))
            )
            return ModelUploadUrlResponse(
                upload_urls=dict(resp.upload_urls),
                model_artifact_id=resp.model_artifact_id,
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not get presigned URLs for file upload: {e.details()}")

    def register_model_version(
        self,
        name: str,
        model_type: Optional[ModelType] = None,
        model_class: Optional[ModelClass] = None,
        model_encoding: Optional[ModelEncoding] = None,
        aliases: Optional[List[str]] = None,
        model: Optional[Any] = None,
        model_paths: Optional[List[str]] = None,
        additional_files: Optional[List[str]] = None,
        input_schema: Optional[Any] = None,
        output_schema: Optional[Any] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        input_features: Optional[list[str]] = None,
        output_features: Optional[list[str]] = None,
        source_config: Optional[SourceConfig] = None,
        dependencies: Optional[List[str]] = None,
        model_image: Optional[Union[str, Any]] = None,
        skip_volume_upload: bool = False,
    ) -> RegisterModelVersionResponse:
        """Register a model in the Chalk model registry.

        Parameters
        ----------
        name
            Unique name for the model.
        model_image
            Docker image for model serving. Can be a string URI (e.g. ``"ghcr.io/org/image:tag"``)
            or a ``chalkcompute.Image`` object (built at deploy time). May be combined with
            ``model=`` or ``model_paths=``: the image serves, and the model is serialized onto a
            volume mounted at ``CHALK_HANDLER_ARTIFACT_PATH`` for the image's handler to load.
            If provided, the model can be deployed to a scaling group via deploy_scaling_group().
        aliases
            List of version aliases (e.g., `["v1.0", "latest"]`).
        model
            Python model object (for object-based registration).
        model_paths
            Paths to model files (for file-based registration).
        additional_files
            Additional files needed for inference (tokenizers, configs, etc.)
        model_type
            Type of model framework.
        model_class
            Task the model solves.
        model_encoding
            Serialization format.
        input_schema
            Definition of the input schema. Can be:
            - `dict`: Dictionary mapping column names to dtypes for tabular data
            - `list`: List of `(shape, dtype)` tuples for tensor data
        output_schema
            Definition of the output schema. Can be:
            - `dict`: Dictionary mapping column names to dtypes for tabular data
            - `list`: List of `(shape, dtype)` tuples for tensor data
        metadata
            Additional metadata dictionary containing framework info,
            training details, performance metrics, etc.
        input_features
            The features to be used as inputs to the model.
            For example, `[User.message]`. Features can also be expressed as snakecased strings,
            e.g. `["user.message"]`.
        output_features
            The features to be used as outputs to the model.
            For example, `[User.is_spam]`. Features can also be expressed as snakecased strings,
            e.g. `["user.is_spam"]`.
        source_config
            Config to pass credentials to access files from a remote source.
        dependencies
            List of package dependencies needed to run this model.

        Returns
        -------
        ModelVersion
           The registered model version object

        Examples
        --------

        Register from Python object (for engine deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model=trained_pytorch_model,
        ...     model_type=ModelType.PYTORCH,
        ... )

        Register from local files (for engine deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model_paths=["./model.pth"],
        ...     model_type=ModelType.PYTORCH,
        ...     input_schema={"content": pa.large_string()},
        ...     output_schema={"prob": pa.float64()},
        ... )

        Register with a Docker image (for scaling group deployment):

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="ner-model",
        ...     input_schema={"text": pa.large_string()},
        ...     output_schema={"entities": pa.large_string()},
        ...     model_image="ghcr.io/my-org/ner-model:latest",
        ... )

        Register from a `@model_handler`-decorated class (one-call deploy):

        >>> from chalk.client import ChalkClient
        >>> from chalk.ml import model_handler
        >>> import pyarrow as pa
        >>> @model_handler
        ... class RFModel:
        ...     def handler(self, input: pa.RecordBatch) -> pa.RecordBatch:
        ...         preds = self.model.predict(input.to_pandas())
        ...         return pa.RecordBatch.from_arrays([pa.array(preds)], names=["prediction"])
        ...
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="rf",
        ...     model=RFModel(model=trained_rf, files=["./scaler.pkl"]),
        ... )

        The framework is auto-inferred from ``trained_rf``; chalkpy deserializes
        it into ``self.model`` before ``handler`` runs. ``self.files["scaler.pkl"]``
        resolves to a ``Path`` inside the deployed container. ``input_schema``
        and ``output_schema`` are inferred from the wrapped model when
        possible (sklearn, PyTorch, XGBoost, CatBoost); pass them explicitly
        if your framework isn't supported by auto-inference or you want to
        override the inferred shape:

        >>> client.register_model_version(
        ...     name="rf",
        ...     model=RFModel(model=trained_rf),
        ...     input_schema={"feature1": pa.float64(), "feature2": pa.float64()},
        ...     output_schema={"prediction": pa.float64()},
        ... )

        """
        if is_model_handler(model):
            if additional_files:
                raise ValueError(
                    "Pass artifact files via the `files=` argument on your @model_handler class, not `additional_files=` on register_model_version."
                )
            if model_paths:
                raise ValueError(
                    "`model_paths=` is not used when `model` is a @model_handler instance. Pass file paths via the instance's `files=` argument."
                )
            if model_image is not None:
                raise ValueError(
                    "`model_image=` cannot be combined with a @model_handler instance. chalkpy builds the image for you from the decorated class."
                )
            staged = stage_chalk_model_handler_image(
                handler_instance=model,
                model_type=model_type,
                dependencies=list(dependencies or []),
            )
            artifact_uploads = staged.artifact_uploads
            owned_tmp_paths = staged.owned_tmp_paths
            if input_schema is None and staged.inferred_input_schema is not None:
                input_schema = staged.inferred_input_schema
            if output_schema is None and staged.inferred_output_schema is not None:
                output_schema = staged.inferred_output_schema
            image_spec_bytes = serialize_image_spec(staged.image)
            try:
                artifact_basenames = [basename for _, basename in artifact_uploads] if artifact_uploads else []
                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned(
                    model_paths=artifact_basenames
                )

                uploaded_model_files: List[_model_artifact_pb2.ModelFile] = []
                if artifact_uploads:
                    model_file_uploader = ModelFileUploader(source_config=None)
                    file_paths = {basename: local_path for local_path, basename in artifact_uploads}
                    dir_allowlist = [local_path for local_path, _ in artifact_uploads]
                    model_files_info, _ = model_file_uploader.upload_files(
                        file_paths,
                        model_file_names=artifact_basenames,
                        presigned_urls=presigned_s3_response.upload_urls,
                        dir_allowlist=dir_allowlist,
                    )
                    uploaded_model_files = [ModelSerializer.fileinfo_to_protobuf(f) for f in model_files_info]

                volume_name: Optional[str] = None
                if artifact_uploads and not skip_volume_upload:
                    volume_name = self._try_upload_to_volume(
                        model_artifact_volume_name(name, presigned_s3_response.model_artifact_id),
                        artifact_uploads,
                    )
                response = self._submit_model_version(
                    name=name,
                    model_image=None,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    aliases=aliases,
                    metadata=metadata,
                    model_artifact_id=presigned_s3_response.model_artifact_id,
                    model_volume=volume_name,
                    model_files=uploaded_model_files,
                    image_spec=image_spec_bytes,
                )
                return response
            finally:
                for p in owned_tmp_paths:
                    try:
                        os.unlink(p)
                    except OSError:
                        pass

        image_spec: Optional[bytes] = None
        image_additional_files: List[_model_artifact_pb2.ModelFile] = []
        image_artifact_id: Optional[str] = None
        if model_image is not None and not isinstance(model_image, str):
            if model is not None or model_paths:
                return self._register_image_and_model(
                    name=name,
                    image=model_image,
                    model=model,
                    model_paths=model_paths,
                    model_type=model_type,
                    model_encoding=model_encoding,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    aliases=aliases,
                    metadata=metadata,
                    source_config=source_config,
                    skip_volume_upload=skip_volume_upload,
                )
            image_spec = serialize_image_spec(model_image)
            image_additional_files, image_artifact_id = self._upload_image_local_files(model_image)
            model_image = None

        if (model_image is not None or image_spec is not None) and model is None and model_paths is None:
            # Image-only registration (for scaling group deployment)
            return self._submit_model_version(
                name=name,
                model_image=model_image,
                input_schema=input_schema,
                output_schema=output_schema,
                aliases=aliases,
                metadata=metadata,
                model_artifact_id=image_artifact_id,
                additional_files=image_additional_files,
                image_spec=image_spec,
            )
        else:
            # Engine deployment path (model serialization)
            return self._register_model_for_engine(
                name=name,
                model_type=model_type,
                model_class=model_class,
                model_encoding=model_encoding,
                model=model,
                model_paths=model_paths,
                additional_files=additional_files,
                input_schema=input_schema,
                output_schema=output_schema,
                metadata=metadata,
                input_features=input_features,
                output_features=output_features,
                source_config=source_config,
                dependencies=dependencies,
                aliases=aliases,
                model_image=model_image,
                skip_volume_upload=skip_volume_upload,
            )

    def _try_upload_to_volume(
        self,
        volume_name: str,
        uploads: List[Tuple[str, str]],
    ) -> Optional[str]:
        """Upload artifacts to a volume, returning the volume name on success or None if volumes aren't configured."""
        try:
            upload_chalk_handler_artifacts(
                volume_name=volume_name,
                uploads=uploads,
                chalk_client=self,
            )
            return volume_name
        except ImportError:
            chalk_logger.info("Volume upload skipped: chalkcompute is not installed")
            return None
        except Exception as e:
            try:
                from chalkcompute import VolumeError  # pyright: ignore[reportMissingImports]
            except ImportError:
                raise e

            if isinstance(e, VolumeError):
                cause = e.__cause__
                native_code = cause.args[0] if cause and cause.args else ""
                if native_code in ("failed_precondition", "unavailable"):
                    chalk_logger.warning(f"Volume upload skipped: volumes not configured ({e})")
                    return None
            raise

    def _upload_image_local_files(self, image: Any) -> Tuple[List[_model_artifact_pb2.ModelFile], Optional[str]]:
        """Upload an Image's strategy='volume' files as additional_files carrying mount_path/mode.

        Returns (additional_files, model_artifact_id); the id ties the uploads to the registration.
        """
        triples = image_local_files(image)
        if not triples:
            return [], None
        from chalk.client.serialization.model_serialization import ModelSerializer
        from chalk.ml.model_file_transfer import ModelFileUploader

        file_paths: Dict[str, str] = {}
        meta: Dict[str, Tuple[str, Optional[int]]] = {}
        for i, (src, dest, mode) in enumerate(triples):
            upload_name = f"{i}_{os.path.basename(dest)}"
            file_paths[upload_name] = src
            meta[upload_name] = (dest, mode)

        presigned = self._get_model_artifact_presigned(model_paths=list(file_paths.keys()))
        _, additional = ModelFileUploader(source_config=None).upload_files(
            file_paths,
            model_file_names=[],
            presigned_urls=presigned.upload_urls,
            dir_allowlist=list(file_paths.values()),
        )
        files: List[_model_artifact_pb2.ModelFile] = []
        for info in additional:
            mf = ModelSerializer.fileinfo_to_protobuf(info)
            dest, mode = meta[mf.name]
            mf.mount_path = dest
            if mode is not None:
                mf.mode = mode
            files.append(mf)
        return files, presigned.model_artifact_id

    def _download_image_local_files(
        self, model_name: str, model_version: int, mount_files: List[_model_artifact_pb2.ModelFile]
    ) -> List[Tuple[str, str, Optional[int]]]:
        """Download additional_files carrying mount_path as (local_path, mount_path, mode) triples.

        Fetches the additional-file URLs directly rather than via download_model_artifact, which
        assumes a serialized model (its model_type conversion fails on a chalkcompute image artifact).
        """

        resp: DownloadModelArtifactResponse = self._stub_refresher.call_model_stub(
            lambda x: x.DownloadModelArtifact(
                DownloadModelArtifactRequest(
                    model_version_key=ModelVersionKey(model_name=model_name, version=model_version)
                )
            )
        )
        tmpdir = tempfile.mkdtemp(prefix="chalk-image-files-")
        ordered: List[str] = []
        by_name: Dict[str, str] = {}
        for item in resp.additional_file_urls:
            base = os.path.basename(urlparse(item).path.rstrip("/")) or f"file_{len(ordered)}"
            local = os.path.join(tmpdir, base)
            r = requests.get(item, stream=True)
            r.raise_for_status()
            with open(local, "wb") as fh:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        fh.write(chunk)
            by_name[base] = local
            ordered.append(local)

        out: List[Tuple[str, str, Optional[int]]] = []
        for i, f in enumerate(mount_files):
            local = by_name.get(f.name) or (ordered[i] if i < len(ordered) else None)
            if local is None:
                raise RuntimeError(f"deploy: could not locate downloaded file for {f.name!r}")
            out.append((local, f.mount_path, f.mode if f.HasField("mode") else None))
        return out

    def _register_image_and_model(
        self,
        name: str,
        image: Any,
        model: Optional[Any],
        model_paths: Optional[List[str]],
        model_type: Optional[ModelType],
        model_encoding: Optional[ModelEncoding],
        input_schema: Optional[Any],
        output_schema: Optional[Any],
        aliases: Optional[List[str]],
        metadata: Optional[Mapping[str, Any]],
        source_config: Optional[SourceConfig],
        skip_volume_upload: bool,
    ) -> RegisterModelVersionResponse:
        """Register a deferred-build custom ``Image`` together with a serialized model.

        Image and model files share one ``model_artifact_id`` so the image files stay
        reachable via ``DownloadModelArtifact`` at deploy.
        """
        from chalk.client.serialization.model_serialization import ModelSerializer
        from chalk.ml.model_file_transfer import ModelFileUploader

        image_spec = serialize_image_spec(image)
        image_triples = image_local_files(image)  # (src, dest, mode)

        owned_dirs: List[str] = []
        resolved_type: Optional[ModelType] = model_type
        resolved_encoding: Optional[ModelEncoding] = model_encoding
        try:
            if model is not None:
                if model_paths:
                    raise ValueError("Pass either `model=` or `model_paths=` with a model_image, not both.")
                with ModelSerializer.from_model(model, model_type) as ser:
                    resolved_type = model_type if model_type is not None else ser.model_type
                    if resolved_type is None:
                        raise ValueError("Could not determine the model type; pass model_type= explicitly.")
                    if input_schema is None or output_schema is None:
                        inferred_in, inferred_out = ser.infer_input_output_schemas(model, resolved_type)
                        input_schema = input_schema if input_schema is not None else inferred_in
                        output_schema = output_schema if output_schema is not None else inferred_out
                    serialized, resolved_encoding = ser.serialize_model(model, resolved_type)
                    # ModelSerializer deletes its temp dir on __exit__; copy the artifact into
                    # a dir we own (cleaned up in finally) before the context closes.
                    stage_dir = tempfile.mkdtemp(prefix="chalk-img-model-")
                    tmp_path = os.path.join(stage_dir, os.path.basename(serialized))
                    shutil.copyfile(serialized, tmp_path)
                owned_dirs.append(stage_dir)
                model_file_paths = [tmp_path]
            else:
                model_file_paths = list(model_paths or [])

            # One presigned batch so image files + model files share one artifact id.
            image_names = [f"{i}_{os.path.basename(dest)}" for i, (_s, dest, _m) in enumerate(image_triples)]
            model_names = [os.path.basename(p) for p in model_file_paths]
            presigned = self._get_model_artifact_presigned(model_paths=image_names + model_names)

            file_paths: Dict[str, str] = {}
            for upload_name, (src, _dest, _mode) in zip(image_names, image_triples):
                file_paths[upload_name] = src
            for upload_name, path in zip(model_names, model_file_paths):
                file_paths[upload_name] = path

            model_infos, additional_infos = ModelFileUploader(source_config).upload_files(
                file_paths,
                model_file_names=model_names,
                presigned_urls=presigned.upload_urls,
                dir_allowlist=list(file_paths.values()),
            )

            model_files = [ModelSerializer.fileinfo_to_protobuf(info) for info in model_infos]
            dest_by_name = {nm: (dest, mode) for nm, (_s, dest, mode) in zip(image_names, image_triples)}
            additional_files: List[_model_artifact_pb2.ModelFile] = []
            for info in additional_infos:
                mf = ModelSerializer.fileinfo_to_protobuf(info)
                dest, mode = dest_by_name[mf.name]
                mf.mount_path = dest
                if mode is not None:
                    mf.mode = mode
                additional_files.append(mf)

            model_volume: Optional[str] = None
            if not skip_volume_upload:
                model_uploads = [(path, os.path.basename(path)) for path in model_file_paths]
                model_volume = self._try_upload_to_volume(
                    model_artifact_volume_name(name, presigned.model_artifact_id),
                    model_uploads,
                )

            return self._submit_model_version(
                name=name,
                model_image=None,
                input_schema=input_schema,
                output_schema=output_schema,
                aliases=aliases,
                metadata=metadata,
                model_artifact_id=presigned.model_artifact_id,
                model_volume=model_volume,
                model_files=model_files,
                additional_files=additional_files,
                image_spec=image_spec,
                model_type=resolved_type,
                model_encoding=resolved_encoding,
            )
        finally:
            for d in owned_dirs:
                shutil.rmtree(d, ignore_errors=True)

    def _submit_model_version(
        self,
        name: str,
        model_image: Optional[str],
        input_schema: Optional[Any],
        output_schema: Optional[Any],
        aliases: Optional[List[str]],
        metadata: Optional[Mapping[str, Any]],
        model_artifact_id: Optional[str] = None,
        model_volume: Optional[str] = None,
        model_files: Optional[List[_model_artifact_pb2.ModelFile]] = None,
        image_spec: Optional[bytes] = None,
        additional_files: Optional[List[_model_artifact_pb2.ModelFile]] = None,
        model_type: Optional[ModelType] = None,
        model_encoding: Optional[ModelEncoding] = None,
    ) -> RegisterModelVersionResponse:
        """Register a model with a serving image (prebuilt ``model_image`` URI or deferred ``image_spec``)."""
        if input_schema is None:
            raise ValueError(
                "input_schema is required when registering with a model_image."
                + ' Pass it as a dict (e.g. `input_schema={"feature": pa.float64()}`)'
                + " or a list of (shape, dtype) tuples for tensor inputs."
                + " If you wrapped a @model_handler around a Python model, chalkpy"
                + " attempted to infer the schema from the wrapped object — pass"
                + " input_schema explicitly if your framework isn't supported by"
                + " auto-inference (currently ONNX, LightGBM, and TensorFlow have no introspector)."
            )
        if output_schema is None:
            raise ValueError(
                "output_schema is required when registering with a model_image."
                + ' Pass it as a dict (e.g. `output_schema={"prediction": pa.float64()}`)'
                + " or a list of (shape, dtype) tuples for tensor outputs."
            )

        from chalk.client.serialization.model_serialization import ModelSerializer

        metadata_converted = None
        if metadata is not None:
            metadata_converted = ModelSerializer.convert_metadata_to_protobuf(metadata)

        try:
            if model_artifact_id is None:
                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned(model_paths=[])
                model_artifact_id = presigned_s3_response.model_artifact_id

            input_model_schema = ModelSerializer.convert_schema(input_schema)
            output_model_schema = ModelSerializer.convert_schema(output_schema)

            artifact_spec = _model_artifact_pb2.ModelArtifactSpec(
                model_files=model_files or [],
                additional_files=additional_files or [],
                model_signature=_model_artifact_pb2.ModelSignature(
                    inputs=input_model_schema,
                    outputs=output_model_schema,
                ),
                model_volume=model_volume,
                model_type=model_type,
                model_encoding=model_encoding,
            )
            if model_image:
                artifact_spec.model_image = model_image
            if image_spec is not None:
                artifact_spec.image_spec = image_spec

            resp: CreateModelVersionResponse = self._stub_refresher.call_model_stub(
                lambda x: x.CreateModelVersion(
                    CreateModelVersionRequest(
                        model_name=name,
                        model_artifact_id=model_artifact_id,
                        model_artifact=artifact_spec,
                        aliases=aliases,
                        metadata=metadata_converted,
                    )
                )
            )
            return RegisterModelVersionResponse(
                model_id=resp.model_version.id,
                model_name=resp.model_version.model_name,
                model_version=resp.model_version.version,
                artifact=resp.model_version.model_artifact,
                aliases=list(resp.model_version.aliases),
                created_by=resp.model_version.created_by,
                created_at=resp.model_version.created_at.ToDatetime(),
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not register model version. {e.details()}")

    def _register_model_for_engine(
        self,
        name: str,
        model_type: Optional[ModelType],
        model_class: Optional[ModelClass],
        model_encoding: Optional[ModelEncoding],
        model: Optional[Any],
        model_paths: Optional[List[str]],
        additional_files: Optional[List[str]],
        input_schema: Optional[Any],
        output_schema: Optional[Any],
        metadata: Optional[Mapping[str, Any]],
        input_features: Optional[list[str]],
        output_features: Optional[list[str]],
        source_config: Optional[SourceConfig],
        dependencies: Optional[List[str]],
        aliases: Optional[List[str]],
        model_image: Optional[str] = None,
        skip_volume_upload: bool = False,
    ) -> RegisterModelVersionResponse:
        """Register a model for engine deployment (with model serialization)."""
        with ModelSerializer.from_model(model, model_type) as model_serializer:
            model_file_uploader = ModelFileUploader(source_config)

            if model_type is None:
                model_type = model_serializer.model_type

            if model_class is None:
                model_class = model_serializer.model_class

            if model is not None:
                inferred_input_schema, inferred_output_schema = model_serializer.infer_input_output_schemas(
                    model, model_type
                )
                if input_schema is None and inferred_input_schema is not None:
                    input_schema = inferred_input_schema
                if output_schema is None and inferred_output_schema is not None:
                    output_schema = inferred_output_schema

                if dependencies is None:
                    dependencies = model_serializer.get_dependencies()

            if input_schema is None:
                raise ValueError("You must specify an input_schema to register a model version.")
            if output_schema is None:
                raise ValueError("You must specify an output_schema to register a model version.")

            try:
                dir_allowlist: List[str] = []
                metadata_converted = model_serializer.convert_metadata_to_protobuf(metadata)

                if model_paths is None:
                    if model is None:
                        raise ValueError("Failed to register model. Please specify a model or model_paths.")

                    assert model_type is not None, "Unable to determine Model Type, please set parameter model_type."

                    tmp_path, model_encoding = model_serializer.serialize_model(model, model_type)
                    model_paths = [tmp_path]
                    dir_allowlist.append(tmp_path)
                else:
                    if model is not None:
                        raise ValueError(
                            "Failed to register model. Ambiguous model, can't specify both model_paths and model."
                        )
                    if model_encoding is None:
                        raise ValueError(
                            "Failed to register model. Please specify a model encoding if using model_paths."
                        )

                # Auto-convert ONNX list schemas to dict format if needed
                if model_type == ModelType.ONNX:
                    input_schema = model_serializer.convert_onnx_list_schema_to_dict(input_schema, model, is_input=True)
                    output_schema = model_serializer.convert_onnx_list_schema_to_dict(
                        output_schema, model, is_input=False
                    )

                input_model_schema = model_serializer.convert_schema(input_schema)
                output_model_schema = model_serializer.convert_schema(output_schema)

                # Final validation: ONNX models must use tabular schemas
                if model_type == ModelType.ONNX:
                    if input_model_schema is not None and not input_model_schema.HasField("tabular"):
                        raise ValueError(
                            "ONNX models must be registered with tabular input schema (dict format). "
                            + "Use dict format like {'input': Tensor[...]} instead of list format."
                        )
                    if output_model_schema is not None and not output_model_schema.HasField("tabular"):
                        raise ValueError(
                            "ONNX models must be registered with tabular output schema (dict format). "
                            + "Use dict format like {'output': Vector[...]} instead of list format."
                        )

                all_files_to_process, model_file_names = model_file_uploader.prepare_file_mapping(
                    model_paths, additional_files
                )

                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned(
                    model_paths=list(all_files_to_process.keys())
                )

                model_upload_paths, additional_files_upload_paths = model_file_uploader.upload_files(
                    all_files_to_process,
                    model_file_names,
                    presigned_s3_response.upload_urls,
                    dir_allowlist,
                )

                volume_name: Optional[str] = None
                if not skip_volume_upload:
                    volume_uploads = [(local_path, filename) for filename, local_path in all_files_to_process.items()]
                    volume_name = self._try_upload_to_volume(
                        model_artifact_volume_name(name, presigned_s3_response.model_artifact_id),
                        volume_uploads,
                    )

                try:
                    resp: CreateModelVersionResponse = self._stub_refresher.call_model_stub(
                        lambda x: x.CreateModelVersion(
                            CreateModelVersionRequest(
                                model_name=name,
                                model_artifact_id=presigned_s3_response.model_artifact_id,
                                model_artifact=_model_artifact_pb2.ModelArtifactSpec(
                                    model_files=[
                                        model_serializer.fileinfo_to_protobuf(file) for file in model_upload_paths
                                    ],
                                    additional_files=[
                                        model_serializer.fileinfo_to_protobuf(file)
                                        for file in additional_files_upload_paths
                                    ],
                                    model_type=model_type,
                                    model_class=model_class,
                                    model_encoding=model_encoding,
                                    model_signature=_model_artifact_pb2.ModelSignature(
                                        inputs=input_model_schema,
                                        outputs=output_model_schema,
                                    ),
                                    input_features=input_features,
                                    output_features=output_features,
                                    python_dependencies=dependencies,
                                    model_image=model_image,
                                    model_volume=volume_name,
                                ),
                                aliases=aliases,
                                metadata=metadata_converted,
                            )
                        )
                    )
                    return RegisterModelVersionResponse(
                        model_id=resp.model_version.id,
                        model_name=resp.model_version.model_name,
                        model_version=resp.model_version.version,
                        artifact=resp.model_version.model_artifact,
                        aliases=list(resp.model_version.aliases),
                        created_by=resp.model_version.created_by,
                        created_at=resp.model_version.created_at.ToDatetime(),
                    )
                except grpc.RpcError as e:
                    raise RuntimeError(f"Could not register model version. {e.details()}")
            except Exception as e:
                raise RuntimeError(f"Could not register model version. {e}")
        raise RuntimeError("Error creating model serializer context to register model version.")

    def download_model_artifact(
        self,
        name: str,
        version: int,
        download_dir: Optional[str] = None,
    ) -> DownloadModelArtifactResult:
        try:
            resp: DownloadModelArtifactResponse = self._stub_refresher.call_model_stub(
                lambda x: x.DownloadModelArtifact(
                    DownloadModelArtifactRequest(model_version_key=ModelVersionKey(model_name=name, version=version))
                )
            )

            base_dir = download_dir or "."
            target_dir = os.path.join(base_dir, f"{name}-{version}")
            os.makedirs(target_dir, exist_ok=True)

            downloaded_model_files: List[str] = []
            downloaded_additional_files: List[str] = []

            def _filename_from_url(u: str, suffix: str) -> str:
                parsed = urlparse(u)
                base = os.path.basename(parsed.path.rstrip("/"))
                return base or f"artifact_{suffix}"

            def _download_file(url: str, local_path: str) -> None:
                if os.path.exists(local_path):
                    return

                with open(local_path, "wb") as f:
                    r = requests.get(url, stream=True)
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            for idx, item in enumerate(list(resp.model_urls)):
                parsed = urlparse(item)
                scheme = parsed.scheme

                if scheme in ("http", "https"):
                    local_path = os.path.join(target_dir, _filename_from_url(item, f"model_file_{idx}"))
                    _download_file(item, local_path)
                    downloaded_model_files.append(local_path)
                    continue

                raise RuntimeError(f"Unsupported url scheme: {scheme} ({item})")

            for idx, item in enumerate(list(resp.additional_file_urls)):
                parsed = urlparse(item)
                scheme = parsed.scheme

                if scheme in ("http", "https"):
                    local_path = os.path.join(target_dir, _filename_from_url(item, f"additional_file_{idx}"))
                    _download_file(item, local_path)
                    downloaded_additional_files.append(local_path)
                    continue

                raise RuntimeError(f"Unsupported url scheme: {scheme} ({item})")

            model_artifact = ModelArtifactSpec(
                model_type=model_type_from_proto(resp.model_artifact.spec.model_type),
                model_class=model_class_from_proto(resp.model_artifact.spec.model_class),
                model_encoding=model_encoding_from_proto(resp.model_artifact.spec.model_encoding),
                model_files=[file.name for file in resp.model_artifact.spec.model_files],
                additional_files=[file.name for file in resp.model_artifact.spec.additional_files],
                input_schema=ModelSerializer.convert_schema_from_protobuf(
                    resp.model_artifact.spec.model_signature.inputs
                ),
                output_schema=ModelSerializer.convert_schema_from_protobuf(
                    resp.model_artifact.spec.model_signature.outputs
                ),
                metadata=ModelSerializer.convert_metadata_from_protobuf(resp.model_artifact.metadata),
                input_features=list(resp.model_artifact.spec.input_features),
                output_features=list(resp.model_artifact.spec.output_features),
                dependencies=list(resp.model_artifact.spec.python_dependencies),
            )

            return DownloadModelArtifactResult(
                model_name=name,
                model_version=version,
                model_artifact=model_artifact,
                downloaded_model_files=downloaded_model_files,
                downloaded_additional_files=downloaded_additional_files,
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not download model artifact: {e.details()}")
        except Exception as e:
            raise RuntimeError(f"Could not download model artifact: {e}")

    def _upload_model_artifact(
        self,
        model: Any,
        additional_files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RegisterModelArtifactResponse:
        with ModelSerializer.from_model(model) as model_serializer:
            try:
                dir_allowlist: List[str] = []
                model_tmp_path, model_encoding = model_serializer.serialize()
                dir_allowlist.append(model_tmp_path)

                model_file_uploader = ModelFileUploader(LocalSourceConfig())

                all_files_to_process, model_file_names = model_file_uploader.prepare_file_mapping(
                    [model_tmp_path], additional_files
                )

                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned(
                    model_paths=list(all_files_to_process.keys())
                )

                metadata_converted = model_serializer.convert_metadata_to_protobuf(metadata)

                input_schema, output_schema = model_serializer.infer_input_output_schemas()

                input_model_schema = model_serializer.convert_schema(input_schema)
                output_model_schema = model_serializer.convert_schema(output_schema)

                model_upload_paths, additional_files_upload_paths = model_file_uploader.upload_files(
                    file_paths=all_files_to_process,
                    model_file_names=model_file_names,
                    presigned_urls=presigned_s3_response.upload_urls,
                    dir_allowlist=dir_allowlist,
                )

                dependencies = model_serializer.get_dependencies()
                try:
                    resp: CreateModelArtifactResponse = self._stub_refresher.call_model_stub(
                        lambda x: x.CreateModelArtifact(
                            CreateModelArtifactRequest(
                                model_artifact_id=presigned_s3_response.model_artifact_id,
                                model_artifact=_model_artifact_pb2.ModelArtifactSpec(
                                    model_files=[
                                        model_serializer.fileinfo_to_protobuf(file) for file in model_upload_paths
                                    ],
                                    additional_files=[
                                        model_serializer.fileinfo_to_protobuf(file)
                                        for file in additional_files_upload_paths
                                    ],
                                    model_type=model_serializer.model_type,
                                    model_class=model_serializer.model_class,
                                    model_encoding=model_encoding,
                                    model_signature=_model_artifact_pb2.ModelSignature(
                                        inputs=input_model_schema,
                                        outputs=output_model_schema,
                                    ),
                                    input_features=[],
                                    output_features=[],
                                    python_dependencies=dependencies,
                                ),
                                metadata=metadata_converted,
                            )
                        )
                    )
                    return RegisterModelArtifactResponse(
                        artifact_id=resp.model_artifact.id,
                        path=resp.model_artifact.path,
                        spec=resp.model_artifact.spec,
                        metadata=dict(resp.model_artifact.metadata),
                        created_by=resp.model_artifact.created_by,
                        created_at=resp.model_artifact.created_at.ToDatetime(),
                    )
                except grpc.RpcError as e:
                    raise RuntimeError(f"Could not register model artifact. {e.details()}")
            except Exception as e:
                raise RuntimeError(f"Could not register model artifact. {e}")
        raise RuntimeError("Error creating model serializer context to create model artifact.")

    def promote_model_artifact(
        self,
        name: str,
        model_artifact_id: Optional[str] = None,
        run_id: Optional[str] = None,
        run_name: Optional[str] = None,
        criterion: Optional[ModelRunCriterion] = None,
        aliases: Optional[List[str]] = None,
    ) -> RegisterModelVersionResponse:
        """
        Register a model in the Chalk model registry.

        Parameters
        ----------
        name : str
            Name of the model namespace to promote into.
        model_artifact_id: str, optional
            Artifact UUID to promote to a model version.
        run_id: str, optional
            run id that produce the artifact to promote.
        run_name: str, optional
            run name used in the checkpointer for artifact to promote.
        criterion: ModelRunCriterion, optional
            criterion on which to select the artifact from the training run.
            If none provided, the latest artifact in the run will be selected.
        aliases: list of str, optional
            List of version aliases (e.g., ["v1.0", "latest"])

        Example
        --------
        Register from Python object:

        >>> client.promote_model_artifact(
        ...     name="RiskModel",
        ...     model_artifact_id=model_artifact_id,
        ...     aliases=["latest"],
        ... )
        """
        if model_artifact_id is not None:
            if run_id is not None or criterion is not None or run_name is not None:
                raise ValueError(
                    "Please specify only one of 'model_artifact_id', (run_id, run criterion), (run_name, run criterion)"
                )
        else:
            if run_name is None and run_id is None:
                raise ValueError(
                    "Please specify only one of 'model_artifact_id', (run_id, run criterion), (run_name, run criterion)"
                )

        try:
            resp: CreateModelVersionFromArtifactResponse = self._stub_refresher.call_model_stub(
                lambda x: x.CreateModelVersionFromArtifact(
                    CreateModelVersionFromArtifactRequest(
                        model_name=name,
                        model_artifact_id=model_artifact_id,
                        training_run=ModelSerializer.convert_run_criterion_to_proto(
                            run_id=run_id,
                            run_name=run_name,
                            criterion=criterion,
                        ),
                        aliases=aliases,
                    )
                )
            )
            return RegisterModelVersionResponse(
                model_id=resp.model_version.id,
                model_name=resp.model_version.model_name,
                model_version=resp.model_version.version,
                artifact=resp.model_version.model_artifact,
                aliases=list(resp.model_version.aliases),
                created_by=resp.model_version.created_by,
                created_at=resp.model_version.created_at.ToDatetime(),
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not promote model artifact. {e.details()}")

    def create_model_training_job(
        self,
        script: str,
        function_name: str,
        experiment_name: str,
        branch: Optional[str] = None,
        config: str | None = None,
        resources: Optional[ResourceRequests] = None,
        env_overrides: Optional[Mapping[str, str]] = None,
        enable_profiling: bool = False,
        max_retries: int = 0,
    ) -> CreateScriptTaskResponse:
        resources_request = {}
        if resources is not None:
            if resources.cpu is not None:
                resources_request["cpu"] = resources.cpu
            if resources.memory is not None:
                resources_request["memory"] = resources.memory

        return self._stub_refresher.call_task_stub(
            lambda x: x.CreateScriptTask(
                CreateScriptTaskRequest(
                    request=ScriptTaskRequest(
                        function_reference_type="file",
                        # Hardcoded script name
                        function_reference=f"train.py::{function_name}",
                        kind=ScriptTaskKind.SCRIPT_TASK_KIND_TRAINING_RUN,
                        training_run=TrainingRunArgs(
                            experiment_name=experiment_name,
                        ),
                        arguments_json=config,
                        branch=branch,
                        resource_requests=resources_pb2.ResourceRequirements(
                            requests=resources_request,
                        ),
                        resource_group=resources.resource_group if resources is not None else None,
                        env_overrides=env_overrides,
                        enable_profiling=enable_profiling,
                        max_retries=max_retries,
                    ),
                    source_file=script.encode("utf-8"),
                ),
            )
        )

    def await_branch_server_start(
        self,
        timeout_seconds: float = 300.0,
        poll_interval_seconds: float = 2.0,
    ) -> "StartBranchResponse":
        """Start and wait for a branch server to be ready.

        This method polls the branch server status until it is ready or a timeout is reached.
        Both 'apply --branch' and 'query --branch' automatically start the branch server if
        it isn't already running, so it isn't usually necessary to manually start it.

        Parameters
        ----------
        timeout_seconds
            Maximum time to wait for the branch server to start, in seconds. Defaults to 300 (5 minutes).
        poll_interval_seconds
            Time to wait between polling attempts, in seconds. Defaults to 2 seconds.

        Returns
        -------
        StartBranchResponse
            The response from the branch server indicating its state.

        Raises
        ------
        TimeoutError
            If the branch server doesn't start within the timeout period.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> response = client.await_branch_server_start()
        """
        import time

        from chalk._gen.chalk.server.v1.builder_pb2 import BranchScalingState, StartBranchRequest

        start_time = time.time()
        while True:
            response = self._stub_refresher.call_builder_stub(lambda x: x.StartBranch(StartBranchRequest()))
            if response.state == BranchScalingState.BRANCH_SCALING_STATE_SUCCESS:
                return response
            if (time.time() - start_time) >= timeout_seconds:
                raise TimeoutError(
                    f"Branch server did not start within {timeout_seconds} seconds. Last state: {BranchScalingState.Name(response.state)}"
                )
            time.sleep(poll_interval_seconds)

    def get_job_queue_operation_summary(
        self,
        operation_id: str,
        environment_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> GetJobQueueOperationSummaryResponse:
        """Get summary information for a job queue operation.

        Parameters
        ----------
        operation_id
            The ID of the operation to get summary for
        environment_id
            The environment ID. If `None`, uses the client's environment.
        limit
            Maximum number of job rows to return. Defaults to 10000.
        offset
            Offset for pagination. Defaults to 0.

        Returns
        -------
        GetJobQueueOperationSummaryResponse
            The operation summary response containing job queue information.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> response = client.get_job_queue_operation_summary(operation_id="op_123")
        """
        env_id = environment_id or self._stub_refresher.environment_id
        if not env_id:
            raise ValueError("No environment specified")

        request = GetJobQueueOperationSummaryRequest(
            operation_id=operation_id,
            environment_id=env_id,
        )

        if limit is not None:
            request.limit = limit
        if offset is not None:
            request.offset = offset

        return self._stub_refresher.call_job_queue_stub(lambda x: x.GetJobQueueOperationSummary(request))

    def follow_model_training_job(
        self,
        operation_id: str,
        poll_interval: float = 2.0,
        output_callback: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        """Follow a model training job, displaying both status and logs.

        This method polls the job queue for status updates while also following logs
        in real-time. It continues until the job reaches a terminal state (completed,
        failed, or canceled).

        Parameters
        ----------
        operation_id
            The operation ID of the model training job
        poll_interval
            Time in seconds between polling for status and logs. Defaults to 2.0 seconds.
        output_callback
            Optional callback function that receives (timestamp, message) for each log entry.
            If `None`, logs are displayed using Rich live display.

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> client.follow_model_training_job(operation_id="op_123")
        """
        from chalk.utils.job_log_display import JobLogDisplay

        # Create display manager
        display = JobLogDisplay(title="Model Training Jobs")

        # Define callback for status polling
        def get_status_callback():
            return self.get_job_queue_operation_summary(operation_id=operation_id)

        # Get log stub and construct log query
        log_query = f'operation_id:"{operation_id}"'
        log_stub = self._stub_refresher.log_stub

        # Delegate to the display manager to handle all threading and coordination
        display.follow_job(
            get_status_callback=get_status_callback,
            log_stub=log_stub,
            log_query=log_query,
            poll_interval=poll_interval,
            output_callback=output_callback,
        )

    def test_streaming_resolver(
        self,
        resolver: str | Resolver,
        message_bodies: "list[str | bytes | BaseModel] | None" = None,
        message_keys: list[str | None] | None = None,
        message_timestamps: list[str | dt.datetime] | None = None,
        message_filepath: str | None = None,
        request_timeout: Optional[float] = None,
    ) -> "StreamResolverTestResponse":
        """Test a streaming resolver with supplied messages.

        This method tests streaming resolvers using the gRPC TestStreamingResolver endpoint.
        It supports both deployed resolvers (by FQN) and static/undeployed resolvers
        (automatically serialized from Resolver objects).

        Parameters
        ----------
        resolver : str | Resolver
            The streaming resolver or its string name. If a StreamResolver object with
            feature_expressions is provided, it will be automatically serialized for testing.
        message_bodies : list[str | bytes | BaseModel], optional
            The message bodies to process. Can be JSON strings, raw bytes,
            or Pydantic models (will be serialized to JSON).
            Either message_bodies or message_filepath must be provided.
        message_keys : list[str | None], optional
            Optional keys for each message. If not provided, all keys will be None.
            Must match length of message_bodies if provided.
        message_timestamps : list[str | datetime], optional
            Optional timestamps for each message. If not provided, current time
            will be used. Must match length of message_bodies if provided.
        message_filepath : str, optional
            A filepath from which test messages will be ingested.
            This file should be newline delimited JSON with format:
            {"message_key": "my-key", "message_body": {"field1": "value1"}}
            Each line may optionally contain a "message_timestamp" field.
            Either message_bodies or message_filepath must be provided.
        request_timeout : float, optional
            Request timeout in seconds.

        Returns
        -------
        StreamResolverTestResponse
            Response containing:
            - status: SUCCESS or FAILURE
            - data_uri: Optional signed URL to parquet file with results
            - errors: List of ChalkError objects
            - message: Human-readable message

        Examples
        --------
        >>> from chalk.client.client_grpc import ChalkGRPCClient
        >>> client = ChalkGRPCClient()
        >>> response = client.test_streaming_resolver(
        ...     resolver="my_module.my_stream_resolver",
        ...     message_bodies=[
        ...         '{"user_id": 1, "event": "login"}',
        ...         '{"user_id": 2, "event": "logout"}',
        ...     ],
        ...     message_keys=["user_1", "user_2"],
        ... )
        >>> print(f"Status: {response.status}")
        >>> if response.data_uri:
        ...     print(f"Results at: {response.data_uri}")
        """
        import base64
        import json
        from uuid import uuid4

        import pyarrow as pa

        from chalk._gen.chalk.streaming.v1.simple_streaming_service_pb2 import TestStreamingResolverRequest
        from chalk.utils.pydanticutil.pydantic_compat import get_pydantic_model_json, is_pydantic_basemodel_instance

        # Determine if resolver is static and needs serialization
        resolver_fqn: str | None = None
        static_stream_resolver_b64: str | None = None

        if isinstance(resolver, str):
            resolver_fqn = resolver
        else:
            from chalk.features.resolver import StreamResolver

            resolver_fqn = resolver.fqn

            if isinstance(resolver, StreamResolver) and resolver.feature_expressions:
                from chalk.parsed.to_proto import ToProtoConverter

                proto_resolver = ToProtoConverter.convert_stream_resolver(resolver)
                static_stream_resolver_b64 = base64.b64encode(
                    proto_resolver.SerializeToString(deterministic=True)
                ).decode("utf-8")

        # Load from file if provided
        if message_filepath is not None:
            if message_bodies is not None:
                raise ValueError("Cannot provide both message_filepath and message_bodies")

            loaded_bodies: list[Any] = []
            loaded_keys: list[str | None] = []
            loaded_timestamps: list[str | None] = []

            with open(message_filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    msg = json.loads(line)
                    loaded_bodies.append(msg.get("message_body", msg))
                    loaded_keys.append(msg.get("message_key"))
                    loaded_timestamps.append(msg.get("message_timestamp"))

            message_bodies = loaded_bodies
            if message_keys is None and any(k is not None for k in loaded_keys):
                message_keys = loaded_keys
            if message_timestamps is None and any(t is not None for t in loaded_timestamps):
                # Cast needed: loaded_timestamps is list[str | None] from JSON,
                # but message_timestamps is list[str | datetime] - strings will be parsed later
                message_timestamps = typing.cast(list[str | dt.datetime], loaded_timestamps)

        # Validate inputs
        if message_bodies is None:
            raise ValueError("Either message_bodies or message_filepath must be provided")

        num_messages = len(message_bodies)
        if num_messages == 0:
            raise ValueError("message_bodies cannot be empty")

        if message_keys is not None and len(message_keys) != num_messages:
            raise ValueError(
                f"message_keys length ({len(message_keys)}) must match message_bodies length ({num_messages})"
            )

        if message_timestamps is not None and len(message_timestamps) != num_messages:
            raise ValueError(
                f"message_timestamps length ({len(message_timestamps)}) must match message_bodies length ({num_messages})"
            )

        # Generate defaults
        message_ids = [str(uuid4()) for _ in range(num_messages)]

        if message_keys is None:
            message_keys = typing.cast(list[str | None], [None] * num_messages)

        if message_timestamps is None:
            message_timestamps = typing.cast(list[str | dt.datetime], [dt.datetime.now()] * num_messages)

        # Convert message bodies to bytes
        processed_bodies: list[bytes] = []
        for body in message_bodies:
            if isinstance(body, bytes):
                processed_bodies.append(body)
            elif isinstance(body, str):
                processed_bodies.append(body.encode("utf-8"))
            elif is_pydantic_basemodel_instance(body):
                # Use utility function that handles both Pydantic v1 and v2
                processed_bodies.append(get_pydantic_model_json(body).encode("utf-8"))
            else:
                # Try JSON serialization for dict-like objects
                processed_bodies.append(json.dumps(body).encode("utf-8"))

        # Convert timestamps to unix timestamps in milliseconds (int64)
        # At this point message_timestamps is guaranteed to be non-None due to the default assignment above
        assert message_timestamps is not None
        processed_timestamps: list[int] = []
        for ts in message_timestamps:
            if isinstance(ts, str):
                # Parse ISO format string
                parsed = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                processed_timestamps.append(int(parsed.timestamp() * 1000))  # milliseconds
            else:
                # Type narrowing: ts must be dt.datetime here
                processed_timestamps.append(int(ts.timestamp() * 1000))  # milliseconds

        # Create Arrow table
        table = pa.table(
            {
                "message_id": message_ids,
                "message_key": message_keys,
                "message_data": processed_bodies,
                "publish_timestamp": processed_timestamps,
            }
        )

        # Serialize to Arrow IPC format
        sink = pa.BufferOutputStream()
        with pa.ipc.new_stream(sink, table.schema) as writer:
            writer.write_table(table)
        input_data = sink.getvalue().to_pybytes()

        # Create gRPC request
        request = TestStreamingResolverRequest(
            resolver_fqn=resolver_fqn or "",
            input_data=input_data,
            operation_id=None,
            debug=True,
        )

        if static_stream_resolver_b64:
            request.static_stream_resolver_b64 = static_stream_resolver_b64

        # Call new TestStreamingResolver endpoint
        proto_response = self._stub_refresher.call_streaming_stub(
            lambda x: x.TestStreamingResolver(
                request,
                timeout=request_timeout,
            ),
            _EngineTarget.GRPC_ENGINE,
        )

        # Convert proto response to StreamResolverTestResponse
        from chalk._gen.chalk.streaming.v1.simple_streaming_service_pb2 import TEST_STREAM_RESOLVER_STATUS_SUCCESS

        status = (
            StreamResolverTestStatus.SUCCESS
            if proto_response.status == TEST_STREAM_RESOLVER_STATUS_SUCCESS
            else StreamResolverTestStatus.FAILURE
        )

        # Convert proto errors to ChalkError objects
        errors_list: list[ChalkError] = []
        if proto_response.errors:
            errors_list = [ChalkErrorConverter.chalk_error_decode(err) for err in proto_response.errors]

        return StreamResolverTestResponse(
            status=status,
            data_uri=proto_response.data_uri if proto_response.HasField("data_uri") else None,
            errors=errors_list if errors_list else None,
            message=proto_response.message if proto_response.message else None,
        )

    def trigger_aggregate_backfill(
        self,
        features: list[str],
        lower_bound: dt.datetime | None = None,
        upper_bound: dt.datetime | None = None,
        resolver: str | None = None,
        query_tags: list[str] | None = None,
        store_offline: bool | None = None,
        allow_empty_tiles: bool = True,
        exact: bool = False,
        enable_profiling: bool = False,
        resource_group: str | None = None,
        input_sql: str | None = None,
        num_shards: int | None = None,
        plan_only: bool = False,
    ) -> AggregateBackfillResponse:
        """Trigger one or more aggregate backfill jobs.

        Parameters
        ----------
        features : list[str]
            The fully-qualified names of the aggregate features to backfill.
        lower_bound : datetime, optional
            The lower bound of the time range to backfill.
        upper_bound : datetime, optional
            The upper bound of the time range to backfill.
        resolver : str, optional
            The resolver to use for the backfill.
        query_tags : list[str], optional
            Resolver tags to prefer when running the backfill.
        store_offline : bool, optional
            If `True`, store materialized aggregate values in the offline store.
            Requires both `lower_bound` and `upper_bound`.
        allow_empty_tiles : bool, optional
            If `True`, empty tile spans are silently skipped instead of raising an error.
            Defaults to `True`, but is only meaningful together with `store_offline=True`:
            without an offline target it is always sent as `False`.
        exact : bool, optional
            If `True`, execute the underlying SQL source to determine the exact
            number of rows that need to migrate.
        enable_profiling : bool, optional
            If `True`, enable profiling while running the backfill jobs.
        resource_group : str, optional
            Resource group to use for the created backfill jobs.
        input_sql : str, optional
            Chalk SQL query to use to resolve event data. Mutually exclusive with `resolver`.
        num_shards : int, optional
            Maximum number of bucket-aligned, time-sharded jobs to split each backfill
            job's window into. Must be > 1 when provided. The server chooses the actual count (at most this many,
            based on its per-shard window-width policy) so that all shards stay aligned
            to the aggregation's bucket grid. Useful when a single job over the full
            window would run out of memory or disk. Requires a Chalk deployment with
            job-queue execution enabled; unset preserves the single-job behavior.
        plan_only : bool, optional
            If `True`, validate the request and return the planner's split with cost
            estimates without creating anything. The response's `job` is absent, and
            there is no backfill id to poll. The same validation runs as for a real
            backfill, so a request that plans cleanly will also create cleanly.
            Requires a Chalk server that supports `CreateAggregateBackfillV2`.

        Returns
        -------
        AggregateBackfillResponse
            `job` is the single aggregate backfill row covering every job this request
            launched -- `job.id` is the aggregate backfill id -- and is `None` when
            `plan_only=True`. `sub_backfills` is the planner's split of the request, each
            entry pairing the features it covers with its cost estimate.
        """
        if store_offline is True and (lower_bound is None or upper_bound is None):
            raise ValueError("When `store_offline=True`, both `lower_bound` and `upper_bound` must be specified.")
        if num_shards is not None and num_shards <= 1:
            raise ValueError("`num_shards` must be > 1 when provided; omit it to run the backfill as a single job.")

        request = CreateAggregateBackfillV2Request(
            features=features,
            lower_bound=datetime_to_proto_timestamp(lower_bound) if lower_bound else None,
            upper_bound=datetime_to_proto_timestamp(upper_bound) if upper_bound else None,
            resolver=resolver,
            exact=exact,
            tags=query_tags or [],
            input_sql=input_sql,
            enable_profiling=enable_profiling,
            mode=AGGREGATE_BACKFILL_MODE_PLAN if plan_only else AGGREGATE_BACKFILL_MODE_CREATE,
        )
        if store_offline is not None:
            request.store_offline = store_offline
        if resource_group is not None:
            request.resource_group = resource_group
        if num_shards is not None:
            request.num_shards = num_shards
        # The server rejects allow_empty_tiles without an offline target, and this argument
        # defaults to True, so every default call would fail validation if it were sent
        # verbatim. The flag has no effect off the offline path anyway.
        request.allow_empty_tiles = bool(allow_empty_tiles) if store_offline else False

        response = self._create_aggregate_backfill_v2(request)
        if response is not None:
            return AggregateBackfillConverter.response_decode(response)

        # The server predates CreateAggregateBackfillV2. Plan mode has no behavior to
        # preserve on such servers, so it fails rather than degrading.
        if plan_only:
            raise ChalkCustomException(
                "This Chalk server does not support plan-only aggregate backfills. Upgrade your "
                + "Chalk server, or omit `plan_only` to run the backfill.",
            )
        # Same for sharding: a server this old would silently run one unsharded job,
        # which defeats the reason to pass num_shards (avoiding OOM), so fail instead.
        if num_shards is not None:
            raise ChalkCustomException(
                "This Chalk server does not support sharded aggregate backfills. Upgrade your "
                + "Chalk server, or omit `num_shards` to run the backfill as a single job.",
            )
        warnings.warn(
            "This Chalk server does not support server-side aggregate backfill planning. "
            + "Falling back to client-side planning.",
            stacklevel=3,
        )
        return self._trigger_aggregate_backfill_legacy(
            features=features,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            resolver=resolver,
            query_tags=query_tags,
            store_offline=store_offline,
            allow_empty_tiles=request.allow_empty_tiles,
            exact=exact,
            enable_profiling=enable_profiling,
            resource_group=resource_group,
            input_sql=input_sql,
        )

    def _create_aggregate_backfill_v2(
        self,
        request: CreateAggregateBackfillV2Request,
    ) -> CreateAggregateBackfillV2Response | None:
        """Call CreateAggregateBackfillV2, returning `None` if the server predates it.

        Only the RPC itself is guarded, so an `UNIMPLEMENTED` raised by anything else
        is never mistaken for version skew.
        """
        try:
            return self._stub_refresher.call_aggregate_stub(
                lambda stub: stub.CreateAggregateBackfillV2(request, timeout=None)
            )
        except grpc.RpcError as e:
            code = e.code()
            if code == grpc.StatusCode.UNIMPLEMENTED:
                return None
            if code == grpc.StatusCode.INVALID_ARGUMENT:
                # Both modes run the same validation and neither creates anything when it
                # fails, so name the operation the caller actually asked for.
                raise ChalkCustomException(
                    (
                        "Failed to plan aggregate backfill."
                        if request.mode == AGGREGATE_BACKFILL_MODE_PLAN
                        else "Failed to create aggregate backfill. No jobs were created."
                    ),
                    detail=e.details(),
                ) from e
            if code == grpc.StatusCode.INTERNAL:
                # Includes the partial-launch case, where some jobs did start. The server's
                # detail says how many, so it has to reach the caller.
                raise ChalkCustomException(
                    "Failed to create aggregate backfill jobs.",
                    detail=e.details(),
                ) from e
            raise

    def _trigger_aggregate_backfill_legacy(
        self,
        features: list[str],
        lower_bound: dt.datetime | None,
        upper_bound: dt.datetime | None,
        resolver: str | None,
        query_tags: list[str] | None,
        store_offline: bool | None,
        allow_empty_tiles: bool,
        exact: bool,
        enable_profiling: bool,
        resource_group: str | None,
        input_sql: str | None,
    ) -> AggregateBackfillResponse:
        """Plan and create one job per sub-backfill, for servers without V2.

        Returns the same `AggregateBackfillResponse` the V2 path does, so callers see one
        type regardless of server version. The per-sub-backfill responses are used only to
        check for errors and to reconstruct the job row if it cannot be read back.
        """
        from chalk._gen.chalk.aggregate.v1.backfill_pb2 import AGGREGATE_BACKFILL_STATUS_QUEUED
        from chalk._gen.chalk.aggregate.v1.backfill_pb2 import AggregateBackfillJob as AggregateBackfillJobProto
        from chalk._gen.chalk.aggregate.v1.backfill_pb2 import AggregateBackfillUserParams
        from chalk._gen.chalk.aggregate.v1.service_pb2 import (
            CreateAggregateBackfillJobRequest,
            GetAggregateBackfillJobRequest,
            PlanAggregateBackfillRequest,
        )

        plan_request = PlanAggregateBackfillRequest(
            params=AggregateBackfillUserParams(
                features=features,
                lower_bound=datetime_to_proto_timestamp(lower_bound) if lower_bound else None,
                upper_bound=datetime_to_proto_timestamp(upper_bound) if upper_bound else None,
                resolver=resolver,
                exact=exact,
                tags=query_tags or [],
                input_sql=input_sql,
            )
        )

        plan_response = self._stub_refresher.call_aggregate_stub(
            lambda stub: stub.PlanAggregateBackfill(plan_request, timeout=None)
        )
        if plan_response.errors:
            raise ChalkCustomException(
                "Failed to plan aggregate backfill.",
                detail="\n".join(plan_response.errors),
            )

        create_responses: list[CreateAggregateBackfillJobResponse] = []
        for backfill_with_estimate in plan_response.backfills:
            backfill = backfill_with_estimate.backfill
            create_request = CreateAggregateBackfillJobRequest(
                resolver=backfill.resolver,
                bucket_feature=backfill.datetime_feature,
                enable_profiling=enable_profiling,
                aggregate_backfill_id=plan_response.aggregate_backfill_id,
                query_tags=query_tags or [],
                input_sql=backfill.input_sql,
            )

            for series in backfill.series:
                for rule in series.rules:
                    create_request.features.extend(rule.dependent_features)

            if backfill.HasField("lower_bound"):
                create_request.lower_bound.CopyFrom(backfill.lower_bound)
            if backfill.HasField("upper_bound"):
                create_request.upper_bound.CopyFrom(backfill.upper_bound)
            if store_offline is not None:
                create_request.store_offline = store_offline

            create_request.allow_empty_tiles = allow_empty_tiles

            if resource_group is not None:
                create_request.resource_group = resource_group

            create_response = self._stub_refresher.call_aggregate_stub(
                lambda stub, req=create_request: stub.CreateAggregateBackfillJob(req, timeout=None)
            )
            if create_response.errors:
                raise ChalkCustomException(
                    "Failed to create aggregate backfill job.",
                    errors=[ChalkErrorConverter.chalk_error_decode(err) for err in create_response.errors],
                )
            create_responses.append(create_response)

        aggregate_backfill_id = plan_response.aggregate_backfill_id
        job_proto: AggregateBackfillJobProto | None = None
        try:
            get_request = GetAggregateBackfillJobRequest(aggregate_backfill_id=aggregate_backfill_id)
            get_response = self._stub_refresher.call_aggregate_stub(
                lambda stub: stub.GetAggregateBackfillJob(get_request, timeout=None)
            )
            # An unset `job` reads back as an empty message rather than None, which would
            # otherwise be returned as a job with no id.
            if get_response.HasField("job"):
                job_proto = get_response.job
        except grpc.RpcError as e:
            # The jobs are already running, so a failed read must not fail the call.
            chalk_logger.warning(
                "Could not read back aggregate backfill %s: %s", aggregate_backfill_id, e, exc_info=True
            )

        if job_proto is None:
            # The jobs did launch, so describe them rather than returning nothing. Only the
            # fields this path can know are set; the rest stay unset and decode to None.
            job_proto = AggregateBackfillJobProto(
                id=aggregate_backfill_id,
                status=AGGREGATE_BACKFILL_STATUS_QUEUED,
                features=[f for response in create_responses for f in response.features],
                resolvers=[b.backfill.resolver for b in plan_response.backfills if b.backfill.resolver],
                query_tags=query_tags or [],
            )

        # Decoding both branches through the converter is what makes the two server paths
        # agree: it is the single place features and resolvers are deduplicated.
        return AggregateBackfillResponse(
            job=AggregateBackfillConverter.job_decode(job_proto),
            sub_backfills=[AggregateBackfillConverter.plan_decode(backfill) for backfill in plan_response.backfills],
        )

    def _lookup_volume_mount(self, volume_name: str, mount_path: str) -> Optional[Dict[str, Any]]:
        """Return a mount for an existing volume, or None when it is absent."""
        from chalkcompute import (  # pyright: ignore[reportMissingImports]
            ConnectClient,
            VolumeClient,
            VolumeNotFoundError,
        )

        with VolumeClient.from_connect(ConnectClient(chalk_client=self)) as client:
            try:
                volume = client.lookup(volume_name)
            except VolumeNotFoundError:
                return None
            return volume.mount(mount_path).to_spec_dict()

    def _resolve_model_volume_mount(self, model_name: str, model_version: int, spec: Any) -> Optional[Dict[str, Any]]:
        """Mount dict for a version's persisted ``model_volume``, or None if it has none.

        Looking up the volume validates that it still exists and lets the volume object
        produce the canonical mount specification.
        """
        if not (spec.HasField("model_volume") and spec.model_volume):
            return None
        volume_name = spec.model_volume
        mount = self._lookup_volume_mount(volume_name, CHALK_HANDLER_ARTIFACT_PATH)
        if mount is None:
            raise ValueError(
                f"Model '{model_name}' v{model_version} references volume '{volume_name}', which no longer "
                + "exists. Restore the volume or re-register the model version before deploying."
            )
        return mount

    def _ensure_model_image(
        self, model_name: str, model_version: int, validate: bool = True
    ) -> tuple[int, List[Dict[str, Any]], Optional[str], Optional[str]]:
        """Resolve the image to deploy: returns (version, volume_mounts, image_uri, serving_handler).

        serving_handler is the chalk-shim entrypoint ("model_handler.handler") for handler/inferred
        images, or None for chalkcompute/user images (the server default / user-supplied handler).
        """
        model_version_resp: GetModelVersionResponse = self._stub_refresher.call_model_stub(
            lambda x: x.GetModelVersion(
                GetModelVersionRequest(
                    model_name=model_name,
                    version=model_version,
                )
            )
        )
        spec = model_version_resp.model_version.model_artifact.spec
        has_model_image = spec.HasField("model_image") and bool(spec.model_image)
        has_build_spec = spec.HasField("image_spec") and bool(spec.image_spec)
        if has_build_spec:
            serving_handler = "model_handler.handler" if image_spec_bakes_handler_shim(spec.image_spec) else None
        elif has_model_image:
            serving_handler = "model_handler.handler" if (spec.HasField("model_volume") and spec.model_volume) else None
        else:
            serving_handler = "model_handler.handler"  # inferred images bake the chalk shim
        if has_build_spec and not has_model_image:
            mount_files = [f for f in spec.additional_files if f.HasField("mount_path") and f.mount_path]
            if mount_files:
                local_files = self._download_image_local_files(model_name, model_version, mount_files)
                try:
                    deploy_image, volume_mounts = build_image_from_spec_with_files(
                        spec.image_spec, local_files, chalk_client=self
                    )
                finally:
                    tmp_root = tempfile.gettempdir()
                    for d in {os.path.dirname(p) for p, _, _ in local_files}:
                        if d.startswith(tmp_root):
                            shutil.rmtree(d, ignore_errors=True)
                # Also mount the model_volume, if any, instead of returning image mounts only.
                model_mount = self._resolve_model_volume_mount(model_name, model_version, spec)
                if model_mount is not None:
                    volume_mounts.append(model_mount)
                return model_version, volume_mounts, deploy_image, serving_handler
        if has_model_image or has_build_spec:
            deploy_image = (
                build_image_from_spec_bytes(spec.image_spec, chalk_client=self)
                if has_build_spec and not has_model_image
                else None
            )
            # New path: model_volume is persisted on the spec at registration time.
            model_mount = self._resolve_model_volume_mount(model_name, model_version, spec)
            if model_mount is not None:
                return model_version, [model_mount], deploy_image, serving_handler

            # Legacy path: model_volume not set, derive volume name from (name, version).
            volume_name = chalk_handler_volume_name(model_name, model_version)
            legacy_mount = self._lookup_volume_mount(volume_name, CHALK_HANDLER_ARTIFACT_PATH)
            if legacy_mount is not None:
                volume_mounts = [legacy_mount]
            else:
                # Only artifact-backed models have files to mount; image-only models deploy as-is.
                if spec.model_files:
                    model_files = self.download_model_artifact(model_name, model_version).downloaded_model_files
                else:
                    model_files = []
                if model_files:
                    try:
                        volume_mount = upload_chalk_handler_artifacts(
                            volume_name=volume_name,
                            uploads=[(model_files[0], os.path.basename(model_files[0]))],
                            chalk_client=self,
                        )
                        volume_mounts = [volume_mount]
                    finally:
                        download_dir = os.path.dirname(model_files[0])
                        if download_dir and os.path.exists(download_dir):
                            shutil.rmtree(download_dir)
                else:
                    volume_mounts = []
            return model_version, volume_mounts, deploy_image, serving_handler

        artifact_result = self.download_model_artifact(model_name, model_version)
        model_files = artifact_result.downloaded_model_files
        if not model_files:
            return model_version, [], None, None

        try:
            vol_name = generate_volume_name(model_name, model_version)

            image_uri, model_filename = build_inferred_image(spec, model_files, vol_name, validate=validate)

            if validate:
                Console().print(
                    Text(
                        f"✓ Model handler validation passed for '{model_name}' v{model_version}",
                        style=Style(color=CHALK_WEBSITE_GREEN, bold=True),
                    )
                )

            chalk_logger.info(f"Inferred image for model '{model_name}' v{model_version}: {image_uri}")
            Console().print(
                Text(
                    f"✓ Inferred image for model '{model_name}' v{model_version}",
                    style=Style(color=CHALK_WEBSITE_GREEN, bold=True),
                )
            )

            volume_mount = upload_chalk_handler_artifacts(
                volume_name=vol_name,
                uploads=[(model_files[0], model_filename)],
                chalk_client=self,
                mount_path=f"/volumes/{vol_name}",
            )
        finally:
            download_dir = os.path.dirname(model_files[0])
            if download_dir and os.path.exists(download_dir):
                shutil.rmtree(download_dir)

        volume_mounts = [volume_mount]
        return model_version, volume_mounts, image_uri, serving_handler

    def deploy_model_version_to_scaling_group(
        self,
        name: str,
        model_name: str,
        model_version: int,
        min_replicas: int = 1,
        max_replicas: int = 1,
        cpu: Optional[str] = None,
        memory: Optional[str] = None,
        gpu: Optional[str] = None,
        handler: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        target_cpu_utilization_percentage: Optional[int] = None,
        validate: bool = True,
        secrets: Optional[List[Any]] = None,
        readiness_probe: Optional["GrpcReadinessProbe"] = None,
        startup_probe: Optional["GrpcStartupProbe"] = None,
    ) -> dict[str, Any]:
        """Deploy a registered model version as a scaling group.

        Uses the authenticated gRPC channel with a raw unary call since
        Python scaling group proto stubs are not yet generated.
        """
        model_version, inferred_volumes, image_uri, serving_handler = self._ensure_model_image(
            model_name, model_version, validate=validate
        )

        if serving_handler is not None:
            if handler is None:
                handler = serving_handler
            if env_vars is None:
                env_vars = {}
            env_vars.setdefault("PYTHONPATH", "/app")

        # Build protobuf-compatible JSON request matching CreateModelScalingGroupRequest
        request_data: Dict[str, Any] = {
            "name": name,
            "model_name": model_name,
            "identifier": {"version": model_version},
            "scaling_spec": {
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
            },
        }

        if target_cpu_utilization_percentage is not None:
            request_data["scaling_spec"]["target_cpu_utilization_percentage"] = target_cpu_utilization_percentage

        container_spec: Dict[str, Any] = {}
        if cpu is not None or memory is not None or gpu is not None:
            resources: Dict[str, str] = {}
            if cpu is not None:
                resources["cpu"] = cpu
            if memory is not None:
                resources["memory"] = memory
            if gpu is not None:
                resources["gpu"] = gpu
            container_spec["resources"] = resources

        if env_vars:
            container_spec["env_vars"] = env_vars

        if secrets is not None:
            try:
                from chalkcompute import (  # pyright: ignore[reportMissingImports]
                    ConnectClient,
                    Secret,
                    resolve_lazy_secrets,
                )

                if not all(isinstance(s, Secret) for s in secrets):
                    raise TypeError("Input `secrets` must be a list of Secret")

                resolved_secrets, _ = resolve_lazy_secrets(secrets, ConnectClient(chalk_client=self))
                container_spec["secretRefs"] = [
                    s._to_proto_dict() for s in resolved_secrets  # pyright: ignore[reportPrivateUsage]
                ]

            except ImportError:
                raise ImportError("Please install `chalkcompute` to enable injecting secrets into Scaling Groups.")

        if inferred_volumes:
            container_spec["volumes"] = inferred_volumes

        if readiness_probe is not None:
            grpc_readiness_probe: Dict[str, Any] = {}
            if readiness_probe.service is not None:
                grpc_readiness_probe["service"] = readiness_probe.service
            readiness_probe_data: Dict[str, Any] = {"grpc": grpc_readiness_probe}
            if readiness_probe.period_seconds is not None:
                readiness_probe_data["period_seconds"] = readiness_probe.period_seconds
            if readiness_probe.timeout_seconds is not None:
                readiness_probe_data["timeout_seconds"] = readiness_probe.timeout_seconds
            if readiness_probe.failure_threshold is not None:
                readiness_probe_data["failure_threshold"] = readiness_probe.failure_threshold
            container_spec["readiness_probe"] = readiness_probe_data

        if startup_probe is not None:
            grpc_startup_probe: Dict[str, Any] = {}
            if startup_probe.method is not None:
                grpc_startup_probe["method"] = startup_probe.method
            container_spec["startup_probe"] = {"grpc": grpc_startup_probe}

        # The server requires container_spec on every deploy, even when empty.
        request_data["container_spec"] = container_spec

        if handler is not None:
            request_data["handler"] = handler

        if image_uri is not None:
            request_data["image"] = image_uri

        from google.protobuf import json_format

        request_json = json.dumps(request_data)

        from chalk._gen.chalk.modeldeployment.v1 import service_pb2

        def create_request_and_call(stub: ModelDeploymentServiceStub) -> dict[str, Any]:
            req = service_pb2.CreateModelScalingGroupRequest()
            json_format.Parse(request_json, req)
            resp = stub.CreateModelScalingGroup(req)
            return json_format.MessageToDict(resp)

        return self._stub_refresher.call_model_deployment_stub(create_request_and_call)

    def list_scaling_groups(self) -> ListScalingGroupsResponse:
        """List all scaling groups in the current environment.

        Returns
        -------
        ListScalingGroupsResponse
            Response containing a list of scaling groups.
        """

        def do_call(stub: ScalingGroupManagerServiceStub):
            req = scalinggroup_service_pb2.ListScalingGroupsRequest()
            resp = stub.ListScalingGroups(req)
            return resp

        resp = self._stub_refresher.call_scaling_group_stub(do_call)
        scaling_groups = [proto_to_scaling_group(sg) for sg in resp.scaling_groups]
        return ListScalingGroupsResponse(scalingGroups=scaling_groups)

    def get_scaling_group(self, name: Optional[str] = None, id: Optional[str] = None) -> ScalingGroup:
        """Get a scaling group by name or id.

        Parameters
        ----------
        name
            Name of the scaling group.
        id
            ID of the scaling group.

        Returns
        -------
        ScalingGroup
            The scaling group details.
        """
        if name is not None and id is not None:
            raise ValueError("Provide either name or id, not both")
        if name is None and id is None:
            raise ValueError("Provide either name or id")

        def do_call(stub: ScalingGroupManagerServiceStub):
            req = scalinggroup_service_pb2.GetScalingGroupRequest()
            if name is not None:
                req.name = name
            if id is not None:
                req.id = id
            resp = stub.GetScalingGroup(req)
            return resp

        resp = self._stub_refresher.call_scaling_group_stub(do_call)
        return proto_to_scaling_group(resp.scaling_group)

    def delete_scaling_group(self, name: Optional[str] = None, id: Optional[str] = None) -> DeleteScalingGroupResponse:
        """Delete a scaling group by name or id.

        Parameters
        ----------
        name
            Name of the scaling group to delete.
        id
            ID of the scaling group to delete.

        Returns
        -------
        DeleteScalingGroupResponse
            Response containing the deleted scaling group.
        """
        if name is not None and id is not None:
            raise ValueError("Provide either name or id, not both")
        if name is None and id is None:
            raise ValueError("Provide either name or id")

        def do_call(stub: ScalingGroupManagerServiceStub):
            req = scalinggroup_service_pb2.DeleteScalingGroupRequest()
            if name is not None:
                req.name = name
            if id is not None:
                req.id = id
            resp = stub.DeleteScalingGroup(req)
            return resp

        resp = self._stub_refresher.call_scaling_group_stub(do_call)
        scaling_group = proto_to_scaling_group(resp.scaling_group) if resp.scaling_group else None
        return DeleteScalingGroupResponse(scalingGroup=scaling_group)

    def _get_remote_call_metadata(self) -> List[tuple[str, str]]:
        """gRPC metadata (Bearer token + env id) for a direct scaling-group call."""
        return self._stub_refresher.get_remote_call_metadata()

    def _get_queue_call_metadata(self) -> List[tuple[str, str]]:
        """gRPC metadata for an enqueue/poll against the function-queue server."""
        return self._stub_refresher.get_queue_call_metadata()

    def _get_engine_grpc_target(self) -> tuple[str, bool]:
        """``(target, use_tls)`` of the grpc-engine ingress that fronts the function queue."""
        return self._stub_refresher.get_engine_grpc_target()

    def _get_queue_client(self) -> Any:
        """
        Cached function-queue client, rebuilt when its baked-in metadata goes stale.
        """
        from chalk.client._model_remote import new_queue_client

        metadata = self._get_queue_call_metadata()
        cached = self._queue_client_cache
        if cached is not None:
            if not cached.is_stale(metadata):
                return cached.client
            cached.client.close()
        client = new_queue_client(self)
        self._queue_client_cache = _CachedQueueClient(metadata=metadata, client=client)
        return client
