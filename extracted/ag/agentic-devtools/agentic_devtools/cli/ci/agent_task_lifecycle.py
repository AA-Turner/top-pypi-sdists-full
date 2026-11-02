"""Typed Agent Task lifecycle models and pure session clock helpers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from .agent_task_inventory import AgentTaskInventoryLoadResult
from .agent_task_lifecycle_raw_evidence import raw_lifecycle_artifact_scope_matches
from .agent_task_pr_identity import AgentTaskPrIdentity


@dataclass(frozen=True)
class AgentTaskSessionLifecycle:
    """Lifecycle evidence for one session, with creation separate from activity."""

    session_id: str
    state: str
    started_at: str = ""
    idle_at: str = ""
    head_sha: str = ""
    workflow_run_id: str = ""
    created_at: str = ""


@dataclass(frozen=True)
class AgentTaskLifecycle:
    """Lifecycle evidence for one task and its known sessions."""

    task_id: str
    repository: str
    pr_number: int
    head_branch: str
    state: str
    created_at: str
    sessions: tuple[AgentTaskSessionLifecycle, ...] = ()
    head_sha: str = ""
    workflow_run_id: str = ""
    started_at: str = ""
    idle_at: str = ""
    pr_identity: AgentTaskPrIdentity = field(default_factory=AgentTaskPrIdentity)


@dataclass(frozen=True)
class AgentTaskInventory(AgentTaskInventoryLoadResult[AgentTaskLifecycle]):
    """Bounded lifecycle inventory with conservatively normalized availability."""


def _newest_valid_lifecycle_clock(
    sources: Iterable[Mapping[str, object]],
    *keys: str,
) -> str:
    candidates = (
        value
        for source in sources
        if (value := select_valid_timestamp_alias(source, *keys)) and parse_lifecycle_timestamp(value) is not None
    )
    return max(
        candidates,
        key=lambda value: parse_lifecycle_timestamp(value) or datetime.min.replace(tzinfo=UTC),
        default="",
    )


def _raw_lifecycle_task_id(task: Mapping[str, object]) -> str | None:
    identifier = next(
        (
            task[key]
            for key in ("id", "task_id", "taskId")
            if isinstance(task.get(key), (str, int)) and not isinstance(task[key], bool)
        ),
        None,
    )
    return str(identifier) if identifier is not None else None


def _raw_lifecycle_repository_scope_matches(task: Mapping[str, object], lifecycle: AgentTaskLifecycle) -> bool:
    """Reject raw evidence with any valid contradictory repository alias."""
    metadata = task.get("metadata")
    sources = (task, metadata) if isinstance(metadata, Mapping) else (task,)
    for source in sources:
        repository = source.get("repository")
        if isinstance(repository, Mapping):
            repository = repository.get("full_name")
        if (
            isinstance(repository, str)
            and repository.strip()
            and repository.strip().casefold() != lifecycle.repository.casefold()
        ):
            return False
        for key in ("repo", "repository_full_name", "repositoryFullName"):
            repository = source.get(key)
            if (
                isinstance(repository, str)
                and repository.strip()
                and repository.strip().casefold() != lifecycle.repository.casefold()
            ):
                return False
    return True


def _raw_lifecycle_pr_scope_matches(task: Mapping[str, object], lifecycle: AgentTaskLifecycle) -> bool:
    """Reject raw evidence with any valid contradictory PR-number alias."""
    metadata = task.get("metadata")
    sources = (task, metadata) if isinstance(metadata, Mapping) else (task,)
    for source in sources:
        for key in ("pr_number", "pull_request_number", "pullRequestNumber"):
            pr_number = source.get(key)
            if isinstance(pr_number, int) and not isinstance(pr_number, bool) and pr_number != lifecycle.pr_number:
                return False
            if (
                isinstance(pr_number, str)
                and pr_number.isascii()
                and pr_number.isdigit()
                and int(pr_number) != lifecycle.pr_number
            ):
                return False
        for key in ("pull_request", "pullRequest"):
            pull_request = source.get(key)
            if isinstance(pull_request, Mapping):
                pr_number = pull_request.get("number")
                if isinstance(pr_number, int) and not isinstance(pr_number, bool) and pr_number != lifecycle.pr_number:
                    return False
                if (
                    isinstance(pr_number, str)
                    and pr_number.isascii()
                    and pr_number.isdigit()
                    and int(pr_number) != lifecycle.pr_number
                ):
                    return False
    return raw_lifecycle_artifact_scope_matches(task, lifecycle.pr_number, repository=lifecycle.repository)


def _raw_lifecycle_scope_matches(task: Mapping[str, object], lifecycle: AgentTaskLifecycle) -> bool:
    return _raw_lifecycle_repository_scope_matches(task, lifecycle) and _raw_lifecycle_pr_scope_matches(task, lifecycle)


def _raw_lifecycle_session_id(session: Mapping[str, object]) -> str:
    session_id = _agent_task_lifecycle_detail_value(session, "session_id", "sessionId") or (
        _agent_task_lifecycle_detail_value(session, "id")
    )
    return session_id if isinstance(session_id, str) else ""


def _merge_lifecycle_session_clocks(
    session: AgentTaskSessionLifecycle,
    raw_sessions: Iterable[Mapping[str, object]],
) -> AgentTaskSessionLifecycle:
    raw = tuple(raw_sessions)
    return replace(
        session,
        started_at=_newest_valid_lifecycle_clock(({"started_at": session.started_at}, *raw), "started_at", "startedAt"),
        idle_at=_newest_valid_lifecycle_clock(
            ({"idle_at": session.idle_at}, *raw), "idle_at", "idleAt", "idle_since", "idleSince"
        ),
        created_at=_newest_valid_lifecycle_clock(({"created_at": session.created_at}, *raw), "created_at", "createdAt"),
    )


def _raw_lifecycle_sessions(
    task: AgentTaskLifecycle,
    raw_tasks: Iterable[Mapping[str, object]],
) -> tuple[AgentTaskSessionLifecycle, ...]:
    raw_records = tuple(raw_tasks)
    raw_sessions: list[object] = []
    for raw in raw_records:
        sessions = raw.get("sessions")
        if isinstance(sessions, list):
            raw_sessions.extend(sessions)
    if not raw_sessions:
        return task.sessions
    records = [session for session in raw_sessions if isinstance(session, Mapping)]
    typed_ids = {session.session_id for session in task.sessions if session.session_id}
    merged = tuple(
        _merge_lifecycle_session_clocks(
            session,
            (raw for raw in records if session.session_id and _raw_lifecycle_session_id(raw) == session.session_id),
        )
        for session in task.sessions
    )
    added: list[AgentTaskSessionLifecycle] = []
    added_ids: set[str] = set()
    for session in records:
        session_id = _raw_lifecycle_session_id(session)
        if session_id and (session_id in typed_ids or session_id in added_ids):
            continue
        raw_group = (
            [raw for raw in records if _raw_lifecycle_session_id(raw) == session_id] if session_id else [session]
        )
        if session_id:
            added_ids.add(session_id)
        session_state = (
            ""
            if task.state.casefold() in {"canceled", "cancelled", "completed", "failed", "stopped", "timed_out"}
            else task.state
        )
        clocks = _merge_lifecycle_session_clocks(AgentTaskSessionLifecycle(session_id, session_state), raw_group)
        if clocks.started_at or clocks.idle_at or clocks.created_at:
            added.append(clocks)
    return (*merged, *added)


def _normalize_agent_task_lifecycle_evidence(
    raw_tasks: Iterable[object],
    typed_tasks: AgentTaskInventory,
) -> AgentTaskInventory:
    """Union valid clocks from same-ID raw tasks without changing typed availability or identity."""
    raw_by_id: dict[str, list[Mapping[str, object]]] = {}
    for raw_task in raw_tasks:
        if not isinstance(raw_task, Mapping) or (task_id := _raw_lifecycle_task_id(raw_task)) is None:
            continue
        raw_by_id.setdefault(task_id, []).append(raw_task)
    normalized: list[AgentTaskLifecycle] = []
    for task in typed_tasks.tasks:
        raw_matches = [raw for raw in raw_by_id.get(task.task_id, ()) if _raw_lifecycle_scope_matches(raw, task)]
        if not raw_matches:
            normalized.append(task)
            continue
        raw_clock_sources = tuple(raw_matches)
        typed_clock_source = {
            "created_at": task.created_at,
            "started_at": task.started_at,
            "idle_at": task.idle_at,
        }
        normalized.append(
            replace(
                task,
                created_at=_newest_valid_lifecycle_clock(
                    (typed_clock_source, *raw_clock_sources), "created_at", "createdAt"
                ),
                started_at=_newest_valid_lifecycle_clock(
                    (typed_clock_source, *raw_clock_sources), "started_at", "startedAt"
                ),
                idle_at=_newest_valid_lifecycle_clock(
                    (typed_clock_source, *raw_clock_sources), "idle_at", "idleAt", "idle_since", "idleSince"
                ),
                sessions=_raw_lifecycle_sessions(task, raw_matches),
            )
        )
    return replace(typed_tasks, tasks=tuple(normalized))


def parse_lifecycle_timestamp(value: object) -> datetime | None:
    """Parse an ISO-8601 lifecycle timestamp and normalize it to UTC."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def select_valid_timestamp_alias(
    record: Mapping[str, object],
    *keys: str,
    fallback: Mapping[str, object] | None = None,
) -> str:
    """Return the newest valid string timestamp across equivalent aliases."""
    values: list[object] = []
    for source in (record, fallback):
        if source is None:
            continue
        values.extend(source[key] for key in keys if key in source)
        metadata = source.get("metadata")
        if isinstance(metadata, Mapping):
            values.extend(metadata[key] for key in keys if key in metadata)
    candidates = [value for value in values if isinstance(value, str) and value.strip()]
    valid = [(timestamp, value) for value in candidates if (timestamp := parse_lifecycle_timestamp(value)) is not None]
    return max(valid, key=lambda item: item[0])[1] if valid else candidates[0] if candidates else ""


