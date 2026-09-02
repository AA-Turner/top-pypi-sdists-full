"""Shared helpers — pipeline factories, error mapping, region helpers."""

from __future__ import annotations

import logging
import os
import re
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

DATA_PLANE_SCOPE = "https://dynamicsessions.io/.default"
DATA_PLANE_BASE = "https://management.azuredevcompute.io"
DATA_PLANE_API_VERSION = "2026-02-01-preview"

_ERROR_MAP: dict[int, type] = {
    401: ClientAuthenticationError,
    403: ClientAuthenticationError,
    404: ResourceNotFoundError,
}


def _validate_segment(value: str, name: str) -> str:
    """Validate a URL path segment to prevent path traversal."""
    if not value or "/" in value or "\\" in value or ".." in value or "\x00" in value:
        raise ValueError(
            f"Invalid {name}: must not contain '/', '\\', '..', or null bytes."
        )
    return value


def _validate_endpoint(endpoint: str) -> str:
    """Validate that an endpoint URL uses HTTPS."""
    if not endpoint.startswith("https://"):
        raise ValueError(
            "endpoint must use HTTPS (got {!r}). "
            "Use endpoint_for_region() to construct a regional endpoint.".format(endpoint)
        )
    return endpoint.rstrip("/")


def _validate_continuation_token(token: str, endpoint: str) -> None:
    """Validate that a continuation token URL belongs to the expected host and uses HTTPS."""
    from urllib.parse import urlparse
    parsed = urlparse(token)
    expected = urlparse(endpoint)
    if parsed.scheme and parsed.scheme != "https":
        raise ValueError(
            f"Continuation URL uses insecure scheme: {parsed.scheme!r} (expected https)"
        )
    if parsed.hostname != expected.hostname:
        raise ValueError(
            f"Unexpected continuation URL host: {parsed.hostname!r} "
            f"(expected {expected.hostname!r})"
        )


def _build_pipeline(
    credential: "TokenCredential",
    scope: str,
    *,
    transport: "HttpTransport | None" = None,
    **kwargs: Any,
) -> Pipeline:
    """Build an azure-core pipeline with standard Azure SDK policies."""
    policies = [
        RequestIdPolicy(**kwargs),
        HeadersPolicy(**kwargs),
        UserAgentPolicy(sdk_moniker=SDK_MONIKER, **kwargs),
        ProxyPolicy(**kwargs),
        ContentDecodePolicy(**kwargs),
        RedirectPolicy(**kwargs),
        # retry_status=10: covers ~60-100s of 403s for RBAC propagation
        # (default is 3 which only covers ~6s — insufficient for fresh role assignments)
        RetryPolicy(retry_on_status_codes=[403], retry_status=10, **kwargs),
        BearerTokenCredentialPolicy(credential, scope, **kwargs),
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


def get_subscription_id() -> str:
    """Detect subscription ID from environment or Azure CLI."""
    sub = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if sub:
        return sub
    try:
        import subprocess
        result = subprocess.run(
            ["az", "account", "show", "--query", "id", "-o", "tsv"],
            capture_output=True, text=True, check=True,
        )
        sub = result.stdout.strip()
        if sub:
            return sub
    except Exception:
        pass
    raise ValueError(
        "subscription_id is required. Pass it to the constructor, set "
        "the AZURE_SUBSCRIPTION_ID environment variable, or run 'az login'."
    )


def endpoint_for_region(region: str) -> str:
    """Construct a regional data-plane endpoint URL."""
    return f"https://management.{region}.azuredevcompute.io"


def region_from_endpoint(endpoint: str) -> str | None:
    """Extract the region from a regional endpoint URL."""
    m = re.match(r"https://management\.([^.]+)\.azuredevcompute\.io", endpoint)
    return m.group(1) if m else None


def _build_async_pipeline(
    credential: "AsyncTokenCredential",
    scope: str,
    *,
    transport: "AsyncHttpTransport | None" = None,
    **kwargs: Any,
) -> "AsyncPipeline":
    """Build an azure-core async pipeline with standard Azure SDK policies."""
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
        # retry_status=10: covers ~60-100s of 403s for RBAC propagation
        # (default is 3 which only covers ~6s — insufficient for fresh role assignments)
        AsyncRetryPolicy(retry_on_status_codes=[403], retry_status=10, **kwargs),
        AsyncBearerTokenCredentialPolicy(credential, scope, **kwargs),
        NetworkTraceLoggingPolicy(**kwargs),
        DistributedTracingPolicy(**kwargs),
        HttpLoggingPolicy(**kwargs),
    ]
    return AsyncPipeline(
        transport=transport or AioHttpTransport(**kwargs),
        policies=policies,
    )
