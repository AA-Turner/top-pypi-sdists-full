"""Copilot session activity detector.

Provides two detection strategies:
- ``is_copilot_session_active_via_agent_task``: Uses ``gh agent-task list`` for
  authoritative session state (preferred, fail-closed).
- ``is_copilot_session_active``: Legacy events-based heuristic (deprecated,
  fail-closed).
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import warnings
from datetime import UTC, datetime

from agentic_devtools.cli.ci.models import (
    COPILOT_SESSION_EVENT_FINISHED,
    COPILOT_SESSION_EVENT_FINISHED_FAILURE,
    COPILOT_SESSION_EVENT_STARTED,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.subprocess_utils import run_safe

logger = logging.getLogger(__name__)

_ACTIVE_TASK_STATUSES = frozenset(
    {"idle", "in_progress", "queued", "requested", "running", "waiting", "waiting_for_user"}
)
_INACTIVE_TASK_STATUSES = frozenset({"canceled", "cancelled", "completed", "failed", "stopped", "timed_out"})
_DEFAULT_AGENT_TASK_TIMEOUT_SECONDS = 10
_AGENT_TASK_LIST_LIMIT = 1000

_DEFAULT_MAX_SESSION_AGE_SECONDS = 3600  # 1 hour


def _get_max_session_age_seconds() -> int:
    """Return the max session age from environment or the default (3600s)."""
    raw = os.environ.get("AGDT_MAX_SESSION_AGE_SECONDS", "").strip()
    if raw:
        try:
            value = int(raw)
        except ValueError:
            logger.warning(
                "AGDT_MAX_SESSION_AGE_SECONDS=%r is not a valid integer; using default %d",
                raw,
                _DEFAULT_MAX_SESSION_AGE_SECONDS,
            )
            return _DEFAULT_MAX_SESSION_AGE_SECONDS
        if value <= 0:
            logger.warning(
                "AGDT_MAX_SESSION_AGE_SECONDS=%d is not positive; using default %d",
                value,
                _DEFAULT_MAX_SESSION_AGE_SECONDS,
            )
            return _DEFAULT_MAX_SESSION_AGE_SECONDS
        return value
    return _DEFAULT_MAX_SESSION_AGE_SECONDS


def _is_session_stale(created_at: str, max_age_seconds: int) -> bool:
    """Return True if the session start event is older than max_age_seconds."""
    try:
        started_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        # If we cannot parse the timestamp, we cannot determine staleness —
        # fall back to treating as potentially active (conservative).
        return False
    # Normalize naive datetimes (no tzinfo) to UTC to avoid TypeError on subtraction.
    if started_time.tzinfo is None:
        started_time = started_time.replace(tzinfo=UTC)
    age = (datetime.now(tz=UTC) - started_time).total_seconds()
    return age > max_age_seconds


def is_copilot_session_active_via_agent_task(
    repo: str,
    pr_number: int,
    *,
    timeout_seconds: int = _DEFAULT_AGENT_TASK_TIMEOUT_SECONDS,
) -> bool | None:
    """Check if a Copilot coding session is active using ``gh agent-task list``.

    This is the preferred session detector. It queries the GitHub CLI for
    authoritative agent task state. If the command's result is unavailable or
    invalid, it returns ``None`` so mutations which require an inactive
    session can fail closed.

    Args:
        repo: Full repository name (e.g. ``owner/repo``).
        pr_number: Pull request number to check.
        timeout_seconds: Maximum time to wait for the ``gh`` subprocess.

    Returns:
        True if at least one agent task for the given repository and PR is in an
        active status (idle, queued, requested, waiting, waiting_for_user,
        in_progress, running).
        False when a valid task inventory contains no active task; ``None``
        when the inventory is unavailable or invalid.
    """
    cmd = [
        "gh",
        "agent-task",
        "list",
        "--limit",
        str(_AGENT_TASK_LIST_LIMIT),
        "--json",
        "id,state,repository,pullRequestNumber,createdAt",
    ]
    try:
        result = run_safe(
            cmd,
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        logger.warning(
            "PR #%d: gh agent-task list timed out after %ds — session state unavailable",
            pr_number,
            timeout_seconds,
        )
        return None
    except (OSError, FileNotFoundError, PermissionError) as exc:
        logger.warning(
            "PR #%d: gh agent-task list failed — session state unavailable: %s",
            pr_number,
            exc,
        )
        return None

    if result.returncode != 0:
        logger.warning(
            "PR #%d: gh agent-task list exited with code %d — session state unavailable",
            pr_number,
            result.returncode,
        )
        return None

    try:
        tasks = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.warning(
            "PR #%d: gh agent-task list returned malformed JSON — session state unavailable: %s",
            pr_number,
            exc,
        )
        return None

    if not isinstance(tasks, list):
        logger.warning(
            "PR #%d: gh agent-task list returned non-list JSON — session state unavailable",
            pr_number,
        )
        return None

    if len(tasks) >= _AGENT_TASK_LIST_LIMIT:
        logger.warning(
            "PR #%d: gh agent-task list reached its limit — session state may be truncated",
            pr_number,
        )
        return None

    inventory_unknown = False
    for task in tasks:
        if not isinstance(task, dict):
            inventory_unknown = True
            continue
        task_repo = task.get("repository")
        if not isinstance(task_repo, str):
            inventory_unknown = True
            continue
        if task_repo != repo:
            continue
        task_pr = task.get("pullRequestNumber")
        if not isinstance(task_pr, int) or isinstance(task_pr, bool):
            inventory_unknown = True
            continue
        if task_pr != pr_number:
            continue
        status = task.get("state")
        if status in _ACTIVE_TASK_STATUSES:
            logger.info(
                "PR #%d: Active agent task detected (id=%s, status=%s)",
                pr_number,
                task.get("id"),
                status,
            )
            return True
        if not isinstance(status, str) or status not in _INACTIVE_TASK_STATUSES:
            inventory_unknown = True

    if inventory_unknown:
        logger.warning(
            "PR #%d: gh agent-task list contained unusable task records — session state unavailable",
            pr_number,
        )
        return None
    return False


def is_copilot_session_active(provider: CIPlatformProvider, pr_number: int) -> bool:
    """Check if a Copilot coding session is currently active.

    .. deprecated::
        Use :func:`is_copilot_session_active_via_agent_task` instead.
        This function uses an unreliable events-based heuristic and will be
        removed in a future release.

    Looks for the latest copilot_work_started event and checks whether
    a terminal event (finished or failure) exists with a higher ID.
    Additionally applies a staleness timeout: if the latest start event
    is older than ``AGDT_MAX_SESSION_AGE_SECONDS`` (default 3600s) with
    no terminal event, the session is considered stale/inactive.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.

    Returns:
        True if an active Copilot session is detected or if the events API
        is unavailable (fail-closed to prevent unsafe side effects).
        False when a terminal event is confirmed after the latest start,
        or when the latest start event exceeds the staleness threshold.
    """
    warnings.warn(
        "is_copilot_session_active() is deprecated. Use is_copilot_session_active_via_agent_task() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    try:
        events = provider.list_pr_issue_events(pr_number)
    except Exception as exc:
        logger.warning(
            "PR #%d: Failed to list issue events — assuming active session (fail-closed): %s",
            pr_number,
            exc,
        )
        return True

    logger.debug(
        "PR #%d: Fetched %d Copilot session event(s): %s",
        pr_number,
        len(events),
        [(e.id, e.event, e.created_at) for e in events],
    )

    latest_start = None
    for event in events:
        if event.event == COPILOT_SESSION_EVENT_STARTED:
            if latest_start is None or event.id > latest_start.id:
                latest_start = event

    if latest_start is None:
        logger.info("PR #%d: No copilot_work_started events found — not active", pr_number)
        return False

    has_terminal = any(
        e.id > latest_start.id
        for e in events
        if e.event in (COPILOT_SESSION_EVENT_FINISHED, COPILOT_SESSION_EVENT_FINISHED_FAILURE)
    )

    if has_terminal:
        logger.info(
            "PR #%d: Latest session (started id=%d) has terminal event — not active",
            pr_number,
            latest_start.id,
        )
        return False

    # Check staleness: if the start event is older than the threshold,
    # treat the session as inactive (handles cancelled/crashed sessions
    # that never emit a terminal event).
    max_age = _get_max_session_age_seconds()
    if _is_session_stale(latest_start.created_at, max_age):
        logger.info(
            "PR #%d: Session (started id=%d, created_at=%s) exceeds staleness threshold "
            "(%d seconds) — treating as inactive",
            pr_number,
            latest_start.id,
            latest_start.created_at,
            max_age,
        )
        return False

    logger.info(
        "PR #%d: Active Copilot session detected (started id=%d, created_at=%s, no terminal event)",
        pr_number,
        latest_start.id,
        latest_start.created_at,
    )
    return True
