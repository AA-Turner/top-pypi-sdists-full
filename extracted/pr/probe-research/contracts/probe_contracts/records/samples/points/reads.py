"""The per-sample metrics' reads: the keys a run logged per sample, one key's series (per step, update or the whole
run, from stored sums), one sample's points with its loss bookkeeping, and the capture check. Empty is None, never 0."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from ....compat import StrEnum
from ..outcome import SampleSplit
from .points import LOSS_TOLERANCE, ContributionSource, LossRole, MetricAgg
from .training import Rollup, TrainingPlan


class PointBy(StrEnum):
    """What one series row covers."""

    STEP = "step"
    UPDATE = "update"  # one optimizer update of one step
    RUN = "run"  # the whole surviving run


class PointKeyOut(BaseModel):
    """One key a run logged per sample, in one split."""

    name: str
    split: SampleSplit
    #: The first `agg` declared for the key on this run; None: none (a series reads the weighted mean).
    agg: MetricAgg | None = None
    #: Stored rows (deliveries included); a sizing hint, not a count of samples.
    rows: int = 0
    first_step: int | None = None
    last_step: int | None = None


class PointKeyList(BaseModel):
    """`GET /v1/runs/{id}/samples/points/keys`. `is_recorded` false: the run has no per-sample metrics (a run from
    before this shipped reads so; nothing is rebuilt for it)."""

    run_id: UUID
    is_recorded: bool
    keys: list[PointKeyOut] = Field(default_factory=list)


class PointSeriesRow(BaseModel):
    """One step (or update, or the whole run) of a key: its `agg` with the sufficient statistics, so steps, ranks and
    runs combine exactly (never an average of averages)."""

    step: int | None = None
    #: by=update: the optimizer update (train) or the eval pass (eval) of the step.
    update: int | None = None
    value: float | None = None
    #: sum(value x weight) and sum(weight) over the population; None when it is empty.
    sum: float | None = None
    weight: float | None = None
    #: Sample occurrences in the population (a sample's fragments are one).
    count: int = 0
    min: float | None = None
    max: float | None = None
    #: The step's commit (it trained). None for a row no commit applies to (eval, by=run).
    is_committed: bool | None = None


class PointSeries(BaseModel):
    """`GET /v1/runs/{id}/samples/points?key=&split=&by=`. A key whose producer declared how its framework reduces it
    (`rollup`) reads each row's value that way; any other key reads `agg` (the weighted mean by default)."""

    run_id: UUID
    key: str
    split: SampleSplit
    by: PointBy
    agg: MetricAgg
    rollup: Rollup | None = None
    #: Who is counted, in words: the samples that logged the key in that step and split; one that did not is absent.
    population: str
    is_recorded: bool
    rows: list[PointSeriesRow] = Field(default_factory=list)
    #: Points delivered twice with different values: reported, the first delivery used.
    conflicts: int = 0
    is_truncated: bool = False


class SamplePoint(BaseModel):
    """One stored point of one sample (its first delivery)."""

    name: str
    value: float
    weight: float
    step: int
    update: int | None = None
    split: SampleSplit
    role: LossRole = LossRole.ACTOR
    rank: int = 0
    micro_batch: int | None = None
    occurrence: int = 0
    fragment: int = 0
    producer: str


class MaskEvidence(StrEnum):
    """The row's mask digest against the trainer bundle's loss mask (`hash_mask`)."""

    SAME_AS_BUNDLE = "same_as_bundle"
    DIFFERS_NOT_STORED = "differs_not_stored"  # the update used another mask; it is not stored (sums only)
    BUNDLE_NOT_KEPT = "bundle_not_kept"  # no trainer token bundle (PROBE_SAMPLES_PER_TOKEN, or none sent)


class SampleStep(BaseModel):
    """How one sample occurrence entered one optimizer update (its loss bookkeeping)."""

    step: int
    #: The optimizer update (train) or eval pass (eval).
    update: int
    split: SampleSplit = SampleSplit.TRAIN
    #: The model whose update it entered (actor or critic).
    role: LossRole = LossRole.ACTOR
    rank: int = 0
    micro_batch: int | None = None
    occurrence: int = 0
    fragment: int = 0
    fragments_expected: int = 1
    token_count: int | None = None
    mask_sha256: str | None = None
    loss_sum: float | None = None
    normalizer: float | None = None
    scale: float | None = None
    contribution: float | None = None
    contribution_terms: dict[str, float] = Field(default_factory=dict)
    contribution_source: ContributionSource | None = None
    #: The row sent no contribution; it is `loss_sum x scale / normalizer` with the update record's normalizer.
    is_contribution_derived: bool = False
    weights_version: int | None = None
    optimizer_step: int | None = None
    #: The update's own record says it was applied (None: no whole-update record).
    applied: bool | None = None
    is_committed: bool = False
    mask: MaskEvidence | None = None
    producer: str


