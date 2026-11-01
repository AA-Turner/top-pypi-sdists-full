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
    "Experiment",
    "LineageEntityType",
    "LineageRelation",
    "MetricNonFinite",
    "MetricPoint",
    "ParentRelation",
    "Project",
    "ProjectKind",
    "Record",
    "Run",
    "RunCounts",
    "RunStatus",
    "Span",
)

__all__ = [*_RECORDS, "CONTRACTS", "Contracts"]


def __getattr__(name: str) -> Any:
    if name in _RECORDS:
        return getattr(importlib.import_module(".records", __name__), name)
    if name in ("CONTRACTS", "Contracts"):
        return getattr(importlib.import_module(".probe_contracts", __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
