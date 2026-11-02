"""Deterministic evidence classification for the AI PR Loop supervisor."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, cast

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    parse_lifecycle_timestamp,
    select_session_lifecycle_timestamp,
)
from agentic_devtools.cli.ci.models import (
    COPILOT_LOGINS,
    AgentTaskInventory,
    CheckRunStatus,
    PRMetadata,
    is_copilot_login,
)
from agentic_devtools.cli.ci.pipeline.session_detector import (
    _agent_task_clock_requests,
    _classify_writer_run,
)
from agentic_devtools.cli.ci.reconciliation.models import CloudWriterRunInventory
from agentic_devtools.cli.ci.session_evidence_presentation import (
    SessionEvidenceBuilder,
    SessionEvidencePresentation,
)

_LOOP_SUMMARY_LOGINS: frozenset[str] = COPILOT_LOGINS | frozenset({"github-actions[bot]"})


class SupervisorState(StrEnum):
    """Top-level state assigned to a pull request by the supervisor."""

    HEALTHY = "healthy"
    ACTIVE = "active"
    WAITING_EXPECTED = "waiting_expected"
    STUCK_CANDIDATE = "stuck_candidate"
    BLOCKED_HUMAN = "blocked_human"
    EXTERNAL_ERROR = "external_error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SupervisorConfig:
    """Thresholds used by the pure supervisor classifier."""

    loop_stale_seconds: int = 30 * 60
    task_stale_seconds: int = 75 * 60
    review_wait_seconds: int = 60 * 60

    def __post_init__(self) -> None:
        for name in ("loop_stale_seconds", "task_stale_seconds", "review_wait_seconds"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True)
class SupervisorEvidence:
    """Bounded facts collected for one open pull request."""

    pr_number: int
    head_sha: str
    labels: tuple[str, ...] = ()
    is_draft: bool = False
    is_fork: bool = False
    ignored: bool = False
    has_auto_merge_label: bool | None = None
    ci_status: str = "unknown"
    review_state: str = ""
    has_review_on_head: bool = False
    unresolved_threads: int = 0
    loop_run_status: str = ""
    loop_run_conclusion: str = ""
    loop_run_updated_at: datetime | None = None
    agent_task_status: str = ""
    agent_task_lifecycle_at: datetime | None = None
    agent_task_lifecycle_status: str = ""
    agent_task_lifecycle_reason: str = ""
    agent_task_incomplete_reasons: tuple[str, ...] = ()
    agent_task_ids: tuple[str, ...] = ()
    agent_task_run_ids: tuple[int, ...] = ()
    session_evidence: SessionEvidencePresentation | None = None
    review_requested_at: datetime | None = None
    last_action: str = ""
    last_action_at: datetime | None = None
    api_errors: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.pr_number) is not int or self.pr_number <= 0:
            raise ValueError("pr_number must be a positive integer")
        if not isinstance(self.head_sha, str) or not self.head_sha.strip():
            raise ValueError("head_sha must be a non-empty string")
        if type(self.unresolved_threads) is not int:
            raise ValueError("unresolved_threads must be an integer")
        if self.unresolved_threads < 0:
            raise ValueError("unresolved_threads must not be negative")


@dataclass(frozen=True)
class SupervisorClassification:
    """Classifier output consumed by the supervisor orchestrator."""

    state: SupervisorState
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class SupervisorCandidate:
    """A PR selected for agent-backed supervisor investigation."""

    evidence: SupervisorEvidence
    classification: SupervisorClassification
    fingerprint: str


_ACTIVE_TASK_STATUSES = frozenset({"idle", "queued", "requested", "waiting", "in_progress", "running"})
_FAILED_CHECK_CONCLUSIONS = frozenset(
    {
        "action_required",
        "cancelled",
        "failure",
        "stale",
        "startup_failure",
        "timed_out",
    }
)
_PASSING_CHECK_CONCLUSIONS = frozenset({"neutral", "skipped", "success"})
_FAILED_LOOP_CONCLUSIONS = _FAILED_CHECK_CONCLUSIONS
_ACTION_TABLE_EXECUTED_PATTERN_TEMPLATE = r"(?m)^\|\s*{action}\s*\|.*\|\s*\*\*executed\*\*"


def _is_action_executed(comment_body: str, *, action: str) -> bool:
    return bool(re.search(_ACTION_TABLE_EXECUTED_PATTERN_TEMPLATE.format(action=re.escape(action)), comment_body))


def _extract_issue_comment_signals(
    comments: Sequence[object],
) -> tuple[datetime | None, str, datetime | None]:
    review_requested_at: datetime | None = None
    last_action = ""
    last_action_at: datetime | None = None
    sorted_comments = sorted(
        comments,
        key=lambda comment: str(getattr(comment, "created_at", "") or ""),
    )
    for comment in sorted_comments:
        author = getattr(comment, "author", "") or ""
        if not isinstance(author, str) or author.casefold() not in {login.casefold() for login in _LOOP_SUMMARY_LOGINS}:
            continue
        body = getattr(comment, "body", "")
        if not isinstance(body, str) or not body:
            continue
        created_at = _parse_timestamp(getattr(comment, "created_at", ""))
        if _is_action_executed(body, action="request_review") and created_at is not None:
            review_requested_at = created_at
            last_action = "review_requested"
            last_action_at = created_at
        if _is_action_executed(body, action="dispatch_repair") and created_at is not None:
            last_action = "repair_dispatched"
            last_action_at = created_at
    return review_requested_at, last_action, last_action_at


def derive_ci_status(checks: Sequence[CheckRunStatus]) -> str:
    """Reduce check-run records to ``passing``, ``failing``, or ``pending``."""
    if not checks:
        return "unknown"
    if any(
        check.status.casefold() == "completed" and check.conclusion.casefold() in _FAILED_CHECK_CONCLUSIONS
        for check in checks
    ):
        return "failing"
    if any(check.status.casefold() != "completed" for check in checks):
        return "pending"
    if all(check.conclusion.casefold() in _PASSING_CHECK_CONCLUSIONS for check in checks):
        return "passing"
    return "pending"


def select_latest_agent_task(tasks: Sequence[object], pr_number: int) -> dict[str, Any] | None:
    """Return the newest well-formed PR task, ordered by creation rather than heartbeat."""
    matching: list[dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        task_data = cast(dict[str, Any], task)
        task_pr = task_data.get("pullRequestNumber")
        if isinstance(task_pr, str) and task_pr.isdigit():
            task_pr = int(task_pr)
        if task_pr == pr_number:
            matching.append(task_data)
    if not matching:
        return None
    return max(
        matching,
        key=lambda task: str(task.get("createdAt") or task.get("created_at") or ""),
    )


def select_latest_loop_run(runs: Sequence[object], pr_number: int) -> tuple[str, str, datetime | None]:
    """Return the latest loop-run status, conclusion, and creation timestamp for a PR."""
    matching: list[tuple[datetime, object]] = []
    for run in runs:
        if not hasattr(run, "pr_number") or getattr(run, "pr_number") != pr_number:
            continue
        timestamp = _parse_timestamp(getattr(run, "created_at", ""))
        if timestamp is not None:
            matching.append((timestamp, run))
    if not matching:
        return "", "", None
    timestamp, latest = max(matching, key=lambda item: item[0])
    conclusion = str(getattr(latest, "conclusion", "") or "").casefold()
    return ("completed" if conclusion else "in_progress"), conclusion, timestamp


def parse_agent_tasks(raw: str | None) -> list[dict[str, Any]]:
    """Parse the JSON list returned by ``gh agent-task list``."""
    if raw is None:
        return []
    try:
        payload: object = json.loads(raw)
    except json.JSONDecodeError, TypeError:
        return []
    if not isinstance(payload, list):
        return []
    parsed_tasks: list[dict[str, Any]] = []
    for item in cast(list[object], payload):
        if isinstance(item, dict):
            parsed_tasks.append(cast(dict[str, Any], item))
    return parsed_tasks


def _parse_timestamp(value: object) -> datetime | None:
    return parse_lifecycle_timestamp(value)


def _latest_task_timestamp(task: dict[str, Any] | None) -> datetime | None:
    if task is None:
        return None
    return _parse_timestamp(task.get("createdAt") or task.get("created_at"))


def _task_lifecycle_timestamp(task: object) -> datetime | None:
    sessions = getattr(task, "sessions", ())
    session_timestamp = select_session_lifecycle_timestamp(sessions)
    if session_timestamp is not None:
        return session_timestamp
    return _parse_timestamp(getattr(task, "created_at", ""))


def _has_copilot_review_on_head(reviews: Sequence[object], head_sha: str) -> bool:
    return any(
        hasattr(review, "user")
        and is_copilot_login(getattr(review, "user"))
        and getattr(review, "commit_sha", "") == head_sha
        for review in reviews
    )


def _metadata_is_fork(metadata: PRMetadata) -> bool:
    return bool(
        metadata.head_repo_full_name
        and metadata.base_repo_full_name
        and metadata.head_repo_full_name.casefold() != metadata.base_repo_full_name.casefold()
    )


def collect_supervisor_evidence(
    provider: Any,
    pr_number: int,
    *,
    tasks: Sequence[object],
    loop_runs: Sequence[object] = (),
    now: datetime,
) -> SupervisorEvidence:
    """Collect one PR's bounded evidence while retaining optional API errors."""
    _validate_now(now)
    metadata = provider.get_pr_metadata(pr_number)
    errors: list[str] = []

    try:
        checks = provider.list_check_runs(metadata.head_sha)
        ci_status = derive_ci_status(checks)
    except Exception as exc:
        checks = []
        ci_status = "unknown"
        errors.append(f"checks: {exc}")

    try:
        reviews = provider.list_reviews(pr_number)
        has_review_on_head = _has_copilot_review_on_head(reviews, metadata.head_sha)
        review_state = next(
            (
                review.state
                for review in reversed(reviews)
                if is_copilot_login(review.user) and review.commit_sha == metadata.head_sha
            ),
            "",
        )
    except Exception as exc:
        reviews = []
        has_review_on_head = False
        review_state = ""
        errors.append(f"reviews: {exc}")

    try:
        unresolved_threads = provider.count_unresolved_review_threads(pr_number)
    except Exception as exc:
        unresolved_threads = 0
        errors.append(f"threads: {exc}")
    review_requested_at: datetime | None = None
    last_action = ""
    last_action_at: datetime | None = None
    try:
        comments = provider.list_issue_comments(pr_number)
        review_requested_at, last_action, last_action_at = _extract_issue_comment_signals(comments)
    except Exception as exc:
        errors.append(f"issue_comments: {exc}")

    task, session_evidence_builder = select_latest_agent_task(tasks, pr_number), SessionEvidenceBuilder()
    loop_run_status, loop_run_conclusion, loop_run_updated_at = select_latest_loop_run(loop_runs, pr_number)
    task_status = str((task or {}).get("state") or (task or {}).get("status") or "") if task else ""
    task_timestamp = _latest_task_timestamp(task)
    lifecycle_status = ""
    lifecycle_reason = ""
    lifecycle_incomplete_reasons: tuple[str, ...] = ()
    task_ids: tuple[str, ...] = ()
    task_run_ids: tuple[int, ...] = ()
    has_expired_task_lifecycle = False
    inventory: AgentTaskInventory | None = None
    list_lifecycles = getattr(provider, "list_pr_agent_task_lifecycles", None)
    if callable(list_lifecycles):
        try:
            if metadata.pr_id is None:
                inventory = list_lifecycles(
                    pr_number,
                    head_branch=metadata.head_branch,
                    head_sha=metadata.head_sha,
                )
            else:
                inventory = list_lifecycles(
                    pr_number,
                    pr_id=metadata.pr_id,
                    head_branch=metadata.head_branch,
                    head_sha=metadata.head_sha,
                )
        except Exception as exc:
            lifecycle_status = "unknown"
            lifecycle_reason = "inventory-unavailable"
            session_evidence_builder.record_exception("lifecycle-reconciliation", exc, errors, "agent_tasks")
        else:
            if isinstance(inventory, AgentTaskInventory):
                task_ids = tuple(task.task_id for task in inventory.tasks)
                first_observed_at: dict[str, dict[str, str]] = {}
                clock_errors: list[str] = []
                read_first_observed = getattr(provider, "get_agent_task_first_observed_at", None)
                if callable(read_first_observed):
                    for lifecycle in inventory.tasks:
                        clocks: dict[str, str] = {}
                        for session_id, key in _agent_task_clock_requests(lifecycle):
                            try:
                                timestamp = read_first_observed(
                                    pr_number,
                                    task_id=lifecycle.task_id,
                                    session_id=session_id,
                                    head_branch=lifecycle.head_branch or metadata.head_branch,
                                    expected_head_sha=metadata.head_sha,
                                )
                            except Exception as exc:
                                clock_errors.append(
                                    session_evidence_builder.record_clock_exception(lifecycle.task_id, session_id, exc)
                                )
                                continue
                            if isinstance(timestamp, str) and timestamp:
                                clocks[key] = timestamp
                        if clocks:
                            first_observed_at[lifecycle.task_id] = clocks
                assessment = session_evidence_builder.classify_and_record_inventory(
                    inventory,
                    now=now,
                    first_observed_at=first_observed_at,
                )
                has_expired_task_lifecycle = assessment.expired
                lifecycle_reason = assessment.reason
                lifecycle_incomplete_reasons = inventory.incomplete_reasons + tuple(clock_errors)
                if assessment.blocking is True:
                    task_status = "in_progress"
                    task_timestamp = assessment.since
                    lifecycle_status = "blocking_with_expired_lifecycle" if assessment.expired else "blocking"
                elif assessment.blocking is None:
                    task_status = "unknown"
                    task_timestamp = None
                    lifecycle_status = "unknown"
                    errors.append(
                        "agent_tasks: incomplete lifecycle inventory: "
                        + (", ".join(lifecycle_incomplete_reasons) or assessment.reason)
                    )
                elif assessment.expired:
                    task_status = "expired"
                    task_timestamp = None
                    lifecycle_status = "expired_ignored_not_completed"
                else:
                    lifecycle_status = "no_blocking_lifecycle"
                    latest_task = max(
                        inventory.tasks,
                        key=lambda value: _task_lifecycle_timestamp(value) or datetime.min.replace(tzinfo=UTC),
                        default=None,
                    )
                    task_status = latest_task.state if latest_task is not None else ""
                    task_timestamp = _task_lifecycle_timestamp(latest_task) if latest_task is not None else None
            else:
                lifecycle_status = "unknown"
                lifecycle_reason = "invalid-inventory-type"
                errors.append("agent_tasks: lifecycle provider returned an invalid inventory")
    list_writer_runs = getattr(provider, "list_correlated_cloud_writer_runs", None)
    if callable(list_writer_runs) and inventory is not None:
        try:
            writer_inventory = list_writer_runs(
                pr_number,
                head_branch=metadata.head_branch,
                tasks=inventory.tasks,
                head_sha=metadata.head_sha,
            )
            if not isinstance(writer_inventory, CloudWriterRunInventory):
                writer_inventory = CloudWriterRunInventory(runs=tuple(writer_inventory))
        except Exception as exc:
            lifecycle_incomplete_reasons += (f"writer-runs:{exc}",)
            session_evidence_builder.record_exception("writer-run-reconciliation", exc, errors, "agent_task_runs")
            if lifecycle_status not in {
                "blocking",
                "blocking_with_expired_lifecycle",
            }:
                task_status = "unknown"
                task_timestamp = None
                lifecycle_status = "unknown"
                lifecycle_reason = "writer-run-inventory-unavailable"
        else:
            writer_runs = writer_inventory.runs
            uncorrelated_run_assessments = [
                (run, uncorrelated_assessment)
                for run in writer_inventory.uncorrelated_runs
                if (uncorrelated_assessment := _classify_writer_run(run, now=now)) is not None
            ]
            uncorrelated_blocking_runs = [
                run for run, assessment in uncorrelated_run_assessments if assessment.blocking is True
            ]
            expired_uncorrelated_runs = [run for run, assessment in uncorrelated_run_assessments if assessment.expired]
            expired_run_ids = {run.id for run in expired_uncorrelated_runs}
            task_run_ids = tuple(
                run.id
                for run in writer_runs + writer_inventory.uncorrelated_runs
                if type(getattr(run, "id", None)) is int
            )
            lifecycle_incomplete_reasons += tuple(
                f"uncorrelated-writer-run:{run.id}" for run, _ in uncorrelated_run_assessments
            )
            if not writer_inventory.complete:
                run_inventory_reasons = writer_inventory.incomplete_reasons or ("incomplete-inventory",)
                lifecycle_incomplete_reasons += tuple(f"writer-runs:{reason}" for reason in run_inventory_reasons)
            run_assessments = [
                (run, writer_run_assessment)
                for run in writer_runs
                if (writer_run_assessment := _classify_writer_run(run, now=now)) is not None
            ]
            blocking_runs = session_evidence_builder.record_blocking_writer_assessments(run_assessments)
            expired_runs = [assessment for _, assessment in run_assessments if assessment.expired]
            expired_run_ids.update(run.id for run, assessment in run_assessments if assessment.expired)
            expired_detail_only = False
            if not writer_inventory.complete:
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
                    and set(detail_run_ids).issubset(expired_run_ids)
                )
                if not expired_detail_only:
                    errors.append(
                        "agent_task_runs: incomplete writer run inventory: "
                        + ", ".join(writer_inventory.incomplete_reasons or ("incomplete-inventory",))
                    )
            if blocking_runs or uncorrelated_blocking_runs:
                task_status = "in_progress"
                task_timestamp = max(
                    (assessment.since for assessment in blocking_runs if assessment.since is not None),
                    default=None,
                )
                has_expired_entity = has_expired_task_lifecycle or bool(expired_runs) or bool(expired_uncorrelated_runs)
                lifecycle_status = "blocking_with_expired_lifecycle" if has_expired_entity else "blocking"
                lifecycle_reason = (
                    "uncorrelated-writer-run"
                    if uncorrelated_blocking_runs
                    else "blocking-writer-run-with-expired-lifecycle"
                    if has_expired_entity
                    else "blocking-writer-run"
                )
            elif (
                not writer_inventory.complete
                and lifecycle_status
                not in {
                    "blocking",
                    "blocking_with_expired_lifecycle",
                }
                and not expired_detail_only
            ):
                task_status = "unknown"
                task_timestamp = None
                lifecycle_status = "unknown"
                lifecycle_reason = "writer-run-inventory-unavailable"
            elif (expired_runs or expired_uncorrelated_runs) and lifecycle_status in {
                "no_blocking_lifecycle",
                "expired_ignored_not_completed",
            }:
                task_status = "expired"
                task_timestamp = None
                lifecycle_status = "expired_ignored_not_completed"
                lifecycle_reason = (
                    "expired-uncorrelated-writer-run-not-cancelled-by-read-only-supervisor"
                    if expired_uncorrelated_runs and not expired_runs
                    else "expired-writer-run-not-cancelled-by-read-only-supervisor"
                )
    labels = tuple(label for label in metadata.labels if isinstance(label, str))
    label_names = {label.casefold() for label in labels}
    return SupervisorEvidence(
        pr_number=metadata.number,
        head_sha=metadata.head_sha,
        labels=labels,
        is_draft=metadata.is_draft,
        is_fork=_metadata_is_fork(metadata),
        ignored="ai-pr-loop-ignore" in label_names,
        has_auto_merge_label="ai-auto-merge-allowed" in label_names,
        ci_status=ci_status,
        review_state=review_state,
        has_review_on_head=has_review_on_head,
        unresolved_threads=unresolved_threads,
        agent_task_status=task_status,
        agent_task_lifecycle_at=task_timestamp,
        agent_task_lifecycle_status=lifecycle_status,
        agent_task_lifecycle_reason=lifecycle_reason,
        agent_task_incomplete_reasons=lifecycle_incomplete_reasons,
        agent_task_ids=task_ids,
        agent_task_run_ids=task_run_ids,
        session_evidence=session_evidence_builder.build(lifecycle_status, lifecycle_reason),
        loop_run_status=loop_run_status,
        loop_run_conclusion=loop_run_conclusion,
        loop_run_updated_at=loop_run_updated_at,
        review_requested_at=review_requested_at,
        last_action=last_action,
        last_action_at=last_action_at,
        api_errors=tuple(errors),
    )


