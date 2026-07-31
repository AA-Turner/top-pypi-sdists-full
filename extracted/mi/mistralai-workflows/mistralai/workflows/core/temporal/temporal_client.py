import asyncio
import contextvars
import math
from typing import List, Type

import structlog
from pydantic import SecretStr
from temporalio.client import Client as TemporalClient
from temporalio.client import Interceptor
from temporalio.contrib.pydantic import PydanticPayloadConverter
from temporalio.converter import DataConverter, PayloadCodec, PayloadConverter
from temporalio.runtime import Runtime
from temporalio.service import ConnectConfig, HttpConnectProxyConfig
from temporalio.service import ServiceClient as TemporalServiceClient

from mistralai.workflows.core.auth import (
    TokenProvider,
    get_token_provider,
)
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.temporal.runtime_metrics import build_client_runtime
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import get_temporal_tracing_interceptors
from mistralai.workflows.exceptions import ErrorCode, WorkflowError, WorkflowsException

logger = structlog.get_logger(__name__)

DEFAULT_NAMESPACE = "default"

_worker_service_client: contextvars.ContextVar["TemporalServiceClient | None"] = contextvars.ContextVar(
    "worker_service_client", default=None
)


def set_worker_service_client(service_client: "TemporalServiceClient | None") -> None:
    _worker_service_client.set(service_client)


def get_worker_service_client() -> "TemporalServiceClient | None":
    return _worker_service_client.get()


# Fire this long after the provider's internal refresh point (exp - margin), so get_token() has already
# re-read the rotated token; also the wait when no new token is ready yet.
_TEMPORAL_TOKEN_REFRESH_DELAY_SECONDS = 5.0

# Retry the connection-token read at startup: the SA-token mount can briefly be empty/unreadable while
# the kubelet rotates it, and FileTokenProvider treats reads as retryable, so a blip shouldn't abort startup.
_TEMPORAL_TOKEN_STARTUP_READ_ATTEMPTS = 3
_TEMPORAL_TOKEN_STARTUP_READ_BACKOFF_SECONDS = 1.0


def _get_proxy_basic_auth(
    proxy_user: str | None,
    proxy_pass: SecretStr | None,
) -> tuple[str, str] | None:
    """
    Helper function to validate and return basic auth (user, password) for `HttpConnectProxyConfig`.
    Logs a warning when only one of user/pass is set instead of silently disabling auth.
    """
    user = (proxy_user or "").strip() or None
    pass_val = (proxy_pass.get_secret_value() if proxy_pass else "") or None
    if user and pass_val:
        return (user, pass_val)
    if (user is not None) != (pass_val is not None):
        logger.warning(
            "Incomplete proxy basic auth config, both user and pass must be set; ignoring auth",
            has_user=user is not None,
            has_pass=pass_val is not None,
        )
    return None


def _resolve_temporal_token() -> TokenProvider | None:
    """Resolve the Temporal bearer source: explicit ``config.temporal.api_key`` wins, else the SDK provider.

    ``get_token_provider`` already applies that precedence — a truthy ``explicit_key`` is wrapped as a
    ``StaticTokenProvider``, otherwise it falls back to the SA-token path then ``MISTRAL_API_KEY``.
    """
    return get_token_provider(config.temporal.api_key)


async def _read_temporal_token(provider: TokenProvider) -> str:
    """Read the Temporal connection bearer at startup, retrying transient mount failures.

    The SA-token file can briefly be empty/unreadable while the kubelet rotates it; FileTokenProvider
    treats reads as retryable, so a blip should retry rather than abort worker startup.
    """
    for attempt in range(1, _TEMPORAL_TOKEN_STARTUP_READ_ATTEMPTS + 1):
        try:
            return provider.get_token()
        except WorkflowError as exc:
            if attempt == _TEMPORAL_TOKEN_STARTUP_READ_ATTEMPTS:
                raise
            logger.warning(
                "failed to read temporal token at startup; retrying",
                attempt=attempt,
                **extract_error_context(exc),
            )
            await asyncio.sleep(_TEMPORAL_TOKEN_STARTUP_READ_BACKOFF_SECONDS)
    raise AssertionError("unreachable")


