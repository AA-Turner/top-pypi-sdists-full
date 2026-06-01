from typing import List, Type

import structlog
from pydantic import SecretStr
from temporalio.client import Client as TemporalClient
from temporalio.client import Interceptor
from temporalio.contrib.pydantic import PydanticPayloadConverter
from temporalio.converter import DataConverter, PayloadCodec, PayloadConverter
from temporalio.runtime import OpenTelemetryConfig, Runtime, TelemetryConfig
from temporalio.service import ConnectConfig, HttpConnectProxyConfig
from temporalio.service import ServiceClient as TemporalServiceClient

from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import get_temporal_tracing_interceptors
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

logger = structlog.get_logger(__name__)

DEFAULT_NAMESPACE = "default"


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


async def create_temporal_service_client() -> TemporalServiceClient:
    runtime = Runtime(telemetry=TelemetryConfig())
    if config.common.otel_enabled:
        metrics_endpoint = config.common.otel_endpoint or config.common.otel_metrics_endpoint
        runtime = Runtime(
            telemetry=TelemetryConfig(metrics=OpenTelemetryConfig(url=f"{metrics_endpoint}/v1/metrics", http=True))
        )
    logger.info(
        "creating temporal service client",
        url=config.temporal.server_url,
        k=config.temporal.api_key,
        tls=config.temporal.tls,
        runtime=runtime,
    )
    api_key = config.temporal.api_key.get_secret_value() if config.temporal.api_key else None

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
                api_key=api_key or None,
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


async def create_temporal_client(
    namespace: str | None = None,
    temporal_service_client: TemporalServiceClient | None = None,
    payload_converter: Type[PayloadConverter] = PydanticPayloadConverter,
    payload_codec: PayloadCodec | None = None,
    extra_interceptors: List[Interceptor] | None = None,
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

    # Get optional tracing interceptor
    interceptors: List[Interceptor] = []
    tracing_interceptors = get_temporal_tracing_interceptors()

    if extra_interceptors:
        for interceptor in extra_interceptors:
            interceptors.append(interceptor)

    if tracing_interceptors:
        interceptors.extend(tracing_interceptors)
        logger.debug("adding OpenTelemetry tracing interceptor to Temporal client")

    if temporal_service_client is None:
        temporal_service_client = await create_temporal_service_client()

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
