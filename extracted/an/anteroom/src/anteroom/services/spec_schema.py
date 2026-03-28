"""Spec artifact schema — dataclasses, parsing, validation, and phase metadata helpers.

A spec artifact stores authored planning content (requirements, design, tasks)
as structured YAML.  Phase approval state lives in the artifact ``metadata``
JSON field, not in the authored content.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Phase status
# ---------------------------------------------------------------------------


class SpecPhaseStatus(str, enum.Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    STALE = "stale"


class SpecMode(str, enum.Enum):
    FEATURE = "feature"
    BUGFIX = "bugfix"


VALID_PHASE_NAMES = frozenset({"requirements", "design", "tasks"})

PENDING_SENTINEL = "[pending — to be derived from design]"

# ---------------------------------------------------------------------------
# Creation flow constants (#1165)
# ---------------------------------------------------------------------------

CREATION_FLOW_PROMPT = "prompt"
CREATION_FLOW_FROM_ISSUE = "from_issue"
CREATION_FLOW_MANUAL = "manual"

# ---------------------------------------------------------------------------
# JSON schema for LLM-assisted spec generation (#1165)
# ---------------------------------------------------------------------------

SPEC_GENERATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["requirements", "design", "tasks"],
    "properties": {
        "requirements": {"type": "string", "description": "Requirements description"},
        "design": {"type": "string", "description": "Design description"},
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "summary"],
                "properties": {
                    "id": {"type": "string"},
                    "summary": {"type": "string"},
                    "depends_on": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
}


def is_pending_content(phase: str, content: SpecContent) -> bool:
    """Check whether the given phase still contains placeholder sentinel content."""
    if phase == "requirements":
        return content.requirements.strip() == PENDING_SENTINEL
    if phase == "design":
        return content.design.strip() == PENDING_SENTINEL
    if phase == "tasks":
        return len(content.tasks) == 1 and content.tasks[0].summary.startswith("[pending")
    return False


# ---------------------------------------------------------------------------
# Authored content dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpecTask:
    """A single task inside a spec."""

    id: str
    summary: str
    depends_on: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SpecContent:
    """Parsed authored content of a spec artifact."""

    requirements: str
    design: str
    tasks: list[SpecTask]
    mode: SpecMode = SpecMode.FEATURE


# ---------------------------------------------------------------------------
# Diff dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PhaseChange:
    """Per-phase diff result."""

    phase: str
    content_changed: bool
    content_diff: str | None = None


@dataclass(frozen=True)
class TaskChange:
    """Task-level change between versions."""

    task_id: str
    change_type: str  # "added", "removed", "modified"
    summary_before: str | None = None
    summary_after: str | None = None


@dataclass(frozen=True)
class SpecDiff:
    """Full diff result between two spec versions."""

    version_from: int
    version_to: int
    phase_changes: list[PhaseChange]
    task_changes: list[TaskChange]
    invalidations: list[tuple[str, str]]  # (phase, reason)


# ---------------------------------------------------------------------------
# Dashboard / portfolio dataclasses (#1016)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunSummary:
    total: int = 0
    completed: int = 0
    failed: int = 0
    running: int = 0
    blocked: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "running": self.running,
            "blocked": self.blocked,
        }


@dataclass(frozen=True)
class SpecSummary:
    fqn: str
    mode: str
    source: str
    phases: dict[str, str]
    overall_status: str
    stale_reasons: dict[str, str]
    run_summary: RunSummary
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "fqn": self.fqn,
            "mode": self.mode,
            "source": self.source,
            "phases": self.phases,
            "overall_status": self.overall_status,
            "stale_reasons": self.stale_reasons,
            "run_summary": self.run_summary.to_dict(),
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True)
class DashboardTotals:
    total_specs: int = 0
    all_approved: int = 0
    in_progress: int = 0
    stale: int = 0
    blocked: int = 0
    draft: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "total_specs": self.total_specs,
            "all_approved": self.all_approved,
            "in_progress": self.in_progress,
            "stale": self.stale,
            "blocked": self.blocked,
            "draft": self.draft,
        }


@dataclass(frozen=True)
class SpecDashboard:
    specs: list[SpecSummary]
    totals: DashboardTotals
    filters_applied: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "specs": [s.to_dict() for s in self.specs],
            "totals": self.totals.to_dict(),
            "filters_applied": self.filters_applied,
        }


# ---------------------------------------------------------------------------
# Parse / serialize
# ---------------------------------------------------------------------------


class SpecValidationError(ValueError):
    """Raised when spec YAML content fails validation."""


def parse_spec_content(yaml_str: str) -> SpecContent:
    """Parse and validate spec YAML content.

    Raises ``SpecValidationError`` on invalid input.
    """
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as exc:
        raise SpecValidationError(f"Invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise SpecValidationError("Spec content must be a YAML mapping")

    requirements = data.get("requirements")
    if not isinstance(requirements, str) or not requirements.strip():
        raise SpecValidationError("'requirements' must be a non-empty string")

    design = data.get("design")
    if not isinstance(design, str) or not design.strip():
        raise SpecValidationError("'design' must be a non-empty string")

    raw_tasks = data.get("tasks")
    if not isinstance(raw_tasks, list):
        raise SpecValidationError("'tasks' must be a list")

    tasks = _parse_tasks(raw_tasks)
    _validate_task_graph(tasks)

    raw_mode = data.get("mode", SpecMode.FEATURE.value)
    try:
        mode = SpecMode(raw_mode)
    except ValueError:
        raise SpecValidationError(f"Invalid mode: {raw_mode!r} — must be one of {[m.value for m in SpecMode]}")

    return SpecContent(requirements=requirements, design=design, tasks=tasks, mode=mode)


def serialize_spec_content(spec: SpecContent) -> str:
    """Serialize a ``SpecContent`` back to YAML."""
    data: dict[str, Any] = {}
    if spec.mode != SpecMode.FEATURE:
        data["mode"] = spec.mode.value
    data["requirements"] = spec.requirements
    data["design"] = spec.design
    data["tasks"] = [_task_to_dict(t) for t in spec.tasks]
    return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)


# ---------------------------------------------------------------------------
# Phase metadata helpers
# ---------------------------------------------------------------------------


def default_phase_metadata() -> dict[str, Any]:
    """Return default metadata for a new spec artifact."""
    phase = {"status": SpecPhaseStatus.DRAFT.value, "approved_at": None, "approved_by": None}
    return {"phases": {name: dict(phase) for name in VALID_PHASE_NAMES}}


def get_phase_status(metadata: dict[str, Any], phase: str) -> SpecPhaseStatus:
    """Read the status of a phase from artifact metadata.

    Raises ``ValueError`` if *phase* is not a valid phase name.
    """
    _validate_phase_name(phase)
    phases = metadata.get("phases", {})
    phase_data = phases.get(phase, {})
    raw = phase_data.get("status", SpecPhaseStatus.DRAFT.value)
    return SpecPhaseStatus(raw)


def set_phase_status(
    metadata: dict[str, Any],
    phase: str,
    status: SpecPhaseStatus | str,
    *,
    approved_by: str | None = None,
    approved_at_version: int | None = None,
) -> dict[str, Any]:
    """Return a *new* metadata dict with the phase status updated.

    Raises ``ValueError`` for invalid phase names or status values.
    """
    _validate_phase_name(phase)
    status_val = SpecPhaseStatus(status).value

    # Deep-copy the relevant portion to avoid mutating the caller's dict
    new_meta = dict(metadata)
    phases = dict(new_meta.get("phases", {}))
    phase_data = dict(phases.get(phase, {}))

    phase_data["status"] = status_val
    if status_val == SpecPhaseStatus.APPROVED.value:
        phase_data["approved_at"] = datetime.now(timezone.utc).isoformat()
        phase_data["approved_by"] = approved_by
        if approved_at_version is not None:
            phase_data["approved_at_version"] = approved_at_version
    elif status_val == SpecPhaseStatus.DRAFT.value:
        phase_data["approved_at"] = None
        phase_data["approved_by"] = None
        phase_data.pop("approved_at_version", None)
    # STALE preserves the original approved_at / approved_by / approved_at_version

    phases[phase] = phase_data
    new_meta["phases"] = phases
    return new_meta


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

FEATURE_TEMPLATE = (
    "requirements: |\n  Describe requirements here.\n\n"
    "design: |\n  Describe the design here.\n\n"
    "tasks:\n  - id: t1\n    summary: First task\n"
)

DESIGN_FIRST_TEMPLATE = (
    'requirements: "' + PENDING_SENTINEL + '"\n\n'
    "design: |\n"
    "  ## Architecture\n"
    "  Describe the system architecture.\n\n"
    "  ## Constraints\n"
    "  List technical constraints.\n\n"
    "  ## Approach\n"
    "  Describe the implementation approach.\n\n"
    "tasks:\n  - id: t1\n    summary: First task derived from design\n"
)

BUGFIX_TEMPLATE = (
    "mode: bugfix\n"
    "requirements: |\n"
    "  ## Current Behavior\n"
    "  Describe what currently happens.\n\n"
    "  ## Expected Behavior\n"
    "  Describe what should happen instead.\n\n"
    "  ## Steps to Reproduce\n"
    "  1. Step one\n"
    "  2. Step two\n\n"
    "design: |\n"
    "  ## Root Cause\n"
    "  Describe the root cause.\n\n"
    "  ## Fix Approach\n"
    "  Describe the fix approach.\n\n"
    "  ## Non-Regression Boundaries\n"
    "  List what must NOT change.\n\n"
    "tasks:\n  - id: t1\n    summary: First fix task\n"
)


# ---------------------------------------------------------------------------
# Topological sort (#1165)
# ---------------------------------------------------------------------------


def topological_sort_tasks(tasks: list[SpecTask]) -> list[list[SpecTask]]:
    """Group tasks by dependency level using Kahn's algorithm.

    Returns tasks grouped so that level 0 has no dependencies, level 1 depends
    only on level 0, etc.  Tasks within each level are independent and can run
    concurrently.  Assumes the DAG is valid (pre-validated by
    ``_validate_task_graph``).
    """
    if not tasks:
        return []

    task_map: dict[str, SpecTask] = {t.id: t for t in tasks}
    in_degree: dict[str, int] = {t.id: 0 for t in tasks}
    dependents: dict[str, list[str]] = {t.id: [] for t in tasks}

    for t in tasks:
        for dep in t.depends_on:
            in_degree[t.id] += 1
            if dep in dependents:
                dependents[dep].append(t.id)

    current_level = [tid for tid, deg in in_degree.items() if deg == 0]
    levels: list[list[SpecTask]] = []

    while current_level:
        levels.append([task_map[tid] for tid in current_level])
        next_level: list[str] = []
        for tid in current_level:
            for dep_id in dependents[tid]:
                in_degree[dep_id] -= 1
                if in_degree[dep_id] == 0:
                    next_level.append(dep_id)
        current_level = next_level

    return levels


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _validate_phase_name(phase: str) -> None:
    if phase not in VALID_PHASE_NAMES:
        raise ValueError(f"Invalid phase name: {phase!r} — must be one of {sorted(VALID_PHASE_NAMES)}")


def _parse_tasks(raw_tasks: list[Any]) -> list[SpecTask]:
    tasks: list[SpecTask] = []
    for i, item in enumerate(raw_tasks):
        if not isinstance(item, dict):
            raise SpecValidationError(f"Task at index {i} must be a mapping")

        task_id = item.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            raise SpecValidationError(f"Task at index {i} must have a non-empty string 'id'")

        summary = item.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            raise SpecValidationError(f"Task '{task_id}' must have a non-empty string 'summary'")

        depends_on = item.get("depends_on", [])
        if not isinstance(depends_on, list) or not all(isinstance(d, str) for d in depends_on):
            raise SpecValidationError(f"Task '{task_id}' depends_on must be a list of strings")

        tasks.append(SpecTask(id=task_id, summary=summary, depends_on=list(depends_on)))

    return tasks


def _validate_task_graph(tasks: list[SpecTask]) -> None:
    ids = {t.id for t in tasks}

    # Check for duplicate IDs
    if len(ids) != len(tasks):
        seen: set[str] = set()
        for t in tasks:
            if t.id in seen:
                raise SpecValidationError(f"Duplicate task ID: {t.id!r}")
            seen.add(t.id)

    # Check depends_on references
    for t in tasks:
        for dep in t.depends_on:
            if dep not in ids:
                raise SpecValidationError(f"Task '{t.id}' depends on unknown task '{dep}'")

    # Check for circular dependencies
    _check_cycles(tasks)


def _check_cycles(tasks: list[SpecTask]) -> None:
    adj: dict[str, list[str]] = {t.id: list(t.depends_on) for t in tasks}
    visited: set[str] = set()
    in_stack: set[str] = set()

    def dfs(node: str) -> None:
        if node in in_stack:
            raise SpecValidationError(f"Circular dependency detected involving task '{node}'")
        if node in visited:
            return
        in_stack.add(node)
        for dep in adj.get(node, []):
            dfs(dep)
        in_stack.discard(node)
        visited.add(node)

    for t in tasks:
        dfs(t.id)


def _task_to_dict(task: SpecTask) -> dict[str, Any]:
    d: dict[str, Any] = {"id": task.id, "summary": task.summary}
    if task.depends_on:
        d["depends_on"] = task.depends_on
    return d
