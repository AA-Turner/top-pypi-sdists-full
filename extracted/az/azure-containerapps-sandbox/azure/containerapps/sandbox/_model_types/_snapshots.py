"""Snapshot models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SnapshotGpu:
    """GPU configuration in a snapshot."""
    sku: str = ""
    quantity: int = 0

    @classmethod
    def _from_dict(cls, d: dict | None) -> SnapshotGpu | None:
        if not d:
            return None
        return cls(sku=d.get("sku", ""), quantity=d.get("quantity", 0))


@dataclass(frozen=True)
class SnapshotResources:
    """Resource allocation captured in a snapshot."""
    cpu: str = ""
    memory: str = ""
    disk: str | None = None
    gpu: SnapshotGpu | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> SnapshotResources | None:
        if not d:
            return None
        return cls(
            cpu=d.get("cpu", ""),
            memory=d.get("memory", ""),
            disk=d.get("disk"),
            gpu=SnapshotGpu._from_dict(d.get("gpu")),
        )


@dataclass(frozen=True)
class Snapshot:
    """A sandbox snapshot."""
    id: str = ""
    labels: dict[str, str] = field(default_factory=dict)
    sandbox_id: str | None = None
    status: str | None = None
    vmm_type: str | None = None
    created_at_utc: str | None = None
    resources: SnapshotResources | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> Snapshot:
        return cls(
            id=d.get("id", ""),
            labels=d.get("labels", {}),
            sandbox_id=d.get("sandboxId"),
            status=d.get("status"),
            vmm_type=d.get("vmmType"),
            created_at_utc=d.get("createdAtUtc"),
            resources=SnapshotResources._from_dict(d.get("resources")),
        )
