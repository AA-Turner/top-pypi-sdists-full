"""The `data` of the `samples.*` notices (rl-next W54). A notice says what changed and where; the sample routes hold
the rest (`GET /v1/runs/{id}/samples/live`, `.../capture`, `.../weights`, `probe checkpoint best`)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..compat import StrEnum

#: Free text a notice carries at most (a reason's message, an activity), in characters.
MAX_NOTICE_TEXT = 300
#: A turn notice's content at most, in UTF-8 bytes: the turn cut to fit the 4 KiB notice (`is_cut`); the whole turn
#: is on `GET .../samples/live/{attempt}/turns`.
MAX_TURN_CONTENT_BYTES = 3 * 1024


class LiveSampleChange(StrEnum):
    """What a `samples.live` notice says happened to one sample. `started` and `ended` come with the write; the
    rest from the 30 s detector, once per change (a sample hung for an hour is one `hung`)."""

    STARTED = "started"
    ENDED = "ended"  # an end arrived: `outcome` says how
    SLOW = "slow"  # running, past its task's p90 of finished samples (`slow_by`)
    HUNG = "hung"  # no progress for 10 min, or its producer went silent (`reason`)
    ABANDONED = "abandoned"  # no end will come: a resume, or its producer let go or died (`reason`)
    RESUMED = "resumed"  # was slow or hung, now running normally again


class StepSealedData(BaseModel):
    """`samples.step_sealed`: a producer sealed a step (or changed its seal)."""

    step: int
    producer: str
    write_epoch: int = Field(ge=1)
    #: The final samples the producer says it sent for the step.
    samples: int = Field(ge=0)
    #: Samples it dropped and counted only by reason (summed over reasons).
    dropped: int = Field(ge=0)


class CaptureData(BaseModel):
    """`samples.capture`: the run's capture answer changed (yes or no, and the first reason's code)."""

    is_complete: bool
    #: The first reason's `CaptureReasonCode` (`in_progress`, `unsealed_step`, ...); None when complete.
    reason: str | None = None
    message: str | None = Field(default=None, max_length=MAX_NOTICE_TEXT)


class LiveSampleData(BaseModel):
    """`samples.live`: one sample started, ended, went slow, hung or abandoned, or resumed. `refs.sample` is the
    attempt id the live routes take."""

    attempt_key: str
    state: LiveSampleChange
    task_key: str | None = None
    #: `ended`: the attempt's `AttemptOutcome` (passed, failed, error, dropped, aborted, canceled, ungraded).
    outcome: str | None = None
    #: `hung` / `abandoned`: the `AttemptStateReason`; `ended`: the error reason, if any.
    reason: str | None = None
    #: Server time since its start, when known.
    elapsed_s: float | None = Field(default=None, ge=0)
    #: `slow`: elapsed over the p90 it was compared with.
    slow_by: float | None = None
    host: str | None = None


class FailingData(BaseModel):
    """`samples.failing`: samples ending in this error passed the threshold in the window (once per crossing)."""

    reason: str
    #: The host with most of them.
    host: str | None = None
    count: int = Field(ge=0)
    window_s: int = Field(ge=1)


class TurnData(BaseModel):
    """`samples.turn`: one turn of a watched sample, credential-scrubbed and cut to fit (`is_cut`)."""

    attempt_key: str
    seq: int = Field(ge=0)
    role: str
    content: str = ""
    tool_name: str | None = None
    is_cut: bool = False


class WeightsData(BaseModel):
    """`samples.weights`: the trainer pushed a new weight version."""

    version: int
    #: The optimizer step it came after, when sent.
    step: int | None = None
    policy_id: str = "policy"
    write_epoch: int = Field(ge=1)


class CheckpointBestData(BaseModel):
    """`samples.checkpoint_best`: a checkpoint save that landed is now the run's best for the metric it names."""

    metric: str
    #: `max` or `min` when the save said; None when the job's own pick decided (`meta.best`).
    mode: str | None = None
    step: int
    value: float | None = None
    name: str