def _age_seconds(timestamp: datetime | None, now: datetime) -> float | None:
    if timestamp is None:
        return None
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware")
    return max(0.0, (now - timestamp.astimezone(UTC)).total_seconds())


def _validate_now(now: datetime) -> None:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")


def classify_supervisor_state(
    evidence: SupervisorEvidence,
    *,
    now: datetime,
    config: SupervisorConfig | None = None,
) -> SupervisorClassification:
    """Classify one PR from collected evidence without performing side effects."""
    _validate_now(now)
    config = config or SupervisorConfig()

    if evidence.api_errors:
        return SupervisorClassification(SupervisorState.UNKNOWN, ("required_evidence_unavailable",))

    task_status = evidence.agent_task_status.casefold()
    task_age = _age_seconds(evidence.agent_task_lifecycle_at, now)
    if evidence.agent_task_lifecycle_status in {"blocking", "blocking_with_expired_lifecycle"}:
        return SupervisorClassification(SupervisorState.ACTIVE, ("active_agent_task",))
    if task_status in _ACTIVE_TASK_STATUSES and task_age is not None and task_age > config.task_stale_seconds:
        return SupervisorClassification(SupervisorState.STUCK_CANDIDATE, ("stale_active_agent_task",))
    if task_status in _ACTIVE_TASK_STATUSES and (task_age is None or task_age <= config.task_stale_seconds):
        return SupervisorClassification(SupervisorState.ACTIVE, ("active_agent_task",))

    if (
        evidence.has_auto_merge_label is False
        and evidence.ci_status == "passing"
        and evidence.review_state == "APPROVED"
    ):
        return SupervisorClassification(SupervisorState.BLOCKED_HUMAN, ("missing_auto_merge_permission",))

    if (
        evidence.loop_run_status.casefold() == "completed"
        and evidence.loop_run_conclusion.casefold() in _FAILED_LOOP_CONCLUSIONS
    ):
        return SupervisorClassification(SupervisorState.EXTERNAL_ERROR, ("failed_loop_run",))

    reasons: list[str] = []
    loop_age = _age_seconds(evidence.loop_run_updated_at, now)
    if evidence.loop_run_status.casefold() in _ACTIVE_TASK_STATUSES and (
        loop_age is not None and loop_age >= config.loop_stale_seconds
    ):
        reasons.append("stale_loop_run")

    if (
        evidence.unresolved_threads > 0
        and evidence.last_action == "repair_dispatched"
        and (_age_seconds(evidence.last_action_at, now) or 0) >= config.loop_stale_seconds
    ):
        reasons.append("unresolved_threads_after_repair")

    if (
        task_status == "completed"
        and not evidence.has_review_on_head
        and task_age is not None
        and task_age > config.task_stale_seconds
    ):
        reasons.append("completed_task_without_review")

    review_age = _age_seconds(evidence.review_requested_at, now)
    review_waiting = (
        review_age is not None
        and review_age >= config.review_wait_seconds
        and evidence.ci_status == "passing"
        and not evidence.is_draft
        and not evidence.has_review_on_head
        and evidence.unresolved_threads == 0
        and task_status not in _ACTIVE_TASK_STATUSES
    )
    if review_waiting:
        reasons.append("review_waiting_without_evaluation")

    if reasons:
        return SupervisorClassification(SupervisorState.STUCK_CANDIDATE, tuple(reasons))

    if evidence.review_requested_at is not None and not evidence.has_review_on_head:
        return SupervisorClassification(SupervisorState.WAITING_EXPECTED, ("waiting_for_review",))

    return SupervisorClassification(SupervisorState.HEALTHY, ())


