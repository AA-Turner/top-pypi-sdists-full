from __future__ import annotations

import collections.abc
import dataclasses
import datetime as dt
import hashlib
import json
import os
import random
import tempfile
import typing
import warnings
from functools import cached_property
from math import ceil
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Mapping, Optional, Sequence, Tuple, TypeVar, Union
from urllib.parse import urlparse

import grpc
import grpc.experimental
import requests
from google.protobuf import empty_pb2, struct_pb2, timestamp_pb2

from chalk import DataFrame, EnvironmentId, chalk_logger
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import offline_query_pb2, online_query_pb2, upload_features_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery, UploadFeaturesBulkRequest
from chalk._gen.chalk.common.v2.execute_plan_pb2 import ExecutePlanRequest, ExecutePlanResponse
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.engine.v2.dataframe_service_pb2_grpc import DataFrameServiceStub
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk._gen.chalk.graph.v1.graph_pb2 import Graph
from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
from chalk._gen.chalk.protosql.v1.sql_service_pb2 import (
    ExecuteSqlQueryRequest,
    GetDbCatalogsRequest,
    GetDbSchemasRequest,
    GetTablesRequest,
    PlanSqlQueryRequest,
)
from chalk._gen.chalk.protosql.v1.sql_service_pb2_grpc import SqlServiceStub
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
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
from chalk._gen.chalk.server.v1.model_registry_pb2 import (
    CreateModelRequest,
    CreateModelResponse,
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
from chalk._gen.chalk.server.v1.offline_queries_pb2 import CreateModelTrainingJobRequest, CreateModelTrainingJobResponse
from chalk._gen.chalk.server.v1.offline_queries_pb2_grpc import OfflineQueryMetadataServiceStub
from chalk._gen.chalk.server.v1.team_pb2 import (
    CreateServiceTokenRequest,
    CreateServiceTokenResponse,
    ListServiceTokensRequest,
    ListServiceTokensResponse,
)
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk.client import ChalkAuthException, FeatureReference
from chalk.client.client_impl import _validate_context_dict  # pyright: ignore[reportPrivateUsage]
from chalk.client.models import (
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    CreateBranchResponse,
    GetRegisteredModelResponse,
    GetRegisteredModelVersionResponse,
    ModelUploadUrlResponse,
    OnlineQuery,
    OnlineQueryResponse,
    RegisterModelResponse,
    RegisterModelVersionResponse,
    ResourceRequests,
    UploadFeaturesResponse,
)
from chalk.client.serialization.protos import ChalkErrorConverter, OnlineQueryConverter, UploadFeaturesBulkConverter
from chalk.config.auth_config import TokenConfig, load_token
from chalk.features import live_updates
from chalk.features._encoding.inputs import GRPC_ENCODE_OPTIONS, InputEncodeOptions, recursive_encode_bulk_inputs
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.tag import DeploymentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.ml import ModelEncoding, ModelType
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils import df_utils
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor

if TYPE_CHECKING:
    from pyarrow import RecordBatch, Table

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


channel_options: List[tuple[str, str | int]] = [
    ("grpc.max_send_message_length", 1024 * 1024 * 100),  # 100MB
    ("grpc.max_receive_message_length", 1024 * 1024 * 100),  # 100MB
    # https://grpc.io/docs/guides/performance/#python
    (grpc.experimental.ChannelOptions.SingleThreadedUnaryStream, 1),
    (
        "grpc.service_config",
        json.dumps(
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
    ),
]


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
    def model_stub(self) -> ModelRegistryServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return ModelRegistryServiceStub(self._server_channel)

    def __init__(
        self,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
    ):
        super().__init__()
        additional_headers_nonempty: List[tuple[str, str]] = [] if additional_headers is None else additional_headers
        token_refresher: TokenRefresher | None = None
        if skip_api_server:
            # Omits the auth handshake with the API server. Primarily for internal use/testing -- if used in production,
            # this client will simply fail to connect. If True then query_server must be provided & point to
            # `localhost/127.0.0.1`.
            if query_server is None:
                raise ValueError("If skipping API server auth, query_server URI must be provided.")
            elif not (query_server.startswith("localhost") or query_server.startswith("127.0.0.1")):
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
                    options=channel_options,
                )
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options,
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
                        options=channel_options,
                    )
                    if parsed_uri.use_tls
                    else grpc.insecure_channel(
                        target=parsed_uri.uri_without_scheme,
                        options=channel_options,
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
    ):
        super().__init__()
        self._token_config = token_config
        self._query_server = query_server
        self._deployment_tag = deployment_tag
        self._skip_api_server = skip_api_server
        self._additional_headers = additional_headers
        self._stub = self._refresh_stub()

    def _refresh_stub(self) -> StubProvider:
        self._stub = StubProvider(
            token_config=self._token_config,
            query_server=self._query_server,
            deployment_tag=self._deployment_tag,
            skip_api_server=self._skip_api_server,
            additional_headers=self._additional_headers,
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

    def call_sql_stub(self, fn: Callable[[SqlServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.sql_stub)

    def call_dataframe_stub(self, fn: Callable[[DataFrameServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.dataframe_stub)

    def call_model_stub(self, fn: Callable[[ModelRegistryServiceStub], T]) -> T:
        return self._retry_callable(fn, lambda: self._stub.model_stub)

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
    ) -> online_query_pb2.OnlineQueryBulkResponse:
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
        return self._stub_refresher.call_query_stub(
            lambda x: x.OnlineQueryBulk(
                request,
                timeout=request_timeout,
                metadata=_canonicalize_headers(headers),
            )
        )

    def online_query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
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
    ) -> BulkOnlineQueryResult:
        response, call = self._online_query_bulk_grpc_request(
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
        )
        return OnlineQueryConverter.online_query_bulk_response_decode(
            response, trace_id=get_trace_id_from_response(call)
        )

    def _online_query_bulk_grpc_request(
        self,
        *,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
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
        input: Mapping[FeatureReference, Sequence[Any]] | DataFrame,
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
        inputs_bytes = get_features_feather_bytes(
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
            inputs_feather=inputs_bytes,
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

    def run_sql(self, sql: str):
        return self._stub_refresher.call_sql_stub(lambda x: x.ExecuteSqlQuery(ExecuteSqlQueryRequest(query=sql)))

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
                    metadata=dict(model_version_resp.model_version.metadata),
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

    @staticmethod
    def _build_tabular_schema(column_dtypes: Mapping[str, Any]) -> _model_artifact_pb2.TabularSchema:
        """
        Build a TabularSchema from a dictionary of column names to dtypes.

        Parameters
        ----------
        column_dtypes : dict
            Dictionary mapping column names to their data types.
            Data types can be PyArrow types or Python types (str, int, float, bool).

        Returns
        -------
        TabularSchema
            A protobuf TabularSchema object

        Examples
        --------
        >>> import pyarrow as pa
        >>> schema = ChalkGRPCClient._build_tabular_schema({
        ...     'alcohol': pa.float64(),
        ...     'malic_acid': pa.float64(),
        ...     'ash': pa.float64(),
        ... })
        """
        import pyarrow as pa

        from chalk.features._encoding.converter import PrimitiveFeatureConverter

        tabular_schema = _model_artifact_pb2.TabularSchema()

        for col_name, dtype in column_dtypes.items():
            # Convert to PyArrow type if needed
            if not isinstance(dtype, pa.DataType):
                # Handle Python types
                if dtype == str:
                    pa_dtype = pa.string()
                elif dtype == int:
                    pa_dtype = pa.int64()
                elif dtype == float:
                    pa_dtype = pa.float64()
                elif dtype == bool:
                    pa_dtype = pa.bool_()
                else:
                    raise ValueError(f"Unsupported dtype {dtype} for column {col_name}")
            else:
                pa_dtype = dtype

            # Convert PyArrow dtype to protobuf Arrow type
            proto_arrow_type = PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(pa_dtype)

            # Create TabularSpec for this column
            column_spec = _model_artifact_pb2.TabularSpec(name=col_name, dtype=proto_arrow_type)

            tabular_schema.columns.append(column_spec)

        return tabular_schema

    @staticmethod
    def _build_tensor_schema(tensor_specs: List[Tuple[List[int], Any]]) -> _model_artifact_pb2.TensorSchema:
        """
        Build a TensorSchema from a list of (shape, dtype) pairs.

        Parameters
        ----------
        tensor_specs : list of tuple
            List of (shape, dtype) tuples where:
            - shape is a list of integers representing tensor dimensions
            - dtype is a PyArrow type or Python type (str, int, float, bool)

        Returns
        -------
        TensorSchema
            A protobuf TensorSchema object

        Examples
        --------
        >>> import pyarrow as pa
        >>> schema = ChalkGRPCClient._build_tensor_schema([
        ...     ([224, 224, 3], pa.float32()),  # RGB image tensor
        ...     ([100], pa.float64()),          # Feature vector
        ... ])
        """
        import pyarrow as pa

        from chalk.features._encoding.converter import PrimitiveFeatureConverter

        tensor_schema = _model_artifact_pb2.TensorSchema()

        for shape, dtype in tensor_specs:
            # Convert to PyArrow type if needed
            if not isinstance(dtype, pa.DataType):
                # Handle Python types
                if dtype == str:
                    pa_dtype = pa.string()
                elif dtype == int:
                    pa_dtype = pa.int64()
                elif dtype == float:
                    pa_dtype = pa.float64()
                elif dtype == bool:
                    pa_dtype = pa.bool_()
                else:
                    raise ValueError(f"Unsupported dtype {dtype} for tensor")
            else:
                pa_dtype = dtype

            # Convert PyArrow dtype to protobuf Arrow type
            proto_arrow_type = PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(pa_dtype)

            # Create TensorSpec
            tensor_spec = _model_artifact_pb2.TensorSpec(dtype=proto_arrow_type, shape=shape)

            tensor_schema.tensors.append(tensor_spec)

        return tensor_schema

    def register_model(
        self,
        name: str,
        description: str,
        metadata: Mapping[str, Any],
    ) -> RegisterModelResponse:
        """
        Register a model in the Chalk model registry.

        Parameters
        ----------
        name : str
            Unique name for the model
        description : str
            Description of the model's purpose and functionality
        metadata : Mapping[str, Any]
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
        >>> client.register_model(
        ...     name="RiskModel",
        ...     description="Credit risk assessment model using transaction history",
        ...     metadata={
        ...         "accuracy": 0.94,
        ...         "training_date": "2024-01-15"
        ...     }
        ... )
        """
        metadata_converted: Dict[str, struct_pb2.Value] = {}

        for k, v in metadata.items():
            converted_v = struct_pb2.Value()
            if isinstance(v, str):
                converted_v.string_value = v
            elif isinstance(v, (int, float)):
                converted_v.number_value = v
            elif isinstance(v, bool):
                converted_v.bool_value = v
            metadata_converted[k] = converted_v

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
        model_type: ModelType,
        model_encoding: Optional[ModelEncoding] = None,
        aliases: Optional[List[str]] = None,
        model: Optional[Any] = None,
        model_paths: Optional[List[str]] = None,
        additional_files: Optional[Mapping[str, str]] = None,
        input_schema: Optional[Any] = None,
        output_schema: Optional[Any] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        input_features: Optional[list[str]] = None,
        output_features: Optional[list[str]] = None,
    ) -> RegisterModelVersionResponse:
        """
        Register a model in the Chalk model registry.

        Parameters
        ----------
        name : str
           Unique name for the model
        aliases : list of str, optional
           List of version aliases (e.g., ["v1.0", "latest"])
        model_paths : list of str, optional
           Paths to model files (for file-based registration)
        model : object, optional
           Python model object (for object-based registration)
        additional_files : list of str, optional
           Additional files needed for inference (tokenizers, configs, etc.)
        model_type : ModelType
           Type of model framework
        model_encoding : ModelEncoding, optional
           Serialization format
        input_schema : dict, list, or Any
           Definition of the input schema. Can be:
           - dict: Dictionary mapping column names to dtypes for tabular data
           - list: List of (shape, dtype) tuples for tensor data
        output_schema : dict, list, or Any
           Definition of the output schema. Can be:
           - dict: Dictionary mapping column names to dtypes for tabular data
           - list: List of (shape, dtype) tuples for tensor data
        metadata : dict, optional
           Additional metadata dictionary containing framework info,
           training details, performance metrics, etc.
        input_features : FeatureReference, str, optional
            The features to be used as inputs to the model.
            For example, `[User.message]`. Features can also be expressed as snakecased strings,
            e.g. `["user.message"]`
        output_features : FeatureReference, str, optional
            The features to be used as outputs to the model.
            For example, `[User.is_spam]`. Features can also be expressed as snakecased strings,
            e.g. `["user.is_spam"]`
        Returns
        -------
        ModelVersion
           The registered model version object

        Examples
        --------
        Register from Python object:

        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model=trained_sklearn_model,
        ...     model_type="pytorch",
        ... )

        Register from local files:

        >>> from chalk.client import ChalkClient
        >>> import pyarrow as pa
        >>> client = ChalkClient()
        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model_paths=["./model.pth"],
        ...     model_type="pytorch",
        ...     input_schema=pa.large_string(),
        ...     output_schema=pa.float32()
        ... )

        Register from s3 path:

        >>> client.register_model_version(
        ...     name="RiskModel",
        ...     model_paths=["s3://my-bucket/path/to/model.pth"],
        ...     model_type="pytorch",
        ... )
        """
        model_upload_paths: List[_model_artifact_pb2.ModelFile] = []
        additional_file_upload_path: List[_model_artifact_pb2.ModelFile] = []
        temp_files_to_cleanup: List[str] = []

        if input_schema is None and input_features is None:
            raise ValueError(
                "You must specify at least one of (input_schema, input_features) to register a model version."
            )
        if output_schema is None and output_features is None:
            raise ValueError(
                "You must specify at least one of (output_schema, output_features) to register a model version."
            )

        try:
            metadata_converted: Dict[str, struct_pb2.Value] = {}
            if metadata is not None:
                for k, v in metadata.items():
                    converted_v = struct_pb2.Value()
                    if isinstance(v, str):
                        converted_v.string_value = v
                    elif isinstance(v, (int, float)):
                        converted_v.number_value = v
                    elif isinstance(v, bool):
                        converted_v.bool_value = v
                    metadata_converted[k] = converted_v

            if model_paths is None:
                if model is None:
                    raise ValueError("Failed to register model. Please specify a model or model_paths.")

                tmp_dir = tempfile.mkdtemp()

                if model_type == ModelType.PYTORCH:
                    try:
                        import torch
                    except ImportError:
                        raise ImportError("Please install PyTorch to save PyTorch models.")
                    model_path = os.path.join(tmp_dir, "model.pth")

                    torch.save(model, model_path)  # Save entire model to support torch.load()

                    model_encoding = ModelEncoding.PICKLE

                elif model_type == ModelType.SKLEARN:
                    try:
                        import joblib
                    except ImportError:
                        raise ImportError("Please install joblib to save sklearn models.")
                    model_path = os.path.join(tmp_dir, "model.pkl")
                    joblib.dump(model, model_path)
                    model_encoding = ModelEncoding.PICKLE

                elif model_type == ModelType.TENSORFLOW:
                    model_path = os.path.join(tmp_dir, "model.h5")
                    model.save(model_path)
                    model_encoding = ModelEncoding.HDF5

                elif model_type == ModelType.XGBOOST:
                    model_path = os.path.join(tmp_dir, "model.json")
                    model.save_model(model_path)
                    model_encoding = ModelEncoding.JSON

                elif model_type == ModelType.LIGHTGBM:
                    model_path = os.path.join(tmp_dir, "model.txt")
                    model.save_model(model_path)
                    model_encoding = ModelEncoding.TEXT

                elif model_type == ModelType.CATBOOST:
                    model_path = os.path.join(tmp_dir, "model.cbm")
                    model.save_model(model_path)
                    model_encoding = ModelEncoding.CBM

                elif model_type == ModelType.ONNX:
                    model_path = os.path.join(tmp_dir, "model.onnx")
                    model.save_model(model_path)
                    model_encoding = ModelEncoding.PROTOBUF

                else:
                    raise NotImplementedError(
                        f"Unsupported model type: {model_type}; Please save the model to a file and register with "
                        + "explicit model_paths or contact Chalk Support."
                    )

                model_paths = [model_path]
                temp_files_to_cleanup.append(model_path)

            else:
                if model is not None:
                    raise ValueError(
                        "Failed to register model. Ambiguous model, can't specify both model_paths and model."
                    )
                if model_encoding is None:
                    raise ValueError("Failed to register model. Please specify a model encoding if using model_paths.")

            input_model_schema = _model_artifact_pb2.ModelSchema()
            if input_schema is not None:
                if isinstance(input_schema, dict):
                    input_model_schema.tabular.CopyFrom(self._build_tabular_schema(input_schema))
                elif isinstance(input_schema, list):
                    input_model_schema.tensor.CopyFrom(self._build_tensor_schema(input_schema))
                else:
                    raise ValueError(f"Invalid input_schema: {input_schema}")

            output_model_schema = _model_artifact_pb2.ModelSchema()
            if output_schema is not None:
                if isinstance(output_schema, dict):
                    output_model_schema.tabular.CopyFrom(self._build_tabular_schema(output_schema))
                elif isinstance(output_schema, list):
                    output_model_schema.tensor.CopyFrom(self._build_tensor_schema(output_schema))
                else:
                    raise ValueError(f"Invalid output_schema: {output_schema}")

            all_files_to_process: Dict[str, str] = {}  # map of filename -> local_path
            model_file_names: List[str] = []

            for model_path in model_paths:
                filename = os.path.basename(model_path)
                all_files_to_process[filename] = model_path
                model_file_names.append(filename)

            additional_file_mapping: Dict[str, str] = {}  # map of filename -> file_type
            if additional_files is not None:
                for file_type, file_path in additional_files.items():
                    filename = os.path.basename(file_path)
                    all_files_to_process[filename] = file_path
                    additional_file_mapping[filename] = file_type

            presigned_s3_response: ModelUploadUrlResponse = self._get_model_artifact_presigned_s3(
                model_paths=list(all_files_to_process.keys())
            )

            try:
                import boto3
            except ImportError:
                raise ImportError("Please install boto3 to enable model registration.")

            aws_profile = os.environ.get("AWS_PROFILE")
            aws_region = os.environ.get("AWS_REGION")

            session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
            s3_client = session.client("s3")

            for filename, local_or_s3_path in all_files_to_process.items():
                presigned_url = presigned_s3_response.upload_urls[filename]
                parsed_path = urlparse(local_or_s3_path)

                filesize_kb: int
                file_hash: bytes

                if parsed_path.scheme == "s3":
                    src_bucket = parsed_path.netloc
                    src_key = parsed_path.path.lstrip("/")
                    try:
                        response = s3_client.get_object(Bucket=src_bucket, Key=src_key)
                        file_data = response["Body"].read()

                        file_hash = hashlib.sha256(file_data).digest()
                        filesize_kb = ceil(response["ContentLength"] / 1024.0)

                        put_response = requests.put(
                            presigned_url,
                            data=file_data,
                            headers={"Content-Type": response.get("ContentType", "application/octet-stream")},
                        )

                        if put_response.status_code != 200:
                            raise RuntimeError(
                                f"Failed to upload to presigned URL for {filename}: "
                                + f"{put_response.status_code} {put_response.text}"
                            )
                    except Exception as e:
                        raise RuntimeError(f"Unable to get object from {local_or_s3_path}. {e}")
                elif parsed_path.scheme == "" or parsed_path.scheme == "file":

                    def _validate_local_path(path: str):
                        abs_path = os.path.abspath(path)
                        if ".." in os.path.relpath(abs_path, start=os.getcwd()).split(os.sep):
                            if not os.path.commonpath([abs_path, tmp_dir]) == tmp_dir:
                                raise ValueError(f"Unsafe file path: {path}")
                        if not os.path.isfile(abs_path):
                            raise FileNotFoundError(f"Local file not found: {path}")
                        return abs_path

                    try:
                        safe_path = _validate_local_path(local_or_s3_path)
                        with open(safe_path, "rb") as f:
                            file_data = f.read()

                        file_hash = hashlib.sha256(file_data).digest()
                        filesize_kb = ceil(os.path.getsize(local_or_s3_path) / 1024.0)

                        put_response = requests.put(presigned_url, data=file_data)

                        if put_response.status_code != 200:
                            raise RuntimeError(
                                f"Failed to upload local file {local_or_s3_path} to presigned URL: "
                                + f"{put_response.status_code} {put_response.text}"
                            )

                    except Exception as e:
                        raise RuntimeError(f"Failed to upload local file {local_or_s3_path}: {e}")
                else:
                    raise ValueError(f"Unsupported file path format: {local_or_s3_path}")

                if filename in model_file_names:
                    model_upload_paths.append(
                        _model_artifact_pb2.ModelFile(
                            name=filename,
                            size_kb=filesize_kb,
                            file_hash=file_hash,
                        )
                    )
                else:
                    additional_file_upload_path.append(
                        _model_artifact_pb2.ModelFile(
                            name=filename,
                            size_kb=filesize_kb,
                            file_hash=file_hash,
                        )
                    )
            try:
                resp: CreateModelVersionResponse = self._stub_refresher.call_model_stub(
                    lambda x: x.CreateModelVersion(
                        CreateModelVersionRequest(
                            model_name=name,
                            model_artifact_id=presigned_s3_response.model_artifact_id,
                            model_artifact=_model_artifact_pb2.ModelArtifactSpec(
                                model_files=model_upload_paths,
                                additional_files=additional_file_upload_path,
                                model_type=model_type,
                                model_encoding=model_encoding,
                                model_signature=_model_artifact_pb2.ModelSignature(
                                    inputs=input_model_schema,
                                    outputs=output_model_schema,
                                ),
                                input_features=input_features,
                                output_features=output_features,
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
                    metadata=dict(resp.model_version.metadata),
                    created_by=resp.model_version.created_by,
                    created_at=resp.model_version.created_at.ToDatetime(),
                )
            except grpc.RpcError as e:
                raise RuntimeError(f"Could not register model version. {e.details()}")

        finally:
            import shutil

            for temp_path in temp_files_to_cleanup:
                try:
                    if os.path.isfile(temp_path):
                        os.remove(temp_path)
                    elif os.path.isdir(temp_path):
                        shutil.rmtree(temp_path)
                    temp_dir = os.path.dirname(temp_path)
                    if temp_dir and os.path.exists(temp_dir) and temp_dir.startswith(tempfile.gettempdir()):
                        shutil.rmtree(temp_dir)
                except Exception:
                    pass

    def create_model_training_job(
        self,
        train_fn: Callable[[Optional[Mapping[str, Any]]], bool],
        model_name: str,
        dataset_name: str,
        config: Optional[Mapping[str, Any]] = None,
        resources: Optional[ResourceRequests] = None,
    ) -> CreateModelTrainingJobResponse:
        return self._stub_refresher.call_offline_query_stub(
            lambda x: x.CreateModelTrainingJob(
                CreateModelTrainingJobRequest(
                    training_job_request=offline_query_pb2.OfflineQueryRequest(
                        dataset_name=dataset_name,
                    )
                )
            )
        )
