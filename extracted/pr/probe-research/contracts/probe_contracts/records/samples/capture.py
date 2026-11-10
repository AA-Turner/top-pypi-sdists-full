"""Capture: the plan, each producer's seals and commits, and the yes/no answer to "is the capture complete?"."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field

from ...compat import StrEnum
from ..command import CommandKind
from ..records import Record
from .outcome import validate_drop_reason
from .provenance import Sha256
from .result import DEFAULT_REWARD_MAX

#: A producer's name in seals and plans: `rollout-0`, `trainer-0`, `harbor`.
PRODUCER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:\-]{0,127}$")
MAX_PRODUCERS = 256


def validate_producer(value: str) -> str:
    if not PRODUCER.match(value):
        raise ValueError(f"producer {value!r} must match {PRODUCER.pattern}")
    return value


def validate_drop_counts(value: dict[str, int]) -> dict[str, int]:
    """Drops declared as counts only, keyed by reason (`filter:<name>` for a named filter)."""
    for reason, count in value.items():
        validate_drop_reason(reason)
        if count < 0:
            raise ValueError(f"drop count for {reason!r} is negative")
    return value


Producer = Annotated[str, AfterValidator(validate_producer)]
DropCounts = Annotated[dict[str, int], AfterValidator(validate_drop_counts)]
#: A refusal's length, as a command's `reason` (`command.MAX_COMMAND_REASON_CHARS`): the ask's refusal carries it.
MAX_REFUSAL_CHARS = 1024
#: Why a producer refuses a command kind, in its framework's words (`SPIKE-W30.md`'s refusal texts).
Refusal = Annotated[str, Field(min_length=1, max_length=MAX_REFUSAL_CHARS)]


class RewindPoint(BaseModel):
    """`Rewind(step=R)` from the reopen in epoch `write_epoch`: older epochs' samples at or past R are rewound."""

    write_epoch: int = Field(ge=1)
    step: int = Field(ge=0)


class Plan(Record):
    """One row per run (Postgres `sample_plans`): what the producers promise, and the owner's terminal manifest."""

    run_id: UUID
    #: Miles `num_rollout`, SkyRL `max_training_steps`; None when unknown up front.
    expected_steps: int | None = Field(default=None, ge=0)
    producers: list[Producer] = Field(default_factory=list, max_length=MAX_PRODUCERS)
    #: The full reward `result` reads against; a task's own `reward_max` overrides it.
    reward_max: float = DEFAULT_REWARD_MAX
    #: The framework's staleness limit; a sample past it reads `is_over_limit` (its staleness is kept).
    max_staleness: int | None = Field(default=None, ge=0)
    #: The terminal manifest: without `final_step` + `is_closed` capture answers "no, completion unproven".
    final_step: int | None = Field(default=None, ge=0)
    is_closed: bool = False
    #: What each producer can be asked about its live samples, only what its framework does safely (DESIGN.md
    #: "Live"); a command it cannot do is refused at once, with why.
    capabilities: dict[Producer, list[CommandKind]] = Field(default_factory=dict)
    #: Why each producer refuses a kind it cannot do (`{producer: {kind: why}}`): the at-once refusal says this
    #: instead of the generic "not supported" line. A declared capability wins over a refusal of the same kind.
    refusals: dict[Producer, dict[CommandKind, Refusal]] = Field(default_factory=dict)
    #: Producers whose adapter saw training but recorded no batch (its hooks never ran, or every record failed):
    #: capture answers "no" and says so.
    adapter_hooks_missing: list[Producer] = Field(default_factory=list, max_length=MAX_PRODUCERS)
    #: read: written by `POST /v1/runs/{id}/reopen` with `rewind_to_step`, never by a producer.
    rewinds: list[RewindPoint] = Field(default_factory=list)
    #: read: the cap counter (distinct generator samples admitted).
    sample_count: int = 0
    updated_at: datetime | None = None


class BundleKind(StrEnum):
    LOGS = "logs"  # full logs, one gzip member per sample
    TOKENS = "tokens"  # per-token arrays, one gzip member per sample


class SealBundle(BaseModel):
    """A bundle the seal promises; capture checks its sha256 against stored artifacts."""

    kind: BundleKind
    sha256: Sha256


class Seal(Record):
    """One producer's declared counts for one step, in one write epoch (Postgres `sample_seals`)."""

    run_id: UUID
    write_epoch: int = Field(ge=1)
    step: int = Field(ge=0)
    producer: Producer
    #: Final samples sent for this step.
    sent: int = Field(ge=0)
    #: Drops that exist only as counts (Miles fully-async stale drops, SkyRL zero-variance drops).
    dropped: DropCounts = Field(default_factory=dict)
    bundles: list[SealBundle] = Field(default_factory=list)
    #: A trainer producer's commit: the optimizer step succeeded, so consumed samples read `trained`.
    is_committed: bool = False
    #: The explicit consume time a commit carries (never guessed from the latest stream timestamp).
    consumed_at: datetime | None = None
    #: read: distinct final parts from this producer stamped with this step (`uniqExact`).
    received: int | None = None
    sealed_at: datetime | None = None


class CaptureReasonCode(StrEnum):
    """Why capture says no. Slow, silent and gone stay apart (the fixture handoff's rule)."""

    IN_PROGRESS = "in_progress"  # live: complete through `complete_through_step`
    MISSING_SAMPLES = "missing_samples"  # received < sent
    UNSEALED_STEP = "unsealed_step"  # an expected step with no seal from a declared producer
    PRODUCER_OPEN = "producer_open"  # a declared producer never sealed its last step
    PRODUCER_SILENT = "producer_silent"  # its lease is past its interval
    PRODUCER_GONE = "producer_gone"  # its lease is marked gone
    NOT_COMMITTED = "not_committed"  # a step consumed, never committed (a crash mid-update)
    COMPLETION_UNPROVEN = "completion_unproven"  # no terminal manifest from the owner
    BUNDLE_MISSING = "bundle_missing"  # a sealed bundle digest matches no stored artifact
    BATCH_REFUSED = "batch_refused"  # a sample batch was refused late (cap, dead letter)
    ADAPTER_HOOKS_MISSING = "adapter_hooks_missing"  # a producer trained but recorded no batch


class CaptureReason(BaseModel):
    code: CaptureReasonCode
    #: One plain line: "step 41: 244 of 256 samples from rollout-0".
    message: str
    step: int | None = None
    producer: str | None = None
    expected: int | None = None
    received: int | None = None
    silent_seconds: int | None = None


class Capture(BaseModel):
    """Question 5: yes or no, never unknown. Read on the surviving lineage (rewound rows left out)."""

    run_id: UUID
    is_complete: bool
    #: The highest step through which every expected seal is met.
    complete_through_step: int | None = None
    final_step: int | None = None
    #: `final_step` is the run's last step with data, taken when a client ended the run (no step count was declared),
    #: so the expected steps run from its first step with data: an answer about what arrived, not a promise kept.
    is_final_step_observed: bool = False
    #: The first reasons, in step order.
    reasons: list[CaptureReason] = Field(default_factory=list)
    is_truncated: bool = False
