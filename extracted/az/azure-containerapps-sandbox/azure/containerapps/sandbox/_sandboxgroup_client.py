"""Azure Sandbox Group data-plane client.

Usage::

    from azure.identity import DefaultAzureCredential
    from azure.containerapps.sandbox import SandboxGroupClient, endpoint_for_region

    client = SandboxGroupClient(
        endpoint_for_region("westus2"),
        DefaultAzureCredential(),
        subscription_id="my-sub",
        resource_group="my-rg",
        sandbox_group="my-group",
    )

    sandbox = client.create_sandbox(disk="ubuntu")  # returns SandboxClient
    result = sandbox.exec("echo hello")
    images = list(client.list_disk_images())
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._api_version import ApiVersion
from azure.containerapps.sandbox._helpers import (
    DATA_PLANE_BASE,
    DATA_PLANE_SCOPE,
    _build_pipeline,
    _raise_if_error,
    _validate_endpoint,
    _validate_segment,
)
from azure.containerapps.sandbox._operations import (
    ImageOperationsMixin,
    SandboxOperationsMixin,
    SecretOperationsMixin,
    SnapshotOperationsMixin,
    VolumeOperationsMixin,
)

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.pipeline.transport import HttpTransport

logger = logging.getLogger("azure.containerapps.sandbox")


class SandboxGroupClient(
    SandboxOperationsMixin,
    ImageOperationsMixin,
    SnapshotOperationsMixin,
    VolumeOperationsMixin,
    SecretOperationsMixin,
):
    """Data-plane client scoped to a sandbox group.

    Provides group-level operations (sandbox CRUD, images, snapshots, volumes,
    secrets) and factory methods for obtaining a sandbox-scoped
    :class:`SandboxClient`.

    :param str endpoint: Data-plane endpoint URL. Use ``endpoint_for_region()``
        to construct a regional URL (e.g. ``endpoint_for_region("westus2")``).
    :param credential: Azure credential for authentication (**required**).
        Use ``DefaultAzureCredential()`` from ``azure-identity``.
    :paramtype credential: ~azure.core.credentials.TokenCredential
    :keyword str subscription_id: Azure subscription ID (**required**).
    :keyword str resource_group: Azure resource group (**required**).
    :keyword str sandbox_group: Sandbox group name (**required**).
    :keyword str audience: Override the OAuth scope/audience.
    :keyword api_version: Override the data-plane API version.
    :paramtype api_version: str or ~azure.containerapps.sandbox.ApiVersion
    :keyword transport: Override the HTTP transport (for testing).
    :paramtype transport: ~azure.core.pipeline.transport.HttpTransport

    Example::

        from azure.identity import DefaultAzureCredential
        from azure.containerapps.sandbox import SandboxGroupClient, endpoint_for_region

        client = SandboxGroupClient(
            endpoint_for_region("westus2"),
            DefaultAzureCredential(),
            subscription_id="my-sub",
            resource_group="my-rg",
            sandbox_group="my-group",
        )
        sandbox = client.create_sandbox(disk="ubuntu")
        result = sandbox.exec("echo hello")
    """

    def __init__(
        self,
        endpoint: str,
        credential: "TokenCredential",
        *,
        subscription_id: str,
        resource_group: str,
        sandbox_group: str,
        audience: str | None = None,
        api_version: str | ApiVersion = ApiVersion.V2026_02_01_PREVIEW,
        transport: "HttpTransport | None" = None,
        **kwargs: Any,
    ):
        if not credential:
            raise ValueError(
                "credential is required. Use DefaultAzureCredential() or another "
                "azure-identity credential."
            )
        if not subscription_id:
            raise ValueError("subscription_id is required.")
        if not resource_group:
            raise ValueError("resource_group is required.")
        if not sandbox_group:
            raise ValueError("sandbox_group is required.")

        _validate_segment(resource_group, "resource_group")
        _validate_segment(sandbox_group, "sandbox_group")

        self._credential = credential
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._sandbox_group = sandbox_group
        self._endpoint = _validate_endpoint(endpoint or DATA_PLANE_BASE)
        self._scope = audience or DATA_PLANE_SCOPE
        self._api_version = api_version.value if isinstance(api_version, ApiVersion) else api_version
        self._pipeline = _build_pipeline(
            credential, self._scope, transport=transport, **kwargs
        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def subscription_id(self) -> str:
        """The Azure subscription ID (read-only)."""
        return self._subscription_id

    @property
    def resource_group(self) -> str:
        """The Azure resource group (read-only)."""
        return self._resource_group

    @property
    def sandbox_group(self) -> str:
        """The sandbox group name (read-only)."""
        return self._sandbox_group

    @property
    def _group_path(self) -> str:
        """URL path prefix scoped to the sandbox group."""
        return (f"/subscriptions/{self._subscription_id}"
                f"/resourceGroups/{self._resource_group}"
                f"/sandboxGroups/{self._sandbox_group}")

    # -------------------------------------------------------------------------
    # Internal HTTP
    # -------------------------------------------------------------------------

    def _send_request(self, request: HttpRequest, *, stream: bool = False) -> HttpResponse:
        """Send request through the pipeline and raise on error."""
        pipeline_response = self._pipeline.run(request, stream=stream)
        response = pipeline_response.http_response
        _raise_if_error(response)
        return response

    def _dp_get(self, path: str, *, params: dict | None = None) -> dict | list:
        all_params = {"api-version": self._api_version, **(params or {})}
        request = HttpRequest("GET", f"{self._endpoint}{path}", params=all_params)
        response = self._send_request(request)
        return response.json() if response.status_code != 204 else {}

    def _dp_put(self, path: str, body: dict | bytes | None = None, *, headers: dict | None = None, params: dict | None = None) -> dict:
        all_params = {"api-version": self._api_version, **(params or {})}
        kwargs: dict[str, Any] = {"params": all_params}
        if headers:
            kwargs["headers"] = headers
        if isinstance(body, bytes):
            kwargs["content"] = body
        elif body is not None:
            kwargs["json"] = body
        request = HttpRequest("PUT", f"{self._endpoint}{path}", **kwargs)
        response = self._send_request(request)
        return response.json()

    def _dp_post(self, path: str, body: dict | None = None) -> dict:
        params = {"api-version": self._api_version}
        if body is not None:
            request = HttpRequest("POST", f"{self._endpoint}{path}", json=body, params=params)
        else:
            request = HttpRequest("POST", f"{self._endpoint}{path}", params=params)
        response = self._send_request(request)
        return response.json() if response.status_code != 204 else {}

    def _dp_delete(self, path: str) -> None:
        request = HttpRequest("DELETE", f"{self._endpoint}{path}", params={"api-version": self._api_version})
        pipeline_response = self._pipeline.run(request)
        response = pipeline_response.http_response
        if response.status_code not in (200, 202, 204):
            _raise_if_error(response)

    # -------------------------------------------------------------------------
    # Factory — sandbox-scoped client
    # -------------------------------------------------------------------------

    def get_sandbox_client(self, sandbox_id: str, **kwargs: Any):
        """Get a :class:`SandboxClient` scoped to a specific sandbox.

        The returned client shares this client's pipeline and does not create
        a new HTTP connection.

        :param str sandbox_id: Sandbox ID.
        :returns: Sandbox-scoped client.
        :rtype: ~azure.containerapps.sandbox.SandboxClient
        """
        from azure.containerapps.sandbox._sandbox_client import SandboxClient

        _validate_segment(sandbox_id, "sandbox_id")
        return SandboxClient(
            self._endpoint,
            self._credential,
            subscription_id=self._subscription_id,
            resource_group=self._resource_group,
            sandbox_group=self._sandbox_group,
            sandbox_id=sandbox_id,
            audience=self._scope,
            api_version=self._api_version,
            _pipeline=self._pipeline,
            **kwargs,
        )

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def close(self) -> None:
        self._pipeline.__exit__(None, None, None)

    def __enter__(self):
        self._pipeline.__enter__()
        return self

    def __exit__(self, *args):
        self._pipeline.__exit__(*args)