async def create_temporal_service_client(runtime: Runtime | None = None) -> TemporalServiceClient:
    # The worker passes its pre-built (buffered) runtime; pump-less callers get a direct-OTLP client runtime
    # (self-exporting, no drainer) — metrics for static creds / explicit endpoints, disabled under rotation.
    if runtime is None:
        runtime = build_client_runtime()
    logger.info(
        "creating temporal service client",
        url=config.temporal.server_url,
        tls=config.temporal.tls,
        runtime=runtime,
    )
    provider = _resolve_temporal_token()
    temporal_api_key = await _read_temporal_token(provider) if provider else None

    http_connect_proxy_config = None
    if config.temporal.http_proxy_target_host:
        basic_auth = _get_proxy_basic_auth(
            config.temporal.http_proxy_basic_auth_user,
            config.temporal.http_proxy_basic_auth_pass,
        )
        http_connect_proxy_config = HttpConnectProxyConfig(
            target_host=config.temporal.http_proxy_target_host,
            basic_auth=basic_auth,
        )
        logger.info(
            "using HTTP CONNECT proxy for temporal connection",
            proxy_target_host=config.temporal.http_proxy_target_host,
        )

    try:
        service_client = await TemporalServiceClient.connect(
            ConnectConfig(
                target_host=config.temporal.server_url,
                api_key=temporal_api_key or None,
                runtime=runtime,
                tls=config.temporal.tls,
                http_connect_proxy_config=http_connect_proxy_config,
            )
        )
    except Exception:
        raise WorkflowsException(
            code=ErrorCode.TEMPORAL_CONNECTION_ERROR, message="Fail to connect to Temporal Service Client"
        )
    logger.info("connected to temporal service client", url=config.temporal.server_url)
    return service_client


async def refresh_temporal_api_key(
    service_client: TemporalServiceClient,
    *,
    delay_seconds: float = _TEMPORAL_TOKEN_REFRESH_DELAY_SECONDS,
) -> None:
    """Keep the live Temporal connection's bearer current for a rotating credential.

    Temporal sets the api_key once at connect and exposes no per-RPC auth callback, so the only way to
    refresh is to push via ``update_api_key``. The provider reports how long until it next refreshes the
    token (``get_token_with_max_age``); we wake ``delay_seconds`` after that point, by which time
    ``get_token()`` has already re-read the rotated token — so the push always lands before expiry.
    Non-rotating credentials never change, so they need no loop.
    """
    provider = _resolve_temporal_token()
    if provider is None:
        return
    last_pushed: str | None = None
    while True:
        try:
            token, time_until_refresh = provider.get_token_with_max_age()
            if math.isinf(time_until_refresh):
                return  # non-rotating credential: the connection already holds it; nothing to maintain
            if token != last_pushed:
                service_client.update_api_key(token)
                last_pushed = token
                logger.debug("updated temporal api key from token provider")
        except Exception as exc:
            logger.warning("failed to refresh temporal token", **extract_error_context(exc), exc_info=exc)
            await asyncio.sleep(delay_seconds)
            continue
        await asyncio.sleep(time_until_refresh + delay_seconds)


async def create_temporal_client(
    namespace: str | None = None,
    temporal_service_client: TemporalServiceClient | None = None,
    payload_converter: Type[PayloadConverter] = PydanticPayloadConverter,
    payload_codec: PayloadCodec | None = None,
    extra_interceptors: List[Interceptor] | None = None,
    add_tracing_interceptors: bool = True,
    runtime: Runtime | None = None,
) -> TemporalClient:
    """
    Create and connect to a Temporal client with appropriate configuration.

    Args:
        namespace: Optional namespace to connect to
        temporal_sevice: Optional Temporal service client to use for namespace lookup

    Returns:
        Connected Temporal client instance

    Raises:
        ValueError: If connection fails
    """
    if not namespace:
        namespace = config.temporal.namespace

    interceptors: List[Interceptor] = []

    if extra_interceptors:
        interceptors.extend(extra_interceptors)

    # The worker supplies pre-ordered tracing interceptors itself (add_tracing_interceptors=False).
    if add_tracing_interceptors:
        tracing_interceptors = get_temporal_tracing_interceptors()
        if tracing_interceptors:
            interceptors.extend(tracing_interceptors)
            logger.debug("adding OpenTelemetry tracing interceptor to Temporal client")

    if temporal_service_client is None:
        temporal_service_client = await create_temporal_service_client(runtime=runtime)

    try:
        # Connect to Temporal
        client = TemporalClient(
            temporal_service_client,
            namespace=namespace,
            data_converter=DataConverter(
                payload_converter_class=payload_converter or PydanticPayloadConverter,
                payload_codec=payload_codec,
            ),
            interceptors=interceptors,
        )

        logger.info(
            "connected to temporal frontend",
            url=config.temporal.server_url,
            namespace=namespace,
            payload_converter=payload_converter,
            payload_codec=payload_codec,
        )
    except Exception as e:
        raise WorkflowsException(
            code=ErrorCode.TEMPORAL_CONNECTION_ERROR,
            message=f"failed to connect to temporal frontend at {config.temporal.server_url}",
        ) from e

    return client
