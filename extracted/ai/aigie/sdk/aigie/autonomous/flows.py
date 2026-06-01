"""Flow dataclass + FlowCache (snapshot-on-read).

Mirrors the platform's ``RemediationFlow`` (backend/src/monitor/models.py:731)
1:1 — a Flow is the JSON row returned by ``GET /v1/sdk/config`` under
``flows: [...]``. The SDK keeps these objects verbatim; FlowEvaluator (Task 4)
ports the platform's ``matches_conditions`` DSL on top of them.

Selector convention
-------------------
The Flow row itself has no selector column. The SDK reads narrowing dimensions
from ``metadata.selector`` as a stable convention::

    metadata = {
      "selector": {
        "customer_id": "...",   # optional
        "workflow_id": "...",   # optional
        "use_case":    "...",   # optional
      },
      ...
    }

A missing ``selector`` (or missing key inside it) means "matches any traffic
on that dimension". The platform-side authoring path is responsible for
writing this block; FlowEvaluator filters on it before running condition DSL.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class FlowSelector:
    """Narrowing dimensions read from ``metadata.selector``.

    All fields are optional. ``None`` means "wildcard on this dimension".
    """

    customer_id: str | None = None
    workflow_id: str | None = None
    use_case: str | None = None


@dataclass(frozen=True, slots=True)
class Flow:
    """SDK-side mirror of ``RemediationFlow`` JSON, kept verbatim.

    Field names and types match the platform's Pydantic model. Datetimes are
    left as ISO strings (the SDK never compares them); UUIDs are strings.
    """

    id: str
    name: str
    description: str = ""
    cluster_id: str | None = None
    steps: tuple[dict[str, Any], ...] = ()
    conditions: dict[str, Any] = field(default_factory=dict)
    success_rate: float = 0.0
    application_count: int = 0
    last_applied_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def selector(self) -> FlowSelector:
        sel = self.metadata.get("selector") if isinstance(self.metadata, dict) else None
        if not isinstance(sel, dict):
            return FlowSelector()
        return FlowSelector(
            customer_id=_opt_str(sel.get("customer_id")),
            workflow_id=_opt_str(sel.get("workflow_id")),
            use_case=_opt_str(sel.get("use_case")),
        )

    @property
    def total_steps(self) -> int:
        return len(self.steps)


def _opt_str(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v)
    return s or None


def _require_dict(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"flow {field_name!r} must be a dict")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"flow {field_name!r} must be a list")
    return value


def parse_flow(d: dict[str, Any]) -> Flow:
    """Parse one RemediationFlow JSON row into a Flow dataclass.

    Unknown keys are ignored. Missing required keys (``id``, ``name``) raise
    ``ValueError`` so a malformed envelope surfaces loudly rather than
    silently dropping rules.
    """
    if not isinstance(d, dict):
        raise ValueError(f"flow row must be a dict, got {type(d).__name__}")
    if d.get("id") is None:
        raise ValueError("flow row missing required field 'id'")
    if d.get("name") is None:
        raise ValueError("flow row missing required field 'name'")
    steps_raw = _require_list(d.get("steps", []), "steps")
    conds = _require_dict(d.get("conditions", {}), "conditions")
    meta = _require_dict(d.get("metadata", {}), "metadata")
    return Flow(
        id=str(d["id"]),
        name=str(d["name"]),
        description=str(d.get("description", "") or ""),
        cluster_id=_opt_str(d.get("cluster_id")),
        steps=tuple(s for s in steps_raw if isinstance(s, dict)),
        conditions=dict(conds),
        success_rate=float(d.get("success_rate", 0.0) or 0.0),
        application_count=int(d.get("application_count", 0) or 0),
        last_applied_at=_opt_str(d.get("last_applied_at")),
        created_at=_opt_str(d.get("created_at")),
        updated_at=_opt_str(d.get("updated_at")),
        metadata=dict(meta),
    )


def parse_flows(rows: Iterable[Any]) -> list[Flow]:
    """Parse a list of RemediationFlow JSON rows. Bad rows are skipped."""
    out: list[Flow] = []
    for row in rows:
        try:
            out.append(parse_flow(row))
        except ValueError:
            # Skip individual malformed rows rather than failing the whole envelope.
            continue
    return out


class FlowCache:
    """Thread-safe flow store using snapshot-on-read (no explicit lock).

    CPython's GIL makes single attribute rebind atomic, so readers that
    snapshot ``self._flows`` before a ``swap`` see a fully consistent old
    tuple; readers that snapshot after see the new tuple. No torn reads.
    No delta API — flows are fully reloaded from the config envelope each
    refresh.
    """

    def __init__(self) -> None:
        self._flows: tuple[Flow, ...] = ()
        self._version: str = ""

    def swap(self, new_version: str, flows: Iterable[Flow]) -> None:
        """Atomically replace the entire flow set."""
        self._flows = tuple(flows)
        self._version = new_version

    @property
    def version(self) -> str:
        return self._version

    def snapshot(self) -> tuple[Flow, ...]:
        """Return the current immutable snapshot for one evaluation pass."""
        return self._flows

    def __len__(self) -> int:
        return len(self._flows)

    def __iter__(self):  # type: ignore[override]
        return iter(self._flows)