def build_supervisor_fingerprint(
    repository: str,
    pr_number: int,
    head_sha: str,
    classification: SupervisorClassification,
) -> str:
    """Build a content-stable identity for one candidate observation."""
    if not repository.strip():
        raise ValueError("repository must be a non-empty string")
    if type(pr_number) is not int or pr_number <= 0:
        raise ValueError("pr_number must be a positive integer")
    if not head_sha.strip():
        raise ValueError("head_sha must be a non-empty string")
    payload: dict[str, Any] = {
        "repository": repository.strip().lower(),
        "pr_number": pr_number,
        "head_sha": head_sha.strip().lower(),
        "state": classification.state.value,
        "reasons": list(classification.reasons),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def discover_supervisor_candidates(
    evidence: list[SupervisorEvidence],
    *,
    now: datetime,
    config: SupervisorConfig | None = None,
    repository: str = "swai-factory/agentic-devtools",
    max_candidates: int = 10,
) -> list[SupervisorCandidate]:
    """Select bounded, non-excluded PRs that need supervisor investigation."""
    if type(max_candidates) is not int or max_candidates <= 0:
        raise ValueError("max_candidates must be a positive integer")

    candidates: list[SupervisorCandidate] = []
    for item in sorted(evidence, key=lambda value: value.pr_number):
        if item.is_fork or item.ignored:
            continue
        classification = classify_supervisor_state(item, now=now, config=config)
        if classification.state not in {
            SupervisorState.STUCK_CANDIDATE,
            SupervisorState.EXTERNAL_ERROR,
            SupervisorState.UNKNOWN,
        }:
            continue
        candidates.append(
            SupervisorCandidate(
                evidence=item,
                classification=classification,
                fingerprint=build_supervisor_fingerprint(repository, item.pr_number, item.head_sha, classification),
            )
        )
        if len(candidates) >= max_candidates:
            break
    return candidates
