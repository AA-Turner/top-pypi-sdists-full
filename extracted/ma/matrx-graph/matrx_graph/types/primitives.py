from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ActionTier(str, Enum):
    """Determinism classification for nodes and actions.

    Shapes replay semantics: PURE nodes replay freely; IDEMPOTENT nodes may be
    re-invoked safely on resume; SIDE_EFFECT nodes must be checkpointed and
    deduped by (run_id, step, node_id, attempt); NON_DETERMINISTIC nodes are
    never replayed, only their persisted output is reused.
    """

    PURE = "pure"
    IDEMPOTENT = "idempotent"
    SIDE_EFFECT = "side_effect"
    NON_DETERMINISTIC = "non_deterministic"


class EdgeKind(str, Enum):
    """Explicit edge semantics. Encoded in edge.data.kind on the wire.

    DATA        — typed payload flows from source handle to target handle
    CONTROL     — "run after" signal only; no payload
    CONDITIONAL — guarded by a predicate evaluated against source output
    ERROR       — taken only when the source node fails (try/catch topology)
    STREAM      — carries an async iterator (LLM token streams, etc.)
    """

    DATA = "data"
    CONTROL = "control"
    CONDITIONAL = "conditional"
    ERROR = "error"
    STREAM = "stream"


Reducer = Literal["replace", "append", "merge", "sum", "last_writer_wins", "topic_map"]
"""Reducer strategies for channel writes.

replace             — new value overwrites old. Default.
append              — new value appended to a list. Value must be a list on channel.
merge               — shallow dict merge. Value must be a dict on channel.
sum                 — numeric sum. Value must be int | float on channel.
last_writer_wins    — like replace but records the writer node_id for auditing.
topic_map           — append to a per-topic list keyed by the writer's 'topic' field.
                      Useful for dynamic fanout gather patterns.
"""


class BackoffStrategy(str, Enum):
    NONE = "none"
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    EXPONENTIAL_JITTER = "exponential_jitter"


class RetryPolicy(BaseModel):
    """Retry configuration for a node. Applied by the scheduler.

    retry_on lists exception class names (not instances) the retry engine will
    react to. Other exceptions propagate immediately to the error edge.
    """

    model_config = {"frozen": True}

    max_attempts: int = Field(default=1, ge=1, le=20)
    backoff: BackoffStrategy = BackoffStrategy.NONE
    initial_delay_ms: int = Field(default=0, ge=0)
    max_delay_ms: int = Field(default=30_000, ge=0)
    retry_on: tuple[str, ...] = ()

    @classmethod
    def default(cls) -> RetryPolicy:
        return cls()

    @classmethod
    def with_exponential(
        cls,
        max_attempts: int = 3,
        initial_delay_ms: int = 200,
        max_delay_ms: int = 10_000,
        retry_on: tuple[str, ...] = ("TimeoutError", "ConnectionError"),
    ) -> RetryPolicy:
        return cls(
            max_attempts=max_attempts,
            backoff=BackoffStrategy.EXPONENTIAL_JITTER,
            initial_delay_ms=initial_delay_ms,
            max_delay_ms=max_delay_ms,
            retry_on=retry_on,
        )


class NodeCategory(str, Enum):
    CONTROL = "control"
    DATA = "data"
    TOOL = "tool"
    LLM = "llm"
    AGENT = "agent"
    SUBGRAPH = "subgraph"
    IO = "io"
    # A step whose EXECUTOR is configuration rather than identity — the same
    # contract satisfied by code, by a person, or by an agent (THE THREE
    # PIPES). Its own category because "which pipe runs this" is a different
    # question from "what kind of work is it".
    PIPE = "pipe"
    CUSTOM = "custom"
    PLAN = "plan"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    INTERRUPTED = "interrupted"
    # Parked for want of a require/ask input (INPUT-SURFACE.md park-not-die):
    # a headless start missing a required input holds here — durable,
    # resumable the moment anyone supplies the value. Sits beside
    # INTERRUPTED in the one "waiting on you" inbox.
    AWAITING_INPUT = "awaiting_input"
    ERRORED = "errored"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunControlStatus(str, Enum):
    """Transitional ``workflow.run.status`` values written by a control request.

    NOT scheduler outcomes (that is ``RunStatus``) — these are the "a human
    asked for something and the scheduler has not observed it yet" states the
    run row passes through between super-steps. They exist on the row, so any
    consumer typing ``run.status`` must accept them.
    """

    PAUSING = "pausing"
    CANCELLING = "cancelling"


# Every value ``workflow.run.status`` can legitimately hold — the scheduler's
# outcomes plus the transitional control states. Single source of truth for the
# generated TypeScript ``WorkflowRunStatus`` union (scripts/generate_types.py).
WORKFLOW_RUN_STATUSES: tuple[str, ...] = tuple(s.value for s in RunStatus) + tuple(
    s.value for s in RunControlStatus
)

# The declared transition map of ``workflow.run.status`` — ``{from: {to: label}}``.
# Transcribed from docs/RUN_LIFECYCLE.md §1 (the state machine the scheduler,
# the pause/cancel poll and the four recovery endpoints implement). Edge LABELS
# are the plain-words reason a run takes that edge. The lifecycle picture on the
# run page (aidream/services/lifecycles) is built from THIS table and nowhere
# else; a test pins that every status in WORKFLOW_RUN_STATUSES has a row here.
RUN_STATUS_TRANSITIONS: dict[str, dict[str, str]] = {
    "pending": {"running": "worker claims it", "awaiting_input": "required input missing"},
    "running": {
        "completed": "all steps done",
        "errored": "a step fails",
        "failed": "engine error",
        "interrupted": "asks a person",
        "pausing": "pause requested",
        "cancelling": "stop requested",
    },
    "pausing": {"paused": "checkpoint saved"},
    "paused": {"running": "resume"},
    "interrupted": {"running": "answered"},
    "awaiting_input": {"running": "input supplied"},
    "errored": {"running": "retry or skip"},
    "cancelling": {"cancelled": "stopped"},
    "completed": {},
    "failed": {},
    "cancelled": {},
}

# Finished forever — no resume, no recovery.
TERMINAL_RUN_STATUSES: tuple[str, ...] = (
    RunStatus.COMPLETED.value,
    RunStatus.FAILED.value,
    RunStatus.CANCELLED.value,
)

# The scheduler is (or is about to be) making progress on this run.
ACTIVE_RUN_STATUSES: tuple[str, ...] = (
    RunStatus.PENDING.value,
    RunStatus.RUNNING.value,
    RunControlStatus.PAUSING.value,
    RunControlStatus.CANCELLING.value,
)
