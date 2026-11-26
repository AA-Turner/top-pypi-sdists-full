"""Shared helpers — pipeline factories, error mapping, region helpers."""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping
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
    SansIOHTTPPolicy,
    UserAgentPolicy,
)
from azure.core.pipeline.transport import RequestsTransport
from azure.core.rest import HttpRequest, HttpResponse

from azure.containerapps.sandbox._version import VERSION

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.core.pipeline import AsyncPipeline, PipelineRequest
    from azure.core.pipeline.transport import AsyncHttpTransport, HttpTransport
    from azure.containerapps.sandbox._models import RegistryCredentials

logger = logging.getLogger("azure.containerapps.sandbox")

SDK_MONIKER = f"azure-containerapps-sandbox/{VERSION}"

DATA_PLANE_SCOPE = "https://dynamicsessions.io/.default"
DATA_PLANE_BASE = "https://management.azuredevcompute.io"
DATA_PLANE_API_VERSION = "2026-09-01-preview"

_ERROR_MAP: dict[int, type] = {
    401: ClientAuthenticationError,
    403: ClientAuthenticationError,
    404: ResourceNotFoundError,
}


def _get_json_array(
    payload: Mapping[str, Any],
    field_name: str,
    *,
    nullable: bool = False,
) -> list[Any]:
    """Read and validate a JSON array property."""
    if not isinstance(payload, Mapping):
        raise TypeError("JSON payload must be an object")
    if field_name not in payload:
        return []

    value = payload[field_name]
    if value is None and nullable:
        return []
    if not isinstance(value, list):
        expected = "a JSON array or null" if nullable else "a JSON array"
        raise TypeError(f"{field_name} must be {expected}")
    return value


def _get_optional_json_array(
    payload: Mapping[str, Any],
    field_name: str,
) -> list[Any] | None:
    """Read an optional JSON array while preserving missing/null as ``None``."""
    if not isinstance(payload, Mapping):
        raise TypeError("JSON payload must be an object")
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, list):
        raise TypeError(f"{field_name} must be a JSON array or null")
    return value


def _validate_segment(value: str, name: str) -> str:
    """Validate a URL path segment to prevent path traversal."""
    if not value or "/" in value or "\\" in value or ".." in value or "\x00" in value:
        raise ValueError(
            f"Invalid {name}: must not contain '/', '\\', '..', or null bytes."
        )
    return value


def _disk_image_create_body(
    base_image: str,
    name: str | None,
    registry_credentials: "RegistryCredentials | None",
    managed_identity_client_id: str | None,
    kwargs: dict[str, Any],
) -> dict:
    """Validate registry import options before data-plane I/O."""
    if "managed_identity_resource_id" in kwargs:
        raise TypeError(
            "managed_identity_resource_id is no longer supported. "
            "Pass managed_identity_client_id='system' or the user-assigned identity's UUID client ID instead."
        )
    for key in ("entrypoint", "cmd"):
        if key in kwargs:
            raise TypeError(
                f"{key} is no longer supported for disk-image creation. "
                "Configure command overrides on the sandbox container instead."
            )
    if registry_credentials is not None and managed_identity_client_id is not None:
        raise ValueError("registry_credentials and managed_identity_client_id are mutually exclusive.")
    source: dict[str, Any] = {
        "kind": "registry",
        "imageUrl": base_image,
        "isPlatformImage": False,
    }
    if registry_credentials is not None:
        if (
            not isinstance(registry_credentials.username, str)
            or not registry_credentials.username.strip()
            or not isinstance(registry_credentials.token, str)
            or not registry_credentials.token.strip()
        ):
            raise ValueError("registry_credentials requires both a nonempty username and token.")
        source["registryCredentials"] = registry_credentials.as_dict()

    identity = managed_identity_client_id
    if identity is not None:
        if not isinstance(identity, str):
            raise ValueError("managed_identity_client_id must be 'system' or a canonical UUID client ID.")
        if identity.lower() == "system":
            identity = "system"
            source["managedIdentityClientId"] = identity
        elif not re.fullmatch(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            identity,
        ):
            raise ValueError(
                "managed_identity_client_id must be 'system' or a canonical UUID client ID."
            )
        else:
            source["managedIdentityClientId"] = identity.lower()
    body: dict[str, Any] = {"source": source}
    if name:
        body["labels"] = {"name": name}
    return body


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


class _ContinuationUrlPolicy(SansIOHTTPPolicy):
    def on_request(self, request: PipelineRequest) -> None:
        endpoint = request.context.options.pop("_continuation_endpoint", None)
        if endpoint is not None:
            _validate_continuation_token(request.http_request.url, endpoint)


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
        _ContinuationUrlPolicy(),
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
        _ContinuationUrlPolicy(),
        AsyncBearerTokenCredentialPolicy(credential, scope, **kwargs),
        NetworkTraceLoggingPolicy(**kwargs),
        DistributedTracingPolicy(**kwargs),
        HttpLoggingPolicy(**kwargs),
    ]
    return AsyncPipeline(
        transport=transport or AioHttpTransport(**kwargs),
        policies=policies,
    )
