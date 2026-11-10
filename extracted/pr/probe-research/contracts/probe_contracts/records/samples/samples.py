"""Sample: one attempt at a task (rollout = trajectory = sample) as every surface reads it, and its group."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, FiniteFloat

from ...compat import StrEnum
from ..records import Record
from .outcome import SampleOutcome, SampleSplit, validate_drop_reason
from .provenance import Generation, Scorer, Sha256
from .result import SampleErrorReason, SampleResult
from .task import MAX_TASK_KEY_CHARS, BlobRef, InlineText, Scenario
from .turns import SampleEvent, Turn

#: A producer key is unique per attempt within a write epoch (DESIGN.md "Identity").
MAX_KEY_CHARS = 512
MAX_ERROR_MESSAGE_CHARS = 1024
MAX_LOG_TAIL_BYTES = 4 * 1024
#: Short machine names: host, worker, engine, sandbox id, environment type.
MAX_NAME_CHARS = 256
#: Turn text a row holds inline; past it the producer sends `turns_blob`.
MAX_TURN_TEXT_BYTES = 64 * 1024
#: Lifecycle events on the row; past it they go in the log bundle.
MAX_EVENTS = 256
MAX_EXTRAS_BYTES = 16 * 1024
#: Log files, and output files, one sample names (the trial's manifest lists every file).
MAX_TRIAL_FILES = 256
MAX_TRIAL_PATH_CHARS = 1024

DropReasonText = Annotated[str, AfterValidator(validate_drop_reason)]


def check_log_tail(value: str) -> str:
    if len(value.encode("utf-8")) > MAX_LOG_TAIL_BYTES:
        raise ValueError("log_tail is over 4 KiB: keep the last 4 KiB, the full log goes in the bundle")
    return value


LogTail = Annotated[str, AfterValidator(check_log_tail)]


def check_turn_text(turns: list[Turn]) -> list[Turn]:
    size = sum(len(message.content.encode("utf-8")) for turn in turns for message in turn.messages)
    if size > MAX_TURN_TEXT_BYTES:
        raise ValueError("turn text is over 64 KiB: send the turns as turns_blob")
    return turns


def check_extras(value: dict) -> dict:
    if len(json.dumps(value, default=str).encode("utf-8")) > MAX_EXTRAS_BYTES:
        raise ValueError("extras are over 16 KiB: put large arrays in the token bundle")
    return value


Turns = Annotated[list[Turn], AfterValidator(check_turn_text)]
Extras = Annotated[dict, AfterValidator(check_extras)]


class FinishReason(StrEnum):
    """Why generation stopped. `length` feeds a group's truncated fraction."""

    STOP = "stop"
    LENGTH = "length"
    ABORT = "abort"
    ERROR = "error"
    OTHER = "other"


class BundleRef(BaseModel):
    """One sample's gzip member inside a per-(step, producer) bundle in R2: a read fetches one byte range."""

    #: The bundle file's digest; the server finds its artifact by it.
    sha256: Sha256
    offset: int = Field(ge=0)
    length: int = Field(ge=0)
    #: Cut to the 1 MiB cap, keeping the tail.
    is_cut: bool = False


class TrialFile(BaseModel):
    """One captured file of a Harbor trial that a sample links as a log or an output (its bytes are the artifact)."""

    artifact_id: UUID
    #: Where it sits in the trial folder (`agent/oracle.txt`, `artifacts/app/answer.txt`).
    path: str = Field(max_length=MAX_TRIAL_PATH_CHARS)
    #: The capture's role for it (`trial_log`, `agent_log`, `verifier`, `artifact`, `output`, ...).
    role: str = Field(max_length=64)
    size_bytes: int | None = Field(default=None, ge=0)
    sha256: str | None = Field(default=None, max_length=128)
    #: What the bytes are, from the file name: text, json, image, audio, video, html, archive or other.
    kind: str | None = Field(default=None, max_length=32)


class EnvironmentLink(BaseModel):
    """The attempt's captured environment: the Harbor trial span and its files (sandbox, verifier, logs), with the
    log files and the outputs named apart."""

    span_id: UUID | None = None
    artifact_ids: list[UUID] = Field(default_factory=list)
    #: The trial's log files (trial log, exception, agent, verifier, simulated user), in reading order.
    logs: list[TrialFile] = Field(default_factory=list, max_length=MAX_TRIAL_FILES)
    #: What the trial produced (Harbor's collected `artifacts/`, a fork's `output/`).
    outputs: list[TrialFile] = Field(default_factory=list, max_length=MAX_TRIAL_FILES)


