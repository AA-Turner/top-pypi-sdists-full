"""Shared helpers for ARM management plane."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceNotFoundError,
    map_error,
)
from azure.core.pipeline import Pipeline
from azure.core.pipeline.policies import (
    BearerTokenCredentialPolicy,
    ContentDecodePolicy,
    DistributedTracingPolicy,
    HeadersPolicy,
    HttpLoggingPolicy,
    NetworkTraceLoggingPolicy,
    ProxyPolicy,
    RedirectPolicy,
    RequestIdPolicy,
    RetryPolicy,
    UserAgentPolicy,
)
from azure.core.pipeline.transport import RequestsTransport
from azure.core.rest import HttpRequest, HttpResponse

from azure.containerapps.sandbox._version import VERSION

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.core.pipeline import AsyncPipeline
    from azure.core.pipeline.transport import AsyncHttpTransport, HttpTransport

logger = logging.getLogger("azure.containerapps.sandbox")

SDK_MONIKER = f"azure-containerapps-sandbox/{VERSION}"
ARM_SCOPE = "https://management.azure.com/.default"

_ERROR_MAP: dict[int, type] = {
    401: ClientAuthenticationError,
    403: ClientAuthenticationError,
    404: ResourceNotFoundError,
}


def _build_arm_pipeline(
    credential: "TokenCredential",
    *,
    transport: "HttpTransport | None" = None,
    **kwargs: Any,
) -> Pipeline:
    """Build an azure-core pipeline for ARM operations."""
    policies = [
        RequestIdPolicy(**kwargs),
        HeadersPolicy(**kwargs),
        UserAgentPolicy(sdk_moniker=SDK_MONIKER, **kwargs),
        ProxyPolicy(**kwargs),
        ContentDecodePolicy(**kwargs),
        RedirectPolicy(**kwargs),
        RetryPolicy(**kwargs),
        BearerTokenCredentialPolicy(credential, ARM_SCOPE, **kwargs),
        NetworkTraceLoggingPolicy(**kwargs),
        DistributedTracingPolicy(**kwargs),
        HttpLoggingPolicy(**kwargs),
    ]
    return Pipeline(
        transport=transport or RequestsTransport(**kwargs),
        policies=policies,
    )


def _raise_if_error(response: HttpResponse, error_map: dict | None = None) -> None:
    """Raise azure.core.exceptions for HTTP error responses."""
    if response.status_code < 400:
        return
    combined = {**_ERROR_MAP, **(error_map or {})}
    map_error(status_code=response.status_code, response=response, error_map=combined)
    raise HttpResponseError(response=response)


def _build_async_arm_pipeline(
    credential: "AsyncTokenCredential",
    *,
    transport: "AsyncHttpTransport | None" = None,
    **kwargs: Any,
) -> "AsyncPipeline":
    """Build an azure-core async pipeline for ARM operations."""
    from azure.core.pipeline import AsyncPipeline
    from azure.core.pipeline.policies import (
        AsyncBearerTokenCredentialPolicy,
        AsyncRedirectPolicy,
        AsyncRetryPolicy,
    )
    from azure.core.pipeline.transport import AioHttpTransport

    policies = [
        RequestIdPolicy(**kwargs),
        HeadersPolicy(**kwargs),
        UserAgentPolicy(sdk_moniker=SDK_MONIKER, **kwargs),
        ProxyPolicy(**kwargs),
        ContentDecodePolicy(**kwargs),
        AsyncRedirectPolicy(**kwargs),
        AsyncRetryPolicy(**kwargs),
        AsyncBearerTokenCredentialPolicy(credential, ARM_SCOPE, **kwargs),
        NetworkTraceLoggingPolicy(**kwargs),
        DistributedTracingPolicy(**kwargs),
        HttpLoggingPolicy(**kwargs),
    ]
    return AsyncPipeline(
        transport=transport or AioHttpTransport(**kwargs),
        policies=policies,
    )
