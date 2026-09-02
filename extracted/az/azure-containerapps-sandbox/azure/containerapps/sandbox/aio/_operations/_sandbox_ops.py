"""Async sandbox CRUD operations for group-scoped client."""
from __future__ import annotations

from typing import Any, Literal

from azure.core.async_paging import AsyncItemPaged
from azure.core.polling import AsyncLROPoller
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import (
    AddPortRequest,
    EgressPolicy,
    Sandbox,
    SandboxVolume,
)
from azure.containerapps.sandbox.aio._polling import (
    AsyncDeletionPoller,
    AsyncResourceStatePoller,
)


class AsyncSandboxOperationsMixin:
    """Async sandbox CRUD operations on a sandbox group."""

    @distributed_trace
    def list_sandboxes(self, *, labels: dict[str, str] | None = None,
                       **kwargs: Any) -> AsyncItemPaged[Sandbox]:
        """List sandboxes in this sandbox group.

        :keyword dict labels: Filter by labels (key=value pairs).
        """
        base_url = f"{self._endpoint}{self._group_path}/sandboxes"
        params: dict[str, str] = {"api-version": self._api_version}
        if labels:
            params["labels"] = ",".join(f"{k}={v}" for k, v in labels.items())

        async def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            return await self._send_request(request)

        async def _extract_data(response):
            data = response.json()
            if isinstance(data, list):
                return None, iter([Sandbox._from_dict(s) for s in data])
            items = [Sandbox._from_dict(s) for s in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return AsyncItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace_async
    async def get_sandbox(self, sandbox_id: str, **kwargs: Any) -> Sandbox:
        """Get a sandbox by ID."""
        _validate_segment(sandbox_id, "sandbox_id")
        return Sandbox._from_dict(await self._dp_get(f"{self._group_path}/sandboxes/{sandbox_id}"))

    @distributed_trace_async
    async def begin_create_sandbox(
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
    ) -> AsyncLROPoller:
        """Begin creating a sandbox. Returns an :class:`~azure.core.polling.AsyncLROPoller`.

        ``await poller.result()`` blocks until the sandbox is *Running* and
        returns a :class:`~azure.containerapps.sandbox.aio.SandboxClient`.

        Sources (pick exactly one):
          disk — public disk image name (default: "ubuntu")
          disk_id — private disk image ID
          snapshot_id — create from a snapshot
          preset — preset sandbox type (e.g., "copilot")

        :keyword str disk_size: Optional base disk size (a storage quantity such
            as "20Gi"). Maps to ``resources.disk``. Ignored for ``preset`` and
            ``snapshot_id`` sources.
        :keyword str auto_suspend_mode: Auto-suspend mode, ``"Memory"`` (default)
            or ``"Disk"``. DataDisk volumes require ``"Disk"`` mode.
        """
        sandbox_client, initial_sbx = await self._do_create_sandbox(
            disk=disk, disk_id=disk_id, snapshot_id=snapshot_id, preset=preset,
            cpu=cpu, memory=memory, disk_size=disk_size,
            auto_suspend_seconds=auto_suspend_seconds,
            auto_suspend_mode=auto_suspend_mode,
            labels=labels, environment=environment, connections=connections,
            egress_policy=egress_policy, volumes=volumes, ports=ports,
            entrypoint=entrypoint, cmd=cmd, skip_egress_proxy=skip_egress_proxy,
            customer_vnet_connection_name=customer_vnet_connection_name,
            vmm_type=vmm_type,
        )
        polling_method = AsyncResourceStatePoller(
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
        return AsyncLROPoller(self, initial_sbx, lambda _: sandbox_client, polling_method)

    async def _do_create_sandbox(
        self,
        *,
        disk, disk_id, snapshot_id, preset,
        cpu, memory, disk_size, auto_suspend_seconds,
        auto_suspend_mode,
        labels, environment, connections,
        egress_policy, volumes, ports,
        entrypoint, cmd, skip_egress_proxy,
        customer_vnet_connection_name, vmm_type,
    ):
        """Async: validate, build payload, PUT, return ``(SandboxClient, Sandbox)``."""
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
        if snapshot_id:
            forbidden = {
                "labels": labels, "environment": environment, "connections": connections,
                "egress_policy": egress_policy, "volumes": volumes, "ports": ports,
                "entrypoint": entrypoint, "cmd": cmd,
                "skip_egress_proxy": skip_egress_proxy,
                "customer_vnet_connection_name": customer_vnet_connection_name,
                "vmm_type": vmm_type,
            }
            bad = [k for k, v in forbidden.items() if v]
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
            if egress_policy:
                body["egressPolicy"] = egress_policy._to_dict()
            if volumes:
                body["volumes"] = [v._to_dict() for v in volumes]
            if ports:
                body["ports"] = [
                    {"port": p} if isinstance(p, int) else p._to_dict() for p in ports
                ]
            if entrypoint:
                body["entrypoint"] = entrypoint
            if cmd:
                body["cmd"] = cmd
            if skip_egress_proxy is not None:
                body["skipEgressProxy"] = skip_egress_proxy
            if customer_vnet_connection_name:
                body["customerVnetConnectionName"] = customer_vnet_connection_name
            if vmm_type:
                body["vmmType"] = vmm_type

        data = await self._dp_put(f"{self._group_path}/sandboxes", body)
        sbx = Sandbox._from_dict(data)
        return self.get_sandbox_client(sbx.id), sbx

    @distributed_trace_async
    async def delete_sandbox(self, sandbox_id: str, **kwargs: Any) -> None:
        """Delete a sandbox (returns immediately; does not wait for tombstone)."""
        _validate_segment(sandbox_id, "sandbox_id")
        await self._dp_delete(f"{self._group_path}/sandboxes/{sandbox_id}")

    @distributed_trace_async
    async def begin_delete_sandbox(
        self,
        sandbox_id: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> AsyncLROPoller:
        """Begin deleting a sandbox; poll until GET returns 404."""
        _validate_segment(sandbox_id, "sandbox_id")
        await self._dp_delete(f"{self._group_path}/sandboxes/{sandbox_id}")
        polling_method = AsyncDeletionPoller(
            getter=lambda: self.get_sandbox(sandbox_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Sandbox {sandbox_id}",
        )
        return AsyncLROPoller(self, None, lambda _: None, polling_method)
