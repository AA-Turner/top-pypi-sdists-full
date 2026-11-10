"""The read routes' shapes (§5): list, get, compare, stats, tasks, curve, weights, logs, tokens and the best checkpoint."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, JsonValue

from ...compat import StrEnum
from .outcome import SampleSplit
from .samples import Sample, TrialFile
from .task import Task
from .weights import WeightVersion

#: Text in a list row is cut to this; `GET /v1/samples/{id}` returns it whole.
MAX_PREVIEW_BYTES = 4 * 1024
#: `stats --measure mean:reward_parts.<name>` and the like: the mean of one numeric field.
MEAN_OF_PREFIX = "mean:"
#: `--by scenario.<key>` and `--where scenario.<key>=<value>`.
SCENARIO_PREFIX = "scenario."


class SampleMeasure(StrEnum):
    """What `stats` and a task curve compute per row. Red samples are left out of means and counted in `errors`."""

    COUNT = "count"
    MEAN_REWARD = "mean_reward"
    MIN = "min"
    MAX = "max"
    PASS_RATE = "pass_rate"
    #: Zero-variance groups over groups with a complete reward set (DESIGN.md "Zero-variance share").
    ZERO_VARIANCE_SHARE = "zero_variance_share"
    #: Seconds a sample took (`Sample.duration_s`), over the samples that name one, red ones included.
    DURATION_P50 = "duration_p50"
    DURATION_P90 = "duration_p90"
    DURATION_MAX = "duration_max"


class SampleDimension(StrEnum):
    """What `stats --by` groups on, besides `scenario.<key>` and `step_window=<n>`."""

    STEP = "step"
    SCHEDULED_STEP = "scheduled_step"
    STEP_WINDOW = "step_window"
    CONSUMED_VERSION = "consumed_version"
    STALENESS_MIN = "staleness_min"
    STALENESS_MAX = "staleness_max"
    RESULT = "result"
    ERROR_REASON = "error_reason"
    OUTCOME = "outcome"
    SPLIT = "split"
    FINISH_REASON = "finish_reason"
    HOST = "host"
    WORKER = "worker"
    ENGINE = "engine"
    SANDBOX_ID = "sandbox_id"
    ENVIRONMENT_TYPE = "environment_type"
    TASK_ID = "task_id"
    RUN_ID = "run_id"


SUMMARY_FIELDS = (
    "id", "run_id", "write_epoch", "task_id", "task_key", "scenario", "group_key", "split", "step",
    "scheduled_step", "consumed_step", "consumed_until_step", "consumed_version", "generated_by",
    "staleness_min", "staleness_max", "is_over_limit", "reward", "normalized_reward", "reward_parts",
    "result", "error_reason", "error_message", "outcome", "drop_reason", "is_rewound", "finish_reason",
    "response_tokens", "host", "worker", "engine", "sandbox_id", "last_heartbeat_at", "response", "attempt_key",
    "duration_s",
)


class SampleOut(Sample.project(*Sample.model_fields)):
    """`GET /v1/samples/{id}`: the whole merged sample, text uncut."""


class SampleSummary(Sample.project(*SUMMARY_FIELDS, response=(str | None, None))):
    """A list row: the response cut to 4 KiB."""

    is_response_cut: bool = False


class SampleList(BaseModel):
    samples: list[SampleSummary] = Field(default_factory=list)
    #: Opaque; pass back as `cursor`. Null on the last page.
    next_cursor: str | None = None


class TaskTotals(BaseModel):
    """A task's samples on the surviving lineage, counted the default way (DESIGN.md "Which samples count")."""

    samples: int = 0
    steps: int = 0
    first_step: int | None = None
    last_step: int | None = None
    mean_reward: float | None = None
    pass_rate: float | None = None
    errors: int = 0
    #: Seconds its samples took (`Sample.duration_s`), over those that name one: which tasks take longest.
    duration_p50_s: float | None = None
    duration_p90_s: float | None = None
    duration_max_s: float | None = None


class TaskSummary(Task.project("task_id", "run_id", "task_key", "scenario", "dataset")):
    """A `GET /v1/runs/{id}/tasks` row, to pick one."""

    totals: TaskTotals = Field(default_factory=TaskTotals)


class TaskList(BaseModel):
    tasks: list[TaskSummary] = Field(default_factory=list)
    next_cursor: str | None = None


class TaskDetail(Task.project(*Task.model_fields)):
    """What the task is: key, full prompt, scenario, dataset row, label, plus its totals."""

    totals: TaskTotals = Field(default_factory=TaskTotals)


class CompareColumn(BaseModel):
    """One `--at`: a run at a step, a weight version or a checkpoint, and the task's samples there."""

    #: As asked: `RUN@step:0`, `RUN@version:41`, `RUN@checkpoint:best(eval/val)`.
    at: str
    run_id: UUID
    split: SampleSplit | None = None
    step: int | None = None
    version: int | None = None
    checkpoint_artifact_id: UUID | None = None
    samples: list[SampleSummary] = Field(default_factory=list)


