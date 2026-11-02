"""Bounded, single-finding dispatch contracts and host adapter.

The Pydantic handoff and value objects are pure validation.  Provider writes are
performed only through ``SingleFindingDispatchHost`` by
``SingleFindingDispatchAdapter``.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.review_orchestration import (
    Action,
    Finding,
    Reservation,
    RetryCounts,
    parse_pr_url,
)
from agentic_devtools.cli.github.single_finding_dispatch_port import SingleFindingDispatchHost

BRANCH_WRITE_RESOURCE = "effect:branch-write"

_CONFIG = ConfigDict(extra="forbid", strict=True, frozen=True)
_SHA_PATTERN = r"^[0-9a-f]{40}$"
_FINDING_ID_PATTERN = r"^[0-9a-f]{64}$"
_RUN_ID_PATTERN = r"^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$"
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_ACCEPTANCE_OUTCOMES = frozenset(
    {"accepted", "already_active", "already_resolved", "head_changed", "unknown", "blocked"}
)
_FAILURE_BUDGET_LIMITS = {
    "throttling": 3,
    "transport": 3,
    "credential": 1,
    "oauth": 1,
    "repair": 2,
}
_DISPATCH_OUTCOMES = frozenset(
    {
        "accepted",
        "acceptance_unknown",
        "already_active",
        "already_resolved",
        "head_changed",
        "blocked",
        "budget_exhausted",
    }
)


class SingleFindingHandoff(BaseModel):
    """One selected finding reserved for a bounded repair task."""

    model_config = _CONFIG

    run_id: str = Field(pattern=_RUN_ID_PATTERN)
    pr_url: str = Field(min_length=1)
    base_ref: str = Field(min_length=1)
    head_ref: str = Field(min_length=1)
    expected_head: str = Field(pattern=_SHA_PATTERN)
    finding_id: str = Field(pattern=_FINDING_ID_PATTERN)
    payload_digest: str = Field(pattern=_FINDING_ID_PATTERN)
    attempt_id: str = Field(min_length=1, pattern=_IDENTIFIER_PATTERN)
    deadline_at: int = Field(gt=0)
    reservation: Reservation
    finding: Finding
    authorized_actions: tuple[Action, ...] = Field(strict=False)
    remaining_failure_budgets: RetryCounts

    @model_validator(mode="after")
    def validate_handoff(self) -> SingleFindingHandoff:
        repo, number, review_hint = parse_pr_url(self.pr_url)
        if review_hint is not None or self.pr_url != f"https://github.com/{repo}/pull/{number}":
            raise ValueError("pr_url must be canonical and must not include a review hint")
        if self.reservation.finding_id != self.finding_id:
            raise ValueError("reservation finding_id must match the selected finding")
        if self.reservation.attempt_id != self.attempt_id:
            raise ValueError("reservation attempt_id must match the selected attempt")
        if self.reservation.head_sha != self.expected_head:
            raise ValueError("reservation head_sha must match expected_head")
        if BRANCH_WRITE_RESOURCE not in self.reservation.resources:
            raise ValueError("reservation must include effect:branch-write")
        if self.finding.identity(self.pr_url) != self.finding_id:
            raise ValueError("finding provenance must match finding_id")
        if self.finding.status != "reserved":
            raise ValueError("finding must be reserved for dispatch")
        if self.finding.thread_id is None:
            raise ValueError("reserved finding must have an assigned thread")
        if self.finding.task_id is not None or self.finding.session_id is not None:
            raise ValueError("reserved finding cannot already have task or session identity")
        if self.finding.attempt_id != self.attempt_id:
            raise ValueError("finding attempt_id must match the selected attempt")
        if self.finding.resources() != frozenset(self.reservation.resources):
            raise ValueError("reservation resources must match finding provenance")
        if "repair" not in self.authorized_actions:
            raise ValueError("repair action must be explicitly authorized")
        for field_name, limit in _FAILURE_BUDGET_LIMITS.items():
            budget = getattr(self.remaining_failure_budgets, field_name)
            if not 0 < budget <= limit:
                raise ValueError(f"remaining {field_name} failure budget must be between 1 and {limit}")
        return self


def _validate_identifier(field_name: str, value: object) -> str:
    if not isinstance(value, str) or not _IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(f"{field_name} must be a non-empty safe identifier")
    return value


def finding_payload_digest(finding_id: str, payload: AgentTasksPayload) -> str:
    """Return the canonical digest binding a finding to its dispatch payload."""
    if not isinstance(finding_id, str) or not re.fullmatch(_FINDING_ID_PATTERN, finding_id):
        raise ValueError("finding_id must be a stable finding fingerprint")
    if not isinstance(payload, AgentTasksPayload):
        raise TypeError("payload must be an AgentTasksPayload")
    canonical = json.dumps(
        [finding_id, payload.to_dict()],
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


@dataclass(frozen=True, slots=True)
class AcceptedTaskIdentity:
    """The task identity accepted by the provider and observed by the host."""

    task_id: str
    session_id: str | None

    def __post_init__(self) -> None:
        _validate_identifier("task_id", self.task_id)
        if self.session_id is not None:
            _validate_identifier("session_id", self.session_id)


@dataclass(frozen=True, slots=True)
class TaskAcceptance:
    """The host's compare-and-swap task-creation observation."""

    outcome: Literal["accepted", "already_active", "already_resolved", "head_changed", "unknown", "blocked"]
    identity: AcceptedTaskIdentity | None
    reason: str

    def __post_init__(self) -> None:
        if self.outcome not in _ACCEPTANCE_OUTCOMES:
            raise ValueError("outcome must be accepted, already_resolved, head_changed, unknown, or blocked")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")
        if self.identity is not None and not isinstance(self.identity, AcceptedTaskIdentity):
            raise ValueError("identity must be an AcceptedTaskIdentity when provided")
        if self.outcome == "accepted" and self.identity is None:
            raise ValueError("accepted task outcome requires task identity")
        if (
            self.outcome in {"already_active", "already_resolved", "head_changed", "blocked"}
            and self.identity is not None
        ):
            raise ValueError(f"{self.outcome} outcome cannot carry task identity")


