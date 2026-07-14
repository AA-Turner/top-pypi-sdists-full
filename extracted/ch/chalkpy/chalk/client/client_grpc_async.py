from __future__ import annotations

import datetime as dt
import json
import random
import typing
import warnings
from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, TypeVar, Union, cast

import grpc
import grpc.aio

from chalk import DataFrame, EnvironmentId, chalk_logger
from chalk._gen.chalk.common.v1 import online_query_pb2, upload_features_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery, UploadFeaturesBulkRequest
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.graph.v1.graph_pb2 import Graph
from chalk._gen.chalk.server.v1.auth_pb2 import GetTokenRequest
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.graph_pb2 import GetGraphRequest, GetGraphResponse
from chalk._gen.chalk.server.v1.graph_pb2_grpc import GraphServiceStub
from chalk._gen.chalk.server.v1.offline_queries_pb2_grpc import OfflineQueryMetadataServiceStub
from chalk._gen.chalk.server.v1.scheduled_query_pb2_grpc import ScheduledQueryServiceStub
from chalk._gen.chalk.server.v1.scheduler_pb2_grpc import SchedulerServiceStub
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk.client.client_grpc import _canonicalize_headers  # pyright: ignore[reportPrivateUsage]
from chalk.client.client_grpc import _inject_trace_context_metadata  # pyright: ignore[reportPrivateUsage]
from chalk.client.client_grpc import _parse_uri_for_engine  # pyright: ignore[reportPrivateUsage]
from chalk.client.client_grpc import get_features_feather_bytes
from chalk.client.client_headers import (
    CHALK_DEPLOYMENT_TAG_HEADER_LOWERCASE,
    CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE,
    CHALK_ENV_ID_HEADER_LOWERCASE,
    CHALK_GRPC_TRACE_ID_HEADER,
)
from chalk.client.client_impl import _validate_context_dict  # pyright: ignore[reportPrivateUsage]
from chalk.client.exc import ChalkAuthException
from chalk.client.models import (
    BulkOnlineQueryResponse,
    BulkOnlineQueryResult,
    BulkUploadFeaturesResult,
    FeatureReference,
    OnlineQuery,
    OnlineQueryResponse,
    UploadFeaturesResponse,
    resolve_multi_query_query_name,
)
from chalk.client.serialization.protos import ChalkErrorConverter, OnlineQueryConverter, UploadFeaturesBulkConverter
from chalk.config.auth_config import TokenConfig, load_token
from chalk.features import live_updates
from chalk.features._encoding.inputs import GRPC_ENCODE_OPTIONS, InputSchemaHint
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.features.tag import DeploymentId
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils.grpc import (
    AsyncAuthenticatedChalkClientInterceptor,
    AsyncTokenRefresher,
    AsyncUnauthenticatedChalkClientInterceptor,
)
from chalk.utils.tracing import current_or_new_trace_context, current_trace_context, safe_trace

if TYPE_CHECKING:
    from google.protobuf import timestamp_pb2
    from pyarrow import RecordBatch, Table


T = TypeVar("T")
U = TypeVar("U")

