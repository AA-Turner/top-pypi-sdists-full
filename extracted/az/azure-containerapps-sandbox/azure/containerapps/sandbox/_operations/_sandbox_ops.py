"""Sandbox CRUD operations for group-scoped client."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import (
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import (
    AddPortRequest,
    EgressPolicy,
    Sandbox,
    SandboxVolume,
)
from azure.containerapps.sandbox._polling import (
    DeletionPoller,
    ResourceStatePoller,
)
from azure.containerapps.sandbox._egress_helpers import validate_egress_policy
from azure.containerapps.sandbox._port_helpers import _prepare_port
from azure.containerapps.sandbox._response_helpers import _normalize_page, _normalize_response
from azure.containerapps.sandbox.models import CreateSandboxContent

if TYPE_CHECKING:
    from azure.containerapps.sandbox._sandbox_client import SandboxClient


class SandboxOperationsMixin:
    """Sandbox CRUD operations on a sandbox group."""

    @distributed_trace
    def list_sandboxes(self, *, labels: dict[str, str] | None = None,
                       states: list[str] | None = None,
                       **kwargs: Any) -> ItemPaged[Sandbox]:
        """List sandboxes in this sandbox group.

        :keyword dict labels: Filter by labels (key=value pairs).
        :keyword list[str] states: Filter by persisted states: Running, Stopped,
            Creating, Stopping, or StopFailed. Combined with labels using AND.
            Filtered results are eventually consistent and may differ from GET
            or unfiltered listing. None or an empty list omits the state filter.
        """
        if isinstance(states, str):
            raise TypeError("states must be a list of state names, not a string")
        return self._generated.sandboxes.list(
            labels=",".join(f"{k}={v}" for k, v in labels.items()) if labels else None,
            states=states or None,
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace
    def get_sandbox(self, sandbox_id: str, **kwargs: Any) -> Sandbox:
        """Get a sandbox by ID."""
        _validate_segment(sandbox_id, "sandbox_id")
        return self._generated.sandboxes.get(
            sandbox_id,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )

    @distributed_trace
    def create_sandbox(
        self,
        *,
        disk: str | None = "ubuntu",
        disk_id: str | None = None,
        snapshot_id: str | None = None,
        preset: str | None = None,
        cpu: str = "1000m",
        memory: str = "2048Mi",
        disk_size: str | None = None,
        auto_suspend_seconds: int = 300,
        auto_suspend_mode: Literal["Memory", "Disk"] = "Memory",
        labels: dict[str, str] | None = None,
        environment: dict[str, str] | None = None,
        connections: list[str] | None = None,
        egress_policy: EgressPolicy | None = None,
        volumes: list[SandboxVolume] | None = None,
        ports: list[AddPortRequest | int] | None = None,
        entrypoint: list[str] | None = None,
        cmd: list[str] | None = None,
        skip_egress_proxy: bool | None = None,
        customer_vnet_connection_name: str | None = None,
        vmm_type: str | None = None,
        **kwargs: Any,
    ) -> SandboxClient:
        """Create a sandbox and return its client on HTTP 201, without polling.

        Sources (pick exactly one): ``disk`` (public image name, default
        ``"ubuntu"``), ``disk_id`` (private image ID), ``snapshot_id``, or
        ``preset`` (for example, ``"GitHubCopilot"``). An explicit source
        overrides the default ``disk``.

        :keyword str disk_size: Optional base disk size, such as ``"20Gi"``.
            Ignored for ``preset`` and ``snapshot_id`` sources.
        :keyword str auto_suspend_mode: ``"Memory"`` (default) or ``"Disk"``.
            DataDisk volumes require ``"Disk"`` mode.
        :raises ValueError: If sources conflict or snapshot options are invalid.
        :returns: The created sandbox's client. No follow-up GET is issued;
            use :meth:`begin_create_sandbox` to explicitly wait for *Running*.
        :rtype: ~azure.containerapps.sandbox.SandboxClient
        """
        sandbox_client, _ = self._do_create_sandbox(
            disk=disk, disk_id=disk_id, snapshot_id=snapshot_id, preset=preset,
            cpu=cpu, memory=memory, disk_size=disk_size,
            auto_suspend_seconds=auto_suspend_seconds,
            auto_suspend_mode=auto_suspend_mode,
            labels=labels, environment=environment, connections=connections,
            egress_policy=egress_policy, volumes=volumes, ports=ports,
            entrypoint=entrypoint, cmd=cmd, skip_egress_proxy=skip_egress_proxy,
            customer_vnet_connection_name=customer_vnet_connection_name,
            vmm_type=vmm_type, **kwargs,
        )
        return sandbox_client

    @distributed_trace
    def begin_create_sandbox(
        self,
        *,
        disk: str | None = "ubuntu",
        disk_id: str | None = None,
        snapshot_id: str | None = None,
        preset: str | None = None,
        cpu: str = "1000m",
        memory: str = "2048Mi",
        disk_size: str | None = None,
        auto_suspend_seconds: int = 300,
        auto_suspend_mode: Literal["Memory", "Disk"] = "Memory",
        labels: dict[str, str] | None = None,
        environment: dict[str, str] | None = None,
        connections: list[str] | None = None,
        egress_policy: EgressPolicy | None = None,
        volumes: list[SandboxVolume] | None = None,
        ports: list[AddPortRequest | int] | None = None,
        entrypoint: list[str] | None = None,
        cmd: list[str] | None = None,
        skip_egress_proxy: bool | None = None,
        customer_vnet_connection_name: str | None = None,
        vmm_type: str | None = None,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin creating a sandbox; returns an :class:`~azure.core.polling.LROPoller`.

        Call :meth:`~azure.core.polling.LROPoller.result` to block until the
        sandbox reaches *Running* state and obtain the resulting
        :class:`~azure.containerapps.sandbox.SandboxClient`. Use
        :meth:`~azure.core.polling.LROPoller.status` /
        :meth:`~azure.core.polling.LROPoller.done` to poll non-blockingly,
        or launch many in parallel and ``[p.result() for p in pollers]``.

        Sources (pick exactly one): see :meth:`create_sandbox`.

        :keyword str disk_size: Optional base disk size (a storage quantity such
            as "20Gi"). Maps to ``resources.disk``. Ignored for ``preset`` and
            ``snapshot_id`` sources.
        :keyword str auto_suspend_mode: Auto-suspend mode, ``"Memory"`` (default)
            or ``"Disk"``. DataDisk volumes require ``"Disk"`` mode.
        :keyword int polling_timeout: Max seconds to wait for *Running* (default 300).
        :keyword int polling_interval: Seconds between polls (default 3).
        :raises ValueError: If zero or multiple sources are provided, or if
            ``snapshot_id`` is combined with options the service rejects.
        :returns: A poller whose ``result()`` is a sandbox-scoped client.
        :rtype: ~azure.core.polling.LROPoller[~azure.containerapps.sandbox.SandboxClient]
        """
        sandbox_client, initial_sbx = self._do_create_sandbox(
            disk=disk, disk_id=disk_id, snapshot_id=snapshot_id, preset=preset,
            cpu=cpu, memory=memory, disk_size=disk_size,
            auto_suspend_seconds=auto_suspend_seconds,
            auto_suspend_mode=auto_suspend_mode,
            labels=labels, environment=environment, connections=connections,
            egress_policy=egress_policy, volumes=volumes, ports=ports,
            entrypoint=entrypoint, cmd=cmd, skip_egress_proxy=skip_egress_proxy,
            customer_vnet_connection_name=customer_vnet_connection_name,
            vmm_type=vmm_type, **kwargs,
        )
        polling_method = ResourceStatePoller(
            getter=lambda: self.get_sandbox(initial_sbx.id),
            state_fn=lambda s: s.state,
            target_states=("Running",),
            failed_states=("Failed", "Deleting"),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {initial_sbx.id}",
            transform=lambda _: sandbox_client,
            initial_resource=initial_sbx,
        )
        return LROPoller(self, initial_sbx, lambda _: sandbox_client, polling_method)

    def _do_create_sandbox(
        self,
        *,
        disk, disk_id, snapshot_id, preset,
        cpu, memory, disk_size, auto_suspend_seconds,
        auto_suspend_mode,
        labels, environment, connections,
        egress_policy, volumes, ports,
        entrypoint, cmd, skip_egress_proxy,
        customer_vnet_connection_name, vmm_type,
        **kwargs,
    ):
        """Validate, create via generated REST, and return ``(SandboxClient, Sandbox)``."""
        # --- Validate sources (Bug 4: multi-source picked silently) ---
        explicit = [k for k, v in (
            ("preset", preset),
            ("snapshot_id", snapshot_id),
            ("disk_id", disk_id),
        ) if v]
        if len(explicit) > 1:
            raise ValueError(
                f"create_sandbox: provide exactly one source — got {explicit}. "
                "Sources are mutually exclusive: preset, snapshot_id, disk_id, disk."
            )
        if explicit and disk and disk != "ubuntu":
            raise ValueError(
                f"create_sandbox: cannot combine 'disk={disk!r}' with {explicit[0]!r}."
            )

        # --- Validate snapshot_id incompatible options (Bug 3) ---
        if snapshot_id:
            forbidden = {
                "labels": labels, "environment": environment, "connections": connections,
                "egress_policy": egress_policy, "volumes": volumes, "ports": ports,
                "entrypoint": entrypoint, "cmd": cmd,
                "skip_egress_proxy": skip_egress_proxy,
                "customer_vnet_connection_name": customer_vnet_connection_name,
                "vmm_type": vmm_type,
            }
            bad = [k for k, v in forbidden.items() if v or (k == "egress_policy" and v is not None)]
            if bad:
                raise ValueError(
                    f"create_sandbox(snapshot_id=...): the following options are "
                    f"not supported when restoring from a snapshot: {bad}. "
                    "Snapshot restore replays the captured sandbox state as-is."
                )

        body: dict = {}
        if preset:
            body["presetSandboxType"] = preset
        elif snapshot_id:
            body["sourcesRef"] = {"snapshot": {"id": snapshot_id}}
        elif disk_id:
            body["sourcesRef"] = {"diskImage": {"id": disk_id}}
        else:
            body["sourcesRef"] = {"diskImage": {"name": disk or "ubuntu", "isPublic": True}}

        if not preset and not snapshot_id:
            resources = {"cpu": cpu, "memory": memory}
            if disk_size:
                resources["disk"] = disk_size
            body["resources"] = resources

        # Lifecycle/labels/env/etc apply to everything EXCEPT snapshot restore
        # (snapshot restore replays captured state as-is — validated above).
        if not snapshot_id:
            body["lifecycle"] = {
                "autoSuspendPolicy": {"enabled": True, "interval": auto_suspend_seconds, "mode": auto_suspend_mode}
            }
            if labels:
                body["labels"] = labels
            if environment:
                body["environment"] = environment
            if connections:
                body["connections"] = connections
            if egress_policy is not None:
                validate_egress_policy(egress_policy)
                body["egressPolicy"] = egress_policy
            if volumes:
                body["volumes"] = volumes
            if ports:
                body["ports"] = [_prepare_port(port) for port in ports]
            if entrypoint:
                body["entrypoint"] = entrypoint
            if cmd:
                body["cmd"] = cmd
            if skip_egress_proxy is not None:
                body["skipEgressProxy"] = skip_egress_proxy
            if customer_vnet_connection_name:
                body["vnetConnectionName"] = customer_vnet_connection_name
            if vmm_type:
                body["vmmType"] = vmm_type

        sbx = self._generated.sandboxes.create(
            CreateSandboxContent(body), **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs}
        )
        return self.get_sandbox_client(sbx.id), sbx

    @distributed_trace
    def delete_sandbox(self, sandbox_id: str, **kwargs: Any) -> None:
        """Delete a sandbox (returns immediately; does not wait for tombstone)."""
        _validate_segment(sandbox_id, "sandbox_id")
        self._generated.sandboxes.delete(sandbox_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_delete_sandbox(
        self,
        sandbox_id: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin deleting a sandbox; poll until GET returns 404."""
        _validate_segment(sandbox_id, "sandbox_id")
        self.delete_sandbox(sandbox_id, **kwargs)
        polling_method = DeletionPoller(
            getter=lambda: self.get_sandbox(sandbox_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {sandbox_id}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)