@dataclass(frozen=True, slots=True)
class SingleFindingDispatchResult:
    """The bounded result returned to the coordinator for one finding."""

    outcome: Literal[
        "accepted",
        "acceptance_unknown",
        "already_active",
        "already_resolved",
        "head_changed",
        "blocked",
        "budget_exhausted",
    ]
    reason: str
    expected_head: str
    finding_id: str
    attempt_id: str
    task_id: str | None
    session_id: str | None

    def __post_init__(self) -> None:
        if self.outcome not in _DISPATCH_OUTCOMES:
            raise ValueError("outcome is not a valid single-finding dispatch result")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string")
        if not isinstance(self.expected_head, str) or not re.fullmatch(_SHA_PATTERN, self.expected_head):
            raise ValueError("expected_head must be a full lowercase Git SHA")
        if not isinstance(self.finding_id, str) or not re.fullmatch(_FINDING_ID_PATTERN, self.finding_id):
            raise ValueError("finding_id must be a stable finding fingerprint")
        _validate_identifier("attempt_id", self.attempt_id)
        if self.task_id is not None:
            _validate_identifier("task_id", self.task_id)
        if self.session_id is not None:
            _validate_identifier("session_id", self.session_id)
        if self.session_id is not None and self.task_id is None:
            raise ValueError("session_id requires task_id")
        if self.outcome == "accepted" and self.task_id is None:
            raise ValueError("accepted outcome requires task_id")
        if self.outcome in {"already_active", "already_resolved", "head_changed", "blocked", "budget_exhausted"} and (
            self.task_id is not None or self.session_id is not None
        ):
            raise ValueError(f"{self.outcome} outcome cannot carry task identity")


class AmbiguousTaskCreationError(RuntimeError):
    """A task-create request may have been delivered, but its result is unknown."""

    def __init__(self, reason: str, identity: AcceptedTaskIdentity | None = None) -> None:
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("reason must be a non-empty string")
        if identity is not None and not isinstance(identity, AcceptedTaskIdentity):
            raise TypeError("identity must be an AcceptedTaskIdentity when provided")
        super().__init__(reason)
        self.reason = reason
        self.identity = identity


class AcceptancePersistenceError(RuntimeError):
    """A task acceptance was observed but its durable record could not be written."""

    def __init__(self, reason: str) -> None:
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("reason must be a non-empty string")
        super().__init__(reason)
        self.reason = reason