class Timing(BaseModel):
    """Where one attempt's time went, in seconds."""

    started_at: datetime | None = None
    ended_at: datetime | None = None
    queued_s: float | None = Field(default=None, ge=0)
    generation_s: float | None = Field(default=None, ge=0)
    environment_s: float | None = Field(default=None, ge=0)
    verifier_s: float | None = Field(default=None, ge=0)
    scored_at: datetime | None = None


class EngineStats(BaseModel):
    """The inference engine's view of one attempt."""

    spec_accept_rate: float | None = Field(default=None, ge=0, le=1)
    prefix_cache_hit_rate: float | None = Field(default=None, ge=0, le=1)
    non_generation_s: float | None = Field(default=None, ge=0)


class TokenStats(BaseModel):
    """Per-sample summaries of the per-token arrays, computed by the SDK when it writes them: sortable columns."""

    entropy_mean: float | None = None
    entropy_max: float | None = None
    ref_entropy_mean: float | None = None
    logprob_diff_abs_mean: float | None = None
    logprob_diff_abs_max: float | None = None
    importance_ratio_mean: float | None = None
    advantage_mean: float | None = None
    advantage_std: float | None = None
    return_mean: float | None = None


def derive_duration_s(duration_s: float | None, timing: Timing | dict | None) -> float | None:
    """The sample's duration: as sent, else its timing's end minus start (None when either is missing or the
    clock ran backwards)."""
    if duration_s is not None:
        return duration_s
    if isinstance(timing, dict):
        timing = Timing.model_validate(timing)
    if timing is None or timing.started_at is None or timing.ended_at is None:
        return None
    seconds = (timing.ended_at - timing.started_at).total_seconds()
    return seconds if seconds >= 0 else None


