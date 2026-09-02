"""Azure Container Apps Sandbox Groups Management Client - ARM control plane only.

Usage::

    from azure.identity import DefaultAzureCredential
    from azure.containerapps.sandbox import SandboxGroupManagementClient

    client = SandboxGroupManagementClient(
        DefaultAzureCredential(),
        subscription_id="my-sub",
        resource_group="my-rg",
    )
    client.create_group("my-group", location="westus2")
    groups = list(client.list_groups())
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.exceptions import ResourceNotFoundError
from azure.core.paging import ItemPaged
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._mgmt_helpers import (
    ARM_SCOPE,
    _build_arm_pipeline,
    _raise_if_error,
)
from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import SandboxGroup

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.pipeline.transport import HttpTransport

logger = logging.getLogger("azure.containerapps.sandbox")

ARM_BASE = "https://management.azure.com"
API_VERSION = "2026-02-01-preview"


class SandboxGroupManagementClient:
    """Client for Azure Container Apps sandbox groups (ARM control plane).

    Use this client to create, list, and delete sandbox groups.

    :param credential: Azure credential for authentication (**required**).
        Use ``DefaultAzureCredential()`` from ``azure-identity``.
    :paramtype credential: ~azure.core.credentials.TokenCredential
    :keyword str subscription_id: Azure subscription ID (**required**).
    :keyword str resource_group: Default resource group (**required**).
    :keyword str api_version: Override the ARM API version.
    :keyword transport: Override the HTTP transport (for testing).
    :paramtype transport: ~azure.core.pipeline.transport.HttpTransport

    Example::

        from azure.identity import DefaultAzureCredential
        from azure.containerapps.sandbox import SandboxGroupManagementClient

        client = SandboxGroupManagementClient(
            DefaultAzureCredential(),
            subscription_id="my-sub",
            resource_group="my-rg",
        )
        client.create_group("my-group", location="westus2")
    """

    def __init__(
        self,
        credential: "TokenCredential",
        *,
        subscription_id: str,
        resource_group: str,
        api_version: str | None = None,
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

        _validate_segment(resource_group, "resource_group")

        self._credential = credential
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._api_version = api_version or API_VERSION
        self._endpoint = ARM_BASE
        self._pipeline = _build_arm_pipeline(
            credential, transport=transport, **kwargs
        )

    @property
    def subscription_id(self) -> str:
        """The Azure subscription ID (read-only)."""
        return self._subscription_id

    @property
    def resource_group(self) -> str:
        """The resource group (read-only)."""
        return self._resource_group

    # -------------------------------------------------------------------------
    # Internal HTTP
    # -------------------------------------------------------------------------

    def _send_request(self, request: HttpRequest, *, stream: bool = False) -> HttpResponse:
        """Send request through the pipeline and raise on error."""
        pipeline_response = self._pipeline.run(request, stream=stream)
        response = pipeline_response.http_response
        _raise_if_error(response)
        return response

    def _arm_get(self, path: str) -> dict:
        request = HttpRequest("GET", f"{self._endpoint}{path}", params={"api-version": self._api_version})
        response = self._send_request(request)
        return response.json()

    def _arm_put(self, path: str, body: dict) -> dict:
        request = HttpRequest("PUT", f"{self._endpoint}{path}", json=body, params={"api-version": self._api_version})
        response = self._send_request(request)
        return response.json()

    def _arm_delete(self, path: str) -> None:
        request = HttpRequest("DELETE", f"{self._endpoint}{path}", params={"api-version": self._api_version})
        pipeline_response = self._pipeline.run(request)
        response = pipeline_response.http_response
        if response.status_code not in (200, 202, 204):
            _raise_if_error(response)

    def _arm_patch(self, path: str, body: dict) -> dict:
        request = HttpRequest("PATCH", f"{self._endpoint}{path}", json=body, params={"api-version": self._api_version})
        response = self._send_request(request)
        return response.json()

    def _arm_call_raw(self, method: str, path: str, body: dict | None = None):
        """Run an ARM request and return the raw PipelineResponse (for ARMPolling)."""
        kwargs: dict = {"params": {"api-version": self._api_version}}
        if body is not None:
            kwargs["json"] = body
        request = HttpRequest(method, f"{self._endpoint}{path}", **kwargs)
        pipeline_response = self._pipeline.run(request)
        response = pipeline_response.http_response
        if response.status_code not in (200, 201, 202, 204):
            _raise_if_error(response)
        return pipeline_response

    def _pipeline_client(self):
        """Wrap our pipeline in a PipelineClient so azure-mgmt-core ARMPolling can drive it."""
        from azure.core import PipelineClient

        return PipelineClient(base_url=self._endpoint, pipeline=self._pipeline)

    # -------------------------------------------------------------------------
    # Sandbox Groups - ARM control plane (Microsoft.App/sandboxGroups)
    # -------------------------------------------------------------------------

    @property
    def _group_base(self) -> str:
        return (f"/subscriptions/{self._subscription_id}"
                f"/resourceGroups/{self._resource_group}"
                f"/providers/Microsoft.App/sandboxGroups")

    @distributed_trace
    def list_groups(self, **kwargs: Any) -> ItemPaged[SandboxGroup]:
        """List sandbox groups in the configured resource group."""
        base_url = f"{self._endpoint}{self._group_base}"
        params = {"api-version": self._api_version}

        def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            try:
                return self._send_request(request)
            except ResourceNotFoundError:
                return None

        def _extract_data(response):
            if response is None:
                return None, iter([])
            data = response.json()
            items = [SandboxGroup._from_dict(item) for item in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return ItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace
    def get_group(self, name: str, **kwargs: Any) -> SandboxGroup:
        """Get a sandbox group by name.

        :param str name: Sandbox group name.
        :returns: The sandbox group.
        :rtype: ~azure.containerapps.sandbox.SandboxGroup
        """
        _validate_segment(name, "sandbox_group")
        return SandboxGroup._from_dict(
            self._arm_get(f"{self._group_base}/{name}")
        )

    @distributed_trace
    def create_group(
        self,
        name: str,
        location: str,
        *,
        identity: dict | None = None,
        tags: dict | None = None,
        properties: dict | None = None,
        **kwargs: Any,
    ) -> SandboxGroup:
        """Create or update a sandbox group (returns immediately; ARM may still be provisioning).

        For provisioning completion, prefer :meth:`begin_create_group`.

        :keyword properties: Optional ARM ``properties`` payload. Pass this
            explicitly — request-pipeline options (``headers``,
            ``raw_response_hook``, etc.) belong in ``**kwargs`` and are
            forwarded to the pipeline rather than serialized into the body.
        """
        _validate_segment(name, "sandbox_group")
        body: dict = {"location": location}
        if identity:
            body["identity"] = identity
        if tags:
            body["tags"] = tags
        if properties:
            body["properties"] = properties
        return SandboxGroup._from_dict(
            self._arm_put(f"{self._group_base}/{name}", body)
        )

    @distributed_trace
    def begin_create_group(
        self,
        name: str,
        location: str,
        *,
        identity: dict | None = None,
        tags: dict | None = None,
        properties: dict | None = None,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "LROPoller":
        """Begin creating/updating a sandbox group. Uses ARM's standard LRO
        contract (``Azure-AsyncOperation`` / ``Location`` / ``Retry-After``
        headers via :class:`azure.mgmt.core.polling.arm_polling.ARMPolling`).

        :keyword properties: Optional ARM ``properties`` payload. See
            :meth:`create_group` for the rationale on separating it from
            ``**kwargs``.
        """
        from azure.core.polling import LROPoller
        from azure.mgmt.core.polling.arm_polling import ARMPolling

        _validate_segment(name, "sandbox_group")
        body: dict = {"location": location}
        if identity:
            body["identity"] = identity
        if tags:
            body["tags"] = tags
        if properties:
            body["properties"] = properties

        initial = self._arm_call_raw("PUT", f"{self._group_base}/{name}", body)
        return LROPoller(
            self._pipeline_client(),
            initial,
            lambda resp: SandboxGroup._from_dict(resp.http_response.json()),
            ARMPolling(polling_interval),
        )

    @distributed_trace
    def delete_group(self, name: str, **kwargs: Any) -> None:
        """Delete a sandbox group (returns immediately; does not wait for tombstone)."""
        _validate_segment(name, "sandbox_group")
        self._arm_delete(f"{self._group_base}/{name}")

    @distributed_trace
    def begin_delete_group(
        self,
        name: str,
        *,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "LROPoller":
        """Begin deleting a sandbox group using ARM's standard LRO contract."""
        from azure.core.polling import LROPoller
        from azure.mgmt.core.polling.arm_polling import ARMPolling

        _validate_segment(name, "sandbox_group")
        initial = self._arm_call_raw("DELETE", f"{self._group_base}/{name}")
        return LROPoller(
            self._pipeline_client(),
            initial,
            lambda _: None,
            ARMPolling(polling_interval),
        )

    @distributed_trace
    def patch_group_identity(self, name: str, identity: dict, **kwargs: Any) -> SandboxGroup:
        """Patch managed identity on a sandbox group (returns immediately).

        For provisioning completion, prefer :meth:`begin_patch_group_identity`.
        """
        _validate_segment(name, "sandbox_group")
        return SandboxGroup._from_dict(
            self._arm_patch(f"{self._group_base}/{name}", {"identity": identity})
        )

    @distributed_trace
    def create_or_update_vnet_connection(
        self,
        sandbox_group_name: str,
        connection_name: str,
        subnet_id: str,
        *,
        location: str | None = None,
        **kwargs: Any,
    ) -> dict:
        """Create or update a sandbox group VNet connection.

        :param str sandbox_group_name: Sandbox group name.
        :param str connection_name: VNet connection name.
        :param str subnet_id: Delegated subnet ARM ID.
        :keyword str location: Optional location. If omitted, uses the sandbox
            group's location.
        :returns: ARM VNet connection resource payload.
        :rtype: dict
        """
        _validate_segment(sandbox_group_name, "sandbox_group")
        _validate_segment(connection_name, "connection_name")
        if not subnet_id:
            raise ValueError("subnet_id is required.")

        resolved_location = location
        if not resolved_location:
            group = self.get_group(sandbox_group_name)
            resolved_location = group.location
        if not resolved_location:
            raise ValueError(
                "location is required when sandbox group location cannot be resolved."
            )

        body = {
            "location": resolved_location,
            "properties": {"subnetId": subnet_id},
        }
        return self._arm_put(
            f"{self._group_base}/{sandbox_group_name}/vnetConnections/{connection_name}",
            body,
        )

    @distributed_trace
    def delete_vnet_connection(
        self,
        sandbox_group_name: str,
        connection_name: str,
        **kwargs: Any,
    ) -> None:
        """Delete a sandbox group VNet connection.

        :param str sandbox_group_name: Sandbox group name.
        :param str connection_name: VNet connection name.
        """
        _validate_segment(sandbox_group_name, "sandbox_group")
        _validate_segment(connection_name, "connection_name")
        self._arm_delete(
            f"{self._group_base}/{sandbox_group_name}/vnetConnections/{connection_name}"
        )

    @distributed_trace
    def begin_patch_group_identity(
        self,
        name: str,
        identity: dict,
        *,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "LROPoller":
        """Begin patching identity using ARM's standard LRO contract."""
        from azure.core.polling import LROPoller
        from azure.mgmt.core.polling.arm_polling import ARMPolling

        _validate_segment(name, "sandbox_group")
        initial = self._arm_call_raw(
            "PATCH", f"{self._group_base}/{name}", {"identity": identity}
        )
        return LROPoller(
            self._pipeline_client(),
            initial,
            lambda resp: SandboxGroup._from_dict(resp.http_response.json()),
            ARMPolling(polling_interval),
        )

    # -------------------------------------------------------------------------
    # Context manager / cleanup
    # -------------------------------------------------------------------------

    def close(self) -> None:
        self._pipeline.__exit__(None, None, None)

    def __enter__(self):
        self._pipeline.__enter__()
        return self

    def __exit__(self, *args):
        self._pipeline.__exit__(*args)