"""Live samples: the rows of `GET /v1/runs/{id}/samples/live`, each one running attempt and its state, read from the
attempt parts at query time (rl-next W31/W32, DESIGN.md "Live"). The UI, routes and CLI say "sample"."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ....compat import StrEnum
from ...command import CommandKind
from ..result import SampleErrorReason
from ..samples import MAX_KEY_CHARS, MAX_NAME_CHARS
from ..task import MAX_TASK_KEY_CHARS, Scenario
from .attempt import MAX_ACTIVITY_CHARS, AttemptOutcome, AttemptPhase

#: No progress for this long, with its producer still live, reads `hung` (`?hung_after=`).
HUNG_AFTER_SECONDS = 600
#: The failing block's window (`?window=`).
FAILING_WINDOW_SECONDS = 600
#: The live read scans attempt parts received in the last day (or the run's life, if shorter).
LIVE_SCAN_SECONDS = 24 * 3600
#: Slow = elapsed above the task's p90 AND this many times the step's median finished duration.
SLOW_STEP_MEDIAN_FACTOR = 2.0
#: Below this many finished attempts at the task, the step's p90 stands in for the task's.
SLOW_MIN_TASK_ATTEMPTS = 3


class AttemptState(StrEnum):
    """Read at query time from the parts, the producer's lease and the run's epochs; never stored."""

    RUNNING = "running"
    HUNG = "hung"  # its producer is live, or silent, and it made no progress for `hung_after` (`reason`)
    ENDED = "ended"  # an end part arrived (its sample may still wait on the step's bundles)
    ABANDONED = "abandoned"  # no end will come: its epoch was superseded, its producer let go or died, or the run ended
    SUPERSEDED = "superseded"  # a retry replaced it


class AttemptStateReason(StrEnum):
    """Why an attempt reads hung, abandoned or superseded."""

    NO_PROGRESS = "no_progress"  # hung: its producer beats, the attempt made no progress
    PRODUCER_SILENT = "producer_silent"  # hung: its producer's lease is past its interval
    EPOCH_SUPERSEDED = "epoch_superseded"  # abandoned: a resume started a newer write epoch
    PRODUCER_RELEASED = "producer_released"  # abandoned: its producer let go of the run with no end
    PRODUCER_GONE = "producer_gone"  # abandoned: its producer's lease went gone with no end
    RUN_ENDED = "run_ended"  # abandoned: the run ended (completed, failed, crashed, canceled, untracked) with no end
    RETRIED = "retried"  # superseded: a retry names it


class SlowAgainst(StrEnum):
    """What a slow attempt's elapsed time was compared with."""

    TASK = "task"  # the p90 of finished attempts at the same task in this run
    STEP = "step"  # the step's p90 (fewer than `SLOW_MIN_TASK_ATTEMPTS` finished at the task)


class LiveSample(BaseModel):
    """One attempt as the live read sees it. Elapsed, idle and hung run on the server's receipt time of each part;
    the producer's own times are shown, never judged, so a GPU box with a wrong clock changes nothing."""

    #: The attempt's own row: `derive_attempt_id(run_id, write_epoch, attempt_key)`; the `{attempt}` of its routes.
    attempt_id: UUID
    run_id: UUID
    write_epoch: int = Field(ge=1)
    attempt_key: str = Field(min_length=1, max_length=MAX_KEY_CHARS)
    producer: str
    task_id: UUID | None = None
    task_key: str | None = Field(default=None, max_length=MAX_TASK_KEY_CHARS)
    scenario: Scenario = Field(default_factory=dict)
    group_key: str | None = Field(default=None, max_length=MAX_KEY_CHARS)
    scheduled_step: int | None = None
    weight_version: int | None = None
    try_number: int = Field(default=1, ge=1)
    retry_of: str | None = Field(default=None, max_length=MAX_KEY_CHARS)
    host: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    worker: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    engine: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    sandbox_id: str | None = Field(default=None, max_length=MAX_NAME_CHARS)

    state: AttemptState
    reason: AttemptStateReason | None = None

    # The server's clock: receipt times of its start (else its first part), its newest progress, its end.
    started_at: datetime | None = None
    progress_at: datetime | None = None
    ended_at: datetime | None = None
    #: To now (or to its end).
    elapsed_s: float | None = Field(default=None, ge=0)
    #: Since its last progress (else its start).
    idle_s: float | None = Field(default=None, ge=0)

    # The producer's clock, shown only.
    producer_started_at: datetime | None = None
    producer_ended_at: datetime | None = None
    last_progress_at: datetime | None = None

    # The newest progress snapshot.
    phase: AttemptPhase | None = None
    turns: int | None = None
    tokens: int | None = None
    activity: str | None = Field(default=None, max_length=MAX_ACTIVITY_CHARS)

    # The end.
    outcome: AttemptOutcome | None = None
    error_reason: SampleErrorReason | None = None

    is_slow: bool = False
    #: elapsed / the p90 it was compared with.
    slow_by: float | None = None
    slow_against: SlowAgainst | None = None
    #: The p90 duration (seconds) it was compared with.
    slow_baseline_s: float | None = None

    #: The samples it ended as (one attempt can end as several: Miles leaves).
    sample_ids: list[UUID] = Field(default_factory=list)
    #: What its producer can be asked (`Plan.capabilities`).
    capabilities: list[CommandKind] = Field(default_factory=list)
    is_watched: bool = False


class LiveCounts(BaseModel):
    """Attempts in the scan, by state; `slow` counts running ones that are slow."""

    running: int = 0
    slow: int = 0
    hung: int = 0
    abandoned: int = 0
    superseded: int = 0
    ended: int = 0


class FailingGroup(BaseModel):
    """Errors in the window for one error reason, host or task."""

    #: The error reason, the host, or the task key.
    value: str
    task_id: UUID | None = None
    errors: int = 0
    #: Attempts of this group that ended in the window.
    ended: int = 0


class LiveFailing(BaseModel):
    """What is failing right now: attempts that ended `error` in the window, against the run's rate before it."""

    window_s: int = FAILING_WINDOW_SECONDS
    ended: int = 0
    errors: int = 0
    error_rate: float | None = None
    #: The run's error rate before the window (in the scan), for contrast.
    error_rate_before: float | None = None
    by_reason: list[FailingGroup] = Field(default_factory=list)
    by_host: list[FailingGroup] = Field(default_factory=list)
    by_task: list[FailingGroup] = Field(default_factory=list)


class LiveSampleList(BaseModel):
    """`GET /v1/runs/{id}/samples/live`: which samples run now, which are slow, hung or abandoned, what is failing."""

    run_id: UUID
    #: The server time the states were read at.
    as_of: datetime
    hung_after_s: int = HUNG_AFTER_SECONDS
    counts: LiveCounts = Field(default_factory=LiveCounts)
    #: Oldest start first.
    samples: list[LiveSample] = Field(default_factory=list)
    failing: LiveFailing = Field(default_factory=LiveFailing)
    is_truncated: bool = False
