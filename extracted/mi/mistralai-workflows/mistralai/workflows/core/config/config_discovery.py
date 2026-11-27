from __future__ import annotations

import warnings
from typing import Any
from urllib.parse import urlparse

from httpx import HTTPStatusError

from mistralai.workflows.client import translate_model
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.auth import get_token_provider
from mistralai.workflows.core.auth.header_files import get_deployment_headers
from mistralai.workflows.core.config.config import AppConfig, adopt_remote_default, apply_remote_defaults
from mistralai.workflows.core.config.config import config as legacy_config
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.worker import WorkerInfo
from mistralai.workflows.worker_client.errors import SDKError

logger = get_logger(__name__)

_IGNORED_WORKER_FEATURES = {"events_api_version"}


class WorkerRuntimeConfig(WorkerInfo):
    def apply(self, target: AppConfig | None = None) -> dict[str, Any]:
        """Apply the resolved configuration, returning the feature values that won."""
        target = target if target is not None else legacy_config
        # The connection settings are adopted field by field rather than through
        # `RemotelyOverridable`: the server names them differently and the scheduler URL needs
        # normalizing. New flags belong on the annotation path instead.
        adopt_remote_default(target.temporal, "namespace", self.namespace)
        adopt_remote_default(target.temporal, "server_url", normalize_temporal_url(self.scheduler_url))
        adopt_remote_default(target.temporal, "tls", self.tls)
        features = self.features.model_dump(exclude=_IGNORED_WORKER_FEATURES)
        return apply_remote_defaults(target, features)


async def _fetch_worker_runtime_config(target: AppConfig) -> WorkerRuntimeConfig:
    async with get_worker_client(
        base_url=target.worker.server_url,
        timeout=target.http.timeout,
        token_provider=get_token_provider(app_config=target),
        headers=get_deployment_headers(target.worker),
    ) as worker_client:
        result = await worker_client.whoami_async()
        response = translate_model(WorkerInfo, result)
    logger.info("Worker runtime config resolved", namespace=response.namespace, scheduler_url=response.scheduler_url)
    return WorkerRuntimeConfig.model_validate_json(response.model_dump_json())


async def apply_worker_runtime_config(
    *,
    config: AppConfig | None = None,
) -> WorkerRuntimeConfig | None:
    target = config if config is not None else legacy_config
    try:
        runtime_config = await _fetch_worker_runtime_config(target)
        effective_features = runtime_config.apply(target)
        logger.info(
            "Applied worker runtime config",
            namespace=runtime_config.namespace,
            scheduler_url=runtime_config.scheduler_url,
            tls=runtime_config.tls,
            effective_namespace=target.temporal.namespace,
            effective_server_url=target.temporal.server_url,
            effective_tls=target.temporal.tls,
            server_features=runtime_config.features.model_dump(),
            effective_features=effective_features,
        )
        return runtime_config
    except (SDKError, HTTPStatusError) as exc:
        status_code = exc.status_code if isinstance(exc, SDKError) else exc.response.status_code
        if status_code == 404:
            warnings.warn("Could not fetch worker config from server. Is your server up to date?")
            return None
        raise WorkflowsException.from_api_client_error(
            exc,
            code=ErrorCode.WORKER_RUNTIME_CONFIG_ERROR,
            message="Failed to fetch worker runtime configuration from server",
        ) from exc


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
