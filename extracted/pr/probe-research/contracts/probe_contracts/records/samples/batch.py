"""The write door's shapes: `POST /v1/runs/{id}/samples/batch` carries one producer's parts, tasks, groups,
seals, commits, weight versions, live turns and plan changes in one durable message."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from ..command import CommandKind
from .capture import MAX_PRODUCERS, Plan, Producer, Refusal, Seal
from .live.turns import LiveTurnIn
from .part import SamplePartIn
from .samples import SampleGroup
from .task import MAX_TASK_KEY_CHARS, Scenario, Task
from .weights import WeightVersion

#: Per list in one batch; the SDK also splits a POST past 4 MiB (`MAX_BATCH_BYTES`).
MAX_BATCH_ITEMS = 1_000
MAX_BATCH_BYTES = 4 * 1024 * 1024


class TaskIn(Task.project("task_key", "scenario", "prompt", "prompt_blob", "dataset", "label", "reward_max")):
    """A task instance, once per run: the server derives its id from the key and the scenario."""


class GroupIn(SampleGroup.project(
    "group_key", "size", "scheduled_step", "consumed_step", "drop_reason",
)):
    """Group facts only; reward mean and variance are read from the members."""

    task_key: str | None = Field(default=None, min_length=1, max_length=MAX_TASK_KEY_CHARS)
    scenario: Scenario | None = None


class SealIn(Seal.project("step", "sent", "dropped", "bundles")):
    """This producer's declared counts for one step."""


class CommitIn(Seal.project("step", "consumed_at", consumed_at=(datetime, ...))):
    """The trainer's optimizer step succeeded: its consumed samples read `trained`."""


class WeightVersionIn(WeightVersion.project("policy_id", "version", "after_step", "pushed_at", "checkpoint")):
    """One weight push; a checkpoint ref is resolved to its artifact by the server."""


class PlanIn(Plan.project(
    "expected_steps", "producers", "reward_max", "max_staleness", "final_step", "is_closed", "capabilities",
    "refusals", "adapter_hooks_missing",
    producers=(list[Producer] | None, Field(default=None, max_length=MAX_PRODUCERS)),
    reward_max=(float | None, None),
    is_closed=(bool | None, None),
    capabilities=(list[CommandKind] | None, None),
    refusals=(dict[CommandKind, Refusal] | None, None),
    adapter_hooks_missing=(bool | None, None),
)):
    """A change to the run's plan: only the fields sent change (`model_fields_set`). `capabilities` is what THIS
    batch's producer can be asked (it replaces that producer's list on the plan row); `refusals` why it refuses the
    kinds it cannot do (it replaces that producer's map). `adapter_hooks_missing` is also
    about THIS batch's producer: true adds it to the plan row's list (never removed)."""


class SampleBatchIn(BaseModel):
    """One producer, one write epoch. Any epoch of the run is accepted: no fence, no status gate (DESIGN.md)."""

    producer: Producer
    write_epoch: int = Field(ge=1)
    session_id: UUID | None = None
    samples: list[SamplePartIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    tasks: list[TaskIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    groups: list[GroupIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    seals: list[SealIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    commits: list[CommitIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    weights: list[WeightVersionIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    #: A watched attempt's turns as they happen (DESIGN.md "Live"); they ride the same message and dedup token.
    live_turns: list[LiveTurnIn] = Field(default_factory=list, max_length=MAX_BATCH_ITEMS)
    plan: PlanIn | None = None

    @model_validator(mode="after")
    def _one_each(self) -> SampleBatchIn:
        if not (self.samples or self.tasks or self.groups or self.seals or self.commits or self.weights
                or self.live_turns or self.plan is not None):
            raise ValueError("an empty sample batch")
        for name, steps in (("seals", [s.step for s in self.seals]), ("commits", [c.step for c in self.commits])):
            if len(steps) != len(set(steps)):
                raise ValueError(f"{name} name a step twice")
        turns = [(turn.attempt_key, turn.seq) for turn in self.live_turns]
        if len(turns) != len(set(turns)):
            raise ValueError("live_turns name an (attempt_key, seq) twice")
        return self

    @property
    def item_count(self) -> int:
        lists = (self.samples, self.tasks, self.groups, self.seals, self.commits, self.weights, self.live_turns)
        return sum(len(items) for items in lists) + (self.plan is not None)


class SampleBatchOut(BaseModel):
    """201, once applied: `unchanged` parts were already stored by an earlier delivery (a retry)."""

    accepted: int
    written: int
    unchanged: int


class SampleBatchQueued(BaseModel):
    """202 with `X-Probe-Async-Ack: 1`: durable in the ingest queue, applied later in order."""

    accepted: int
    queued: bool = True
    messages: list[str] = Field(default_factory=list)