class SingleFindingDispatchAdapter:
    """Execute one selected-finding handoff through a bounded host port."""

    def __init__(self, host: SingleFindingDispatchHost, *, clock: Callable[[], int]) -> None:
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._host = host
        self._clock = clock

    def dispatch(
        self,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
    ) -> SingleFindingDispatchResult:
        """Reserve, compare the expected head, create, and persist one task."""
        if not isinstance(handoff, SingleFindingHandoff):
            raise TypeError("handoff must be a SingleFindingHandoff")
        if not isinstance(payload, AgentTasksPayload):
            raise TypeError("payload must be an AgentTasksPayload")
        if payload.base_ref != handoff.base_ref or payload.head_ref != handoff.head_ref:
            raise ValueError("payload refs must match the validated handoff refs")
        if finding_payload_digest(handoff.finding_id, payload) != handoff.payload_digest:
            raise ValueError("payload digest must match the selected finding and handoff payload")

        timeout_seconds = self._remaining_seconds(handoff)
        if timeout_seconds <= 0:
            return self._result(handoff, "budget_exhausted", "finite dispatch deadline has expired")
        try:
            reserved = self._host.reserve_branch_write(handoff, timeout_seconds)
        except OSError as error:
            return self._result(
                handoff,
                "blocked",
                f"branch-write reservation could not be acquired: {error}",
            )
        if type(reserved) is not bool:
            self._host.release_branch_write(handoff)
            raise TypeError("reserve_branch_write must return a boolean")
        if not reserved:
            return self._result(handoff, "blocked", "branch-write reservation is already owned")

        timeout_seconds = self._remaining_seconds(handoff, release_on_error=True)
        if timeout_seconds <= 0:
            self._host.release_branch_write(handoff)
            return self._result(handoff, "budget_exhausted", "finite dispatch deadline expired while reserved")

        try:
            acceptance = self._host.create_task_if_head(handoff, payload, timeout_seconds)
        except AmbiguousTaskCreationError as error:
            acceptance = TaskAcceptance("unknown", error.identity, error.reason)
        if not isinstance(acceptance, TaskAcceptance):
            self._host.release_branch_write(handoff)
            raise TypeError("create_task_if_head must return TaskAcceptance")
        if acceptance.outcome in ("already_active", "already_resolved", "head_changed", "blocked"):
            return self._result(handoff, acceptance.outcome, acceptance.reason)
        if acceptance.outcome == "unknown":
            timeout_seconds = self._remaining_seconds(handoff, release_on_error=True)
            if timeout_seconds <= 0:
                self._host.release_branch_write(handoff)
                return self._result(
                    handoff,
                    "acceptance_unknown",
                    "unknown task acceptance could not be persisted before deadline",
                    acceptance.identity,
                )
            try:
                persisted = self._host.persist_acceptance(handoff, acceptance, timeout_seconds)
            except AcceptancePersistenceError as error:
                return self._result(handoff, "acceptance_unknown", error.reason, acceptance.identity)
            if type(persisted) is not bool:
                raise TypeError("persist_acceptance must return a boolean")
            return self._result(
                handoff,
                "acceptance_unknown",
                acceptance.reason if persisted else "unknown task acceptance could not be persisted",
                acceptance.identity,
            )
        if acceptance.identity is None:  # pragma: no cover - TaskAcceptance validates this
            raise ValueError("accepted task outcome has no identity")
        timeout_seconds = self._remaining_seconds(handoff, release_on_error=True)
        if timeout_seconds <= 0:
            self._host.release_branch_write(handoff)
            return self._result(
                handoff,
                "acceptance_unknown",
                "accepted task identity could not be persisted before deadline",
                acceptance.identity,
            )
        try:
            persisted = self._host.persist_acceptance(handoff, acceptance, timeout_seconds)
        except AcceptancePersistenceError as error:
            return self._result(handoff, "acceptance_unknown", error.reason, acceptance.identity)
        if type(persisted) is not bool:
            raise TypeError("persist_acceptance must return a boolean")
        if not persisted:
            return self._result(
                handoff,
                "acceptance_unknown",
                "accepted task identity could not be persisted",
                acceptance.identity,
            )
        return self._result(
            handoff,
            "accepted",
            "accepted task identity persisted",
            acceptance.identity,
        )

    def _ensure_clock_value(self) -> int:
        value = self._clock()
        if type(value) is not int:
            raise ValueError("clock must return an integer epoch timestamp")
        return value

    def _remaining_seconds(self, handoff: SingleFindingHandoff, *, release_on_error: bool = False) -> int:
        try:
            return handoff.deadline_at - self._ensure_clock_value()
        except ValueError:
            if release_on_error:
                self._host.release_branch_write(handoff)
            raise

    @staticmethod
    def _result(
        handoff: SingleFindingHandoff,
        outcome: Literal[
            "accepted",
            "acceptance_unknown",
            "already_active",
            "already_resolved",
            "head_changed",
            "blocked",
            "budget_exhausted",
        ],
        reason: str,
        identity: AcceptedTaskIdentity | None = None,
    ) -> SingleFindingDispatchResult:
        return SingleFindingDispatchResult(
            outcome=outcome,
            reason=reason,
            expected_head=handoff.expected_head,
            finding_id=handoff.finding_id,
            attempt_id=handoff.attempt_id,
            task_id=identity.task_id if identity is not None else None,
            session_id=identity.session_id if identity is not None else None,
        )


__all__ = [
    "BRANCH_WRITE_RESOURCE",
    "AcceptedTaskIdentity",
    "AcceptancePersistenceError",
    "AmbiguousTaskCreationError",
    "SingleFindingDispatchAdapter",
    "SingleFindingDispatchHost",
    "SingleFindingDispatchResult",
    "SingleFindingHandoff",
    "finding_payload_digest",
    "TaskAcceptance",
]
