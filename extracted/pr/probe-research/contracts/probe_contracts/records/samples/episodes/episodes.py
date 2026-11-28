"""The episode reads' shapes (dashboard-redesign D7, D20): a run's episodes per step, one episode whole (rollouts →
branches → turns), and where an old rollout link's episode is. Episode = rows sharing `episode_key`; rollout = rows
sharing `attempt_key` inside it; branch = `segment`."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ....compat import StrEnum
from ..evidence import CompactEvidence, GradeStatus, SampleEvidence
from ..outcome import SampleOutcome, SampleSplit
from ..provenance import Scorer
from ..samples import BranchCause, EnvironmentLink, FinishReason, Timing, TrialFile
from ..task import BlobRef
from ..turns import ToolDefinition, Turn, TurnsSource
from .status import EpisodeState, EpisodeStatus

#: Episodes one list page holds at most.
MAX_EPISODE_PAGE = 500


class EpisodeGrouping(StrEnum):
    """How the Episodes tab piles its rows: one row an episode, grouped by environment, or rollouts newest first."""

    EPISODE = "episode"
    ENVIRONMENT = "environment"
    RECENT_ROLLOUTS = "recent_rollouts"


class EpisodeReward(BaseModel):
    """An episode's reward: its trained rollouts' (an episode with none trained, such as an eval, scores them all);
    several = their mean and the best."""

    mean: float | None = None
    best: float | None = None
    #: Rollouts that hold a reward.
    count: int = 0


class EpisodeRewardPoint(BaseModel):
    step: int
    reward: float | None
    total: int
    reported: int
    graded: int
    ungraded: int
    unknown: int


class EpisodeRewardCurve(BaseModel):
    points: list[EpisodeRewardPoint]
    evidence_snapshot: str


class EpisodeLabels(BaseModel):
    """What every row of one episode shares."""

    episode_key: str
    #: The Episode # column: its place in the step by creation order, from 1.
    number: int
    step: int | None = None
    task_id: UUID
    task_key: str
    task_name: str | None = None
    #: The Part column.
    split: SampleSplit
    environment_name: str | None = None
    environment_version: str | None = None
    group_key: str | None = None
    #: The Try column, `try_number / try_count`: its place in its group by creation order over the group's size.
    #: None for an episode with no group (every eval).
    try_number: int | None = None
    try_count: int | None = None


class EpisodeRow(EpisodeLabels):
    """One row of the Episodes tab: the drawn columns, then the Display popover's extras."""

    rollouts: int
    grade_status: GradeStatus = GradeStatus.UNKNOWN
    #: The explicit grader verdict when every included sample agrees. Mixed or absent evidence has no verdict.
    grade_passed: bool | None = None
    recorded_reward: EpisodeReward | None = None
    state: EpisodeState
    status: EpisodeStatus
    #: The exact reason behind the state (an error reason, finish reason, drop or live phase).
    reason: str | None = None
    reward: EpisodeReward
    created_at: datetime | None = None
    duration_s: float | None = None
    tokens: int | None = None
    turns: int | None = None
    branches: int = 1


class RolloutRow(EpisodeLabels):
    """One rollout, for the `recent_rollouts` grouping (newest first, not piled into episodes)."""

    attempt_key: str
    grade_status: GradeStatus = GradeStatus.UNKNOWN
    #: The explicit grader verdict when every included sample agrees. Mixed or absent evidence has no verdict.
    grade_passed: bool | None = None
    #: '' or None reads "Agent".
    agent: str | None = None
    is_trained: bool | None = None
    state: EpisodeState
    status: EpisodeStatus
    reason: str | None = None
    reward: float | None = None
    created_at: datetime | None = None
    duration_s: float | None = None
    tokens: int | None = None
    turns: int | None = None
    branches: int = 1


class EpisodeGroup(BaseModel):
    """One pile of the chosen grouping: its key (`minibugs@0.1.0`, '' for none) and how many rows it holds."""

    key: str
    count: int


class EpisodeList(BaseModel):
    """`GET /v1/runs/{id}/episodes`: one step's episodes and the step bar's facts."""

    step: int | None = None
    #: Every step that has episodes, ascending, and the newest of them (the bar's "Latest").
    steps: list[int] = Field(default_factory=list)
    latest_step: int | None = None
    evidence_snapshot: str | None = None
    group_by: EpisodeGrouping = EpisodeGrouping.EPISODE
    episodes: list[EpisodeRow] = Field(default_factory=list)
    #: The `recent_rollouts` grouping's rows (empty otherwise).
    rollouts: list[RolloutRow] = Field(default_factory=list)
    groups: list[EpisodeGroup] = Field(default_factory=list)
    next_cursor: str | None = None
    #: The step held more samples than one read takes: later episodes are left out.
    is_truncated: bool = False