class Sample(Record):
    """One attempt, merged from its producers' parts by field ownership (`part.FIELD_OWNERS`).

    Fields marked "read" are derived by the server; a producer never writes them.
    """

    # Identity. `id` = uuid5(run_id, f"{write_epoch}:{key}"); every id is the server's (identity.py).
    id: UUID
    run_id: UUID
    write_epoch: int = Field(ge=1)
    key: str = Field(min_length=1, max_length=MAX_KEY_CHARS)
    #: The live attempt it came from, named when the rollout started (DESIGN.md "Live"): one attempt can end as
    #: several samples (Miles leaves), and a retry keeps its link. An attempt part's own key is its attempt key.
    attempt_key: str | None = Field(default=None, min_length=1, max_length=MAX_KEY_CHARS)
    task_id: UUID
    task_key: str = Field(min_length=1, max_length=MAX_TASK_KEY_CHARS)
    scenario: Scenario = Field(default_factory=dict)
    group_key: str | None = Field(default=None, max_length=MAX_KEY_CHARS)
    group_id: UUID | None = None
    #: A framework that splits one attempt into training rows (Miles compaction, SkyRL step-wise): row i of n.
    segment: int | None = Field(default=None, ge=0)
    segment_count: int | None = Field(default=None, ge=1)
    split: SampleSplit = SampleSplit.TRAIN

    # Steps: three coordinates, never merged (DESIGN.md "Provenance").
    #: read: the lineage step, `consumed_step` when a trainer consumed it, else `scheduled_step`.
    step: int | None = None
    scheduled_step: int | None = Field(default=None, ge=0)
    consumed_step: int | None = Field(default=None, ge=0)
    #: One sample trained over several optimizer steps (TRL's steps_per_generation x num_iterations).
    consumed_until_step: int | None = Field(default=None, ge=0)
    #: The trainer's weight version when it drained the sample.
    consumed_version: int | None = Field(default=None, ge=0)

    # Who made it and who graded it.
    generated_by: list[Generation] = Field(default_factory=list)
    scored_by: list[Scorer] = Field(default_factory=list)
    #: read: consumed_version - max / min policy version. Stored exactly, never clamped.
    staleness_min: int | None = None
    staleness_max: int | None = None
    #: read: staleness past the plan's `max_staleness`.
    is_over_limit: bool = False
    #: read: more than one decode version made the response.
    is_mixed_version: bool = False

    # What it said.
    response: InlineText | None = None
    response_blob: BlobRef | None = None
    turns: Turns = Field(default_factory=list)
    turns_blob: BlobRef | None = None
    turn_count: int | None = Field(default=None, ge=0)
    tool_call_count: int | None = Field(default=None, ge=0)
    finish_reason: FinishReason | None = None
    prompt_tokens: int | None = Field(default=None, ge=0)
    response_tokens: int | None = Field(default=None, ge=0)

    # Numbers. `reward` is the grade (Miles `raw_reward`); `normalized_reward` is after group normalization.
    #: Finite only: JSON cannot carry NaN, and a NaN grade is an error (`error_reason`), not a number.
    reward: FiniteFloat | None = None
    normalized_reward: FiniteFloat | None = None
    reward_parts: dict[str, FiniteFloat] = Field(default_factory=dict)
    #: Per-sample numbers that do not define the task: correct, format_ok, tokens_in, cost_usd.
    metrics: dict[str, FiniteFloat] = Field(default_factory=dict)

    # Result (§3.3b): read `result`; producers send the error facts.
    result: SampleResult | None = None
    error_reason: SampleErrorReason | None = None
    #: One line: type + message.
    error_message: str | None = Field(default=None, max_length=MAX_ERROR_MESSAGE_CHARS)
    log_tail: LogTail | None = None
    log: BundleRef | None = None

    # Outcome: read, from the parts present plus commits, rewinds and supersedes.
    outcome: SampleOutcome = SampleOutcome.GENERATED
    drop_reason: DropReasonText | None = None
    #: read: an older epoch rewound past this sample's lineage step (DESIGN.md "Rewind").
    is_rewound: bool = False

    # Where it ran.
    host: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    worker: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    engine: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    sandbox_id: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    environment_type: str | None = Field(default=None, max_length=MAX_NAME_CHARS)
    timing: Timing | None = None
    #: Seconds the attempt took, one value per sample (its first generator delivery, like every generator field);
    #: when not sent, a read takes `timing` (`derive_duration_s`). Quantiles are read over the merged samples.
    duration_s: FiniteFloat | None = Field(default=None, ge=0)
    engine_stats: EngineStats | None = None
    #: read: the newest attempt heartbeat and command time (the in-flight sandboxes view).
    last_heartbeat_at: datetime | None = None
    last_command_at: datetime | None = None

    # The trainer's side.
    trainer_rank: int | None = Field(default=None, ge=0)
    #: Rollout tokens did not line up with trainer tokens (Miles `alignment_failed`).
    is_misaligned: bool | None = None
    #: The same sample index met this many times in one step.
    occurrence: int | None = Field(default=None, ge=1)

    # Per-token data: inference arrays from the generator, trainer arrays from the trainer (one bundle each).
    tokens: BundleRef | None = None
    trainer_tokens: BundleRef | None = None
    token_stats: TokenStats | None = None
    events: list[SampleEvent] = Field(default_factory=list, max_length=MAX_EVENTS)

    # Links.
    environment: EnvironmentLink | None = None
    #: The span holding the trajectory (a Harbor trial's ATIF).
    trace_span_id: UUID | None = None
    extras: Extras = Field(default_factory=dict)

    # Evidence (read).
    #: The producers whose parts merged into this sample.
    producers: list[str] = Field(default_factory=list)
    #: More than one distinct content hash for one role: the first delivery is shown, the rest kept.
    has_conflict: bool = False
    received_at: datetime | None = None


class SampleGroup(Record):
    """One task's attempts at one step: group facts only. Reward mean, std and variance are read from members."""

    group_id: UUID
    run_id: UUID
    write_epoch: int = Field(ge=1)
    group_key: str = Field(min_length=1, max_length=MAX_KEY_CHARS)
    task_id: UUID | None = None
    #: Members the producer expected (n_samples_per_prompt); a group short of it is "variance unknown".
    size: int | None = Field(default=None, ge=1)
    scheduled_step: int | None = Field(default=None, ge=0)
    consumed_step: int | None = Field(default=None, ge=0)
    #: A whole group dropped (DAPO): its members read as dropped with this reason.
    drop_reason: DropReasonText | None = None
    #: read, from the members.
    reward_mean: float | None = None
    reward_std: float | None = None
    is_zero_variance: bool | None = None
