"""Sandbox-scoped data-plane client.

Usage::

    from azure.containerapps.sandbox import SandboxGroupClient, endpoint_for_region

    client = SandboxGroupClient(
        endpoint_for_region("westus2"),
        credential,
        subscription_id="my-sub",
        resource_group="my-rg",
        sandbox_group="my-group",
    )
    sandbox = client.get_sandbox_client("sandbox-123")
    result = sandbox.exec("echo hello")
    sandbox.write_file("/tmp/test.txt", "hello")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.exceptions import HttpResponseError
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._api_version import ApiVersion
from azure.containerapps.sandbox._generated._client import SandboxGroupClient as _GeneratedClient
from azure.containerapps.sandbox._port_forward import PortForwardSession, _open_port_forward
from azure.containerapps.sandbox._port_forward_helpers import _port_forward_url
from azure.containerapps.sandbox._helpers import (
    DATA_PLANE_BASE,
    DATA_PLANE_SCOPE,
    _ERROR_MAP,
    _build_pipeline,
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
from azure.containerapps.sandbox._operations import (
    EgressOperationsMixin,
    FileOperationsMixin,
    PortOperationsMixin,
)
from azure.containerapps.sandbox.models import AddVolumeMountContent
from azure.containerapps.sandbox._response_helpers import _normalize_response

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.pipeline import Pipeline
    from azure.core.pipeline.transport import HttpTransport

logger = logging.getLogger("azure.containerapps.sandbox")


class SandboxClient(
    EgressOperationsMixin,
    PortOperationsMixin,
    FileOperationsMixin,
):
    """Data-plane client scoped to a single sandbox.

    Typically obtained via :meth:`SandboxGroupClient.get_sandbox_client` or
    :meth:`SandboxGroupClient.create_sandbox`, but can also be constructed
    directly.

    :param str endpoint: Data-plane endpoint URL (use ``endpoint_for_region()``).
    :param credential: Azure credential for authentication.
    :paramtype credential: ~azure.core.credentials.TokenCredential
    :keyword str subscription_id: Azure subscription ID (**required**).
    :keyword str resource_group: Azure resource group (**required**).
    :keyword str sandbox_group: Sandbox group name (**required**).
    :keyword str sandbox_id: Sandbox ID (**required**).
    :keyword str audience: Override the OAuth scope/audience.
    :keyword api_version: Override the data-plane API version.
    :paramtype api_version: str or ~azure.containerapps.sandbox.ApiVersion
    :keyword transport: Override the HTTP transport (for testing).
    :paramtype transport: ~azure.core.pipeline.transport.HttpTransport

    Example::

        from azure.containerapps.sandbox import SandboxGroupClient, endpoint_for_region

        group = SandboxGroupClient(
            endpoint_for_region("westus2"), credential,
            subscription_id="sub", resource_group="rg", sandbox_group="sg",
        )
        sandbox = group.get_sandbox_client("sandbox-123")
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
        sandbox_id: str,
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

    def start_port_forward(
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

        :param int port: Target TCP port, from 1 through 65535.
        :keyword str container_name: Optional target container; omitted selects
            the default container.
        :keyword float connect_timeout: WebSocket upgrade timeout in seconds.
        :keyword float handshake_timeout: TCP connected response timeout.
        :keyword float close_timeout: Bounded graceful close timeout.
        :returns: A binary session; use ``with`` or call ``close()``.
        :rtype: ~azure.containerapps.sandbox.PortForwardSession
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
        token = self._credential.get_token(self._scope)
        return _open_port_forward(
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

    @distributed_trace
    def get(self, **kwargs: Any) -> Sandbox:
        """Get this sandbox's current state."""
        return self._generated.sandboxes.get(
            self._sandbox_id,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )

    @distributed_trace
    def delete(self, **kwargs: Any) -> None:
        """Delete this sandbox (returns immediately; does not wait for tombstone)."""
        self._generated.sandboxes.delete(
            self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace
    def begin_delete(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin deleting this sandbox; poll until GET returns 404."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import DeletionPoller

        self.delete(**kwargs)
        polling_method = DeletionPoller(
            getter=self.get,
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)

    @distributed_trace
    def stop(self, **kwargs: Any) -> None:
        """Stop (suspend) this sandbox (returns immediately)."""
        self._generated.sandboxes.stop(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_stop(
        self, *, polling_timeout: int = 180, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin stopping this sandbox; poll until state in ``Stopped``/``Suspended``."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceStatePoller

        self.stop(**kwargs)
        polling_method = ResourceStatePoller(
            getter=self.get,
            state_fn=lambda s: s.state,
            target_states=("Stopped", "Suspended", "Idle"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id} (stop)",
        )
        return LROPoller(self, None, lambda _: polling_method.resource(), polling_method)

    @distributed_trace
    def resume(self, **kwargs: Any) -> None:
        """Resume this sandbox (returns immediately)."""
        self._generated.sandboxes.resume(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_resume(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin resuming this sandbox; poll until state == ``Running``."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceStatePoller

        self.resume(**kwargs)
        polling_method = ResourceStatePoller(
            getter=self.get,
            state_fn=lambda s: s.state,
            target_states=("Running",),
            failed_states=("Failed", "Deleting"),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {self._sandbox_id} (resume)",
        )
        return LROPoller(self, None, lambda _: polling_method.resource(), polling_method)

    def wait_for_running(
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
        import time

        deadline = time.monotonic() + timeout
        while True:
            sbx = self.get()
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
            time.sleep(poll_interval)

    def ensure_running(self, *, timeout: int = 300, **kwargs: Any) -> None:
        """Ensure this sandbox is Running, resuming it if necessary.

        If the sandbox is Stopped or Suspended it is resumed automatically,
        unless ``state_details.stopped_reason`` is ``Disabled``.  If already
        Running this returns immediately.

        Mirrors the Rust CLI ``ensure_running_with_client()`` pattern.

        :param int timeout: Maximum seconds to wait for Running state (default 300).
        :raises RuntimeError: If the sandbox is in a non-resumable terminal state
            or administratively disabled.
        """
        sbx = self.get()
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
                self.resume()
            except HttpResponseError:
                pass  # may already be resuming
            self.wait_for_running(timeout=timeout)
            return

        raise RuntimeError(
            f"Sandbox {self._sandbox_id} is in unexpected state '{sbx.state}'."
        )

    # -------------------------------------------------------------------------
    # Exec
    # -------------------------------------------------------------------------

    @distributed_trace
    def exec(self, command: str, *,
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
        return self._generated.sandboxes.execute_shell_command(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    # -------------------------------------------------------------------------
    # Snapshot
    # -------------------------------------------------------------------------

    @distributed_trace
    def create_snapshot(self, *, name: str | None = None, **kwargs: Any) -> Snapshot:
        """Create a snapshot of this sandbox (returns immediately).

        For build completion, prefer :meth:`begin_create_snapshot`.
        """
        body = {"labels": {"name": name}} if name else {}
        return self._generated.sandboxes.create_snapshot(
            self._sandbox_id,
            body,
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace
    def begin_create_snapshot(
        self,
        *,
        name: str | None = None,
        polling_timeout: int = 600,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "LROPoller":
        """Begin creating a snapshot.

        The dataplane ``POST /snapshot`` endpoint is synchronous: it returns
        the populated :class:`Snapshot` (id, ``sizeInMB``, etc.) once the
        snapshot has been captured. The returned :class:`LROPoller` therefore
        verifies that the snapshot is :meth:`get_snapshot`\\ -able from the
        group-scoped path (handling eventual consistency) and then completes.
        """
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceExistsPoller

        initial = self.create_snapshot(name=name, **kwargs)
        group_client = self._group_client_for_polling()
        polling_method = ResourceExistsPoller(
            getter=lambda: group_client.get_snapshot(initial.id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Snapshot {initial.id}",
            initial_resource=initial,
        )
        return LROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    def _group_client_for_polling(self):
        """Build a transient :class:`SandboxGroupClient` sharing this pipeline.

        Used by ``begin_*`` methods that need to poll group-scoped resources
        (snapshots, disk images) created by sandbox operations.
        """
        from azure.containerapps.sandbox._sandboxgroup_client import SandboxGroupClient

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

    @distributed_trace
    def get_stats(self, **kwargs: Any) -> SandboxStats:
        """Get sandbox resource stats."""
        return self._generated.sandboxes.get_stats(self._sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    # -------------------------------------------------------------------------
    # Lifecycle policy
    # -------------------------------------------------------------------------

    @distributed_trace
    def set_lifecycle_policy(self, policy: LifecyclePolicy, **kwargs: Any) -> LifecyclePolicy:
        """Set lifecycle policy (auto-suspend, auto-delete)."""
        result = self._generated.sandboxes.set_lifecycle_policy(
            self._sandbox_id,
            policy,
            **{"error_map": _ERROR_MAP, **kwargs},
        )
        return result.lifecycle if result.lifecycle is not None else LifecyclePolicy()

    # -------------------------------------------------------------------------
    # Commit (save sandbox as disk image)
    # -------------------------------------------------------------------------

    @distributed_trace
    def commit(self, *, name: str | None = None, **kwargs: Any) -> DiskImage:
        """Commit sandbox state as a new disk image (returns immediately).

        For build completion, prefer :meth:`begin_commit`.
        """
        body = {"labels": {"name": name}} if name else {}
        result = self._generated.sandboxes.commit(self._sandbox_id, body, **{"error_map": _ERROR_MAP, **kwargs})
        if "diskImage" in result:
            return result.disk_image
        resp = dict(result)
        # Legacy variant: top-level ``diskImageId`` without ``id``.
        if isinstance(resp, dict) and "diskImageId" in resp and "id" not in resp:
            resp = dict(resp)
            resp["id"] = resp["diskImageId"]
            if name:
                resp.setdefault("name", name)
                resp.setdefault("labels", {}).setdefault("name", name)
        return DiskImage(resp)

    @distributed_trace
    def begin_commit(
        self,
        *,
        name: str | None = None,
        polling_timeout: int = 900,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> "LROPoller":
        """Begin committing sandbox state as a disk image; poll until ``status.state == "Ready"``."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceStatePoller

        initial = self.commit(name=name, **kwargs)
        group_client = self._group_client_for_polling()
        polling_method = ResourceStatePoller(
            getter=lambda: group_client.get_disk_image(initial.id),
            state_fn=lambda i: i.status.state if (i and i.status) else None,
            target_states=("Ready", "Succeeded"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {initial.id} (commit)",
            initial_resource=initial,
        )
        return LROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    # -------------------------------------------------------------------------
    # Volume mount
    # -------------------------------------------------------------------------

    @distributed_trace
    def add_volume_mount(self, volume_mount: AddVolumeMountRequest, **kwargs: Any) -> None:
        """Add a volume mount to this sandbox."""
        self._generated.sandboxes.add_volume_mount(
            self._sandbox_id,
            AddVolumeMountContent(volume_mount=volume_mount),
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def close(self) -> None:
        """Close the client. No-op if the pipeline is shared from a parent."""
        if self._owns_pipeline:
            self._pipeline.__exit__(None, None, None)

    def __enter__(self):
        if self._owns_pipeline:
            self._pipeline.__enter__()
        return self

    def __exit__(self, *args):
        if self._owns_pipeline:
            self._pipeline.__exit__(*args)
