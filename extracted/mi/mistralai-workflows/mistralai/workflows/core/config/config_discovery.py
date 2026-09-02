from __future__ import annotations

import warnings
from urllib.parse import urlparse

import structlog
from httpx import HTTPStatusError

from mistralai.workflows.client import translate_model
from mistralai.workflows.core.auth import get_token_provider
from mistralai.workflows.core.config.config import adopt_remote_default, apply_remote_defaults, config
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.worker import WorkerInfo

logger = structlog.get_logger(__name__)


class WorkerRuntimeConfig(WorkerInfo):
    def apply(self) -> dict[str, bool]:
        """Apply the resolved configuration, returning the feature values that won."""
        # The connection settings are adopted field by field rather than through
        # `RemotelyOverridable`: the server names them differently, they are not booleans, and the
        # scheduler URL needs normalizing. New boolean flags belong on the annotation path instead.
        adopt_remote_default(config.temporal, "namespace", self.namespace)
        adopt_remote_default(config.temporal, "server_url", normalize_temporal_url(self.scheduler_url))
        adopt_remote_default(config.temporal, "tls", self.tls)
        return apply_remote_defaults(config, self.features.model_dump())


async def _fetch_worker_runtime_config() -> WorkerRuntimeConfig:
    async with get_worker_client(
        base_url=config.worker.server_url,
        token_provider=get_token_provider(),
        headers=config.worker.mistral_api_headers,
    ) as worker_client:
        result = await worker_client.whoami_async()
        response = translate_model(WorkerInfo, result)
    logger.info("Worker runtime config resolved", namespace=response.namespace, scheduler_url=response.scheduler_url)
    return WorkerRuntimeConfig.model_validate_json(response.model_dump_json())


async def apply_worker_runtime_config(api_key: str | None = None) -> WorkerRuntimeConfig | None:
    if api_key is not None:
        warnings.warn(
            "Passing `api_key` to apply_worker_runtime_config is deprecated and ignored; "
            "authentication resolves through the token provider.",
            DeprecationWarning,
            stacklevel=2,
        )
    try:
        runtime_config = await _fetch_worker_runtime_config()
        effective_features = runtime_config.apply()
        logger.info(
            "Applied worker runtime config",
            namespace=runtime_config.namespace,
            scheduler_url=runtime_config.scheduler_url,
            tls=runtime_config.tls,
            effective_namespace=config.temporal.namespace,
            effective_server_url=config.temporal.server_url,
            effective_tls=config.temporal.tls,
            server_features=runtime_config.features.model_dump(),
            effective_features=effective_features,
        )
        return runtime_config
    except HTTPStatusError as exc:
        if exc.response.status_code == 404:
            warnings.warn("Could not fetch worker config from server. Is your server up to date?")
            return None
        raise WorkflowsException(
            code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
            message="Failed to fetch worker runtime configuration from server",
        )


def normalize_temporal_url(url: str) -> str:
    original_url = url
    # If there's no scheme, urlparse misparses host:port inputs.
    # Prepend a dummy scheme so we can extract host and port correctly.
    if "://" not in url:
        url = f"dummy://{url}"

    parsed = urlparse(url)
    host = parsed.hostname
    if not host:
        raise ValueError(f"Unable to determine host from URL: {original_url}")

    if parsed.port is not None:
        port = parsed.port
    elif parsed.scheme == "https":
        port = 443
    elif parsed.scheme == "http":
        port = 80
    else:
        raise ValueError(f"Unable to determine port from URL: {original_url}")
    return f"{host}:{port}"
