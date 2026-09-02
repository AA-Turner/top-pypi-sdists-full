"""Decision gate — pending decision persistence and resolution.

Provides ``DecisionRequired``, ``write_pending_decision()``,
``read_pending_decisions()``, and ``resolve_decision()`` for managing
human-in-the-loop gates in LangGraph workflows.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .run_id import validate_run_id


@dataclass(frozen=True)
class DecisionRequired:
    """A pending decision requiring human approval.

    Attributes:
        decision_id: Unique identifier for this decision (UUID hex).
        action_name: The tool/action that requires approval.
        arguments: Arguments that would be passed to the tool.
        policy_rule: The policy rule that triggered the gate.
        node_name: Name of the requesting node.
        run_id: The workflow run identifier.
        timestamp: Unix epoch when the decision was created.
        status: Current status (pending, approved, denied).
    """

    decision_id: str
    action_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    policy_rule: str = "requires_confirmation"
    node_name: str = ""
    run_id: str = ""
    timestamp: float = 0.0
    status: str = "pending"

    @staticmethod
    def create(
        *,
        action_name: str,
        arguments: dict[str, Any] | None = None,
        policy_rule: str = "requires_confirmation",
        node_name: str = "",
        run_id: str = "",
    ) -> DecisionRequired:
        """Factory method to create a new pending decision."""
        return DecisionRequired(
            decision_id=uuid.uuid4().hex,
            action_name=action_name,
            arguments=arguments or {},
            policy_rule=policy_rule,
            node_name=node_name,
            run_id=run_id,
            timestamp=time.time(),
            status="pending",
        )


def _get_decisions_path(state_dir: Path, run_id: str) -> Path:
    """Get the path to the pending-decisions.json file."""
    safe_run_id = validate_run_id(run_id)
    decisions_dir = state_dir / "orchestration" / safe_run_id
    decisions_dir.mkdir(parents=True, exist_ok=True)
    return decisions_dir / "pending-decisions.json"


def write_pending_decision(state_dir: Path, run_id: str, decision: DecisionRequired) -> None:
    """Persist a pending decision to disk.

    Uses file locking to prevent lost-update races when multiple
    processes/threads write decisions concurrently.

    Args:
        state_dir: Base state directory.
        run_id: Workflow run identifier.
        decision: The decision to persist.
    """
    from agentic_devtools.file_locking import locked_file

    path = _get_decisions_path(state_dir, run_id)

    # locked_file creates the file atomically if absent (empty content);
    # _parse_decisions_content() handles that gracefully as an empty list.
    with locked_file(path, "r+") as f:
        decisions = _parse_decisions_content(f.read())
        decisions.append(asdict(decision))
        f.seek(0)
        f.write(json.dumps(decisions, indent=2))
        f.truncate()


def read_pending_decisions(state_dir: Path, run_id: str) -> list[DecisionRequired]:
    """Read all pending decisions for a run.

    Args:
        state_dir: Base state directory.
        run_id: Workflow run identifier.

    Returns:
        List of ``DecisionRequired`` instances.  Non-dict entries (e.g. from
        manual edits or partial corruption) are silently skipped.
    """
    path = _get_decisions_path(state_dir, run_id)
    raw = _load_decisions_raw(path)
    decisions: list[DecisionRequired] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        try:
            decisions.append(DecisionRequired(**entry))
        except TypeError:
            continue
    return decisions


def resolve_decision(
    state_dir: Path,
    run_id: str,
    decision_id: str,
    *,
    approved: bool,
) -> DecisionRequired:
    """Resolve a pending decision by ID.

    Uses file locking so that concurrent ``write_pending_decision()`` calls
    cannot race with resolution and corrupt the file.

    Args:
        state_dir: Base state directory.
        run_id: Workflow run identifier.
        decision_id: The UUID hex of the decision to resolve.
        approved: Whether the decision is approved (True) or denied (False).

    Returns:
        The updated ``DecisionRequired`` with new status.

    Raises:
        ValueError: If the decision_id is not found.
    """
    from agentic_devtools.file_locking import locked_file

    path = _get_decisions_path(state_dir, run_id)

    # locked_file creates the file atomically if absent (empty content);
    # _parse_decisions_content() handles that gracefully as an empty list.
    with locked_file(path, "r+") as f:
        decisions = _parse_decisions_content(f.read())

        found_idx = None
        for idx, entry in enumerate(decisions):
            if isinstance(entry, dict) and entry.get("decision_id") == decision_id:
                found_idx = idx
                break

        if found_idx is None:
            raise ValueError(f"Decision not found: {decision_id}")

        new_status = "approved" if approved else "denied"
        decisions[found_idx]["status"] = new_status

        f.seek(0)
        f.write(json.dumps(decisions, indent=2))
        f.truncate()

    try:
        return DecisionRequired(**decisions[found_idx])
    except TypeError as exc:
        raise ValueError(f"Corrupt decision entry for {decision_id}: {exc}") from exc


def _parse_decisions_content(content: str) -> list[dict[str, Any]]:
    """Parse JSON content into a list of decision dicts.

    Returns an empty list on blank content, malformed JSON, or non-list values.
    Handles the ``"{}"`` sentinel that ``locked_file`` writes when creating a
    new file (treats it as an empty list).
    """
    if not content.strip():
        return []
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return []
    return data if isinstance(data, list) else []


def _load_decisions_raw(path: Path) -> list[dict[str, Any]]:
    """Load raw decision entries from file (with shared read lock)."""
    if not path.exists():
        return []
    try:
        from agentic_devtools.file_locking import locked_file

        with locked_file(path, mode="r", exclusive=False) as f:
            content = f.read()
        return _parse_decisions_content(content)
    except OSError:
        return []
