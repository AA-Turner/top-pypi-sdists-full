"""Pure, fail-closed contracts for the single-PR review orchestration skill.

These guards neither read providers nor dispatch tasks, persist state, request reviews,
or authorize merging. A repair plan is valid only for its supplied observation.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

_CONFIG = ConfigDict(extra="forbid", strict=True, frozen=True)
_PR_URL = re.compile(
    r"https://github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)/"
    r"([A-Za-z0-9_.-]{1,100})/pull/([1-9][0-9]*)(?:#pullrequestreview-([1-9][0-9]*))?"
)
_ACTIVE = {"reserved", "acceptance_unknown", "accepted", "delivered", "blocked"}
_RETRY_LIMITS = {"throttling": 3, "transport": 3, "repair": 2}
Nonempty = Annotated[str, Field(min_length=1, pattern=r"^[\s\S]*\S[\s\S]*$")]
Sha = Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]
Fingerprint = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
Positive = Annotated[int, Field(gt=0)]
Counter = Annotated[int, Field(ge=0)]
Strings = Annotated[tuple[Nonempty, ...], Field(strict=False)]
Completeness = Literal["complete", "incomplete", "unknown"]
Terminal = Literal["waiting", "blocked", "budget_exhausted", "closed", "merged"]
Action = Literal["repair", "reply", "resolve", "review", "issue", "label", "merge"]


def parse_pr_url(value: str) -> tuple[str, int, int | None]:
    """Return case-normalized repository, PR number, and optional review hint."""
    match = _PR_URL.fullmatch(value) if isinstance(value, str) else None
    if match is None or match[2] in {".", ".."}:
        raise ValueError("expected a canonical GitHub PR URL, optionally with a review fragment")
    return f"{match[1]}/{match[2]}".lower(), int(match[3]), int(match[4]) if match[4] else None


def _file_key(path: str) -> str:
    """Conservatively unify Windows separators/case for file reservations."""
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")
    if (
        any(part in {"", ".", ".."} or part != part.strip() or part.endswith(".") for part in parts)
        or ":" in normalized
        or any(ord(char) < 32 for char in normalized)
    ):
        raise ValueError("expected an unambiguous repository-relative file path")
    return f"file:{normalized.casefold()}"


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate fields rather than silently overwriting persisted progress."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


class Finding(BaseModel):
    """One original finding, including supporting-file and side-effect footprint."""

    model_config = _CONFIG
    review_id: Positive
    reviewer_id: Positive
    comment_id: Positive | None
    suppressed_body: Nonempty | None
    thread_id: Nonempty | None
    path: Nonempty
    side: Literal["LEFT", "RIGHT"]
    supporting_files: Strings
    side_effects: tuple[Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9:._/-]*$")], ...] = Field(strict=False)
    status: Literal["pending", "reserved", "acceptance_unknown", "accepted", "delivered", "resolved", "blocked"]
    attempt_id: Nonempty | None
    task_id: Nonempty | None
    session_id: Nonempty | None

    @model_validator(mode="after")
    def validate_finding(self) -> Self:
        if (self.comment_id is None) == (self.suppressed_body is None):
            raise ValueError("provide exactly one original comment_id or suppressed_body")
        self.resources()
        if self.status == "pending" and any((self.attempt_id, self.task_id, self.session_id)):
            raise ValueError("pending finding cannot carry a previous dispatch identity")
        if self.status in _ACTIVE and not self.attempt_id:
            raise ValueError("in-flight finding requires an attempt_id")
        if self.status in {"accepted", "delivered"} and not self.task_id:
            raise ValueError("accepted task identity is required")
        return self

    def identity(self, pr_url: str) -> str:
        """Hash original provenance, never list ordinal, task ID, or observed head.

        Suppressed text only normalizes line endings; code whitespace stays meaningful.
        A subsequently assigned synthetic thread does not change the original identity.
        """
        repo, number, _ = parse_pr_url(pr_url)
        source: object = self.comment_id
        if self.suppressed_body is not None:
            source = [
                _file_key(self.path),
                self.side,
                self.suppressed_body.replace("\r\n", "\n").replace("\r", "\n"),
            ]
        payload = [repo, number, self.reviewer_id, self.review_id, source]
        return hashlib.sha256(json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()

    def resources(self) -> frozenset[str]:
        """Return all assigned/supporting files plus declared shared side effects."""
        return frozenset(
            [_file_key(self.path), *(_file_key(path) for path in self.supporting_files)]
            + [f"effect:{effect}" for effect in self.side_effects]
        )


class Evidence(BaseModel):
    """Completeness is independent of counts and CI success; fingerprint covers both."""

    model_config = _CONFIG
    head_sha: Sha
    fingerprint: Fingerprint
    reviewed_head_sha: Sha | None
    review_id: Positive | None
    reviewer_id: Positive | None
    reviews: Completeness
    threads: Completeness
    checks: Completeness
    tasks: Completeness


class Reservation(BaseModel):
    """Exclusive attempt ownership retained until explicitly reconciled."""

    model_config = _CONFIG
    finding_id: Fingerprint
    attempt_id: Nonempty
    head_sha: Sha
    resources: Strings


class RetryCounts(BaseModel):
    """Failed attempts by class, not a shared retry counter."""

    model_config = _CONFIG
    throttling: Counter
    transport: Counter
    credential: Counter
    oauth: Counter
    repair: Counter


class RunState(BaseModel):
    """Versioned single-PR envelope; missing fields are errors, not defaults."""

    model_config = _CONFIG
    schema_version: Literal[1]
    run_id: Annotated[str, Field(pattern=r"^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$")]
    pr_url: Nonempty
    expected_reviewer_id: Positive
    authorized_actions: tuple[Action, ...] = Field(strict=False)
    started_at: Counter
    deadline_at: Counter
    next_due_at: Counter
    max_cycles: Annotated[int, Field(ge=1, le=12)]
    cycles: Counter
    max_parallel: Annotated[int, Field(ge=1, le=4)]
    status: Terminal
    evidence: Evidence
    findings: tuple[Finding, ...] = Field(strict=False)
    reservations: tuple[Reservation, ...] = Field(strict=False)
    failures: RetryCounts
    review_requested_head: Sha | None

    @field_validator("schema_version", mode="before")
    @classmethod
    def validate_version(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError("schema_version must be an integer")
        return value

    @model_validator(mode="after")
    def validate_state(self) -> Self:
        repo, number, hint = parse_pr_url(self.pr_url)
        if hint is not None or self.pr_url != f"https://github.com/{repo}/pull/{number}":
            raise ValueError("state pr_url must be canonical and have no review hint")
        if not self.started_at < self.deadline_at <= self.started_at + 3600:
            raise ValueError("deadline must be within one hour of run start")
        if not self.started_at <= self.next_due_at <= self.deadline_at:
            raise ValueError("next_due_at must be inside the run window")
        identities = {finding.identity(self.pr_url): finding for finding in self.findings}
        if len(identities) != len(self.findings):
            raise ValueError("duplicate finding identity")
        seen_dispatch_ids: dict[str, set[str]] = {"attempt_id": set(), "task_id": set(), "session_id": set()}
        for candidate in self.findings:
            for field, seen in seen_dispatch_ids.items():
                value = getattr(candidate, field)
                if value is not None and value in seen:
                    raise ValueError("duplicate dispatch identity")
                if value is not None:
                    seen.add(value)
        reserved: set[str] = set()
        occupied: set[str] = set()
        reserved_attempts: set[str] = set()
        for reservation in self.reservations:
            owner = identities.get(reservation.finding_id)
            if (
                owner is None
                or owner.status not in _ACTIVE
                or reservation.finding_id in reserved
                or reservation.attempt_id in reserved_attempts
                or reservation.attempt_id != owner.attempt_id
                or frozenset(reservation.resources) != owner.resources()
                or occupied.intersection(reservation.resources)
            ):
                raise ValueError("invalid or conflicting reservation ownership")
            reserved.add(reservation.finding_id)
            reserved_attempts.add(reservation.attempt_id)
            occupied.update(reservation.resources)
        required = {key for key, finding in identities.items() if finding.status in _ACTIVE}
        if required != reserved:
            raise ValueError("in-flight findings require matching reservations")
        return self

    @classmethod
    def from_json(cls, raw: str, *, expected_pr_url: str, expected_run_id: str) -> Self:
        """Validate persisted state and the caller's independently supplied run identity."""
        state = cls.model_validate(json.loads(raw, object_pairs_hook=_unique_json_object))
        if parse_pr_url(state.pr_url)[:2] != parse_pr_url(expected_pr_url)[:2] or state.run_id != expected_run_id:
            raise ValueError("resume identity does not match the requested run and PR")
        return state


