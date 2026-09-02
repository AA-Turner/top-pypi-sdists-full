"""Resource usage and stats models."""

from __future__ import annotations

from dataclasses import dataclass

from azure.containerapps.sandbox._model_types._egress import EgressDecisionEntry


@dataclass(frozen=True)
class ResourceUsage:
    """Memory or storage usage."""
    used_bytes: int | None = None
    total_bytes: int | None = None
    available_bytes: int | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> ResourceUsage | None:
        if not d:
            return None
        return cls(
            used_bytes=d.get("usedBytes"),
            total_bytes=d.get("totalBytes"),
            available_bytes=d.get("availableBytes"),
        )


@dataclass(frozen=True)
class CpuUsage:
    """CPU usage stats."""
    usage_nano_cores: int | None = None
    usage_core_nano_seconds: int | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> CpuUsage | None:
        if not d:
            return None
        return cls(
            usage_nano_cores=d.get("usageNanoCores"),
            usage_core_nano_seconds=d.get("usageCoreNanoSeconds"),
        )


@dataclass(frozen=True)
class NetworkUsage:
    """Network usage stats."""
    rx_bytes: int | None = None
    tx_bytes: int | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> NetworkUsage | None:
        if not d:
            return None
        return cls(rx_bytes=d.get("rxBytes"), tx_bytes=d.get("txBytes"))


@dataclass(frozen=True)
class NetworkEgressDecisions:
    """Network egress decisions grouped by allowed/denied."""
    allowed: list[EgressDecisionEntry]
    denied: list[EgressDecisionEntry]

    @classmethod
    def _from_dict(cls, d: dict | None) -> NetworkEgressDecisions | None:
        if not d:
            return None
        return cls(
            allowed=[EgressDecisionEntry._from_dict(e) for e in d.get("allowed", [])],
            denied=[EgressDecisionEntry._from_dict(e) for e in d.get("denied", [])],
        )


@dataclass(frozen=True)
class SandboxStats:
    """Resource usage statistics for a sandbox."""
    cpu: CpuUsage | None = None
    memory: ResourceUsage | None = None
    storage: ResourceUsage | None = None
    network: NetworkUsage | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> SandboxStats:
        return cls(
            cpu=CpuUsage._from_dict(d.get("cpu")),
            memory=ResourceUsage._from_dict(d.get("memory")),
            storage=ResourceUsage._from_dict(d.get("storage")),
            network=NetworkUsage._from_dict(d.get("network")),
        )
