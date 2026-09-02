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
        api_version: str | ApiVersion = ApiVersion.V2026_02_01_PREVIEW,
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
        self._pipeline = _pipeline or _build_pipeline(
            credential, self._scope, transport=transport, **kwargs
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

    # -------------------------------------------------------------------------
    # Internal HTTP
    # -------------------------------------------------------------------------

    def _send_request(self, request: HttpRequest, *, stream: bool = False) -> HttpResponse:
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
    # Sandbox lifecycle
    # -------------------------------------------------------------------------

    _RESUMABLE_STATES = frozenset({"stopped", "suspended", "idle"})
    _TERMINAL_STATES = frozenset({"deleting", "failed"})

    @distributed_trace
    def get(self, **kwargs: Any) -> Sandbox:
        """Get this sandbox's current state."""
        return Sandbox._from_dict(self._dp_get(self._sbx_path))

    @distributed_trace
    def delete(self, **kwargs: Any) -> None:
        """Delete this sandbox (returns immediately; does not wait for tombstone)."""
        self._dp_delete(self._sbx_path)

    @distributed_trace
    def begin_delete(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin deleting this sandbox; poll until GET returns 404."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import DeletionPoller

        self._dp_delete(self._sbx_path)
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
        self._dp_post(f"{self._sbx_path}/stop")

    @distributed_trace
    def begin_stop(
        self, *, polling_timeout: int = 180, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin stopping this sandbox; poll until state in ``Stopped``/``Suspended``."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceStatePoller

        self._dp_post(f"{self._sbx_path}/stop")
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
        self._dp_post(f"{self._sbx_path}/resume")

    @distributed_trace
    def begin_resume(
        self, *, polling_timeout: int = 300, polling_interval: int = 3, **kwargs: Any,
    ) -> "LROPoller":
        """Begin resuming this sandbox; poll until state == ``Running``."""
        from azure.core.polling import LROPoller
        from azure.containerapps.sandbox._polling import ResourceStatePoller

        self._dp_post(f"{self._sbx_path}/resume")
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
            if sbx.state_details and not sbx.state_details.is_auto_resume_allowed():
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
        return ExecResult._from_dict(self._dp_post(f"{self._sbx_path}/executeShellCommand", body))

    # -------------------------------------------------------------------------
    # Snapshot
    # -------------------------------------------------------------------------

    @distributed_trace
    def create_snapshot(self, *, name: str | None = None, **kwargs: Any) -> Snapshot:
        """Create a snapshot of this sandbox (returns immediately).

        For build completion, prefer :meth:`begin_create_snapshot`.
        """
        body = {"labels": {"name": name}} if name else {}
        return Snapshot._from_dict(self._dp_post(f"{self._sbx_path}/snapshot", body))

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

        initial = self.create_snapshot(name=name)
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
        return SandboxStats._from_dict(self._dp_get(f"{self._sbx_path}/stats"))

    # -------------------------------------------------------------------------
    # Lifecycle policy
    # -------------------------------------------------------------------------

    @distributed_trace
    def set_lifecycle_policy(self, policy: LifecyclePolicy, **kwargs: Any) -> LifecyclePolicy:
        """Set lifecycle policy (auto-suspend, auto-delete)."""
        wire = policy._to_dict()
        result = self._dp_post(f"{self._sbx_path}/lifecycle", wire)
        return LifecyclePolicy._from_dict(result if isinstance(result, dict) else None) or LifecyclePolicy()

    # -------------------------------------------------------------------------
    # Commit (save sandbox as disk image)
    # -------------------------------------------------------------------------

    @distributed_trace
    def commit(self, *, name: str | None = None, **kwargs: Any) -> DiskImage:
        """Commit sandbox state as a new disk image (returns immediately).

        For build completion, prefer :meth:`begin_commit`.
        """
        body = {"labels": {"name": name}} if name else {}
        resp = self._dp_post(f"{self._sbx_path}/commit", body)
        # The dataplane wraps the result as ``{"diskImage": {...}}``.
        if isinstance(resp, dict) and "diskImage" in resp:
            resp = resp["diskImage"]
        # Legacy variant: top-level ``diskImageId`` without ``id``.
        if isinstance(resp, dict) and "diskImageId" in resp and "id" not in resp:
            resp = dict(resp)
            resp["id"] = resp["diskImageId"]
            if name:
                resp.setdefault("name", name)
                resp.setdefault("labels", {}).setdefault("name", name)
        return DiskImage._from_dict(resp)

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

        initial = self.commit(name=name)
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
        self._dp_post(f"{self._sbx_path}/volumes/add", volume_mount._to_dict())

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