@dataclass(frozen=True)
class RepairPlan:
    """A snapshot-scoped repair proposal, never an authorization or merge verdict."""

    status: Literal["ready", "waiting", "blocked", "budget_exhausted", "closed", "merged"]
    reason: str
    next_due_at: int
    batches: tuple[tuple[str, ...], ...] = ()
    invalidate_evidence: bool = False


def plan_repairs(state: RunState, *, observed_head: str, observed_fingerprint: str, now: int) -> RepairPlan:
    """Plan deterministic batches without provider writes or modifying the input state.

    The caller increments/persists the cycle before acting, reserves a batch atomically,
    and revalidates after any head change. A future batch is not permission to dispatch.
    """
    if not isinstance(observed_head, str) or not re.fullmatch(r"[0-9a-f]{40}", observed_head):
        raise ValueError("observed_head must be a full Git SHA")
    if not isinstance(observed_fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", observed_fingerprint):
        raise ValueError("observed_fingerprint must be a SHA-256 fingerprint")
    if type(now) is not int or now < state.started_at:
        raise ValueError("now must be integer epoch seconds at or after run start")
    due = min(now + 300, state.deadline_at)
    if state.status != "waiting":
        return RepairPlan(state.status, "run is stopped", due)
    if now >= state.deadline_at or state.cycles > state.max_cycles:
        return RepairPlan("budget_exhausted", "cycle or elapsed-time budget exhausted", due)
    if state.failures.credential or state.failures.oauth:
        return RepairPlan("blocked", "credentials or OAuth require human reauthentication", due)
    if any(getattr(state.failures, kind) >= limit for kind, limit in _RETRY_LIMITS.items()):
        return RepairPlan("budget_exhausted", "failure-class retry budget exhausted", due)
    if now < state.next_due_at:
        return RepairPlan("waiting", "five-minute tick is not due", state.next_due_at)
    evidence = state.evidence
    if evidence.head_sha != observed_head or evidence.fingerprint != observed_fingerprint:
        return RepairPlan("waiting", "refresh head-scoped evidence and decisions", due, invalidate_evidence=True)
    if any(getattr(evidence, surface) != "complete" for surface in ("reviews", "threads", "checks", "tasks")):
        return RepairPlan("waiting", "provider evidence is unknown or incomplete", due)
    if any(finding.status == "pending" for finding in state.findings) and (
        evidence.review_id is None
        or evidence.reviewer_id != state.expected_reviewer_id
        or evidence.reviewed_head_sha != observed_head
    ):
        return RepairPlan("blocked", "exact CCR reviewer, review, and head correlation is missing", due)
    if any(finding.status == "pending" for finding in state.findings) and "repair" not in state.authorized_actions:
        return RepairPlan("blocked", "explicit repair authorization is missing", due)
    if any(finding.status == "acceptance_unknown" for finding in state.findings):
        return RepairPlan("blocked", "reconcile uncertain task acceptance before retrying", due)
    if any(finding.status == "blocked" for finding in state.findings):
        return RepairPlan("blocked", "blocked findings require reconciliation", due)
    if any(reservation.head_sha != observed_head for reservation in state.reservations):
        return RepairPlan("blocked", "reconcile stale reservation ownership without releasing it", due)
    if state.review_requested_head is not None:
        return RepairPlan("waiting", "reconcile the in-flight review request", due)
    candidates = [finding for finding in state.findings if finding.status == "pending"]
    if any(
        finding.review_id != evidence.review_id or finding.reviewer_id != evidence.reviewer_id for finding in candidates
    ):
        return RepairPlan("blocked", "finding provenance does not match the current CCR review", due)
    if not candidates:
        if state.reservations:
            return RepairPlan("waiting", "active reservations require reconciliation", due)
        return RepairPlan("waiting", "no pending repairs; use the separate review-readiness gate", due)
    slots = state.max_parallel - len(state.reservations)
    if slots <= 0:
        return RepairPlan("waiting", "active reservations occupy all planning slots", due)
    occupied = {resource for reservation in state.reservations for resource in reservation.resources}
    remaining = sorted(
        (finding.identity(state.pr_url), finding.resources())
        for finding in candidates
        if not occupied.intersection(finding.resources())
    )
    batches: list[tuple[str, ...]] = []
    while remaining:
        batch: list[str] = []
        resources: set[str] = set()
        deferred: list[tuple[str, frozenset[str]]] = []
        for key, footprint in remaining:
            if len(batch) >= slots or resources.intersection(footprint):
                deferred.append((key, footprint))
            else:
                batch.append(key)
                resources.update(footprint)
        batches.append(tuple(batch))
        remaining = deferred
    if not batches:
        return RepairPlan("waiting", "pending repairs conflict with active reservations", due)
    return RepairPlan("ready", "repair batches planned; not a review or merge verdict", due, tuple(batches))