class SampleCompare(BaseModel):
    """One task instance across runs, steps, versions and checkpoints. `match` widens to shared scenario keys."""

    task: TaskDetail | None = None
    #: The scenario keys a column may match on instead of the exact instance (`--match scenario.template`).
    match: list[str] = Field(default_factory=list)
    columns: list[CompareColumn] = Field(default_factory=list)


class StatsRow(BaseModel):
    #: One value per `by` dimension, by its name.
    keys: dict[str, JsonValue] = Field(default_factory=dict)
    #: One value per measure, by its name; None when no sample qualifies.
    values: dict[str, float | None] = Field(default_factory=dict)
    count: int = 0
    #: Red samples in this row, reported beside the means they are left out of.
    errors: int = 0
    #: Groups with an error or a missing member, or counted stale/aborted drops: outside the share.
    variance_unknown_groups: int | None = None


class SampleStats(BaseModel):
    run_ids: list[UUID] = Field(default_factory=list)
    by: list[str] = Field(default_factory=list)
    measures: list[str] = Field(default_factory=list)
    rows: list[StatsRow] = Field(default_factory=list)
    is_truncated: bool = False


class CurvePoint(BaseModel):
    run_id: UUID
    step: int
    count: int = 0
    errors: int = 0
    values: dict[str, float | None] = Field(default_factory=dict)


class TaskCurve(BaseModel):
    """One point per (run, step) for one task: its reward across every step."""

    task_id: UUID
    measures: list[str] = Field(default_factory=list)
    points: list[CurvePoint] = Field(default_factory=list)


class WeightVersionOut(WeightVersion.project(*WeightVersion.model_fields)):
    """A weight version as `GET /v1/runs/{id}/samples/weights` lists it."""


class WeightList(BaseModel):
    weights: list[WeightVersionOut] = Field(default_factory=list)


class LogSource(StrEnum):
    BUNDLE = "bundle"  # the sample's member of its log bundle
    TRIAL_FILES = "trial_files"  # a final Harbor attempt: its trial files, not a copy
    ROW = "row"  # no full log was sent: `log_tail` only


class SampleLog(BaseModel):
    sample_id: UUID
    source: LogSource
    text: str = ""
    #: Cut to 1 MiB at the producer, keeping the tail.
    is_cut: bool = False
    #: The trial files a TRIAL_FILES log comes from.
    artifact_ids: list[UUID] = Field(default_factory=list)
    #: The log files the sample names (`environment.logs`), in its order.
    files: list[TrialFile] = Field(default_factory=list)


class TokenArrays(BaseModel):
    """One sample's per-token arrays, as a bundle member holds them (gzip JSON) and a read returns a slice.

    Inference arrays come from the generator's bundle, trainer arrays from the trainer's: a read joins them.
    """

    token_ids: list[int] = Field(default_factory=list)
    #: Decoded by the adapter, which has the tokenizer.
    token_text: list[str] = Field(default_factory=list)
    inference_logprobs: list[float | None] = Field(default_factory=list)
    trainer_logprobs: list[float | None] = Field(default_factory=list)
    ref_logprobs: list[float | None] = Field(default_factory=list)
    entropy: list[float | None] = Field(default_factory=list)
    ref_entropy: list[float | None] = Field(default_factory=list)
    advantages: list[float | None] = Field(default_factory=list)
    returns: list[float | None] = Field(default_factory=list)
    loss_mask: list[int] = Field(default_factory=list)
    #: Optional, for distillation: the top-k ids and logprobs at each position.
    top_k_ids: list[list[int]] = Field(default_factory=list)
    top_k_logprobs: list[list[float]] = Field(default_factory=list)


class SampleTokens(TokenArrays):
    """`GET /v1/samples/{id}/tokens?start=&end=`: a slice, plus what the read derives."""

    sample_id: UUID
    start: int = 0
    end: int = 0
    total: int = 0
    #: read: trainer - inference logprob, per token.
    logprob_diff: list[float | None] = Field(default_factory=list)
    #: read: exp(trainer - inference logprob), per token.
    importance_ratio: list[float | None] = Field(default_factory=list)


class MetricMode(StrEnum):
    MAX = "max"
    MIN = "min"


class LineageInput(BaseModel):
    """A base model or data file the run declared (`use_checkpoint`, `use_dataset`)."""

    name: str | None = None
    uri: str | None = None
    sha256: str | None = None
    artifact_id: UUID | None = None


class CheckpointLineage(BaseModel):
    base_models: list[LineageInput] = Field(default_factory=list)
    datasets: list[LineageInput] = Field(default_factory=list)
    config: dict = Field(default_factory=dict)
    commit: str | None = None
    is_dirty: bool | None = None
    parent_run_id: UUID | None = None
    #: `derived_from` edges, those the samples wrote (a teacher, an RFT sampling run) included.
    derived_from: list[UUID] = Field(default_factory=list)


class BestCheckpoint(BaseModel):
    """`GET /v1/runs/{id}/checkpoints/best`: the checkpoint whose step's value of a NAMED metric is best."""

    run_id: UUID
    metric: str
    mode: MetricMode = MetricMode.MAX
    step: int
    value: float
    checkpoint_artifact_id: UUID
    name: str
    uri: str | None = None
    lineage: CheckpointLineage = Field(default_factory=CheckpointLineage)
