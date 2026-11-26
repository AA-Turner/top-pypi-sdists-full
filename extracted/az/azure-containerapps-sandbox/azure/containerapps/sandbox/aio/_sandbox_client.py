"""Async sandbox-scoped data-plane client.

Usage::

    from azure.containerapps.sandbox.aio import SandboxGroupClient
    from azure.containerapps.sandbox import endpoint_for_region

    client = SandboxGroupClient(
        endpoint_for_region("westus2"),
        credential,
        subscription_id="my-sub",
        resource_group="my-rg",
        sandbox_group="my-group",
    )
    sandbox = client.get_sandbox_client("sandbox-123")
    result = await sandbox.exec("echo hello")
    await sandbox.write_file("/tmp/test.txt", "hello")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.exceptions import HttpResponseError
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._api_version import ApiVersion
from azure.containerapps.sandbox._generated.aio._client import SandboxGroupClient as _GeneratedClient
from azure.containerapps.sandbox._port_forward_helpers import _port_forward_url
from azure.containerapps.sandbox.aio._port_forward import PortForwardSession, _open_port_forward
from azure.containerapps.sandbox._helpers import (
    DATA_PLANE_BASE,
    DATA_PLANE_SCOPE,
    _ERROR_MAP,
    _build_async_pipeline,
    _validate_endpoint,
    _validate_segment,
)
from azure.containerapps.sandbox._models import (
    AddVolumeMountRequest,
    DiskImage,
    ExecResult,
    Sandbox,
    LifecyclePolicy,
    SandboxStats,
    Snapshot,
)
from azure.containerapps.sandbox.aio._operations import (
    AsyncEgressOperationsMixin,
    AsyncFileOperationsMixin,
    AsyncPortOperationsMixin,
)
from azure.containerapps.sandbox.models import AddVolumeMountContent
from azure.containerapps.sandbox._response_helpers import _normalize_response

if TYPE_CHECKING:
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.core.pipeline import AsyncPipeline
    from azure.core.pipeline.transport import AsyncHttpTransport

logger = logging.getLogger("azure.containerapps.sandbox")


class SandboxClient(
    AsyncEgressOperationsMixin,
    AsyncPortOperationsMixin,
    AsyncFileOperationsMixin,
):
    """Async data-plane client scoped to a single sandbox.

    Typically obtained via :meth:`SandboxGroupClient.get_sandbox_client` or
    :meth:`SandboxGroupClient.create_sandbox`, but can also be constructed
    directly.

    :param str endpoint: Data-plane endpoint URL (use ``endpoint_for_region()``).
    :param credential: Azure credential for authentication.
    :paramtype credential: ~azure.core.credentials_async.AsyncTokenCredential
    :keyword str subscription_id: Azure subscription ID (**required**).
    :keyword str resource_group: Azure resource group (**required**).
    :keyword str sandbox_group: Sandbox group name (**required**).
    :keyword str sandbox_id: Sandbox ID (**required**).
    :keyword str audience: Override the OAuth scope/audience.
    :keyword api_version: Override the data-plane API version.
    :paramtype api_version: str or ~azure.containerapps.sandbox.ApiVersion
    :keyword transport: Override the HTTP transport (for testing).
    :paramtype transport: ~azure.core.pipeline.transport.AsyncHttpTransport

    Example::

        from azure.containerapps.sandbox.aio import SandboxGroupClient
        from azure.containerapps.sandbox import endpoint_for_region

        group = SandboxGroupClient(
            endpoint_for_region("westus2"), credential,
            subscription_id="sub", resource_group="rg", sandbox_group="sg",
        )
        sandbox = group.get_sandbox_client("sandbox-123")
        result = await sandbox.exec("echo hello")
    """

    def __init__(
        self,
        endpoint: str,
        credential: "AsyncTokenCredential",
        *,
        subscription_id: str,
        resource_group: str,
        sandbox_group: str,
        sandbox_id: str,
        audience: str | None = None,
        api_version: str | ApiVersion = ApiVersion.V2026_09_01_PREVIEW,
        transport: "AsyncHttpTransport | None" = None,
        _pipeline: "AsyncPipeline | None" = None,
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
        if not sandbox_id:
            raise ValueError("sandbox_id is required.")

        _validate_segment(resource_group, "resource_group")
        _validate_segment(sandbox_group, "sandbox_group")
        _validate_segment(sandbox_id, "sandbox_id")

        self._credential = credential
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._sandbox_group = sandbox_group
        self._sandbox_id = sandbox_id
        self._endpoint = _validate_endpoint(endpoint or DATA_PLANE_BASE)
        self._scope = audience or DATA_PLANE_SCOPE
        self._api_version = api_version.value if isinstance(api_version, ApiVersion) else api_version
        self._owns_pipeline = _pipeline is None
        self._pipeline = _pipeline if _pipeline is not None else _build_async_pipeline(
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
    def sandbox_id(self) -> str:
        """The sandbox ID (read-only)."""
        return self._sandbox_id

    @property
    def _group_path(self) -> str:
        """URL path prefix scoped to the sandbox group."""
        return (f"/subscriptions/{self._subscription_id}"
                f"/resourceGroups/{self._resource_group}"
                f"/sandboxGroups/{self._sandbox_group}")

    @property
    def _sbx_path(self) -> str:
        """URL path to this specific sandbox."""
        return f"{self._group_path}/sandboxes/{self._sandbox_id}"

    async def start_port_forward(
        self,
        port: int,
        *,
        container_name: str | None = None,
        connect_timeout: float = 10,
        handshake_timeout: float = 10,
        close_timeout: float = 5,
    ) -> PortForwardSession:
        """Open an owned binary TCP tunnel to an ACA Sandboxes container port.

        Uses this client's regional management endpoint, ARM sandbox scope,
        configured API version, credential, and data-plane audience. Waits for
        TCP connection confirmation; creates no ingress or local listener.
        Cancellation releases the owned WebSocket before propagating.

        :param int port: Target TCP port, from 1 through 65535.
        :keyword str container_name: Optional target container; omitted selects
            the default container.
        :keyword float connect_timeout: WebSocket upgrade timeout in seconds.
        :keyword float handshake_timeout: TCP connected response timeout.
        :keyword float close_timeout: Bounded graceful close timeout.
        :returns: A binary session; use ``async with`` or await ``close()``.
        :rtype: ~azure.containerapps.sandbox.aio.PortForwardSession
        :raises ValueError: On invalid inputs, before authentication/network.
        :raises PortForwardError: On upgrade refusal or protocol/server errors.
        :raises TimeoutError: If a handshake times out.
        """
        url = _port_forward_url(
            self._endpoint,
            self._subscription_id,
            self._resource_group,
            self._sandbox_group,
            self._sandbox_id,
            self._api_version,
            port,
            container_name,
            connect_timeout=connect_timeout,
            handshake_timeout=handshake_timeout,
            close_timeout=close_timeout,
        )
        token = await self._credential.get_token(self._scope)
        return await _open_port_forward(
            url,
            token.token,
            port,
            connect_timeout=connect_timeout,
            handshake_timeout=handshake_timeout,
            close_timeout=close_timeout,
        )

    # -------------------------------------------------------------------------
    # Sandbox lifecycle
    # -------------------------------------------------------------------------

    _RESUMABLE_STATES = frozenset({"stopped", "suspended", "idle"})
    _TERMINAL_STATES = frozenset({"deleting", "failed"})

    @distributed_trace_async
    async def get(self, **kwargs: Any) -> Sandbox:
        """Get this sandbox's current state."""
        return await self._generated.sandboxes.get(
            self._sandbox_id,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )

    @distributed_trace_async
    async def delete(self, **kwargs: Any) -> None:
        """Delete this sandbox (returns immediately; does not wait for tombstone)."""
        await self._generated.sandboxes.delete(
            self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace_async
    async def begin_delete(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "AsyncLROPoller":
        """Begin deleting this sandbox; poll until GET returns 404."""
        from azure.core.polling import AsyncLROPoller
        from azure.containerapps.sandbox.aio._polling import AsyncDeletionPoller

        await self.delete(**kwargs)
        polling_method = AsyncDeletionPoller(
            getter=self.get,
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id}",
        )
        return AsyncLROPoller(self, None, lambda _: None, polling_method)

    @distributed_trace_async
    async def stop(self, **kwargs: Any) -> None:
        """Stop (suspend) this sandbox (returns immediately)."""
        await self._generated.sandboxes.stop(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace_async
    async def begin_stop(
        self, *, polling_timeout: int = 180, polling_interval: int = 3, **kwargs: Any,
    ) -> "AsyncLROPoller":
        """Begin stopping; poll until state in ``Stopped``/``Suspended``."""
        from azure.core.polling import AsyncLROPoller
        from azure.containerapps.sandbox.aio._polling import AsyncResourceStatePoller

        await self.stop(**kwargs)
        polling_method = AsyncResourceStatePoller(
            getter=self.get,
            state_fn=lambda s: s.state,
            target_states=("Stopped", "Suspended", "Idle"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id} (stop)",
        )
        return AsyncLROPoller(self, None, lambda _: polling_method.resource(), polling_method)

    @distributed_trace_async
    async def resume(self, **kwargs: Any) -> None:
        """Resume this sandbox (returns immediately)."""
        await self._generated.sandboxes.resume(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace_async
    async def begin_resume(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "AsyncLROPoller":
        """Begin resuming; poll until state == ``Running``."""
        from azure.core.polling import AsyncLROPoller
        from azure.containerapps.sandbox.aio._polling import AsyncResourceStatePoller

        await self.resume(**kwargs)
        polling_method = AsyncResourceStatePoller(
            getter=self.get,
            state_fn=lambda s: s.state,
            target_states=("Running",),
            failed_states=("Failed", "Deleting"),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id} (resume)",
        )
        return AsyncLROPoller(self, None, lambda _: polling_method.resource(), polling_method)

    async def wait_for_running(
        self,
        *,
        timeout: int = 180,
        poll_interval: int = 3,
        **kwargs: Any,
    ) -> Sandbox:
        """Poll until this sandbox reaches *Running* state.

        :param int timeout: Maximum seconds to wait (default 180).
        :param int poll_interval: Seconds between polls (default 3).
        :raises TimeoutError: If the sandbox does not reach Running within *timeout*.
        :raises RuntimeError: If the sandbox enters a terminal state (Deleting, Failed).
        :returns: The sandbox in Running state.
        """
        import asyncio
        import time

        deadline = time.monotonic() + timeout
        while True:
            sbx = await self.get()
            state = (sbx.state or "").lower()
            if state == "running":
                return sbx
            if state in self._TERMINAL_STATES:
                raise RuntimeError(
                    f"Sandbox {self._sandbox_id} entered terminal state '{sbx.state}'"
                )
            if time.monotonic() > deadline:
                raise TimeoutError(
                    f"Sandbox {self._sandbox_id} did not reach Running state "
                    f"within {timeout}s (last state: '{sbx.state}')"
                )
            logger.info(
                "Waiting for sandbox %s (state=%s), polling in %ds...",
                self._sandbox_id, sbx.state, poll_interval,
            )
            await asyncio.sleep(poll_interval)

    async def ensure_running(self, *, timeout: int = 300, **kwargs: Any) -> None:
        """Ensure this sandbox is Running, resuming it if necessary.

        If the sandbox is Stopped or Suspended it is resumed automatically,
        unless ``state_details.stopped_reason`` is ``Disabled``.  If already
        Running this returns immediately.

        Mirrors the Rust CLI ``ensure_running_with_client()`` pattern.

        :param int timeout: Maximum seconds to wait for Running state (default 300).
        :raises RuntimeError: If the sandbox is in a non-resumable terminal state
            or administratively disabled.
        """
        sbx = await self.get()
        state = (sbx.state or "").lower()

        if state == "running":
            return

        if state in self._TERMINAL_STATES:
            raise RuntimeError(
                f"Sandbox {self._sandbox_id} is in '{sbx.state}' state and "
                "cannot be resumed."
            )

        if state in self._RESUMABLE_STATES:
            # Check if administratively disabled via state_details
            if sbx.state_details is not None and sbx.state_details.stopped_reason == "Disabled":
                raise RuntimeError(
                    f"Sandbox {self._sandbox_id} is administratively disabled "
                    "(stopped_reason='Disabled') and cannot be auto-resumed. "
                    "To re-enable the sandbox and restore auto-resume capability, "
                    "call the enable endpoint (POST /sandboxes/<id>/enable) "
                    "or contact your administrator."
                )
            logger.info("Auto-resuming sandbox %s (state=%s)...", self._sandbox_id, sbx.state)
            try:
                await self.resume()
            except HttpResponseError:
                pass  # may already be resuming
            await self.wait_for_running(timeout=timeout)
            return

        raise RuntimeError(
            f"Sandbox {self._sandbox_id} is in unexpected state '{sbx.state}'."
        )

    # -------------------------------------------------------------------------
    # Exec
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def exec(self, command: str, *,
                   working_directory: str | None = None,
                   **kwargs: Any) -> ExecResult:
        """Execute a shell command in this sandbox.

        .. warning::
            **Never interpolate untrusted user input** into the ``command`` string.
            Commands execute inside the sandbox VM. Use ``shlex.quote()`` for
            user-provided arguments.
        """
        body: dict = {"command": command}
        if working_directory:
            body["workingDirectory"] = working_directory
        return await self._generated.sandboxes.execute_shell_command(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    # -------------------------------------------------------------------------
    # Snapshot
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def create_snapshot(self, *, name: str | None = None, **kwargs: Any) -> Snapshot:
        """Create a snapshot of this sandbox (returns immediately)."""
        body = {"labels": {"name": name}} if name else {}
        return await self._generated.sandboxes.create_snapshot(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace_async
    async def begin_create_snapshot(
        self,
        *,
        name: str | None = None,
        polling_timeout: int = 600,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "AsyncLROPoller":
        """Begin creating a snapshot. See sync :meth:`SandboxClient.begin_create_snapshot`."""
        from azure.core.polling import AsyncLROPoller
        from azure.containerapps.sandbox.aio._polling import AsyncResourceExistsPoller

        initial = await self.create_snapshot(name=name, **kwargs)
        group_client = self._group_client_for_polling()
        polling_method = AsyncResourceExistsPoller(
            getter=lambda: group_client.get_snapshot(initial.id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Snapshot {initial.id}",
            initial_resource=initial,
        )
        return AsyncLROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    def _group_client_for_polling(self):
        from azure.containerapps.sandbox.aio._sandboxgroup_client import SandboxGroupClient

        return SandboxGroupClient(
            self._endpoint,
            self._credential,
            subscription_id=self._subscription_id,
            resource_group=self._resource_group,
            sandbox_group=self._sandbox_group,
            api_version=self._api_version,
            audience=self._scope,
            _pipeline=self._pipeline,
        )

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def get_stats(self, **kwargs: Any) -> SandboxStats:
        """Get sandbox resource stats."""
        return await self._generated.sandboxes.get_stats(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    # -------------------------------------------------------------------------
    # Lifecycle policy
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def set_lifecycle_policy(self, policy: LifecyclePolicy, **kwargs: Any) -> LifecyclePolicy:
        """Set lifecycle policy (auto-suspend, auto-delete)."""
        result = await self._generated.sandboxes.set_lifecycle_policy(
            self._sandbox_id,
            policy,
            **{"error_map": _ERROR_MAP, **kwargs},
        )
        return result.lifecycle if result.lifecycle is not None else LifecyclePolicy()

    # -------------------------------------------------------------------------
    # Commit (save sandbox as disk image)
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def commit(self, *, name: str | None = None, **kwargs: Any) -> DiskImage:
        """Commit sandbox state as a new disk image (returns immediately)."""
        body = {"labels": {"name": name}} if name else {}
        result = await self._generated.sandboxes.commit(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, **kwargs},
        )
        if "diskImage" in result:
            return result.disk_image
        resp = dict(result)
        if isinstance(resp, dict) and "diskImageId" in resp and "id" not in resp:
            resp = dict(resp)
            resp["id"] = resp["diskImageId"]
            if name:
                resp.setdefault("name", name)
                resp.setdefault("labels", {}).setdefault("name", name)
        return DiskImage(resp)

    @distributed_trace_async
    async def begin_commit(
        self,
        *,
        name: str | None = None,
        polling_timeout: int = 900,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "AsyncLROPoller":
        """Begin committing; poll until ``status.state == "Ready"``."""
        from azure.core.polling import AsyncLROPoller
        from azure.containerapps.sandbox.aio._polling import AsyncResourceStatePoller

        initial = await self.commit(name=name, **kwargs)
        group_client = self._group_client_for_polling()
        polling_method = AsyncResourceStatePoller(
            getter=lambda: group_client.get_disk_image(initial.id),
            state_fn=lambda i: i.status.state if (i and i.status) else None,
            target_states=("Ready", "Succeeded"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {initial.id} (commit)",
            initial_resource=initial,
        )
        return AsyncLROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    # -------------------------------------------------------------------------
    # Volume mount
    # -------------------------------------------------------------------------

    @distributed_trace_async
    async def add_volume_mount(self, volume_mount: AddVolumeMountRequest, **kwargs: Any) -> None:
        """Add a volume mount to this sandbox."""
        await self._generated.sandboxes.add_volume_mount(
            self._sandbox_id,
            AddVolumeMountContent(volume_mount=volume_mount),
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    async def close(self) -> None:
        """Close the client. No-op if the pipeline is shared from a parent."""
        if self._owns_pipeline:
            await self._pipeline.__aexit__(None, None, None)

    async def __aenter__(self):
        if self._owns_pipeline:
            await self._pipeline.__aenter__()
        return self

    async def __aexit__(self, *args):
        if self._owns_pipeline:
            await self._pipeline.__aexit__(*args)
