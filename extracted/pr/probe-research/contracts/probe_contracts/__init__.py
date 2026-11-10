"""probe-contracts: what the server, the SDK/CLI and the dashboard must agree on, defined once.

The front door is lazy: `import probe_contracts.scrubber` must not pay for
pydantic and every record class. `from probe_contracts import Run` loads them.
"""

from __future__ import annotations

import importlib
from typing import Any

_RECORDS = (
    "AnchorLevel",
    "Artifact",
    "ArtifactStatus",
    "EDIT_OP_ARGS",
    "EditActorKind",
    "EditCounts",
    "EditOp",
    "EditPhase",
    "EditState",
    "EditTarget",
    "Experiment",
    "HideArgs",
    "LineageEntityType",
    "LineageRelation",
    "MetricNonFinite",
    "MetricPoint",
    "MoveSeriesArgs",
    "ParentRelation",
    "Project",
    "ProjectKind",
    "Record",
    "RenameArgs",
    "RevertArgs",
    "Run",
    "RunCounts",
    "RunEdit",
    "RunStatus",
    "ScaleArgs",
    "SetConfigArgs",
    "ShiftStepArgs",
    "ShiftTimeArgs",
    "Span",
)

_CLIENT_MESSAGES = (
    "Action",
    "Audience",
    "ClientMessage",
    "ClientMessageList",
    "ClientRefusalBody",
    "MessageCode",
    "Severity",
)

__all__ = [*_RECORDS, *_CLIENT_MESSAGES, "CONTRACTS", "Contracts"]


def __getattr__(name: str) -> Any:
    if name in _RECORDS:
        return getattr(importlib.import_module(".records", __name__), name)
    if name in _CLIENT_MESSAGES:
        return getattr(importlib.import_module(".client_messages", __name__), name)
    if name in ("CONTRACTS", "Contracts"):
        return getattr(importlib.import_module(".probe_contracts", __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
