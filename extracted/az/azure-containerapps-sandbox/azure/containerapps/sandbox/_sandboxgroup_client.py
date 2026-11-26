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

from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._api_version import ApiVersion
from azure.containerapps.sandbox._generated._client import SandboxGroupClient as _GeneratedClient
from azure.containerapps.sandbox._helpers import (
    DATA_PLANE_BASE,
    DATA_PLANE_SCOPE,
    _build_pipeline,
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
    from azure.core.pipeline import Pipeline
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
        api_version: str | ApiVersion = ApiVersion.V2026_09_01_PREVIEW,
        transport: "HttpTransport | None" = None,
        _pipeline: "Pipeline | None" = None,
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
        self._transport = transport
        self._pipeline_options = dict(kwargs)
        self._owns_pipeline = _pipeline is None
        self._pipeline = _pipeline if _pipeline is not None else _build_pipeline(
            credential, self._scope, transport=transport, **kwargs
        )
        self._generated = _GeneratedClient(
            self._endpoint, credential, subscription_id, resource_group, sandbox_group,
            api_version=self._api_version, credential_scopes=[self._scope],
            pipeline=self._pipeline,
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
        if self._owns_pipeline:
            self._pipeline.__exit__(None, None, None)

    def __enter__(self):
        if self._owns_pipeline:
            self._pipeline.__enter__()
        return self

    def __exit__(self, *args):
        if self._owns_pipeline:
            self._pipeline.__exit__(*args)