# Channel options for grpc.aio — excludes the sync-only SingleThreadedUnaryStream hint
_ASYNC_CHANNEL_OPTIONS: Dict[str, str | int] = {
    "grpc.max_send_message_length": 1024 * 1024 * 100,  # 100MB
    "grpc.max_receive_message_length": 1024 * 1024 * 100,  # 100MB
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


async def get_trace_id_from_async_response(call: Any) -> Optional[str]:
    for k, v in (await call.trailing_metadata()) or []:
        if k == CHALK_GRPC_TRACE_ID_HEADER:
            if isinstance(v, bytes):
                v = v.decode("utf-8")
            assert isinstance(v, str)
            return v
    return None


class _Bootstrap(typing.NamedTuple):
    """Bootstrap data from the initial token exchange, used to construct AsyncStubProvider."""

    initial_token: Any
    environment_id: str
    server_host: str
    query_server: Optional[str]


class AsyncStubProvider:
    def __init__(
        self,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
        channel_options: List[tuple[str, str | int]] | None = None,
        _bootstrap: Optional[_Bootstrap] = None,
    ):
        super().__init__()
        additional_headers_nonempty: List[tuple[str, str]] = [] if additional_headers is None else additional_headers
        channel_options_merged: Dict[str, str | int] = _ASYNC_CHANNEL_OPTIONS.copy()
        if channel_options:
            channel_options_merged.update(dict(channel_options))
        channel_options_list = list(channel_options_merged.items())

        async_token_refresher: AsyncTokenRefresher | None = None

        self._auth_channel: Optional[grpc.aio.Channel] = None
        if skip_api_server:
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
            self._server_channel: Optional[grpc.aio.Channel] = None
        else:
            if _bootstrap is None:
                raise RuntimeError("AsyncStubProvider must be constructed via AsyncStubProvider.create().")
            initial_token = _bootstrap.initial_token
            self.environment_id = _bootstrap.environment_id
            server_host = _bootstrap.server_host
            query_server = _bootstrap.query_server

            # aio channel for server (used to create the async auth stub and authenticated server calls)
            self._auth_channel: Optional[grpc.aio.Channel] = (
                grpc.aio.insecure_channel(target=server_host, options=channel_options_list)
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.aio.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options_list,
                )
            )
            _aio_auth_stub = AuthServiceStub(self._auth_channel)  # pyright: ignore[reportArgumentType]

            async_token_refresher = AsyncTokenRefresher(
                initial_token=initial_token,
                async_auth_stub=_aio_auth_stub,
                client_id=token_config.clientId,
                client_secret=token_config.clientSecret,
            )

            server_interceptor = AsyncAuthenticatedChalkClientInterceptor(
                refresher=async_token_refresher,
                server="go-api",
                environment_id=self.environment_id,
                additional_headers=additional_headers_nonempty,
            )
            self._server_channel = (
                grpc.aio.insecure_channel(
                    target=server_host,
                    options=channel_options_list,
                    interceptors=[server_interceptor],  # pyright: ignore[reportArgumentType]
                )
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.aio.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options_list,
                    interceptors=[server_interceptor],  # pyright: ignore[reportArgumentType]
                )
            )

        engine_headers = additional_headers_nonempty + [(CHALK_DEPLOYMENT_TYPE_HEADER_LOWERCASE, "engine-grpc")]
        if deployment_tag is not None:
            engine_headers += [(CHALK_DEPLOYMENT_TAG_HEADER_LOWERCASE, deployment_tag)]

        engine_interceptor = (
            AsyncAuthenticatedChalkClientInterceptor(
                refresher=async_token_refresher,
                environment_id=self.environment_id,
                server="engine",
                additional_headers=engine_headers,
            )
            if async_token_refresher is not None
            else AsyncUnauthenticatedChalkClientInterceptor(
                server="engine",
                additional_headers=engine_headers + [(CHALK_ENV_ID_HEADER_LOWERCASE, self.environment_id)],
            )
        )

        self._engine_channel: Optional[grpc.aio.Channel] = None
        if query_server is not None:
            parsed_uri = _parse_uri_for_engine(query_server_uri=query_server)
            self._engine_channel = (
                grpc.aio.secure_channel(
                    target=parsed_uri.uri_without_scheme,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options_list,
                    interceptors=[engine_interceptor],  # pyright: ignore[reportArgumentType]
                )
                if parsed_uri.use_tls
                else grpc.aio.insecure_channel(
                    target=parsed_uri.uri_without_scheme,
                    options=channel_options_list,
                    interceptors=[engine_interceptor],  # pyright: ignore[reportArgumentType]
                )
            )

    @classmethod
    async def _async_bootstrap(
        cls,
        token_config: TokenConfig,
        query_server: Optional[str],
        channel_options_list: List[tuple],
        additional_headers_nonempty: List[tuple[str, str]],
    ) -> _Bootstrap:
        """Fetches the initial auth token via a temporary grpc.aio channel. Fully async."""
        server_host = token_config.apiServer or "api.chalk.ai"
        for pfx in ("https://", "http://", "www."):
            server_host = server_host.removeprefix(pfx)
        _temp_interceptor = AsyncUnauthenticatedChalkClientInterceptor(
            server="go-api",
            additional_headers=additional_headers_nonempty,
        )
        _temp_channel = (
            grpc.aio.insecure_channel(
                target=server_host,
                options=channel_options_list,
                interceptors=[_temp_interceptor],  # pyright: ignore[reportArgumentType]
            )
            if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
            else grpc.aio.secure_channel(
                target=server_host,
                credentials=grpc.ssl_channel_credentials(),
                options=channel_options_list,
                interceptors=[_temp_interceptor],  # pyright: ignore[reportArgumentType]
            )
        )
        try:
            _temp_auth_stub = AuthServiceStub(_temp_channel)  # pyright: ignore[reportArgumentType]
            initial_token = await _temp_auth_stub.GetToken(  # pyright: ignore[reportGeneralTypeIssues]
                GetTokenRequest(
                    client_id=token_config.clientId,
                    client_secret=token_config.clientSecret,
                    grant_type="client_credentials",
                )
            )
        finally:
            await _temp_channel.close(grace=None)
        environment_id = token_config.activeEnvironment or initial_token.primary_environment
        if not environment_id:
            raise ValueError("No environment specified")
        if environment_id not in initial_token.environment_id_to_name:
            lower_env_id = environment_id.lower()
            valid = [
                eid for eid, ename in initial_token.environment_id_to_name.items() if ename.lower() == lower_env_id
            ]
            if len(valid) > 1:
                raise ValueError(f"Multiple environments with name {environment_id}: {valid}")
            elif len(valid) == 0:
                raise ValueError(f"No environment with name {environment_id}: {initial_token.environment_id_to_name}")
            else:
                environment_id = valid[0]
        query_server = query_server or initial_token.grpc_engines.get(environment_id, None)
        return _Bootstrap(
            initial_token=initial_token,
            environment_id=environment_id,
            server_host=server_host,
            query_server=query_server,
        )

    @classmethod
    async def create(
        cls,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
        channel_options: List[tuple[str, str | int]] | None = None,
    ) -> "AsyncStubProvider":
        additional_headers_nonempty: List[tuple[str, str]] = additional_headers or []
        channel_options_merged: Dict[str, str | int] = _ASYNC_CHANNEL_OPTIONS.copy()
        if channel_options:
            channel_options_merged.update(dict(channel_options))
        channel_options_list = list(channel_options_merged.items())
        bootstrap: Optional[_Bootstrap] = None
        if not skip_api_server:
            bootstrap = await cls._async_bootstrap(
                token_config, query_server, channel_options_list, additional_headers_nonempty
            )
        return cls(
            token_config=token_config,
            query_server=query_server,
            deployment_tag=deployment_tag,
            skip_api_server=skip_api_server,
            additional_headers=additional_headers,
            channel_options=channel_options,
            _bootstrap=bootstrap,
        )

    async def close(self):
        if self._auth_channel is not None:
            await self._auth_channel.close(grace=None)
        if self._server_channel is not None:
            await self._server_channel.close(grace=None)
        if self._engine_channel is not None:
            await self._engine_channel.close(grace=None)

    @cached_property
    def query_stub(self) -> QueryServiceStub:
        if self._engine_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return QueryServiceStub(self._engine_channel)  # pyright: ignore[reportArgumentType]

    @cached_property
    def graph_stub(self) -> GraphServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return GraphServiceStub(self._server_channel)  # pyright: ignore[reportArgumentType]

    @cached_property
    def team_stub(self) -> TeamServiceStub:
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return TeamServiceStub(self._server_channel)  # pyright: ignore[reportArgumentType]

    @cached_property
    def offline_query_stub(self) -> OfflineQueryMetadataServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return OfflineQueryMetadataServiceStub(self._server_channel)  # pyright: ignore[reportArgumentType]

    @cached_property
    def scheduled_query_stub(self) -> SchedulerServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return SchedulerServiceStub(self._server_channel)  # pyright: ignore[reportArgumentType]

    @cached_property
    def scheduled_query_run_stub(self) -> ScheduledQueryServiceStub:
        if self._server_channel is None:
            raise ValueError(
                "The GRPC engine service is not available. If you would like to set up a GRPC service, please contact Chalk."
            )
        return ScheduledQueryServiceStub(self._server_channel)  # pyright: ignore[reportArgumentType]


