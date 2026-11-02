"""Typed specialist profiles and controller-owned dispatch planning."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from agentic_devtools.cli.ci.reconciliation.loop_control import LoopController
from agentic_devtools.cli.ci.reconciliation.models import PermitRequest, QueueState


class SpecialistRole(StrEnum):
    """Supported bounded repair roles."""

    CODE_REPAIR = "code_repair"
    TEST_REPAIR = "test_repair"
    DOC_REPAIR = "doc_repair"
    THREAD_ADJUDICATOR = "thread_adjudicator"
    REVIEW_READINESS = "review_readiness"


@dataclass(frozen=True)
class SpecialistProfile:
    """A role with an explicit model and declared file/test footprint."""

    role: SpecialistRole
    model: str = "gpt-5.6-luna"
    file_footprint: tuple[str, ...] = ()
    test_footprint: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.model not in {"gpt-5.6-luna", "gpt-6-astra"}:
            raise ValueError("specialist model must be gpt-5.6-luna or gpt-6-astra")
        if not isinstance(self.role, SpecialistRole):
            raise TypeError("role must be a SpecialistRole")
        if any(not isinstance(path, str) or not path.strip() for path in (*self.file_footprint, *self.test_footprint)):
            raise ValueError("specialist footprints must contain non-empty paths")
        if len(set(self.file_footprint)) != len(self.file_footprint) or len(set(self.test_footprint)) != len(
            self.test_footprint
        ):
            raise ValueError("specialist footprints must be unique")

    @property
    def is_recovery(self) -> bool:
        """Whether this profile uses the explicit Astra recovery model."""
        return self.model == "gpt-6-astra"


@dataclass(frozen=True)
class SpecialistTask:
    """A durable admission request plus the specialist's declared footprint."""

    profile: SpecialistProfile
    request: PermitRequest


DEFAULT_SPECIALIST_PROFILES: dict[SpecialistRole, SpecialistProfile] = {
    role: SpecialistProfile(role) for role in SpecialistRole
}


def recovery_profile(
    role: SpecialistRole,
    *,
    file_footprint: Iterable[str] = (),
    test_footprint: Iterable[str] = (),
) -> SpecialistProfile:
    """Create an Astra profile for bounded recovery only."""
    return SpecialistProfile(role, "gpt-6-astra", tuple(file_footprint), tuple(test_footprint))


def dispatch_specialist(
    controller: LoopController,
    state: QueueState,
    *,
    profile: SpecialistProfile,
    request_id: str,
    pr_number: int,
    obligation_id: str,
    batch_id: str,
    worker_id: str,
    provider: str = "github",
    deadline_at: datetime | None = None,
    parent_request_id: str | None = None,
) -> tuple[QueueState, SpecialistTask]:
    """Queue a specialist through the controller, never dispatching directly."""
    if not isinstance(profile, SpecialistProfile):
        raise TypeError("profile is required")
    updated, request = controller.request_worker_admission(
        state,
        request_id=request_id,
        pr_number=pr_number,
        obligation_id=obligation_id,
        batch_id=batch_id,
        worker_id=worker_id,
        provider=provider,
        model=profile.model,
        deadline_at=deadline_at,
        parent_request_id=parent_request_id,
    )
    return updated, SpecialistTask(profile, request)


def route_specialist(role: SpecialistRole, *, recovery: bool = False, **footprints: Iterable[str]) -> SpecialistProfile:
    """Return the canonical Luna profile or explicit Astra recovery profile."""
    if not isinstance(role, SpecialistRole):
        raise TypeError("role must be a SpecialistRole")
    args = {
        "file_footprint": tuple(footprints.get("file_footprint", ())),
        "test_footprint": tuple(footprints.get("test_footprint", ())),
    }
    if recovery:
        return recovery_profile(role, **args)
    return SpecialistProfile(role, model="gpt-5.6-luna", **args)
