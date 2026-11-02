"""Copilot session activity detector.

Provides typed task/session lifecycle detection and reconciliation, plus latest-session
outcome correlation for failed-session recovery. The legacy events-based heuristic is
deprecated and fail-closed.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import warnings
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from enum import Enum
from functools import partial
from typing import Any, cast

from agentic_devtools.cli.ci.agent_task_inventory import (
    inventory_failure_result,
    load_agent_task_inventory,
    normalize_agent_task_inventory,
)
from agentic_devtools.cli.ci.agent_task_lifecycle import (
    _normalize_agent_task_lifecycle_evidence,
    parse_lifecycle_timestamp,
    select_session_lifecycle_timestamp,
    select_task_lifecycle_timestamp,
)
from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import (
    LifecycleAssessment,
    _inventory_lifecycle_assessment,
    _malformed_task_ids,
    _parent_lifecycle_clock,
)
from agentic_devtools.cli.ci.models import (
    COPILOT_SESSION_EVENT_FINISHED,
    COPILOT_SESSION_EVENT_FINISHED_FAILURE,
    COPILOT_SESSION_EVENT_STARTED,
    AgentTaskInventory,
    AgentTaskInventoryAvailability,
    AgentTaskInventoryLoadResult,
    AgentTaskLifecycle,
    FailureCategory,
)
from agentic_devtools.cli.ci.pipeline.lifecycle_reconciliation_support import (
    LIFECYCLE_RECONCILIATION_EXCEPTIONS,
    _session_failure_metadata,
    read_reconciliation_lifecycle_inventory,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory, WorkflowRun
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

logger = logging.getLogger(__name__)

_ACTIVE_TASK_STATUSES = frozenset(
    {"idle", "in_progress", "queued", "requested", "running", "waiting", "waiting_for_user"}
)
_INACTIVE_TASK_STATUSES = frozenset({"canceled", "cancelled", "completed", "failed", "stopped", "timed_out"})
_DEFAULT_AGENT_TASK_TIMEOUT_SECONDS = 10
_AGENT_TASK_INVENTORY_UNSET = object()

_DEFAULT_MAX_SESSION_AGE_SECONDS = 3600  # 1 hour
_FAILED_TASK_STATUSES = frozenset({"canceled", "cancelled", "failed", "timed_out"})
_FINISHED_TASK_STATUSES = frozenset({"completed"})


class SessionOutcome(Enum):
    """Latest Copilot session outcome; expired lifecycles are ignored, not completed."""

    ACTIVE = "active"
    EXPIRED = "expired"
    FAILED = "failed"
    FINISHED = "finished"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SessionState:
    """Outcome, stable identity, and failure time for the latest Copilot session."""

    outcome: SessionOutcome
    failure_event_id: int | None = None
    task_id: str | None = None
    failure_created_at: str | None = None
    inventory_availability: AgentTaskInventoryAvailability = AgentTaskInventoryAvailability.COMPLETE
    failure_category: FailureCategory | None = None
    http_status: int | None = None
    failure_source: str | None = None


def _task_pr_number(task: dict[str, Any]) -> int | None:
    """Return the pull-request number from supported Agent Task record shapes."""
    metadata = task.get("metadata")
    for container in (task, metadata if isinstance(metadata, dict) else {}):
        for key in ("pr_number", "pull_request_number", "pullRequestNumber"):
            value = container.get(key)
            if isinstance(value, int) and not isinstance(value, bool):
                return value

    for key in ("pull_request", "pullRequest"):
        pull_request = task.get(key)
        if isinstance(pull_request, dict):
            value = pull_request.get("number")
            if isinstance(value, int) and not isinstance(value, bool):
                return value

    artifacts = task.get("artifacts")
    if not isinstance(artifacts, list):
        return None
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_type = artifact.get("type")
        artifact_data = artifact.get("data")
        if artifact_type == "pull" and isinstance(artifact_data, dict):
            for key in ("number", "pull_request_number", "target_id"):
                value = artifact_data.get(key)
                if isinstance(value, int) and not isinstance(value, bool):
                    return value
                if isinstance(value, str) and value.isdigit():
                    return int(value)
        for artifact_container in (artifact_data, artifact):
            if not isinstance(artifact_container, dict):
                continue
            for key in ("url", "html_url", "target_id", "targetId"):
                value = artifact_container.get(key)
                if isinstance(value, str):
                    match = re.search(r"/pull/(\d+)(?:/|[?#]|$)", value)
                    if match:
                        return int(match.group(1))
                    if artifact_type == "pull" and value.isdigit():
                        return int(value)
    return None


def _task_matches_pr(task: object, pr_number: int, head_branch: str | None, pr_id: int | None) -> bool:
    """Return whether an Agent Task record can be tied to the requested PR."""
    if not isinstance(task, dict):
        return False

    task_pr_number = _task_pr_number(task)
    if task_pr_number == pr_number:
        return True

    task_name = task.get("name")
    if (
        task_pr_number is None
        and isinstance(task_name, str)
        and re.search(rf"\b(?:pr|pull\s+request)\s*#?\s*{pr_number}\b", task_name, re.IGNORECASE)
    ):
        return True

    artifacts = task.get("artifacts")
    if not isinstance(artifacts, list):
        return False
    normalized_branch = head_branch.removeprefix("refs/heads/") if isinstance(head_branch, str) and head_branch else ""
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        data = artifact.get("data")
        if not isinstance(data, dict):
            continue
        if artifact.get("type") == "pull":
            artifact_id = data.get("id")
            if (
                pr_id is not None
                and isinstance(artifact_id, int)
                and not isinstance(artifact_id, bool)
                and artifact_id == pr_id
            ):
                return True
        elif artifact.get("type") == "branch" and task_pr_number is None:
            head_ref = data.get("head_ref")
            if isinstance(head_ref, str) and (
                (normalized_branch and head_ref.removeprefix("refs/heads/") == normalized_branch)
                or re.search(rf"\b(?:pr|pull)[-_]?{pr_number}\b", head_ref, re.IGNORECASE)
            ):
                return True
    return False


def _correlate_task_failure_event(
    task_created_at: object,
    failure_created_at: object,
    events: Sequence[object],
) -> tuple[int, str] | None:
    """Return the timeline failure event and timestamp correlated with a task."""
    if not isinstance(task_created_at, str):
        return None
    try:
        task_started = datetime.fromisoformat(task_created_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    if task_started.tzinfo is None:
        task_started = task_started.replace(tzinfo=UTC)
    task_started = task_started.astimezone(UTC)
    task_failed = None
    if failure_created_at is not None:
        if not isinstance(failure_created_at, str):
            return None
        try:
            task_failed = datetime.fromisoformat(failure_created_at.replace("Z", "+00:00"))
        except ValueError:
            return None
        if task_failed.tzinfo is None:
            task_failed = task_failed.replace(tzinfo=UTC)
        task_failed = task_failed.astimezone(UTC)
        if task_started > task_failed:
            return None

    relevant_events: list[tuple[int, str, str]] = []
    for event in events:
        event_id = getattr(event, "id", None)
        event_type = getattr(event, "event", None)
        event_created_at = getattr(event, "created_at", None)
        if (
            event_type
            not in (
                COPILOT_SESSION_EVENT_STARTED,
                COPILOT_SESSION_EVENT_FINISHED,
                COPILOT_SESSION_EVENT_FINISHED_FAILURE,
            )
            or not isinstance(event_id, int)
            or isinstance(event_id, bool)
            or event_id <= 0
            or not isinstance(event_created_at, str)
        ):
            continue
        relevant_events.append((event_id, event_type, event_created_at))

    if task_failed is None:
        for _, event_type, event_created_at in relevant_events:
            if event_type != COPILOT_SESSION_EVENT_STARTED:
                continue
            try:
                event_time = datetime.fromisoformat(event_created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=UTC)
            if event_time.astimezone(UTC) > task_started:
                return None
        if not relevant_events:
            return None
        latest_event = max(relevant_events, key=lambda item: item[0])
        if latest_event[1] != COPILOT_SESSION_EVENT_FINISHED_FAILURE:
            return None
        try:
            event_time = datetime.fromisoformat(latest_event[2].replace("Z", "+00:00"))
        except ValueError:
            return None
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=UTC)
        event_time = event_time.astimezone(UTC)
        return (latest_event[0], latest_event[2]) if task_started <= event_time else None

    correlated_events: list[tuple[int, str]] = []
    for event_id, event_type, event_created_at in relevant_events:
        if event_type != COPILOT_SESSION_EVENT_FINISHED_FAILURE:
            continue
        try:
            event_time = datetime.fromisoformat(event_created_at.replace("Z", "+00:00"))
        except ValueError:
            continue
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=UTC)
        event_time = event_time.astimezone(UTC)
        if task_started <= event_time <= task_failed:
            correlated_events.append((event_id, event_created_at))
    return max(correlated_events, default=None)


def _session_state_from_events(
    provider: CIPlatformProvider,
    pr_number: int,
    events: Sequence[object] | None = None,
) -> SessionState:
    if events is None:
        try:
            events = provider.list_pr_issue_events(pr_number)
        except Exception as exc:
            if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                raise
            logger.warning("PR #%d: Failed to read Copilot session events: %s", pr_number, exc)
            return SessionState(SessionOutcome.UNKNOWN)

    if not isinstance(events, list):
        logger.warning("PR #%d: Copilot session events returned an unusable inventory", pr_number)
        return SessionState(SessionOutcome.UNKNOWN)
    relevant_events = [
        event
        for event in events
        if getattr(event, "event", None)
        in (COPILOT_SESSION_EVENT_STARTED, COPILOT_SESSION_EVENT_FINISHED, COPILOT_SESSION_EVENT_FINISHED_FAILURE)
        and isinstance(getattr(event, "id", None), int)
        and not isinstance(getattr(event, "id", None), bool)
    ]
    if not relevant_events:
        return SessionState(SessionOutcome.NONE)
    latest = max(relevant_events, key=lambda event: event.id)
    if latest.event == COPILOT_SESSION_EVENT_STARTED:
        return SessionState(SessionOutcome.ACTIVE)
    if latest.event == COPILOT_SESSION_EVENT_FINISHED_FAILURE:
        return SessionState(SessionOutcome.FAILED, failure_event_id=latest.id, failure_created_at=latest.created_at)
    return SessionState(SessionOutcome.FINISHED)


def _list_session_events(provider: CIPlatformProvider, pr_number: int) -> Sequence[object] | None:
    """Read timeline events for task correlation, preserving provider cooldowns."""
    try:
        events = provider.list_pr_issue_events(pr_number)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        logger.warning("PR #%d: Failed to read Copilot session events: %s", pr_number, exc)
        return None
    if not isinstance(events, list):
        logger.warning("PR #%d: Copilot session events returned an unusable inventory", pr_number)
        return None
    return events


def _newer_timeline_state(
    events: Sequence[object] | None,
    task_terminal_at: object,
) -> SessionState | None:
    """Return the newest timeline outcome only when it follows a terminal task."""
    if events is None or not isinstance(task_terminal_at, str):
        return None
    try:
        terminal_time = datetime.fromisoformat(task_terminal_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    if terminal_time.tzinfo is None:
        terminal_time = terminal_time.replace(tzinfo=UTC)
    terminal_time = terminal_time.astimezone(UTC)

    relevant_events: list[tuple[datetime, int, str, str]] = []
    for event in events:
        event_id = getattr(event, "id", None)
        event_type = getattr(event, "event", None)
        event_created_at = getattr(event, "created_at", None)
        if (
            event_type
            not in (
                COPILOT_SESSION_EVENT_STARTED,
                COPILOT_SESSION_EVENT_FINISHED,
                COPILOT_SESSION_EVENT_FINISHED_FAILURE,
            )
            or not isinstance(event_id, int)
            or isinstance(event_id, bool)
            or event_id <= 0
            or not isinstance(event_created_at, str)
        ):
            continue
        try:
            event_time = datetime.fromisoformat(event_created_at.replace("Z", "+00:00"))
        except ValueError:
            continue
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=UTC)
        relevant_events.append((event_time.astimezone(UTC), event_id, event_type, event_created_at))
    if not relevant_events:
        return None

    latest_time, latest_id, latest_type, latest_created_at = max(relevant_events, key=lambda item: (item[0], item[1]))
    if latest_time <= terminal_time:
        return None
    if latest_type == COPILOT_SESSION_EVENT_STARTED:
        return SessionState(SessionOutcome.ACTIVE)
    if latest_type == COPILOT_SESSION_EVENT_FINISHED_FAILURE:
        return SessionState(SessionOutcome.FAILED, failure_event_id=latest_id, failure_created_at=latest_created_at)
    return SessionState(SessionOutcome.FINISHED)


def _reconcile_terminal_task_timeline(
    events: Sequence[object] | None,
    task_created_at: object,
    task_terminal_at: object,
    expected_terminal_event: str | None,
    task_id: str | None = None,
) -> SessionState | None:
    """Reconcile timeline activity after a terminal task, failing closed if ordering is unclear."""
    if expected_terminal_event is None:
        if events is None or not isinstance(task_created_at, str) or not isinstance(task_terminal_at, str):
            return SessionState(SessionOutcome.UNKNOWN)
        try:
            task_started = datetime.fromisoformat(task_created_at.replace("Z", "+00:00"))
            task_finished = datetime.fromisoformat(task_terminal_at.replace("Z", "+00:00"))
        except ValueError:
            return SessionState(SessionOutcome.UNKNOWN)
        if task_started.tzinfo is None:
            task_started = task_started.replace(tzinfo=UTC)
        if task_finished.tzinfo is None:
            task_finished = task_finished.replace(tzinfo=UTC)
        task_started = task_started.astimezone(UTC)
        task_finished = task_finished.astimezone(UTC)
        if task_started > task_finished:
            return SessionState(SessionOutcome.UNKNOWN)

        task_terminal_events: list[tuple[datetime, int, str, str]] = []
        for event in events:
            event_id = getattr(event, "id", None)
            event_type = getattr(event, "event", None)
            event_created_at = getattr(event, "created_at", None)
            if (
                event_type not in (COPILOT_SESSION_EVENT_FINISHED, COPILOT_SESSION_EVENT_FINISHED_FAILURE)
                or not isinstance(event_id, int)
                or isinstance(event_id, bool)
                or event_id <= 0
                or not isinstance(event_created_at, str)
            ):
                continue
            try:
                event_time = datetime.fromisoformat(event_created_at.replace("Z", "+00:00"))
            except ValueError:
                continue
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=UTC)
            event_time = event_time.astimezone(UTC)
            if task_started <= event_time <= task_finished:
                task_terminal_events.append((event_time, event_id, event_type, event_created_at))

        if not task_terminal_events:
            return _newer_timeline_state(events, task_terminal_at) or SessionState(SessionOutcome.UNKNOWN)
        _event_time, event_id, event_type, event_created_at = max(
            task_terminal_events,
            key=lambda item: (item[0], item[1]),
        )
        if event_type == COPILOT_SESSION_EVENT_FINISHED_FAILURE:
            task_state = SessionState(
                SessionOutcome.FAILED,
                failure_event_id=event_id,
                task_id=task_id,
                failure_created_at=event_created_at,
            )
        else:
            task_state = SessionState(SessionOutcome.FINISHED, task_id=task_id)
        return _newer_timeline_state(events, event_created_at) or task_state

    if isinstance(task_terminal_at, str):
        return _newer_timeline_state(events, task_terminal_at)
    if events is None:
        return None
    if not isinstance(task_created_at, str):
        return SessionState(SessionOutcome.UNKNOWN)
    try:
        task_started = datetime.fromisoformat(task_created_at.replace("Z", "+00:00"))
    except ValueError:
        return SessionState(SessionOutcome.UNKNOWN)
    if task_started.tzinfo is None:
        task_started = task_started.replace(tzinfo=UTC)
    task_started = task_started.astimezone(UTC)

    terminal_events: list[tuple[datetime, int, str, str]] = []
    has_later_event = False
    for event in events:
        event_id = getattr(event, "id", None)
        event_type = getattr(event, "event", None)
        event_created_at = getattr(event, "created_at", None)
        if (
            event_type
            not in (
                COPILOT_SESSION_EVENT_STARTED,
                COPILOT_SESSION_EVENT_FINISHED,
                COPILOT_SESSION_EVENT_FINISHED_FAILURE,
            )
            or not isinstance(event_id, int)
            or isinstance(event_id, bool)
            or event_id <= 0
            or not isinstance(event_created_at, str)
        ):
            continue
        try:
            event_time = datetime.fromisoformat(event_created_at.replace("Z", "+00:00"))
        except ValueError:
            continue
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=UTC)
        event_time = event_time.astimezone(UTC)
        if event_time > task_started:
            has_later_event = True
        if event_time >= task_started and event_type != COPILOT_SESSION_EVENT_STARTED:
            terminal_events.append((event_time, event_id, event_type, event_created_at))

    if not terminal_events:
        return SessionState(SessionOutcome.UNKNOWN) if has_later_event else None
    _terminal_time, _terminal_id, terminal_type, terminal_created_at = min(
        terminal_events,
        key=lambda item: (item[0], item[1]),
    )
    if terminal_type != expected_terminal_event:
        return SessionState(SessionOutcome.UNKNOWN)
    return _newer_timeline_state(events, terminal_created_at)


def _normalize_session_inventory(value: object) -> AgentTaskInventoryLoadResult:
    """Normalize legacy list inputs only at the latest-session boundary."""
    if isinstance(value, AgentTaskInventoryLoadResult):
        normalized = normalize_agent_task_inventory(list(value.tasks))
        if not value.complete or normalized.complete:
            return value
        return replace(
            value, complete=False, availability=normalized.availability, failure_category=normalized.failure_category
        )
    return normalize_agent_task_inventory(value)


def _load_session_inventory(
    provider: CIPlatformProvider, pr_number: int, *, repo: str, supplied: object
) -> AgentTaskInventoryLoadResult:
    """Select supplied evidence, provider override, or the direct typed REST loader."""
    if supplied is not _AGENT_TASK_INVENTORY_UNSET:
        return _normalize_session_inventory(supplied)
    task_loader = getattr(type(provider), "list_agent_tasks", None)
    if task_loader is None or task_loader is CIPlatformProvider.list_agent_tasks:
        return _normalize_session_inventory(load_agent_task_inventory(repo, pr_number=pr_number))
    try:
        return _normalize_session_inventory(task_loader(provider, repo))
    except Exception as exc:
        return inventory_failure_result(exc)


def _session_inventory_state(
    outcome: SessionOutcome, *, inventory: AgentTaskInventoryLoadResult, **identity: Any
) -> SessionState:
    """Attach raw inventory diagnostics without letting incomplete evidence prove absence."""
    return _with_session_inventory(SessionState(outcome, **identity), inventory)


def _with_session_inventory(state: SessionState, inventory: AgentTaskInventoryLoadResult) -> SessionState:
    """Retain the failing evidence source while propagating raw inventory incompleteness."""
    if inventory.complete:
        return state
    if state.outcome is not SessionOutcome.ACTIVE:
        state = replace(state, outcome=SessionOutcome.UNKNOWN, task_id=None)
    if state.failure_category is not None:
        return state
    return replace(
        state,
        inventory_availability=inventory.availability or AgentTaskInventoryAvailability.UNAVAILABLE,
        failure_category=inventory.failure_category,
        http_status=inventory.http_status,
        failure_source="agent-task-inventory",
    )


@dataclass(frozen=True)
class _LifecycleEvidenceProvider:
    """Reuse boundary-validated evidence while delegating other read-only provider methods."""

    provider: CIPlatformProvider
    inventory: AgentTaskInventory

    def __getattr__(self, name: str) -> Any:
        if name == "list_pr_agent_task_lifecycles":
            return lambda *_args, **_kwargs: self.inventory
        return getattr(self.provider, name)


def _protect_terminal_session_state(
    state: SessionState, provider: CIPlatformProvider, pr_number: int, *, repo: str, **scope: Any
) -> SessionState:
    """Protect terminal outcomes with current evidence without assigning their stale identity."""
    if state.outcome not in {SessionOutcome.FAILED, SessionOutcome.FINISHED}:
        return state
    inventory = _read_task_lifecycle_inventory(
        provider, pr_number, include_pr_id=scope.get("pr_id") is not None, **scope
    )
    if isinstance(inventory, SessionState):
        return replace(
            inventory,
            task_id=state.task_id,
            failure_event_id=state.failure_event_id,
            failure_created_at=state.failure_created_at,
        )
    active = is_copilot_session_active_via_agent_task(
        repo, pr_number, provider=cast(CIPlatformProvider, _LifecycleEvidenceProvider(provider, inventory)), **scope
    )
    if active is False:
        return state
    lifecycle = classify_agent_task_inventory(inventory, now=datetime.now(UTC))
    return replace(
        state,
        outcome=SessionOutcome.ACTIVE if active else SessionOutcome.UNKNOWN,
        task_id=None if active else state.task_id,
        inventory_availability=lifecycle.inventory_availability,
        failure_category=lifecycle.failure_category,
        http_status=lifecycle.http_status,
        failure_source=lifecycle.failure_source,
    )


def _raw_task_values(task: dict) -> tuple[object, str | None, str | None, str | None]:
    """Read legacy state, stable identifier, and the two task clocks."""
    identifier = next(
        (
            task[k]
            for k in ("id", "task_id", "taskId")
            if isinstance(task.get(k), (str, int)) and not isinstance(task[k], bool)
        ),
        None,
    )
    clocks = tuple(
        next((task[k] for k in keys if isinstance(task.get(k), str) and task[k].strip()), None)
        for keys in (("createdAt", "created_at"), ("updatedAt", "updated_at"))
    )
    return (
        task.get("state") or task.get("status"),
        str(identifier) if identifier is not None else None,
        clocks[0],
        clocks[1],
    )


def _raw_task_sort_key(pair: tuple[int, dict]) -> tuple[str, int]:
    """Sort by creation before update while retaining stable provider order."""
    task = pair[1]
    return str(
        task.get("createdAt") or task.get("created_at") or task.get("updatedAt") or task.get("updated_at") or ""
    ), -pair[0]


def _raw_task_is_active(task: dict) -> bool:
    """Recognize supported raw active states without accepting malformed states."""
    return isinstance(status := task.get("state") or task.get("status"), str) and status in _ACTIVE_TASK_STATUSES


def _raw_terminal_session_state(task: dict, events: Sequence[object] | None) -> SessionState:
    """Resolve terminal raw evidence against the same task-scoped timeline bounds."""
    status, task_id, created, terminal = _raw_task_values(task)
    unknown = SessionState(SessionOutcome.UNKNOWN, task_id=task_id)
    if not created and not terminal and events is None:
        return unknown
    failed = isinstance(status, str) and (
        status in _FAILED_TASK_STATUSES or (status == "completed" and task.get("outcome") == "failure")
    )
    expected: str | None
    if failed and task_id:
        correlated = (
            _correlate_task_failure_event(created, terminal, events) if created and events is not None else None
        )
        failure_id, terminal = correlated if correlated is not None else (None, terminal)
        state = SessionState(
            SessionOutcome.FAILED, failure_event_id=failure_id, task_id=task_id, failure_created_at=terminal
        )
        expected = COPILOT_SESSION_EVENT_FINISHED_FAILURE
    elif status == "completed" and task.get("outcome") == "success":
        state, expected = SessionState(SessionOutcome.FINISHED, task_id=task_id), COPILOT_SESSION_EVENT_FINISHED
    elif status == "completed":
        state, expected = unknown, None
    else:
        return unknown
    timeline = _reconcile_terminal_task_timeline(
        events, created, terminal, expected, task_id=task_id if expected is None else None
    )
    if timeline is not None:
        return unknown if timeline.outcome is SessionOutcome.UNKNOWN else timeline
    return state


def get_latest_session_state(
    provider: CIPlatformProvider,
    pr_number: int,
    *,
    repo: str,
    head_branch: str | None,
    pr_id: int | None,
    head_sha: str = "",
    agent_task_inventory: object = _AGENT_TASK_INVENTORY_UNSET,
) -> SessionState:
    """Resolve the latest agent-task or timeline outcome for a pull request.

    The Agent Tasks API is preferred because it exposes failed tasks directly.
    Timeline events provide a compatibility fallback. Active task outcomes are
    checked against the shared lifecycle assessment so expired tasks are ignored,
    not reported as completed. UNKNOWN prevents retry or publication.
    """
    if not repo or "/" not in repo or pr_number <= 0:
        logger.warning("PR #%d: Invalid repository or pull-request identity for session lookup", pr_number)
        return SessionState(SessionOutcome.UNKNOWN)

    inventory = _load_session_inventory(provider, pr_number, repo=repo, supplied=agent_task_inventory)
    tasks = inventory.tasks
    session_state = partial(_session_inventory_state, inventory=inventory)
    assess = partial(
        _assess_active_task_lifecycle,
        provider,
        pr_number,
        repo=repo,
        head_branch=head_branch,
        pr_id=pr_id,
        head_sha=head_sha,
    )
    if not inventory.complete and not tasks:
        return session_state(SessionOutcome.UNKNOWN)

    matching: list[tuple[int, dict]] = [
        (index, task)
        for index, task in enumerate(tasks)
        if _task_matches_pr(task, pr_number, head_branch, pr_id) and isinstance(task, dict)
    ]
    if matching:
        active_matching = [pair for pair in matching if _raw_task_is_active(pair[1])]
        _index, task = max(active_matching or matching, key=_raw_task_sort_key)
        status, normalized_task_id, _, _ = _raw_task_values(task)
        active_task_lifecycle_outcome = None
        if isinstance(status, str) and status in _ACTIVE_TASK_STATUSES:
            active_task_lifecycle_outcome = assess(task_id=normalized_task_id, raw_task=task)
            if (
                inventory.complete
                and status in {"in_progress", "running"}
                and active_task_lifecycle_outcome.failure_source == "unsupported-agent-task-lifecycle"
            ):
                return session_state(SessionOutcome.ACTIVE, task_id=normalized_task_id)
            if active_task_lifecycle_outcome.outcome is SessionOutcome.EXPIRED:
                non_active_matching = [pair for pair in matching if not _raw_task_is_active(pair[1])]
                if non_active_matching:
                    _index, task = max(non_active_matching, key=_raw_task_sort_key)
                    status, normalized_task_id, _, _ = _raw_task_values(task)
                    active_task_lifecycle_outcome = None
        events: Sequence[object] | None = None
        if isinstance(status, str) and (status in _FAILED_TASK_STATUSES or status in _FINISHED_TASK_STATUSES):
            if not inventory.complete:
                protective = assess(task_id=normalized_task_id)
                if protective.outcome is SessionOutcome.ACTIVE:
                    return _with_session_inventory(protective, inventory)
                return _with_session_inventory(replace(protective, outcome=SessionOutcome.UNKNOWN), inventory)
            events = _list_session_events(provider, pr_number)
        if isinstance(status, str) and status in _ACTIVE_TASK_STATUSES:
            return _with_session_inventory(
                active_task_lifecycle_outcome or session_state(SessionOutcome.UNKNOWN, task_id=normalized_task_id),
                inventory,
            )
        return _with_session_inventory(
            _protect_terminal_session_state(
                _raw_terminal_session_state(task, events),
                provider,
                pr_number,
                repo=repo,
                head_branch=head_branch,
                pr_id=pr_id,
                head_sha=head_sha,
            ),
            inventory,
        )
    if not inventory.complete:
        return session_state(SessionOutcome.UNKNOWN)
    events = _list_session_events(provider, pr_number)
    return (
        SessionState(SessionOutcome.NONE) if events is None else _session_state_from_events(provider, pr_number, events)
    )


_ACTIVE_WRITER_RUN_STATUSES = _ACTIVE_TASK_STATUSES | {"pending"}


_TASK_LIFECYCLE_MAX_AGE = timedelta(minutes=75)


def _parse_lifecycle_timestamp(value: object) -> datetime | None:
    """Parse an ISO-8601 lifecycle timestamp and normalize it to UTC."""
    return parse_lifecycle_timestamp(value)


def _classify_task_lifecycle(
    state: object,
    *,
    lifecycle_at: object,
    created_at: object,
    first_observed_at: object,
    now: datetime,
    future_is_unknown: bool = False,
    fallback_lifecycle_at: object | None = None,
) -> LifecycleAssessment:
    """Classify one lifecycle using provider time, task creation, then durable observation."""
    now_utc = now.replace(tzinfo=UTC) if now.tzinfo is None else now.astimezone(UTC)
    if not isinstance(state, str):
        return LifecycleAssessment(None, False, None, "missing-state")

    normalized_state = state.casefold()
    if normalized_state in _INACTIVE_TASK_STATUSES:
        since = _parse_lifecycle_timestamp(lifecycle_at)
        if future_is_unknown and since is not None and since > now_utc:
            return LifecycleAssessment(None, False, since, "future-lifecycle-clock")
        return LifecycleAssessment(False, False, None, "terminal")
    if normalized_state not in _ACTIVE_TASK_STATUSES:
        return LifecycleAssessment(
            None,
            False,
            None,
            "unknown-state",
            failure_category=FailureCategory.UNKNOWN_TASK_STATE,
            failure_source="agent-task-lifecycle",
        )

    since = _parse_lifecycle_timestamp(lifecycle_at)
    reason = "lifecycle-timestamp"
    if since is None:
        since = _parse_lifecycle_timestamp(created_at)
        reason = "task-created-at"
    if since is None:
        since = _parse_lifecycle_timestamp(first_observed_at)
        reason = "first-observed-at"
    if since is None:
        return LifecycleAssessment(None, False, None, "missing-clock")

    if future_is_unknown and since > now_utc:
        fallback = _parse_lifecycle_timestamp(fallback_lifecycle_at)
        if fallback is not None and fallback <= now_utc:
            expired = now_utc - fallback > _TASK_LIFECYCLE_MAX_AGE
            return LifecycleAssessment(not expired, expired, fallback, "expired" if expired else "parent-lifecycle")
        return LifecycleAssessment(None, False, since, "future-lifecycle-clock")
    expired = now_utc - since > _TASK_LIFECYCLE_MAX_AGE
    return LifecycleAssessment(not expired, expired, since, "expired" if expired else reason)


def _classify_agent_task_lifecycle(
    task: AgentTaskLifecycle,
    *,
    first_observed_at: dict[str, str],
    now: datetime,
    future_is_unknown: bool = False,
) -> LifecycleAssessment:
    """Use the newest eligible session clock, falling back to task creation only when absent."""
    parent_clock = _parent_lifecycle_clock(task)
    task_clock = select_task_lifecycle_timestamp(task)
    parent_assessment = _classify_task_lifecycle(
        task.state,
        lifecycle_at=task_clock.isoformat() if task_clock is not None else None,
        created_at=task.created_at,
        first_observed_at=first_observed_at.get("task"),
        now=now,
        future_is_unknown=future_is_unknown,
        fallback_lifecycle_at=parent_clock.isoformat() if task_clock != parent_clock and parent_clock else None,
    )
    assessments = [parent_assessment]
    if task.state.casefold() == "queued" and not task.sessions and not assessments[0].expired:
        return LifecycleAssessment(None, False, assessments[0].since, "queued-without-session")
    for session in task.sessions:
        lifecycle_at = select_session_lifecycle_timestamp((session,))
        assessments.append(
            _classify_task_lifecycle(
                session.state,
                lifecycle_at=lifecycle_at.isoformat() if lifecycle_at is not None else None,
                created_at=None,
                first_observed_at=first_observed_at.get(session.session_id),
                now=now,
                future_is_unknown=future_is_unknown,
            )
        )

    blocking = [assessment for assessment in assessments if assessment.blocking is True]
    if blocking:
        since = max((item.since for item in blocking if item.since is not None), default=None)
        return LifecycleAssessment(True, any(item.expired for item in assessments), since, "blocking-lifecycle")
    unknown = next((assessment for assessment in assessments if assessment.blocking is None), None)
    if unknown is not None:
        return replace(unknown, expired=any(item.expired for item in assessments))
    return LifecycleAssessment(False, any(item.expired for item in assessments), None, "no-blocking-lifecycle")


def classify_agent_task_inventory(
    inventory: AgentTaskInventory,
    *,
    now: datetime,
    first_observed_at: dict[str, dict[str, str]] | None = None,
) -> LifecycleAssessment:
    """Classify bounded task/session evidence without performing provider mutations."""
    assessment = partial(_inventory_lifecycle_assessment, inventory=inventory)
    assessments = [
        _classify_agent_task_lifecycle(
            task,
            first_observed_at=(first_observed_at or {}).get(task.task_id, {}),
            now=now,
            future_is_unknown=not inventory.complete,
        )
        for task in inventory.tasks
    ]
    malformed_task_ids = _malformed_task_ids(inventory, now=now, max_age=_TASK_LIFECYCLE_MAX_AGE)
    assessments = [
        replace(item, blocking=None, reason="malformed-lifecycle")
        if task.task_id in malformed_task_ids and item.blocking is True
        else item
        for task, item in zip(inventory.tasks, assessments, strict=True)
    ]
    expired_task_ids = {task.task_id for task, item in zip(inventory.tasks, assessments, strict=True) if item.expired}
    blocking = [assessment for assessment in assessments if assessment.blocking is True]
    expired = bool(expired_task_ids)
    if blocking:
        newest_since = max((item.since for item in blocking if item.since is not None), default=None)
        return assessment(True, expired, newest_since, "blocking-lifecycle")
    unknown = next((assessment for assessment in assessments if assessment.blocking is None), None)
    if unknown is not None:
        return assessment(None, expired, unknown.since, unknown.reason, failure_category=unknown.failure_category)

    incomplete_reasons = inventory.incomplete_reasons
    task_scoped_incomplete = bool(incomplete_reasons) and all(
        reason.startswith(("task-detail:", "malformed-session:", "missing-session-id:"))
        and reason.partition(":")[2] in expired_task_ids
        for reason in incomplete_reasons
    )
    expired_only = expired and all(assessment.expired or assessment.blocking is False for assessment in assessments)
    if not inventory.complete and not (expired_only and task_scoped_incomplete):
        return assessment(None, expired, None, "incomplete-inventory")
    if expired_only and not inventory.complete:
        return assessment(False, True, None, "expired-incomplete-task")
    return assessment(False, expired, None, "expired-lifecycle" if expired else "no-blocking-lifecycle")


def _assess_active_task_lifecycle(
    provider: CIPlatformProvider, pr_number: int, *, repo: str, task_id: str | None, **scope: Any
) -> SessionState:
    """Use typed lifecycle evidence before treating a legacy active task as blocking."""
    if not task_id:
        return SessionState(SessionOutcome.UNKNOWN)
    head_branch, head_sha, raw_task = scope.get("head_branch"), scope.get("head_sha", ""), scope.pop("raw_task", None)
    inventory = _read_task_lifecycle_inventory(provider, pr_number, **scope)
    if isinstance(inventory, SessionState):
        return replace(inventory, task_id=task_id)
    if isinstance(raw_task, dict) and _task_pr_number(raw_task) not in (None, pr_number):
        raw_task = None
    matched_task = next((task for task in inventory.tasks if task.task_id == task_id), None)
    if (
        isinstance(raw_task, dict)
        and matched_task is not None
        and matched_task.repository.casefold() == repo.casefold()
        and matched_task.pr_number == pr_number
    ):
        inventory = _normalize_agent_task_lifecycle_evidence((raw_task,), inventory)
    matched_task = next((task for task in inventory.tasks if task.task_id == task_id), None)

    first_observed_by_task = _read_lifecycle_clocks(provider, pr_number, inventory, head_branch, head_sha)
    now = datetime.now(UTC)
    inventory_assessment = classify_agent_task_inventory(
        inventory,
        now=now,
        first_observed_at=first_observed_by_task,
    )
    lifecycle_state = partial(
        SessionState,
        inventory_availability=inventory_assessment.inventory_availability,
        failure_category=inventory_assessment.failure_category,
        http_status=inventory_assessment.http_status,
        failure_source=inventory_assessment.failure_source,
    )
    task_assessment = (
        _classify_agent_task_lifecycle(
            matched_task,
            first_observed_at=first_observed_by_task.get(task_id, {}),
            now=now,
            future_is_unknown=not inventory.complete,
        )
        if matched_task is not None
        else None
    )
    if inventory_assessment.blocking is True:
        return lifecycle_state(
            SessionOutcome.ACTIVE,
            task_id=task_id
            if task_assessment is not None
            and task_assessment.blocking is True
            and matched_task is not None
            and matched_task.state in _ACTIVE_TASK_STATUSES
            else None,
        )
    if inventory_assessment.blocking is None or task_assessment is None:
        return lifecycle_state(SessionOutcome.UNKNOWN, task_id=task_id)
    if task_assessment.expired:
        if not callable(getattr(provider, "list_correlated_cloud_writer_runs", None)):
            return lifecycle_state(SessionOutcome.UNKNOWN, task_id=task_id)
        aggregate_active = is_copilot_session_active_via_agent_task(repo, pr_number, provider=provider, **scope)
        if aggregate_active is True:
            return lifecycle_state(SessionOutcome.ACTIVE)
        if aggregate_active is None:
            return lifecycle_state(SessionOutcome.UNKNOWN, task_id=task_id)
        logger.info(
            "PR #%d: Expired task lifecycle is ignored, not completed (task_id=%s)",
            pr_number,
            task_id,
        )
        return lifecycle_state(SessionOutcome.EXPIRED, task_id=task_id)
    return lifecycle_state(SessionOutcome.UNKNOWN, task_id=task_id)


def _read_task_lifecycle_inventory(
    provider: CIPlatformProvider, pr_number: int, *, include_pr_id: bool = True, **scope: Any
) -> AgentTaskInventory | SessionState:
    """Read typed evidence once, preserving cooldowns and diagnostic failure facts."""
    unavailable = partial(
        SessionState,
        SessionOutcome.UNKNOWN,
        inventory_availability=AgentTaskInventoryAvailability.UNAVAILABLE,
        failure_source="agent-task-lifecycle",
    )
    list_lifecycles = getattr(provider, "list_pr_agent_task_lifecycles", None)
    if not callable(list_lifecycles):
        return unavailable(failure_category=FailureCategory.PROVIDER_UNAVAILABLE)
    try:
        scope["head_branch"] = scope.get("head_branch") or ""
        if not include_pr_id:
            scope.pop("pr_id", None)
        inventory = list_lifecycles(pr_number, **scope)
    except Exception as exc:
        if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
            raise
        category, status = _session_failure_metadata(exc)
        return unavailable(failure_category=category, http_status=status)
    if not isinstance(inventory, AgentTaskInventory):
        unsupported = (
            getattr(type(provider), "list_pr_agent_task_lifecycles", None) is None
            and inventory is not None
            and not isinstance(inventory, (dict, list, tuple, str, int, float, bool))
        )
        return unavailable(
            failure_category=FailureCategory.MALFORMED_RESPONSE,
            failure_source="unsupported-agent-task-lifecycle" if unsupported else "agent-task-lifecycle",
        )
    return inventory


def _read_lifecycle_clocks(
    provider: CIPlatformProvider,
    pr_number: int,
    inventory: AgentTaskInventory,
    head_branch: str | None,
    head_sha: str,
) -> dict[str, dict[str, str]]:
    """Read only missing lifecycle clocks, preserving provider rate-limit signals."""
    first_observed_by_task: dict[str, dict[str, str]] = {}
    get_first_observed = getattr(provider, "get_agent_task_first_observed_at", None)
    if callable(get_first_observed):
        for task in inventory.tasks:
            clocks: dict[str, str] = {}
            for session_id, key in _agent_task_clock_requests(task):
                try:
                    timestamp = get_first_observed(
                        pr_number,
                        task_id=task.task_id,
                        session_id=session_id,
                        head_branch=task.head_branch or head_branch or "",
                        expected_head_sha=head_sha,
                    )
                except (ProviderRateLimitError, RuntimeError, OSError, ValueError, TypeError, RetryableError) as exc:
                    if isinstance(exc, ProviderRateLimitError) and exc.is_rate_limit:
                        raise
                    inventory_failure_result(exc)
                    logger.warning(
                        "PR #%d: Could not read first-observed time for task %s/session %s: %s",
                        pr_number,
                        task.task_id,
                        session_id or "<task>",
                        exc,
                    )
                    continue
                if isinstance(timestamp, str) and timestamp:
                    clocks[key] = timestamp
            if clocks:
                first_observed_by_task[task.task_id] = clocks

    return first_observed_by_task


def _github_lifecycle_provider(repo: str) -> CIPlatformProvider:
    """Create a provider for an independent evaluation, never a process-wide cache."""
    from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

    return GitHubActionsProvider(repo=repo)


def _agent_task_clock_requests(task: AgentTaskLifecycle) -> list[tuple[str, str]]:
    """Select fallback clocks only when provider timestamps are unusable."""
    requests = []
    if select_task_lifecycle_timestamp(task) is None and _parse_lifecycle_timestamp(task.created_at) is None:
        requests.append(("", "task"))
    requests.extend(
        (session.session_id, session.session_id)
        for session in task.sessions
        if select_session_lifecycle_timestamp((session,)) is None
    )
    return requests


def reconcile_agent_task_lifecycles(
    repo: str,
    pr_number: int,
    *,
    head_branch: str = "",
    head_sha: str = "",
    pr_id: int | None = None,
    provider: CIPlatformProvider,
    persist_clocks_only: bool = False,
) -> SessionState | None:
    """Explicitly persist missing clocks and best-effort cancel verified expired attempts.

    This mutation phase is separate from action evaluation. Cancellation requires
    refreshed HEAD, task inventory, and current-attempt evidence; failures are
    audited without reclassifying expired lifecycles as active or completed.
    ``persist_clocks_only`` is for safety-validated scheduler preflight and skips
    writer-run inventory and cancellation.
    """
    try:
        provider.invalidate_agent_task_inventory(pr_number)
        if not head_sha or provider.get_pr_metadata(pr_number).head_sha != head_sha:
            return None
        inventory = read_reconciliation_lifecycle_inventory(
            provider, pr_number, pr_id=pr_id, head_branch=head_branch, head_sha=head_sha
        )
        if isinstance(inventory, SessionState):
            logger.warning(
                "PR #%d: Lifecycle reconciliation unavailable from %s (%s, HTTP %s)",
                pr_number,
                inventory.failure_source,
                inventory.failure_category,
                inventory.http_status,
            )
            return inventory
        for task in inventory.tasks:
            for session_id, _ in _agent_task_clock_requests(task):
                provider.get_or_record_agent_task_first_observed_at(
                    pr_number,
                    task_id=task.task_id,
                    session_id=session_id,
                    head_branch=task.head_branch or head_branch,
                    expected_head_sha=head_sha,
                )
        if persist_clocks_only:
            return None
        list_runs = getattr(provider, "list_correlated_cloud_writer_runs", None)
        cancel_run = getattr(provider, "cancel_workflow_run", None)
        if not callable(list_runs) or not callable(cancel_run):
            return None
        runs = list_runs(pr_number, head_branch=head_branch, tasks=inventory.tasks, head_sha=head_sha)
        if isinstance(runs, CloudWriterRunInventory):
            if not runs.complete or runs.uncorrelated_runs:
                return None
            runs = runs.runs
        for run in runs:
            assessment = _classify_writer_run(run)
            if assessment is None or not assessment.expired or run.run_attempt <= 0:
                continue
            try:
                provider.invalidate_agent_task_inventory(pr_number)
                if provider.get_pr_metadata(pr_number).head_sha != head_sha:
                    return None
                active = is_copilot_session_active_via_agent_task(
                    repo,
                    pr_number,
                    head_branch=head_branch,
                    pr_id=pr_id,
                    head_sha=head_sha,
                    provider=provider,
                )
                if active is not False:
                    return None
                provider.invalidate_agent_task_inventory(pr_number)
                if pr_id is None:
                    current_inventory = provider.list_pr_agent_task_lifecycles(
                        pr_number, head_branch=head_branch, head_sha=head_sha
                    )
                else:
                    current_inventory = provider.list_pr_agent_task_lifecycles(
                        pr_number, pr_id=pr_id, head_branch=head_branch, head_sha=head_sha
                    )
                current_runs = list_runs(
                    pr_number, head_branch=head_branch, tasks=current_inventory.tasks, head_sha=head_sha
                )
                if isinstance(current_runs, CloudWriterRunInventory):
                    if not current_runs.complete or current_runs.uncorrelated_runs:
                        return None
                    current_runs = current_runs.runs
                current_run = next(
                    (
                        current
                        for current in current_runs
                        if current.id == run.id and current.run_attempt == run.run_attempt
                    ),
                    None,
                )
                current_assessment = _classify_writer_run(current_run) if current_run is not None else None
                if current_assessment is None or not current_assessment.expired:
                    continue
                cancel_run(run.id)
            except (
                RuntimeError,
                OSError,
                ValueError,
                TypeError,
                subprocess.TimeoutExpired,
                ProviderRateLimitError,
                RetryableError,
            ) as exc:
                logger.warning(
                    "PR #%d: Expired writer run %d cancellation failed; ignoring expired run, not completed: %s",
                    pr_number,
                    run.id,
                    exc,
                )
            else:
                logger.info("PR #%d: Expired writer run %d cancellation requested; not completed", pr_number, run.id)
            finally:
                provider.invalidate_agent_task_inventory(pr_number)
    except LIFECYCLE_RECONCILIATION_EXCEPTIONS as exc:
        logger.warning("PR #%d: Lifecycle reconciliation unavailable: %s", pr_number, exc)
    return None


def _classify_writer_run(run: WorkflowRun, *, now: datetime | None = None) -> LifecycleAssessment | None:
    """Classify only active cloud-writer runs using their own start clock."""
    status = run.status.casefold()
    if status in {"completed", "cancelled", "canceled", "failure", "failed", "success", "skipped"}:
        return None
    if status not in _ACTIVE_WRITER_RUN_STATUSES:
        return LifecycleAssessment(True, False, None, "unknown-writer-run-status")
    started_at = _parse_lifecycle_timestamp(run.run_started_at)
    if started_at is None and run.run_attempt == 1:
        started_at = _parse_lifecycle_timestamp(run.created_at)
    if started_at is None:
        return LifecycleAssessment(True, False, None, "missing-writer-run-start")
    now_utc = (
        datetime.now(UTC) if now is None else (now.replace(tzinfo=UTC) if now.tzinfo is None else now.astimezone(UTC))
    )
    expired = now_utc - started_at > _TASK_LIFECYCLE_MAX_AGE
    return LifecycleAssessment(
        not expired, expired, started_at, "expired-writer-run" if expired else "young-writer-run"
    )


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
    except ValueError, AttributeError:
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
    head_branch: str | None = None,
    pr_id: int | None = None,
    timeout_seconds: int = _DEFAULT_AGENT_TASK_TIMEOUT_SECONDS,
    provider: CIPlatformProvider | None = None,
    head_sha: str = "",
) -> bool | None:
    """Classify correlated task/session lifecycle clocks with a 75-minute expiry.

    Returns:
        True if a current task/session blocks progress, False if none do, or None if
        the required inventory cannot be classified.
    """
    lifecycle_provider = provider or _github_lifecycle_provider(repo)
    try:
        if pr_id is None:
            inventory = lifecycle_provider.list_pr_agent_task_lifecycles(
                pr_number,
                head_branch=head_branch or "",
                head_sha=head_sha,
            )
        else:
            inventory = lifecycle_provider.list_pr_agent_task_lifecycles(
                pr_number,
                pr_id=pr_id,
                head_branch=head_branch or "",
                head_sha=head_sha,
            )
    except ProviderRateLimitError:
        raise
    except (RuntimeError, OSError, ValueError, TypeError, RetryableError) as exc:
        logger.warning("PR #%d: Agent Tasks lifecycle inventory unavailable: %s", pr_number, exc)
        return None

    evaluation_now = datetime.now(UTC)
    first_observed_by_task: dict[str, dict[str, str]] = {}
    expired_task_ids, malformed_ids = (
        set[str](),
        _malformed_task_ids(inventory, now=evaluation_now, max_age=_TASK_LIFECYCLE_MAX_AGE),
    )
    younger_task = False
    first_observed = getattr(lifecycle_provider, "get_agent_task_first_observed_at", None)

    def get_first_observed(task: AgentTaskLifecycle, session_id: str = "") -> str | None:
        if not callable(first_observed):
            return None
        try:
            result = first_observed(
                pr_number,
                task_id=task.task_id,
                session_id=session_id,
                head_branch=task.head_branch or head_branch or "",
                expected_head_sha=head_sha,
            )
        except ProviderRateLimitError:
            raise
        except (RuntimeError, OSError, ValueError, TypeError, RetryableError) as exc:
            logger.warning(
                "PR #%d: Could not read first-observed time for task %s/session %s: %s",
                pr_number,
                task.task_id,
                session_id or "<task>",
                exc,
            )
            return None
        return result if isinstance(result, str) else None

    for task in inventory.tasks:
        first_seen: dict[str, str] = {}
        for session_id, key in _agent_task_clock_requests(task):
            timestamp = get_first_observed(task, session_id)
            if timestamp is not None:
                first_seen[key] = timestamp
        first_observed_by_task[task.task_id] = first_seen
        assessment = _classify_agent_task_lifecycle(
            task,
            first_observed_at=first_seen,
            now=evaluation_now,
            future_is_unknown=not inventory.complete,
        )
        if assessment.expired:
            expired_task_ids.add(task.task_id)
            logger.info(
                "PR #%d: Agent Task lifecycle exceeded 75 minutes and will not block by itself; "
                "no supported task-finalization operation, not completed (task_id=%s)",
                pr_number,
                task.task_id,
            )
        if assessment.blocking is True and task.task_id not in malformed_ids:
            younger_task = True
            logger.info(
                "PR #%d: Agent Task lifecycle remains blocking (task_id=%s, since=%s)",
                pr_number,
                task.task_id,
                assessment.since,
            )

    run_listing_failed = False
    younger_run = False
    writer_inventory: CloudWriterRunInventory | None = None
    expired_writer_run_ids: set[int] = set()
    list_correlated_runs = getattr(lifecycle_provider, "list_correlated_cloud_writer_runs", None)
    if callable(list_correlated_runs):
        try:
            runs = list_correlated_runs(
                pr_number,
                head_branch=head_branch or "",
                tasks=inventory.tasks,
                head_sha=head_sha,
            )
        except ProviderRateLimitError as exc:
            run_listing_failed = True
            logger.warning("PR #%d: Writer Actions run inventory was rate limited: %s", pr_number, exc)
        except (RuntimeError, OSError, ValueError, TypeError, RetryableError) as exc:
            run_listing_failed = True
            logger.warning("PR #%d: Writer Actions run inventory unavailable: %s", pr_number, exc)
        else:
            if isinstance(runs, CloudWriterRunInventory):
                writer_inventory = runs
                run_listing_failed = not runs.complete
                if runs.incomplete_reasons:
                    logger.warning(
                        "PR #%d: Incomplete writer run inventory: %s", pr_number, ", ".join(runs.incomplete_reasons)
                    )
                if runs.uncorrelated_runs:
                    protective_run_ids = []
                    expired_run_ids = []
                    for run in runs.uncorrelated_runs:
                        uncorrelated_assessment = _classify_writer_run(run)
                        if uncorrelated_assessment is None:
                            continue
                        if uncorrelated_assessment.expired:
                            expired_run_ids.append(str(run.id))
                            expired_writer_run_ids.add(run.id)
                        else:
                            protective_run_ids.append(str(run.id))
                    if protective_run_ids:
                        logger.warning(
                            "PR #%d: Uncorrelated writer runs remain protective, not cancellation candidates: %s",
                            pr_number,
                            ", ".join(protective_run_ids),
                        )
                        younger_run = True
                    if expired_run_ids:
                        logger.info(
                            "PR #%d: Ignoring expired uncorrelated writer runs without cancellation or completion: %s",
                            pr_number,
                            ", ".join(expired_run_ids),
                        )
                runs = runs.runs
            for run in runs:
                writer_run_assessment = _classify_writer_run(run)
                if writer_run_assessment is None:
                    continue
                if writer_run_assessment.blocking is True:
                    younger_run = True
                    continue
                expired_writer_run_ids.add(run.id)

    if writer_inventory is not None and not writer_inventory.complete:
        detail_reasons = writer_inventory.corroboration_incomplete_reasons
        detail_run_ids = []
        for reason in detail_reasons:
            prefix, separator, raw_run_id = reason.partition(":")
            if prefix != "dispatch-detail" or not separator or not raw_run_id.isdigit():
                break
            detail_run_ids.append(int(raw_run_id))
        expired_detail_only = (
            writer_inventory.enumeration_complete is True
            and bool(detail_reasons)
            and set(writer_inventory.incomplete_reasons) == set(detail_reasons)
            and bool(detail_run_ids)
            and set(detail_run_ids).issubset(expired_writer_run_ids)
        )
        run_listing_failed = not expired_detail_only

    if younger_task or younger_run:
        return True
    inventory_assessment = classify_agent_task_inventory(
        inventory,
        now=evaluation_now,
        first_observed_at=first_observed_by_task,
    )
    if inventory_assessment.blocking is None:
        logger.warning(
            "PR #%d: Agent Tasks inventory is incomplete; lifecycle state remains unknown: %s",
            pr_number,
            ", ".join(inventory.incomplete_reasons) or inventory_assessment.reason,
        )
        return None
    if run_listing_failed:
        return None
    if inventory_assessment.expired and not inventory.complete:
        logger.warning(
            "PR #%d: Ignoring incomplete detail for demonstrably expired Agent Tasks: %s",
            pr_number,
            f"{', '.join(sorted(expired_task_ids))}; incomplete reasons: {', '.join(inventory.incomplete_reasons)}",
        )
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
