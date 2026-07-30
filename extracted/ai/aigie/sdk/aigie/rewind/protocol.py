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
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True)
class ToolCallOverride:
    """Redirect the failed call to ``name``.

    ``source_call_id`` / ``source_tool`` identify *which* call failed: an
    assistant turn can carry several parallel calls, and redirecting the wrong
    one breaks a healthy call while leaving the broken one in place. A
    capability that cannot identify the failed call must decline rather than
    guess positionally.
    """

    name: str
    args: Mapping[str, Any] | None = None
    arg_mapping: Mapping[str, str] | None = None
    required_args: tuple[str, ...] = ()
    source_call_id: str | None = None
    source_tool: str | None = None

    def resolve_args(self, source_args: Mapping[str, Any] | None) -> dict[str, Any]:
        if self.args is not None:
            return dict(self.args)
        source = dict(source_args or {})
        if not self.arg_mapping:
            return source
        return {self.arg_mapping.get(key, key): value for key, value in source.items()}

    def missing_required(self, source_args: Mapping[str, Any] | None) -> tuple[str, ...]:
        resolved = self.resolve_args(source_args)
        return tuple(name for name in self.required_args if name not in resolved)


@dataclass(frozen=True)
class Corrective:
    """Optional steering a capability may apply during rewind."""

    prompt: str | None = None
    state_patch: Mapping[str, Any] | None = None
    tool_call: ToolCallOverride | None = None

    @property
    def is_empty(self) -> bool:
        return self.prompt is None and self.state_patch is None and self.tool_call is None


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
    def skipped(cls, reason: str, handle: RewindHandle | None = None) -> RewindOutcome:
        return cls(status=RewindStatus.SKIPPED, reason=reason, handle=handle)

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