class AsyncStubRefresher:
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

    @classmethod
    async def create(
        cls,
        token_config: TokenConfig,
        query_server: str | None = None,
        deployment_tag: str | None = None,
        skip_api_server: bool = False,
        additional_headers: List[tuple[str, str]] | None = None,
        channel_options: List[tuple[str, str | int]] | None = None,
    ) -> "AsyncStubRefresher":
        instance = cls(
            token_config=token_config,
            query_server=query_server,
            deployment_tag=deployment_tag,
            skip_api_server=skip_api_server,
            additional_headers=additional_headers,
            channel_options=channel_options,
        )
        instance._stub = await AsyncStubProvider.create(
            token_config=token_config,
            query_server=query_server,
            deployment_tag=deployment_tag,
            skip_api_server=skip_api_server,
            additional_headers=additional_headers,
            channel_options=channel_options,
        )
        return instance

    async def _async_create_stub(self) -> AsyncStubProvider:
        return await AsyncStubProvider.create(
            token_config=self._token_config,
            query_server=self._query_server,
            deployment_tag=self._deployment_tag,
            skip_api_server=self._skip_api_server,
            additional_headers=self._additional_headers,
            channel_options=self._channel_options,
        )

    async def close(self):
        await self._stub.close()

    async def _retry_callable(self, fn: Callable[[T], Any], get_service: Callable[[], T]) -> Any:
        try:
            return await fn(get_service())
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                details = (e.details() or "").lower()
                if "fd shutdown" in details or "goaway" in details:
                    chalk_logger.info("Detected FD shutdown; retrying connection: %s", details)
                    old_stub = self._stub
                    self._stub = await self._async_create_stub()
                    await old_stub.close()
                    return await fn(get_service())
            raise

    async def call_query_stub(self, fn: Callable[[QueryServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.query_stub)

    async def call_graph_stub(self, fn: Callable[[GraphServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.graph_stub)

    async def call_team_stub(self, fn: Callable[[TeamServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.team_stub)

    async def call_offline_query_stub(self, fn: Callable[[OfflineQueryMetadataServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.offline_query_stub)

    async def call_scheduled_query_stub(self, fn: Callable[[SchedulerServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.scheduled_query_stub)

    async def call_scheduled_query_run_stub(self, fn: Callable[[ScheduledQueryServiceStub], Any]) -> Any:
        return await self._retry_callable(fn, lambda: self._stub.scheduled_query_run_stub)

    @property
    def environment_id(self) -> str | None:
        return self._stub.environment_id


class AsyncChalkGRPCClient:
    """The `AsyncChalkGRPCClient` is an async Python interface for interacting with Chalk gRPC servers.

    Uses native `grpc.aio` for true asyncio-compatible gRPC calls, supporting high-concurrency
    use cases without thread overhead.
    """

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
        """Create an async Chalk gRPC client.

        Use as an async context manager (``async with AsyncChalkGRPCClient(...) as client``)
        or via the :meth:`create` factory (``client = await AsyncChalkGRPCClient.create(...)``).
        Both paths perform an async token exchange before the client is ready.

        If no arguments are provided, credentials and configuration are loaded
        from the local Chalk token file (created by ``chalk login``).

        Parameters
        ----------
        environment
            The target Chalk environment ID. If not provided, uses the active
            environment from the local token config.
        client_id
            The client ID for authentication. If not provided, loaded from the
            local token config.
        client_secret
            The client secret for authentication. If not provided, loaded from
            the local token config.
        api_server
            The URL of the Chalk API server. Defaults to the value in the local
            token config.
        deployment_tag
            If specified, routes queries to the deployment with this tag.
        additional_headers
            Extra HTTP headers to include with every request.
        query_server
            Override the query server URL. If not provided, the query server
            is resolved from the API server.
        input_compression
            Compression algorithm to use for query inputs. One of "lz4",
            "zstd", or "uncompressed". Defaults to "lz4".
        channel_options
            Additional gRPC channel options passed directly to the underlying
            gRPC channel.
        """
        super().__init__()
        self._input_compression: typing.Literal["lz4", "zstd", "uncompressed"] = input_compression

        environment_id = kwargs.get("environment_id", None)
        if environment is not None and environment_id is not None:
            raise ValueError("Both environment and environment_id specified; only pass environment.")
        if environment_id is not None:
            environment = EnvironmentId(environment_id)

        if CHALK_IMPORT_FLAG.get() is True:
            raise RuntimeError(
                "Attempting to instantiate a Chalk client while importing source modules is forbidden. "
                + "Please exclude this file from import using your `.chalkignore` file "
                + "(see https://docs.chalk.ai/cli/apply), or wrap this query in a function that is not called upon import."
            )

        self._environment = environment
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_server = api_server
        self._deployment_tag = deployment_tag
        self._additional_headers = additional_headers
        self._query_server = query_server
        self._channel_options = channel_options
        self._skip_api_server: bool = kwargs.get("_skip_api_server", False)

    _INPUT_ENCODE_OPTIONS = GRPC_ENCODE_OPTIONS

    async def _async_init(self) -> None:
        token_config = load_token(
            client_id=self._client_id,
            client_secret=self._client_secret,
            active_environment=self._environment,
            api_server=self._api_server,
            skip_cache=False,
        )
        if token_config is None:
            raise ChalkAuthException()
        self._stub_refresher = await AsyncStubRefresher.create(
            token_config=token_config,
            query_server=self._query_server,
            deployment_tag=self._deployment_tag,
            additional_headers=self._additional_headers,
            skip_api_server=self._skip_api_server,
            channel_options=self._channel_options,
        )

    async def close(self) -> None:
        """Close the client and release all underlying gRPC channel resources.

        Must be called when the client is no longer needed if it was constructed
        via :meth:`create`. Not required when using the client as an async context
        manager (``async with``), which closes automatically on exit.
        """
        await self._stub_refresher.close()

    async def __aenter__(self):
        await self._async_init()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        await self._stub_refresher.close()

    @classmethod
    async def create(
        cls,
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
    ) -> "AsyncChalkGRPCClient":
        """Async factory: performs the token exchange and returns a ready-to-use client.

        Prefer this over ``async with`` when you need a client that outlives a single
        block. Remember to call ``await client.close()`` when done.

        Accepts the same parameters as :meth:`__init__`.
        """
        instance = cls(
            environment=environment,
            client_id=client_id,
            client_secret=client_secret,
            api_server=api_server,
            deployment_tag=deployment_tag,
            additional_headers=additional_headers,
            query_server=query_server,
            input_compression=input_compression,
            channel_options=channel_options,
            **kwargs,
        )
        await instance._async_init()
        return instance

    async def ping_engine(self, num: Optional[int] = None) -> int:
        """Ping the engine to check if it is alive."""

        async def fn(stub: QueryServiceStub):
            return await cast(
                Any, stub.Ping(query_server_pb2.PingRequest(num=num if num is not None else random.randint(0, 999)))
            )

        return (await self._stub_refresher.call_query_stub(fn)).num

    async def online_query(
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
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> OnlineQueryResponse:
        """Compute feature values using online resolvers.

        Parameters
        ----------
        input
            A mapping of feature references to input values for a single row.
        output
            The features to compute and return.
        now
            Override the current time for this query. Useful for backtesting.
        staleness
            Maximum acceptable staleness for each output feature, e.g.
            ``{"user.score": "10m"}``.
        tags
            If provided, only resolvers with at least one matching tag are used.
        correlation_id
            A caller-supplied ID for correlating this query with external systems.
        query_name
            A name for this query, used for monitoring and metrics.
        query_name_version
            The version of the named query.
        include_meta
            If True, include metadata about resolver execution in the response.
        meta
            Arbitrary key-value metadata to attach to the query.
        explain
            If True, return a query plan explanation instead of executing.
        store_plan_stages
            If True, persist intermediate plan stage results for debugging.
        value_metrics_tag_by_features
            Features whose values should be used as metric tags.
        encoding_options
            Options controlling how feature values are encoded in the request.
        required_resolver_tags
            If provided, only resolvers with all of these tags will be used.
        planner_options
            Advanced options passed to the query planner.
        request_timeout
            Timeout in seconds for the gRPC request.
        headers
            Additional headers to include with this specific request.
        query_context
            Key-value context propagated to resolvers during this query.
        trace
            If True, enable distributed tracing for this query.
        input_schema_hint
            Pins the wire schema of has-many inputs to the listed columns, e.g.
            ``{User.transactions: [Transaction.id, Transaction.amount]}``, so the schema is
            identical whether or not the given has rows. See
            :meth:`ChalkGRPCClient.online_query` for full semantics.
        """
        bulk_response = await self._online_query_grpc_request(
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
            input_schema_hint=input_schema_hint,
        )
        return OnlineQueryConverter.online_query_bulk_response_decode_to_single(bulk_response)

    async def query(
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
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> OnlineQueryResponse:
        """A synonym for :meth:`online_query`.

        See :meth:`online_query` for the full documentation.
        """
        return await self.online_query(
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
            input_schema_hint=input_schema_hint,
        )

    async def _online_query_grpc_request(
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
        query_context: Mapping[str, Union[str, int, float, bool, None]] | str | None = None,
        trace: bool = False,
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
            metadata = _canonicalize_headers(headers)

            async def fn(stub: QueryServiceStub):
                return await cast(Any, stub.OnlineQueryBulk(request, timeout=request_timeout, metadata=metadata))

            return await self._stub_refresher.call_query_stub(fn)

    async def online_query_bulk(
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
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> BulkOnlineQueryResult:
        """Compute feature values for multiple rows using online resolvers.

        Either ``input`` or ``input_sql`` must be provided, but not both.

        Parameters
        ----------
        input
            A mapping of feature references to sequences of input values, one
            per row. Mutually exclusive with ``input_sql``.
        output
            The features to compute and return.
        now
            A sequence of timestamps overriding the current time for each row.
        staleness
            Maximum acceptable staleness for each output feature.
        tags
            If provided, only resolvers with at least one matching tag are used.
        correlation_id
            A caller-supplied ID for correlating this query with external systems.
        query_name
            A name for this query, used for monitoring and metrics.
        query_name_version
            The version of the named query.
        include_meta
            If True, include metadata about resolver execution in the response.
        meta
            Arbitrary key-value metadata to attach to the query.
        explain
            If True, return a query plan explanation instead of executing.
        store_plan_stages
            If True, persist intermediate plan stage results for debugging.
        encoding_options
            Options controlling how feature values are encoded in the request.
        required_resolver_tags
            If provided, only resolvers with all of these tags will be used.
        value_metrics_tag_by_features
            Features whose values should be used as metric tags.
        planner_options
            Advanced options passed to the query planner.
        request_timeout
            Timeout in seconds for the gRPC request.
        headers
            Additional headers to include with this specific request.
        query_context
            Key-value context propagated to resolvers during this query.
        input_sql
            A SQL query whose results are used as inputs. Mutually exclusive
            with ``input``.
        """
        if input is None and input_sql is None:
            raise TypeError("One of `input` or `input_sql` is required")
        if input is not None and input_sql is not None:
            raise TypeError("`input` and `input_sql` are mutually exclusive")
        if input_sql is not None and now is not None:
            raise TypeError(
                "When using `input_sql`, `now` is not allowed: instead, to provide a query time, you can have the SQL query output a column named `__ts__`"
            )

        response, call = await self._online_query_bulk_grpc_request(
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
        )
        return OnlineQueryConverter.online_query_bulk_response_decode(
            response, trace_id=await get_trace_id_from_async_response(call)
        )

    async def _online_query_bulk_grpc_request(
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
        input_schema_hint: Optional[InputSchemaHint] = None,
    ) -> Tuple[online_query_pb2.OnlineQueryBulkResponse, Any]:
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
        trace_context = current_trace_context()
        if trace_context is not None:
            headers = _inject_trace_context_metadata(headers, trace_context)
        metadata = _canonicalize_headers(headers)

        async def fn(stub: QueryServiceStub):
            call = cast(Any, stub.OnlineQueryBulk(request, timeout=request_timeout, metadata=metadata))
            response = await call
            return response, call

        return await self._stub_refresher.call_query_stub(fn)

    async def multi_query(
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
        """Execute a series of independent online queries in parallel.

        Parameters
        ----------
        queries
            A list of :class:`OnlineQuery` objects to execute concurrently.
            Each query specifies its own inputs, outputs, and options.
        correlation_id
            A caller-supplied ID for correlating this request with external systems.
        query_name
            A name applied to all queries in this request, used for monitoring.
        query_name_version
            The version of the named query.
        include_meta
            If True, include metadata about resolver execution in each response.
        meta
            Arbitrary key-value metadata to attach to the request.
        explain
            If True, return query plan explanations instead of executing.
        store_plan_stages
            If True, persist intermediate plan stage results for debugging.
        value_metrics_tag_by_features
            Features whose values should be used as metric tags. Overrides
            per-query settings if provided.
        encoding_options
            Options controlling how feature values are encoded in the request.
        required_resolver_tags
            If provided, only resolvers with all of these tags will be used.
        planner_options
            Advanced options passed to the query planner.
        request_timeout
            Timeout in seconds for the gRPC request.
        headers
            Additional headers to include with this specific request.
        query_context
            Key-value context propagated to resolvers during this query.
        """
        requests: List[GenericSingleQuery] = []
        for query in queries:
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

        metadata = _canonicalize_headers(headers)

        async def fn(stub: QueryServiceStub):
            call = cast(
                Any,
                stub.OnlineQueryMulti(
                    online_query_pb2.OnlineQueryMultiRequest(queries=requests),
                    timeout=request_timeout,
                    metadata=metadata,
                ),
            )
            response = await call
            return response, call

        response, call = await self._stub_refresher.call_query_stub(fn)
        return OnlineQueryConverter.online_query_multi_response_decode(
            response, trace_id=await get_trace_id_from_async_response(call)
        )

    async def upload_features(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
        write_offline: bool = False,
        write_online: Optional[bool] = None,
    ) -> UploadFeaturesResponse:
        """Upload feature values to be inserted into the online and offline stores.

        Parameters
        ----------
        inputs
            A mapping of feature references to sequences of values to upload,
            or a DataFrame/Table/RecordBatch with feature columns.
        request_timeout
            Timeout in seconds for the gRPC request.
        headers
            Additional headers to include with this specific request.
        write_offline
            Whether to write features to the offline store. Defaults to False.
        write_online
            Whether to write features to the online store. Defaults to True when not set.
        """
        options = upload_features_pb2.UploadFeaturesOptions()
        if write_offline:
            options.write_offline = write_offline
        if write_online is not None:
            options.write_online = write_online
        request = upload_features_pb2.UploadFeaturesRequest(
            inputs_table=get_features_feather_bytes(inputs, self._INPUT_ENCODE_OPTIONS),
            options=options,
        )
        metadata = _canonicalize_headers(headers)

        async def fn(stub: QueryServiceStub):
            call = cast(Any, stub.UploadFeatures(request, timeout=request_timeout, metadata=metadata))
            response = await call
            return response, call

        response, call = await self._stub_refresher.call_query_stub(fn)
        trace_id = await get_trace_id_from_async_response(call)
        py_errors = [ChalkErrorConverter.chalk_error_decode(err) for err in response.errors]
        return UploadFeaturesResponse(errors=py_errors, trace_id=trace_id)

    async def upload_features_bulk(
        self,
        inputs: "Union[Mapping[FeatureReference, Sequence[Any]], DataFrame, Table, RecordBatch]",
        request_timeout: Optional[float] = None,
        headers: Mapping[str, str] | Sequence[tuple[str, str | bytes]] | None = None,
    ) -> BulkUploadFeaturesResult:
        """Upload feature values in bulk to the online and offline stores.

        Uses the bulk upload endpoint, which is more efficient than
        :meth:`upload_features` for large datasets.

        Parameters
        ----------
        inputs
            A mapping of feature references to sequences of values to upload,
            or a DataFrame/Table/RecordBatch with feature columns.
        request_timeout
            Timeout in seconds for the gRPC request.
        headers
            Additional headers to include with this specific request.
        """
        request = UploadFeaturesBulkRequest(
            inputs_feather=get_features_feather_bytes(inputs, self._INPUT_ENCODE_OPTIONS),
        )
        metadata = _canonicalize_headers(headers)

        async def fn(stub: QueryServiceStub):
            call = cast(Any, stub.UploadFeaturesBulk(request, timeout=request_timeout, metadata=metadata))
            response = await call
            return response, call

        response, call = await self._stub_refresher.call_query_stub(fn)
        return UploadFeaturesBulkConverter.upload_features_bulk_response_decode(
            response,
            trace_id=await get_trace_id_from_async_response(call),
        )

    async def get_graph(self, deployment: DeploymentId | None = None) -> Graph:
        """Fetch the feature graph for a deployment.

        Parameters
        ----------
        deployment
            The deployment ID to fetch the graph for. If not provided, returns
            the graph for the active deployment in the configured environment.
        """

        async def fn(stub: GraphServiceStub):
            return await cast(Any, stub.GetGraph(GetGraphRequest(deployment_id=deployment)))

        resp: GetGraphResponse = await self._stub_refresher.call_graph_stub(fn)
        return resp.graph

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
