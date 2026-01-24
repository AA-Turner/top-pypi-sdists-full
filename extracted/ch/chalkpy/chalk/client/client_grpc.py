from __future__ import annotations

import collections.abc
import dataclasses
import datetime as dt
import json
import random
import typing
import warnings
from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Mapping, Optional, Sequence, Tuple, TypeVar, Union
from urllib.parse import urlparse

import grpc
import grpc.experimental
from google.protobuf import empty_pb2, timestamp_pb2

from chalk import DataFrame, EnvironmentId, chalk_logger
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import online_query_pb2, resources_pb2, upload_features_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery, UploadFeaturesBulkRequest
from chalk._gen.chalk.common.v1.script_task_pb2 import ScriptTaskKind, ScriptTaskRequest, TrainingRunArgs
from chalk._gen.chalk.common.v2.execute_plan_pb2 import ExecutePlanRequest, ExecutePlanResponse
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.engine.v2.dataframe_service_pb2_grpc import DataFrameServiceStub
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk._gen.chalk.graph.v1.graph_pb2 import Graph
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
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2 import (
    GetJobQueueOperationSummaryRequest,
    GetJobQueueOperationSummaryResponse,
)
from chalk._gen.chalk.server.v1.dataplanejobqueue_pb2_grpc import DataPlaneJobQueueServiceStub
from chalk._gen.chalk.server.v1.deploy_pb2 import (
    CreateBranchFromSourceDeploymentRequest,
    CreateBranchFromSourceDeploymentResponse,
)
from chalk._gen.chalk.server.v1.deploy_pb2_grpc import DeployServiceStub
from chalk._gen.chalk.server.v1.graph_pb2 import (
    GetCodegenFeaturesFromGraphRequest,
    GetCodegenFeaturesFromGraphResponse,
    GetGraphRequest,
    GetGraphResponse,
    PythonVersion,
)
from chalk._gen.chalk.server.v1.graph_pb2_grpc import GraphServiceStub
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
    GetModelArtifactUploadUrlsRequest,
    GetModelArtifactUploadUrlsResponse,
    GetModelRequest,
    GetModelResponse,
    GetModelVersionRequest,
    GetModelVersionResponse,
)
from chalk._gen.chalk.server.v1.model_registry_pb2_grpc import ModelRegistryServiceStub
from chalk._gen.chalk.server.v1.offline_queries_pb2_grpc import OfflineQueryMetadataServiceStub
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
from chalk.client import ChalkAuthException, FeatureReference
from chalk.client.client_impl import _validate_context_dict  # pyright: ignore[reportPrivateUsage]
from chalk.client.models import (
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    CreateBranchResponse,
    GetRegisteredModelResponse,
    GetRegisteredModelVersionResponse,
)
from chalk.client.models import ManualTriggerScheduledQueryResponse as ManualTriggerScheduledQueryResponseDataclass
from chalk.client.models import (
    ModelUploadUrlResponse,
    OnlineQuery,
    OnlineQueryResponse,
    RegisterModelArtifactResponse,
    RegisterModelResponse,
    RegisterModelVersionResponse,
    ResourceRequests,
    ScheduledQueryRun,
    StreamResolverTestResponse,
    StreamResolverTestStatus,
    UploadFeaturesResponse,
)
from chalk.client.serialization.model_serialization import ModelSerializer
from chalk.client.serialization.protos import ChalkErrorConverter, OnlineQueryConverter, UploadFeaturesBulkConverter
from chalk.config.auth_config import TokenConfig, load_token
from chalk.features import live_updates
from chalk.features._encoding.inputs import GRPC_ENCODE_OPTIONS, InputEncodeOptions, recursive_encode_bulk_inputs
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.resolver import Resolver
from chalk.features.tag import DeploymentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.ml import LocalSourceConfig, ModelEncoding, ModelRunCriterion, ModelType, SourceConfig
from chalk.ml.model_file_transfer import ModelFileUploader
from chalk.ml.utils import ModelClass
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils import df_utils
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor
from chalk.utils.tracing import add_trace_headers, safe_trace

if TYPE_CHECKING:
    from pyarrow import RecordBatch, Table
    from pydantic import BaseModel

    from chalk._gen.chalk.server.v1.builder_pb2 import StartBranchResponse
    from chalk._gen.chalk.server.v1.builder_pb2_grpc import BuilderServiceStub
    from chalk.client import ChalkError

CHALK_GRPC_TRACE_ID_HEADER: str = "x-chalk-trace-id"


@dataclasses.dataclass
class ParsedUri:
    uri_without_scheme: str
    use_tls: bool


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