class TurnState(StrEnum):
    """A turn's colour on the timeline: ended normally, a tool call in it failed, or it ended the rollout with an error."""

    OK = "ok"
    UNKNOWN = "unknown"
    TOOL_FAILED = "tool_failed"
    ENDED_WITH_ERROR = "ended_with_error"


class EpisodeTurn(BaseModel):
    """One turn as the transcript and timeline read it. Times come from the rollout's events naming the turn; tokens
    from its own model call (`Turn.usage`), else the branch's counts when this turn was its only model call, else
    None (never a guess)."""

    index: int
    state: TurnState
    turn: Turn
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_s: float | None = None
    tool_calls: int = 0
    tool_errors: int = 0
    prompt_tokens: int | None = None
    response_tokens: int | None = None


class EpisodeBranch(BaseModel):
    """One branch: a sample row of the rollout (`segment` i of n), what started it and its turns. A conversation
    stored as a blob has no turns here: `turns_blob` names it (`GET /v1/samples/{sample_id}` reads it)."""

    index: int
    sample_id: UUID
    #: One graph per original sample. Shared prefixes are transmitted once.
    evidence: SampleEvidence | None = None
    key: str
    started_by: BranchCause | None = None
    parent_branch: int | None = None
    parent_turn: int | None = None
    turns: list[EpisodeTurn] = Field(default_factory=list)
    turns_blob: BlobRef | None = None
    turns_source: TurnsSource | None = None
    turn_count: int | None = None
    finish_reason: FinishReason | None = None
    prompt_tokens: int | None = None
    response_tokens: int | None = None
    #: The tools the model was offered in this branch (the transcript's "Tool definitions" row).
    tools: list[ToolDefinition] = Field(default_factory=list)
    started_at: datetime | None = None
    ended_at: datetime | None = None


class RolloutActivity(BaseModel):
    """The Details pane's activity counts."""

    turns: int = 0
    tool_calls: int = 0
    tool_errors: int | None = None
    branches: int = 1


class RolloutUsage(BaseModel):
    """Tokens over every branch."""

    prompt_tokens: int | None = None
    response_tokens: int | None = None
    total_tokens: int | None = None


class RolloutResult(BaseModel):
    """Why it ended as it did: the failure reason, the error, the Harbor trial's files (its outputs: the files after;
    the task's own files, before, are in `GET /v1/runs/{id}/tasks/{task_id}`) and its test output (verifier logs)."""

    failure_reason: str | None = None
    error_reason: str | None = None
    error_message: str | None = None
    log_tail: str | None = None
    files: EnvironmentLink | None = None
    test_output: list[TrialFile] = Field(default_factory=list)


class EpisodeRollout(BaseModel):
    """One agent's attempt in the play, with its Details (D20): reward and its parts, activity, usage, state, and the
    JSON the script and environment wrote (`timing`, `metrics`, `extras`)."""

    attempt_key: str
    evidence_summary: CompactEvidence | None = None
    agent: str | None = None
    is_trained: bool | None = None
    state: EpisodeState
    status: EpisodeStatus
    reason: str | None = None
    outcome: SampleOutcome
    reward: float | None = None
    normalized_reward: float | None = None
    reward_parts: dict[str, float] = Field(default_factory=dict)
    scored_by: list[Scorer] = Field(default_factory=list)
    activity: RolloutActivity
    usage: RolloutUsage
    duration_s: float | None = None
    timing: Timing | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    extras: dict[str, Any] = Field(default_factory=dict)
    #: The span holding its trajectory (the Timeline's spans: `GET /v1/runs/{id}/spans`).
    trace_span_id: UUID | None = None
    result: RolloutResult
    branches: list[EpisodeBranch] = Field(default_factory=list)


class EpisodeDetail(EpisodeLabels):
    """`GET /v1/runs/{id}/episodes/{key}`: one episode whole, its rollouts in creation order."""

    run_id: UUID
    state: EpisodeState
    status: EpisodeStatus
    reason: str | None = None
    reward: EpisodeReward
    created_at: datetime | None = None
    rollouts: list[EpisodeRollout] = Field(default_factory=list)


class EpisodeLink(BaseModel):
    """`GET /v1/runs/{id}/episodes/find`: the episode an old rollout, trial or sample link opens (R5)."""

    episode_key: str
    step: int | None = None
    sample_id: UUID
