"""Per-scan completeness signals used for absence authority."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
import threading
from typing import Protocol


class CompletionStatusSink(Protocol):
    def mark_incomplete(self, reason: str) -> None: ...


@dataclass
class ScanCompletionStatus:
    """Findings may survive while any ordinary failure removes absence authority."""

    complete: bool = True
    reasons: list[str] = field(default_factory=list)
    _lock: threading.Lock = field(
        default_factory=threading.Lock,
        init=False,
        repr=False,
        compare=False,
    )

    def mark_incomplete(self, reason: str) -> None:
        with self._lock:
            self.complete = False
            if reason not in self.reasons:
                self.reasons.append(reason)

    def merge(self, other: "ScanCompletionStatus") -> None:
        if other is self:
            return

        with other._lock:
            other_complete = other.complete
            other_reasons = tuple(other.reasons)

        with self._lock:
            if not other_complete:
                self.complete = False
                for reason in other_reasons:
                    if reason not in self.reasons:
                        self.reasons.append(reason)

    def reason(self, fallback: str) -> str:
        return self.reasons[0] if self.reasons else fallback


class CompletionStatusResult:
    """Compatibility view for result dataclasses backed by canonical status."""

    completion: ScanCompletionStatus

    @property
    def complete(self) -> bool:
        return self.completion.complete

    @property
    def incomplete_reasons(self) -> list[str]:
        return self.completion.reasons

    def mark_incomplete(self, reason: str) -> None:
        self.completion.mark_incomplete(reason)


@dataclass
class ScanCompleteness:
    """Category/surface completion assembled from independent scan phases."""

    mcp_host_static: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    skill_host_static: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    plugin_host_static: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    plugin_device: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    agent_host_static: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    agent_definition_host_static: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    runtime: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    container_artifacts: ScanCompletionStatus = field(
        default_factory=ScanCompletionStatus
    )
    wsl_static: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)
    client_presence: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)

    def mark_incomplete(self, reason: str, *names: str) -> None:
        for name in names:
            status = getattr(self, name)
            status.mark_incomplete(reason)

    def merge(self, other: "ScanCompleteness") -> None:
        """Fold every surface of ``other`` into this one (incompleteness wins)."""
        for surface in fields(self):
            status: ScanCompletionStatus = getattr(self, surface.name)
            status.merge(getattr(other, surface.name))