class PointsUnavailable(StrEnum):
    """Why a sample (or one key of it) has no points: never a zero."""

    DROPPED = "dropped"
    NEVER_CONSUMED = "never_consumed"
    CONSUMED_NOT_COMMITTED = "consumed_not_committed"
    UNSUPPORTED = "unsupported"  # its producers declared they cannot capture it
    NOT_RECORDED = "not_recorded"  # nothing recorded (a run from before this shipped, or no hook)


class SamplePoints(BaseModel):
    """`GET /v1/samples/{id}/points[?key=]`."""

    sample_id: UUID
    run_id: UUID
    key: str | None = None
    is_available: bool
    reason: PointsUnavailable | None = None
    #: The producer's own words when `reason` is unsupported.
    why: str | None = None
    points: list[SamplePoint] = Field(default_factory=list)
    steps: list[SampleStep] = Field(default_factory=list)
    conflicts: int = 0
    #: The update records read for `steps` stopped at their row cap: a step from the cut on shows no `applied` (and no
    #: contribution derived from its records) for want of them, never because the update was not applied.
    is_truncated: bool = False


class PointsCheck(StrEnum):
    """One step's answer: complete against what was declared, and matching what the trainer reported."""

    RECONCILED = "reconciled"  # every check run is within the tolerance
    UNRECONCILED = "unreconciled"  # a check is outside it (the residuals say by how much)
    PARTIAL = "partial"  # something declared did not arrive (`missing` names it)
    UNDECLARED = "undeclared"  # rows of an update that has no whole-update record
    UNCHECKED = "unchecked"  # complete, and nothing to check against


class UpdateCapture(BaseModel):
    """One update (or eval pass) of a step: declared vs received, and the shard check (rows' contributions + batch
    terms vs the micro-batch's reported loss)."""

    #: The optimizer update, or the eval pass when `split` is eval.
    update: int
    split: SampleSplit = SampleSplit.TRAIN
    #: The model the update trains: an actor's and a critic's update of one step are checked apart.
    role: LossRole = LossRole.ACTOR
    applied: bool | None = None
    skipped_reason: str | None = None
    reported_loss: float | None = None
    ranks_expected: int | None = None
    ranks_received: int = 0
    micro_batches_expected: int | None = None
    micro_batches_received: int = 0
    rows_expected: int | None = None
    rows_received: int = 0
    #: The largest |sum of a micro-batch's contributions + its batch terms - its reported loss|; None: no check.
    shard_residual: float | None = None
    #: The relative bound the shard check used (by the pass's declared dtype).
    tolerance: float = LOSS_TOLERANCE
    #: Micro-batches with no rows that count in the framework's averages, and data-parallel padding rows.
    padding_micro_batches: int = 0
    padding_rows: int = 0
    missing: list[str] = Field(default_factory=list)


class TrainerCheck(BaseModel):
    """A per-sample key rolled up the declared way, against the run's own logged series of the same step (a rollup
    logged per update: one check per update, at the step its series has there)."""

    key: str
    run_key: str
    rollup: Rollup
    #: `Rollup.logged_per` update: the update this check folds, and the step of the run's series it read
    #: (step x updates_in_step + update; None when the step's records name no single `updates_in_step`).
    update: int | None = None
    logged_step: int | None = None
    rebuilt: float | None = None
    logged: float | None = None
    residual: float | None = None
    is_within: bool | None = None
    #: The relative bound used, by the key's declared dtype.
    tolerance: float = LOSS_TOLERANCE
    #: Why the framework's own series is approximate (`Rollup.approximate`): both numbers shown, never a failure.
    approximate: str | None = None
    #: Why the two numbers could not be compared exactly (`logging window N`: a window reaching before the steps read,
    #: or an earlier step of it missing or itself incomplete): the check reads unchecked, never unreconciled.
    unchecked_reason: str | None = None


class StepCapture(BaseModel):
    step: int
    state: PointsCheck
    is_committed: bool = False
    #: The actor's updates in the step (its whole-update records' `updates_in_step`); the critic's apart.
    updates_expected: int | None = None
    critic_updates_expected: int | None = None
    updates: list[UpdateCapture] = Field(default_factory=list)
    trainer: list[TrainerCheck] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class ProducerTraining(BaseModel):
    producer: str
    plan: TrainingPlan


class PointConflict(BaseModel):
    """One point delivered more than once with values further apart than `CONFLICT_TOLERANCE`."""

    sample_id: UUID
    name: str
    step: int
    update: int | None = None
    first: float
    other: float
    deliveries: int


class PointsCapture(BaseModel):
    """`GET /v1/runs/{id}/samples/points/capture`: per producer what it sends and cannot (with why), per step declared
    vs received and both checks. A run from before this shipped reads `is_recorded` false: nothing is rebuilt."""

    run_id: UUID
    is_recorded: bool
    #: The fp32 bound; each check names its own (`tolerance`, by dtype).
    tolerance: float = LOSS_TOLERANCE
    producers: list[ProducerTraining] = Field(default_factory=list)
    steps: list[StepCapture] = Field(default_factory=list)
    conflicts: list[PointConflict] = Field(default_factory=list)
    is_truncated: bool = False
