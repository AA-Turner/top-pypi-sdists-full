"""Framework-agnostic rewind value types and capability protocol."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class RewindStatus(str, Enum):
    OK = "ok"
    UNSUPPORTED = "unsupported"
    NOT_FOUND = "not_found"
    FAILED = "failed"


@dataclass(frozen=True)
class Corrective:
    """Optional steering a capability may apply during rewind."""

    prompt: str | None = None
    state_patch: Mapping[str, Any] | None = None

    @property
    def is_empty(self) -> bool:
        return self.prompt is None and self.state_patch is None


@dataclass(frozen=True)
class RewindHandle:
    framework: str
    trace_id: str
    span_id: str
    # Framework-owned pointer with schema defined by the matching capability.
    payload: Any


@dataclass(frozen=True)
class RewindOutcome:
    status: RewindStatus
    handle: RewindHandle | None = None
    reason: str | None = None
    # Framework-specific result payload (e.g. Claude forked session id).
    result: Mapping[str, Any] | None = None

    @classmethod
    def ok(cls, handle: RewindHandle, result: Mapping[str, Any] | None = None) -> RewindOutcome:
        return cls(status=RewindStatus.OK, handle=handle, result=result)

    @classmethod
    def not_found(cls, span_id: str) -> RewindOutcome:
        return cls(status=RewindStatus.NOT_FOUND, reason=f"no handle for span {span_id}")

    @classmethod
    def unsupported(cls, span_id: str | None = None, *, reason: str | None = None) -> RewindOutcome:
        return cls(
            status=RewindStatus.UNSUPPORTED,
            reason=reason or f"no capability supports span {span_id}",
        )

    @classmethod
    def failed(cls, reason: str, handle: RewindHandle | None = None) -> RewindOutcome:
        return cls(status=RewindStatus.FAILED, reason=reason, handle=handle)


class RewindCapability(Protocol):
    """A per-framework rewind implementation registered with the coordinator."""

    framework: str

    def supports(self, handle: RewindHandle) -> bool:
        """True if this run is actually rewindable (e.g. has a checkpointer)."""
        ...

    # Framework-specific capture input with shape defined by each integration.
    async def capture(self, span_id: str, trace_id: str, context: Any) -> RewindHandle | None: ...

    async def rewind(
        self, handle: RewindHandle, corrective: Corrective | None
    ) -> RewindOutcome: ...
