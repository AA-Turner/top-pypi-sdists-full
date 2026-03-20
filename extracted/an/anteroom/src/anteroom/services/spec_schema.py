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
