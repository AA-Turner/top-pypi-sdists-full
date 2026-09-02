"""Sandbox core models (response-only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from azure.containerapps.sandbox._model_types._egress import EgressPolicy
from azure.containerapps.sandbox._model_types._lifecycle import LifecyclePolicy
from azure.containerapps.sandbox._model_types._ports import SandboxPort


#: Why the sandbox was stopped.  Mirrors the server-side ``StoppedReason`` enum
#: added in ADC PR #6836.
StoppedReason = Literal["Idle", "Disabled", "UserStopped"]


@dataclass(frozen=True)
class SandboxStateDetails:
    """Companion to :attr:`Sandbox.state`.

    Populated when a sandbox transitions to ``Stopped``; ``None`` on running
    sandboxes and on legacy stopped documents written before this field existed.

    * ``stopped_reason`` – why the sandbox stopped (``Idle``, ``Disabled``, or
      ``UserStopped``).
    * ``stopped_at`` – UTC wall-clock time of the transition (ISO-8601 string).

    When ``stopped_reason`` is ``Disabled``, on-demand auto-resume is blocked
    and explicit resume calls are rejected by the server.
    """
    stopped_reason: StoppedReason | None = None
    stopped_at: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> SandboxStateDetails | None:
        if not d:
            return None
        return cls(
            stopped_reason=d.get("stoppedReason"),
            stopped_at=d.get("stoppedAt"),
        )

    def is_auto_resume_allowed(self) -> bool:
        """Return *True* unless the sandbox was administratively disabled."""
        return self.stopped_reason != "Disabled"


@dataclass(frozen=True)
class SandboxResources:
    """CPU, memory, and disk allocation for a sandbox."""
    cpu: str = ""
    memory: str = ""
    disk: str = ""

    @classmethod
    def _from_dict(cls, d: dict | None) -> SandboxResources | None:
        if not d:
            return None
        return cls(cpu=d.get("cpu", ""), memory=d.get("memory", ""), disk=d.get("disk", ""))


@dataclass(frozen=True)
class DiskImageRef:
    """Reference to a disk image used to create a sandbox."""
    name: str | None = None
    id: str | None = None
    is_public: bool | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> DiskImageRef | None:
        if not d:
            return None
        return cls(name=d.get("name"), id=d.get("id"), is_public=d.get("isPublic"))


@dataclass(frozen=True)
class SnapshotRef:
    """Reference to a snapshot used to create a sandbox."""
    id: str = ""

    @classmethod
    def _from_dict(cls, d: dict | None) -> SnapshotRef | None:
        if not d:
            return None
        return cls(id=d.get("id", ""))


@dataclass(frozen=True)
class SandboxSourcesRef:
    """Source reference for sandbox creation (disk image or snapshot)."""
    disk_image: DiskImageRef | None = None
    snapshot: SnapshotRef | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> SandboxSourcesRef | None:
        if not d:
            return None
        return cls(
            disk_image=DiskImageRef._from_dict(d.get("diskImage")),
            snapshot=SnapshotRef._from_dict(d.get("snapshot")),
        )


@dataclass(frozen=True)
class Sandbox:
    """A sandbox instance returned by get/create operations."""
    id: str = ""
    state: Literal["Running", "Stopped", "Suspended",
                    "Resuming", "Stopping", "Creating", "Deleting"] | None = None
    state_details: SandboxStateDetails | None = None
    labels: dict[str, str] = field(default_factory=dict)
    vmm_type: str | None = None
    ports: list[SandboxPort] = field(default_factory=list)
    resources: SandboxResources | None = None
    egress_policy: EgressPolicy | None = None
    environment: dict[str, str] = field(default_factory=dict)
    connections: list[str] = field(default_factory=list)
    customer_vnet_connection_name: str | None = None
    sandbox_group_id: str | None = None
    lifecycle: LifecyclePolicy | None = None
    sources_ref: SandboxSourcesRef | None = None
    preset_sandbox_type: str | None = None
    hostname: str | None = None
    created_at: str | None = None
    region: str | None = None
    entrypoint: list[str] | None = None
    management_url: str | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> Sandbox:
        return cls(
            id=d.get("id", ""),
            state=d.get("state"),
            state_details=SandboxStateDetails._from_dict(d.get("stateDetails")),
            labels=d.get("labels", {}),
            vmm_type=d.get("vmmType"),
            ports=[SandboxPort._from_dict(p) for p in d.get("ports", [])],
            resources=SandboxResources._from_dict(d.get("resources")),
            egress_policy=EgressPolicy._from_dict(d.get("egressPolicy")),
            environment=d.get("environment", {}),
            connections=d.get("connections", []),
            customer_vnet_connection_name=d.get("customerVnetConnectionName"),
            sandbox_group_id=d.get("sandboxGroupId"),
            lifecycle=LifecyclePolicy._from_dict(d.get("lifecycle")),
            sources_ref=SandboxSourcesRef._from_dict(d.get("sourcesRef")),
            preset_sandbox_type=d.get("presetSandboxType"),
            hostname=d.get("hostname"),
            created_at=d.get("createdAt"),
            region=d.get("region"),
            entrypoint=d.get("entrypoint"),
            management_url=d.get("managementUrl"),
        )