def session_lifecycle_timestamp_values(
    session: Mapping[str, object],
    *,
    include_created: bool = True,
    fallback: Mapping[str, object] | None = None,
) -> tuple[str, str, str]:
    """Return validated start, creation, and idle values from session aliases."""
    return (
        select_valid_timestamp_alias(session, "started_at", "startedAt", fallback=fallback),
        select_valid_timestamp_alias(session, "created_at", "createdAt", fallback=fallback) if include_created else "",
        select_valid_timestamp_alias(session, "idle_at", "idleAt", "idle_since", "idleSince", fallback=fallback),
    )


def has_session_activity_timestamp(
    record: Mapping[str, object],
    *,
    fallback: Mapping[str, object] | None = None,
) -> bool:
    """Return whether a record has a parseable start or idle clock alias."""
    return any(
        parse_lifecycle_timestamp(value) is not None
        for value in (
            select_valid_timestamp_alias(record, "started_at", "startedAt", fallback=fallback),
            select_valid_timestamp_alias(record, "idle_at", "idleAt", "idle_since", "idleSince", fallback=fallback),
        )
    )


def select_session_lifecycle_timestamp(sessions: Iterable[object]) -> datetime | None:
    """Select the newest eligible per-session activity or creation timestamp."""
    newest: datetime | None = None
    for session in sessions:
        activity = max(
            (
                timestamp
                for value in (getattr(session, "started_at", ""), getattr(session, "idle_at", ""))
                if (timestamp := parse_lifecycle_timestamp(value)) is not None
            ),
            default=None,
        )
        eligible = activity or parse_lifecycle_timestamp(getattr(session, "created_at", ""))
        if eligible is not None and (newest is None or eligible > newest):
            newest = eligible
    return newest