def get_features_feather_bytes(
    inputs: "Mapping[FeatureReference, Sequence[Any]] | DataFrame | Table | RecordBatch",
    options: InputEncodeOptions,
    compression: Literal["lz4", "zstd", "uncompressed"] = "lz4",
) -> bytes:
    import pyarrow as pa

    if isinstance(inputs, Mapping):
        inputs, _ = recursive_encode_bulk_inputs(inputs, options=options)

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


default_channel_options: Dict[str, str | int] = {
    "grpc.max_send_message_length": 1024 * 1024 * 100,  # 100MB
    "grpc.max_receive_message_length": 1024 * 1024 * 100,  # 100MB
    # https://grpc.io/docs/guides/performance/#python
    grpc.experimental.ChannelOptions.SingleThreadedUnaryStream: 1,
    "grpc.service_config": json.dumps(
        {
            "methodConfig": [
                {
                    "name": [{}],
                    "maxAttempts": 5,
                    "initialBackoff": "0.1s",
                    "maxBackoff": "1s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": ["UNAVAILABLE"],
                }
            ]
        }
    ),
}


T = TypeVar("T")
U = TypeVar("U")


class StubProvider:
    def close(self):
        if self._server_channel is not None:
            self._server_channel.close()
        if self._engine_channel is not None:
            self._engine_channel.close()

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

    @cached_property
    def query_stub(self) -> QueryServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return QueryServiceStub(self._engine_channel)

    @cached_property
    def offline_query_stub(self) -> OfflineQueryMetadataServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return OfflineQueryMetadataServiceStub(self._server_channel)

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
    def sql_stub(self) -> SqlServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return SqlServiceStub(self._engine_channel)

    @cached_property
    def dataframe_stub(self) -> DataFrameServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return DataFrameServiceStub(self._engine_channel)

    @cached_property
    def streaming_stub(self) -> SimpleStreamingServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return SimpleStreamingServiceStub(self._engine_channel)

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
        channel_options_merged: Dict[str, str | int] = default_channel_options.copy()
        if channel_options:
            channel_options_merged.update(dict(channel_options))
        if skip_api_server:
            # Omits the auth handshake with the API server. Primarily for internal use/testing -- if used in production,
            # this client will simply fail to connect. If True then query_server must be provided & point to
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
        engine_headers = additional_headers_nonempty + [("x-chalk-deployment-type", "engine-grpc")]
        if deployment_tag is not None:
            engine_headers += [("x-chalk-deployment-tag", deployment_tag)]
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
                    additional_headers=engine_headers + [("x-chalk-env-id", self.environment_id)],
                )
            )
        ]

        self._engine_channel: Optional[grpc.Channel] = None
        if query_server is not None:
            parsed_uri = _parse_uri_for_engine(query_server_uri=query_server)
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

    def call_query_stub(self, fn: Callable[[QueryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.query_stub)

    def call_offline_query_stub(self, fn: Callable[[OfflineQueryMetadataServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.offline_query_stub)

    def call_scheduled_query_stub(self, fn: Callable[[SchedulerServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.scheduled_query_stub)

    def call_scheduled_query_run_stub(self, fn: Callable[[ScheduledQueryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.scheduled_query_run_stub)

    def call_sql_stub(self, fn: Callable[[SqlServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.sql_stub)

    def call_dataframe_stub(self, fn: Callable[[DataFrameServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.dataframe_stub)

    def call_model_stub(self, fn: Callable[[ModelRegistryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.model_stub)

    def call_task_stub(self, fn: Callable[[ScriptTaskServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.task_stub)

    def call_builder_stub(self, fn: Callable[["BuilderServiceStub"], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.builder_stub)

    def call_log_stub(self, fn: Callable[[LogSearchServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.log_stub)

    def call_job_queue_stub(self, fn: Callable[[DataPlaneJobQueueServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.job_queue_stub)

    def call_streaming_stub(self, fn: Callable[[SimpleStreamingServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.streaming_stub)

    @property
    def log_stub(self) -> LogSearchServiceStub:
        return self._stub.log_stub

    @property
    def environment_id(self) -> str | None:
        return self._stub.environment_id


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

        self._stub_refresher = StubRefresher(
            token_config=token_config,
            query_server=query_server,
            deployment_tag=deployment_tag,
            additional_headers=additional_headers,
            skip_api_server=kwargs.get("_skip_api_server", False),
            channel_options=channel_options,
        )

    _INPUT_ENCODE_OPTIONS = GRPC_ENCODE_OPTIONS

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
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
            lambda x: x.Ping(query_server_pb2.PingRequest(num=num if num is not None else random.randint(0, 999)))
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
        )
        return OnlineQueryConverter.online_query_bulk_response_decode_to_single(bulk_response)

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
    ) -> online_query_pb2.OnlineQueryBulkResponse:
        with safe_trace("_online_query_grpc_request"):
            request = self._make_query_bulk_request(
                input={k: [v] for k, v in input.items()},
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
            if trace:
                extra_headers: dict[str, str] = {}
                extra_headers = add_trace_headers(extra_headers)
                headers = _merge_headers(extra_headers, headers)
            metadata = _canonicalize_headers(headers)
            return self._stub_refresher.call_query_stub(
                lambda x: x.OnlineQueryBulk(
                    request,
                    timeout=request_timeout,
                    metadata=metadata,
                )
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
        *,
        input_sql: str | None = None,
    ) -> BulkOnlineQueryResult:
        if input is None and input_sql is None:
            raise TypeError("One of `input` or `input_sql` is required")
        if input is not None and input_sql is not None:
            raise TypeError("`input` and `input_sql` are mutually exclusive")
        if input_sql is not None and now is not None:
            raise TypeError(
                "When using `input_sql`, `now` is not allowed: instead, to provide a query time, you can have the SQL query output a column named `__ts__`"
            )

        response, call = self._online_query_bulk_grpc_request(
            input=input,
            input_sql=input_sql,
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
    ) -> Tuple[online_query_pb2.OnlineQueryBulkResponse, grpc.Call]:
        """Returns the raw GRPC response and metadata"""

        request = self._make_query_bulk_request(
            input=input,
            input_sql=input_sql,
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
        return self._stub_refresher.call_query_stub(
            lambda x: x.OnlineQueryBulk.with_call(
                request,
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            )
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
            )
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

        Returns
        -------
        UploadFeaturesResponse
            which contains a list of errors if any occurred.
        """
        request = upload_features_pb2.UploadFeaturesRequest(
            inputs_table=get_features_feather_bytes(inputs, self._INPUT_ENCODE_OPTIONS)
        )
        response, call = self._stub_refresher.call_query_stub(
            lambda x: x.UploadFeatures.with_call(
                request, timeout=request_timeout, metadata=_canonicalize_headers(headers)
            )
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
    ) -> BulkOnlineQueryResponse:
        """Execute a series of independent requests in parallel."""
        requests: List[GenericSingleQuery] = []
        for query in queries:
            # NOTE: This assumed every request is a 'bulk' request.
            if value_metrics_tag_by_features is not None:
                query_vmtbf = value_metrics_tag_by_features
            else:
                query_vmtbf = query.value_metrics_tag_by_features
            request = self._make_query_bulk_request(
                input=query.input,
                output=query.output,
                now=(),
                staleness=query.staleness or {},
                tags=query.tags or (),
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
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
        response, call = self._stub_refresher.call_query_stub(
            lambda x: x.OnlineQueryMulti.with_call(
                online_query_pb2.OnlineQueryMultiRequest(
                    queries=requests,
                ),
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            )
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
                    current_mainline_deployment=empty_pb2.Empty()
                    if source_branch_name is None and source_deployment_id is None
                    else None,
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
                input, self._INPUT_ENCODE_OPTIONS, compression=self._input_compression
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

    def run_scheduled_query(
        self,
        name: str,
        planner_options: Optional[Mapping[str, Any]],
        incremental_resolvers: Optional[Sequence[str]],
        max_samples: Optional[int],
        env_overrides: Optional[Mapping[str, str]],
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
                ),
            )
        )
        return ManualTriggerScheduledQueryResponseDataclass.from_proto(proto_resp)

    def get_scheduled_query_run_history(
        self,
        name: str,
        limit: int = 10,
    ) -> List[ScheduledQueryRun]:
        """
        Get the run history for a scheduled query.

        Parameters
        ----------
        name
            The name of the scheduled query.
        limit
            The maximum number of runs to return. Defaults to 10.

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
        return [ScheduledQueryRun.from_proto(run) for run in proto_resp.runs]

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

    def run_sql(self, sql: str, persistence_settings: Optional[Dict[str, Any]] = None):
        request = ExecuteSqlQueryRequest(query=sql)

        if persistence_settings is not None:
            # Convert dict to proto message
            enabled = persistence_settings.get("enabled", False)
            request.persistence_settings.CopyFrom(ExecuteSqlResultPersistenceSettings(enabled=enabled))

        return self._stub_refresher.call_sql_stub(lambda x: x.ExecuteSqlQuery(request))

    def explain_sql(self, sql: str):
        return self._stub_refresher.call_sql_stub(lambda x: x.PlanSqlQuery(PlanSqlQueryRequest(query=sql)))

    def get_sql_catalogs(self):
        return self._stub_refresher.call_sql_stub(lambda x: x.GetDbCatalogs(GetDbCatalogsRequest()))

    def get_sql_schemas(self, catalog: str | None = None, db_schema_filter_pattern: str | None = None):
        return self._stub_refresher.call_sql_stub(
            lambda x: x.GetDbSchemas(
                GetDbSchemasRequest(catalog=catalog, db_schema_filter_pattern=db_schema_filter_pattern)
            )
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
            )
        )

    def execute_plan(self, *, lazy_frame_calls: expr_pb.LogicalExprNode) -> ExecutePlanResponse:
        return self._stub_refresher.call_dataframe_stub(
            lambda x: x.ExecutePlan(ExecutePlanRequest(lazy_frame_calls=lazy_frame_calls))
        )

    def get_model(
        self,
        name: str,
        version: Optional[int] = None,
    ) -> Union[GetRegisteredModelResponse, GetRegisteredModelVersionResponse]:
        """
        Retrieve a registered model from the Chalk model registry.

        Parameters
        ----------
        name : str
            Name of the model to retrieve
        version : int, optional
            Specific version number to retrieve. If not provided, returns
            information about all versions of the model

        Returns
        -------
        GetRegisteredModelResponse
            Model information including metadata, versions, and configuration details

        Examples
        --------
        Get model by name:

        >>> from chalk.client import ChalkClient
        >>> client = ChalkClient()
        >>> model = client.get_model(name="RiskScoreModel")
        >>> print(f"Latest version: {model.latest_version}")
        >>> print(f"Available versions: {model.versions}")

        Get specific model version:

        >>> model_v1 = client.get_model(name="RiskScoreModel", version=1)
        >>> print(f"Performance: {model_v1.metadata['training_metrics']}")
        """

        if version is not None:
            try:
                model_version_resp: GetModelVersionResponse = self._stub_refresher.call_model_stub(
                    lambda x: x.GetModelVersion(
                        GetModelVersionRequest(
                            model_name=name,
                            version=version,
                        )
                    )
                )
                return GetRegisteredModelVersionResponse(
                    model_id=model_version_resp.model_version.id,
                    model_name=model_version_resp.model_version.model_name,
                    created_by=model_version_resp.model_version.created_by,
                    created_at=model_version_resp.model_version.created_at.ToDatetime(),
                    model_artifact=model_version_resp.model_version.model_artifact,
                )
            except grpc.RpcError as e:
                raise RuntimeError(f"Could not register model version. {e.details()}")
        else:
            try:
                model_resp: GetModelResponse = self._stub_refresher.call_model_stub(
                    lambda x: x.GetModel(
                        GetModelRequest(
                            model_name=name,
                        )
                    )
                )
                return GetRegisteredModelResponse(
                    model_id=model_resp.model.id,
                    model_name=model_resp.model.model_name,
                    description=model_resp.model.description,
                    metadata=dict(model_resp.model.metadata),
                    created_by=model_resp.model.created_by,
                    created_at=model_resp.model.created_at.ToDatetime(),
                    updated_at=model_resp.model.updated_at.ToDatetime(),
                    archived_at=model_resp.model.archived_at.ToDatetime(),
                    latest_model_version=model_resp.model.latest_model_version,
                )
            except grpc.RpcError as e:
                raise RuntimeError(f"Could not register model version. {e.details()}")

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

    def _get_model_artifact_presigned_s3(self, model_paths: List[str]) -> ModelUploadUrlResponse:
        try:
            resp: GetModelArtifactUploadUrlsResponse = self._stub_refresher.call_model_stub(
                lambda x: x.GetModelArtifactUploadUrls(GetModelArtifactUploadUrlsRequest(file_names=model_paths))
            )
            return ModelUploadUrlResponse(
                upload_urls=dict(resp.upload_urls),
                model_artifact_id=resp.model_artifact_id,
            )
        except grpc.RpcError as e:
            raise RuntimeError(f"Could not get presigned S3 URLs for file upload: {e.details()}")

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
    ) -> RegisterModelVersionResponse:
        """Register a model in the Chalk model registry.

        Parameters
        ----------
        name
            Unique name for the model.
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
            e.g. `["torch==2.7.1", "numpy==1.26.4"]`.

        Returns
        -------
        ModelVersion
            The registered model version object.

        Examples
        --------
        Register from Python object:

        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model=trained_pytorch_model,
        ...     model_type=ModelType.PYTORCH,
        ... )

        Register from local files:

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

        Register from s3 path:
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model_paths=["s3://my-bucket/path/to/model.pth"],
        ...     model_type=ModelType.PYTORCH,
        ... )
        """
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

                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned_s3(
                    model_paths=list(all_files_to_process.keys())
                )

                model_upload_paths, additional_files_upload_paths = model_file_uploader.upload_files(
                    all_files_to_process,
                    model_file_names,
                    presigned_s3_response.upload_urls,
                    dir_allowlist,
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

                presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned_s3(
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
            The environment ID. If None, uses the client's environment.
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
            If None, logs are displayed using Rich live display.

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
            )
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