def select_task_lifecycle_timestamp(task: AgentTaskLifecycle) -> datetime | None:
    """Select the newest task activity or eligible session lifecycle timestamp."""
    timestamps = [
        timestamp
        for value in (task.started_at, task.idle_at)
        if (timestamp := parse_lifecycle_timestamp(value)) is not None
    ]
    session_timestamp = select_session_lifecycle_timestamp(task.sessions)
    if session_timestamp is not None:
        timestamps.append(session_timestamp)
    return max(timestamps, default=None)


def _agent_task_lifecycle_detail_value(record: Mapping[str, object], *keys: str) -> object:
    """Return the first matching record or metadata alias."""
    for key in keys:
        if key in record:
            return record[key]
    metadata = record.get("metadata")
    if isinstance(metadata, dict):
        for key in keys:
            if key in metadata:
                return metadata[key]
    return None


def _map_agent_task_lifecycle_session(
    task: Mapping[str, object],
    session: object,
    *,
    task_id: str,
    task_state: str,
    top_level_session_record: bool,
) -> tuple[AgentTaskSessionLifecycle | None, tuple[str, ...]]:
    """Normalize one session record while preserving identity and malformed-data facts."""
    if not isinstance(session, dict):
        return None, (f"malformed-session:{task_id}",)
    reasons: list[str] = []
    session_id_value = _agent_task_lifecycle_detail_value(session, "session_id", "sessionId") or (
        _agent_task_lifecycle_detail_value(task, "session_id", "sessionId")
        if top_level_session_record
        else _agent_task_lifecycle_detail_value(session, "id")
    )
    if not isinstance(session_id_value, str) or not session_id_value:
        reasons.append(f"missing-session-id:{task_id}")
        session_id_value = ""
    session_state_value = _agent_task_lifecycle_detail_value(session, "state", "status")
    if top_level_session_record:
        session_state_value = task_state
    started, session_created_at, idle = session_lifecycle_timestamp_values(
        session,
        include_created=not top_level_session_record,
        fallback=task if top_level_session_record else None,
    )
    session_state = session_state_value if isinstance(session_state_value, str) else ""
    session_head_sha = _agent_task_lifecycle_detail_value(session, "head_sha", "headSha")
    head_sha = session_head_sha if isinstance(session_head_sha, str) else ""
    session_run_id = _agent_task_lifecycle_detail_value(session, "workflow_run_id", "workflowRunId", "run_id", "runId")
    run_id = (
        str(session_run_id) if isinstance(session_run_id, (str, int)) and not isinstance(session_run_id, bool) else ""
    )
    session_values = (session_state, started, session_created_at, idle, head_sha, run_id)
    if not session_id_value and not any(session_values):
        return None, tuple(reasons)
    return (
        AgentTaskSessionLifecycle(
            session_id=session_id_value,
            state=session_state,
            started_at=started,
            idle_at=idle,
            head_sha=head_sha,
            workflow_run_id=run_id,
            created_at=session_created_at,
        ),
        tuple(reasons),
    )


def _map_agent_task_lifecycle_sessions(
    task: Mapping[str, object],
    detail: Mapping[str, object],
    *,
    task_id: str,
    task_state: str,
) -> tuple[tuple[AgentTaskSessionLifecycle, ...], tuple[str, ...]]:
    """Normalize nested or singleton sessions and return task-scoped diagnostics."""
    session_records = detail.get("sessions", task.get("sessions"))
    reasons: list[str] = []
    top_level_session_record = False
    if not isinstance(session_records, list):
        if session_records is not None:
            reasons.append(f"malformed-session:{task_id}")
        top_level_session_record = bool(
            _agent_task_lifecycle_detail_value(detail, "session_id", "sessionId")
            or has_session_activity_timestamp(detail, fallback=task)
        )
        session_records = [detail] if top_level_session_record else []
    sessions: list[AgentTaskSessionLifecycle] = []
    for session in session_records:
        normalized, diagnostics = _map_agent_task_lifecycle_session(
            task,
            session,
            task_id=task_id,
            task_state=task_state,
            top_level_session_record=top_level_session_record,
        )
        reasons.extend(diagnostics)
        if normalized is not None:
            sessions.append(normalized)
    return tuple(sessions), tuple(reasons)


def _map_agent_task_lifecycle_detail(
    task: Mapping[str, object],
    detail: Mapping[str, object],
    *,
    task_id: str,
    repository: str,
    pr_number: int,
    task_pr_number: int | None,
    head_branch: str,
) -> tuple[AgentTaskLifecycle, tuple[str, ...]]:
    """Normalize one fetched task detail record and retain task-scoped diagnostics."""
    state_value = _agent_task_lifecycle_detail_value(detail, "state", "status")
    if not isinstance(state_value, str) or not state_value.strip():
        state_value = _agent_task_lifecycle_detail_value(task, "state", "status")
    state = state_value if isinstance(state_value, str) else ""
    created_at = select_valid_timestamp_alias(detail, "created_at", "createdAt", fallback=task)
    started_at = select_valid_timestamp_alias(detail, "started_at", "startedAt", fallback=task)
    idle_at = select_valid_timestamp_alias(detail, "idle_at", "idleAt", "idle_since", "idleSince", fallback=task)
    sessions, reasons = _map_agent_task_lifecycle_sessions(
        task,
        detail,
        task_id=task_id,
        task_state=state,
    )
    task_head_sha = _agent_task_lifecycle_detail_value(detail, "head_sha", "headSha")
    task_run_id = _agent_task_lifecycle_detail_value(detail, "workflow_run_id", "workflowRunId", "run_id", "runId")
    lifecycle = AgentTaskLifecycle(
        task_id=task_id,
        repository=repository,
        pr_number=task_pr_number if task_pr_number is not None else pr_number,
        head_branch=head_branch,
        state=state,
        created_at=created_at,
        sessions=sessions,
        head_sha=task_head_sha if isinstance(task_head_sha, str) else "",
        workflow_run_id=str(task_run_id)
        if isinstance(task_run_id, (str, int)) and not isinstance(task_run_id, bool)
        else "",
        started_at=started_at,
        idle_at=idle_at,
    )
    return lifecycle, reasons
