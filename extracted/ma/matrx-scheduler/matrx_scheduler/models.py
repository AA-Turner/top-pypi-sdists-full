"""
Pydantic models mirroring the sch_* table shapes. Used as the package's
internal contract — host code converts ORM models to these on the way in.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _coerce_json_object(value: Any, *, empty: Any) -> Any:
    """Accept dicts and JSON-encoded strings (asyncpg jsonb text form)."""
    if isinstance(value, str):
        return json.loads(value) if value.strip() else empty
    return value


# Trigger types — keep in lockstep with sch_trigger_type_chk and the FE union.
TriggerType = Literal[
    "one-shot",
    "interval",
    "cron",
    "heartbeat",
    "context-match",
    "event",
    "manual",
    "dependency",
]

RunStatus = Literal[
    "queued",
    "claimed",
    "running",
    "success",
    "failed",
    "cancelled",
    "skipped",
    # The process holding the run went away (deploy SIGTERM, hard kill); the run
    # is closed and a continuation is queued. Neither success nor failure — see
    # ``continuation.py``. Keep in lockstep with sch_run_status_chk and the FE union.
    "interrupted",
]

AuthMode = Literal["ask", "auto"]


class SchTask(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    user_id: str
    organization_id: str
    kind: str  # 'agent' for v0
    title: str
    description: str | None = None
    queue: str = "default"
    surfaces: list[str] = Field(default_factory=list)
    enabled: bool = True
    expires_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    taxonomy_node_id: str | None = None
    next_due_at: datetime | None = None
    last_run_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SchAgentTask(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str  # FK -> sch_task.id
    agent_id: str | None = None
    mandate_key: str | None = None
    prompt: str
    variables: dict[str, Any] = Field(default_factory=dict)
    persistent_conversation_id: str | None = None
    auth_mode: AuthMode = "ask"
    max_runtime_seconds: int = 600
    max_concurrent: int = 1

    @field_validator("variables", mode="before")
    @classmethod
    def _coerce_variables(cls, value: Any) -> Any:
        return _coerce_json_object(value, empty={})


class SchTrigger(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    task_id: str
    user_id: str
    type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    next_due_at: datetime | None = None
    last_fired_at: datetime | None = None

    @field_validator("config", mode="before")
    @classmethod
    def _coerce_config(cls, value: Any) -> Any:
        return _coerce_json_object(value, empty={})


class SchRun(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    task_id: str
    trigger_id: str | None = None
    user_id: str
    organization_id: str
    status: RunStatus
    surface: str | None = None
    queue: str | None = None
    output_ref: dict[str, Any] | None = None
    due_at: datetime
    claimed_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    claim_token: str | None = None
    claim_expires_at: datetime | None = None
    result_summary: str | None = None
    error_message: str | None = None
    result_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None

    @field_validator("output_ref", "result_metadata", mode="before")
    @classmethod
    def _coerce_jsonb(cls, value: Any) -> Any:
        return _coerce_json_object(value, empty=None)

    @field_validator("metadata", mode="before")
    @classmethod
    def _coerce_metadata(cls, value: Any) -> Any:
        return _coerce_json_object(value, empty={})


class HydratedTask(BaseModel):
    """Joined task + agent_task + (active) trigger as the runner sees it.

    ``agent_task`` is optional because non-agent kinds (``ping``,
    ``tool``, and future additions) don't have a ``sch_agent_task``
    row. The runner's kind dispatch in ``runner.py`` enforces presence
    per kind: ``agent`` and ``tool`` both require ``agent_task`` (the
    latter reuses it for tool_name + args until a dedicated
    ``sch_tool_task`` ships); ``ping`` ignores it entirely.
    """

    task: SchTask
    agent_task: SchAgentTask | None = None
    trigger: SchTrigger | None = None


class AgentRunInput(BaseModel):
    """What the runner hands to the host's agent_runner."""

    task_id: str
    run_id: str
    user_id: str
    organization_id: str
    agent_id: str | None = None
    mandate_key: str | None = None
    prompt: str
    variables: dict[str, Any]
    persistent_conversation_id: str | None
    max_runtime_seconds: int

    @model_validator(mode="after")
    def _require_holder_selection(self) -> AgentRunInput:
        self.agent_id = (self.agent_id or "").strip() or None
        self.mandate_key = (self.mandate_key or "").strip() or None
        if not (self.agent_id or self.mandate_key):
            raise ValueError("agent_id or mandate_key is required for scheduled agent dispatch")
        return self


class ToolRunInput(BaseModel):
    """What the runner hands to the host's tool_runner (kind='tool' tasks).

    The shape is intentionally parallel to ``AgentRunInput`` so a host
    can wire up both with the same plumbing. Tool args live in
    ``args``; ``tool_name`` is the registered handler key on the host
    (e.g. a matrx-extend tool name, a desktop capability id).

    ``task_id`` and ``run_id`` are included so the tool_runner can
    persist auxiliary artifacts (logs, intermediate files) keyed back
    to the sch_run row.
    """

    user_id: str
    tool_name: str
    args: dict[str, Any] = Field(default_factory=dict)
    max_runtime_seconds: int = 600
    task_id: str
    run_id: str


class AgentRunResult(BaseModel):
    """What the host's agent_runner (or tool_runner) returns to the
    scheduler.

    The same shape is used by both runners -- it's the generic
    "ran something, here's the outcome" envelope. For tool runs,
    ``conversation_id`` is typically None; ``result_summary`` is a
    short string echoed to the FE, and ``metadata`` carries the
    structured tool result.
    """

    success: bool
    conversation_id: str | None = None
    result_summary: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    #: Units of work this run COMMITTED before it returned -- keywords
    #: classified, sites synced, rows swept. MEASURED by the handler from what
    #: landed, never assumed from what was attempted. The runner stamps it into
    #: ``sch_run.result_metadata[RUN_UNITS_DONE_KEY]`` on every terminal write,
    #: so the ledger can tell "did nothing" from "did 839 things and then hit a
    #: transient blip" -- a distinction ``success`` alone erased, which is how
    #: the repeat guard concluded a working schedule had "NEVER succeeded once"
    #: and disabled it (2026-08-26). See ``bounded_work``.
    units_done: int = 0
    #: Why a bounded run stopped short of its own ceiling, in one human
    #: sentence -- or None when it ran to its natural end. Stamped into
    #: ``result_metadata[RUN_STOPPED_EARLY_KEY]``; ``bounded_work`` also puts it
    #: in ``result_summary`` so nothing about the stop is only in a log.
    stopped_early: str | None = None
    #: The run did NOTHING on purpose -- its feature is switched off, its
    #: cadence has not elapsed, there was nothing to do. A skip is not a
    #: failure, but it is not a success either: recording it as ``success``
    #: made a switched-off drainer report 1,925 "successful" runs in a week
    #: (2026-09-25). The runner writes ``status='skipped'`` for it, with the
    #: reason in ``result_summary``. See :meth:`terminal_status`.
    skipped: bool = False

    def terminal_status(self) -> str:
        """THE ONE place a handler's result becomes a ledger status.

        ``skipped`` only when the handler both succeeded and did no work
        (units_done == 0): a skip that committed units is a success, and a
        failed run is failed whatever else it says."""
        if not self.success:
            return "failed"
        if self.skipped and int(self.units_done or 0) == 0:
            return "skipped"
        return "success"

    @classmethod
    def bounded_work(
        cls,
        *,
        units_done: int,
        failures: list[str] | tuple[str, ...],
        summary: str,
        metadata: dict[str, Any] | None = None,
        conversation_id: str | None = None,
        max_failures_named: int = 3,
        stop_reason: str | None = None,
    ) -> AgentRunResult:
        """THE ONE VERDICT for a bounded multi-pass / multi-item run.

        A run that loops over passes, sites, or items and stops early on an
        error is not "failed" if earlier iterations committed real work -- it
        is a partial success with a named reason it stopped short. Deriving
        ``success`` from the LAST iteration's error (or from "any failure at
        all") throws the committed work away from the status signal, and every
        consumer of that status -- the repeat guard, the failure sink, the
        operator -- is then lied to.

        The rule, in one place so every handler agrees:

        * ``units_done > 0``  -> ``success=True``. The stop is reported, loudly,
          as ``stopped_early`` (in the summary AND the metadata) and the
          failures are still carried in ``error_message``; nothing is hidden.
        * ``units_done == 0`` and failures -> ``success=False`` with the
          failures as the error. Nothing landed; it IS a failed run.
        * no failures -> ``success=True``, no stop reason.
        * ``stop_reason`` -> the handler stopped ITSELF short of its ceiling for a
          reason that is not a failure -- the run lease (``current_run_lease()
          .stop_reason()``) is the canonical one. It is named in the summary
          and in ``stopped_early`` but never becomes the ``error_message``:
          a clean stop with work landed is a success that says why it stopped.
        """
        failure_list = [str(f) for f in failures if f]
        named = "; ".join(failure_list[:max_failures_named])
        if len(failure_list) > max_failures_named:
            named += f" (+{len(failure_list) - max_failures_named} more)"
        stopped_early: str | None = None
        if failure_list and units_done > 0:
            stopped_early = f"stopped short after committing {units_done} unit(s): {named}"
            summary = f"{summary} STOPPED_EARLY: {named}"
        if stop_reason:
            stop_text = f"stopped short after committing {units_done} unit(s): {stop_reason}"
            stopped_early = f"{stopped_early}; {stop_reason}" if stopped_early else stop_text
            summary = f"{summary} STOPPED_EARLY: {stop_reason}"
        return cls(
            success=units_done > 0 or not failure_list,
            conversation_id=conversation_id,
            result_summary=summary,
            error_message=named or None,
            metadata=dict(metadata or {}),
            units_done=max(0, int(units_done)),
            stopped_early=stopped_early,
        )


class BacklogRearmResult(AgentRunResult):
    """Opt-in result for a bounded on-demand tool that has more work.

    The runner converts this into :class:`BacklogRearmRequest`; callers cannot
    supply task, actor, organization, run, or claim authority through the
    handler result.  Those values come only from the claimed scheduler rows.
    """

    success: Literal[True] = True
    recovery_key: str = Field(min_length=4, max_length=512)
    rearm_at: datetime

    @field_validator("recovery_key")
    @classmethod
    def _versioned_recovery_key(cls, value: str) -> str:
        if not value.startswith("v1:"):
            raise ValueError("must be an opaque v1: recovery key")
        return value

    @field_validator("rearm_at")
    @classmethod
    def _aware_rearm_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("must be timezone-aware")
        return value


#: Reserved keys the runner stamps into ``sch_run.result_metadata`` from
#: ``AgentRunResult.units_done`` / ``stopped_early``. They are the CONTRACT the
#: repeat guard reads back; a handler's own metadata never overrides them.
RUN_UNITS_DONE_KEY = "units_done"
RUN_STOPPED_EARLY_KEY = "stopped_early"

#: THE RESUMABLE TERMINAL STATE: the run's process went away and a continuation
#: was queued. Never counted by the failure sink or the repeat guard.
RUN_INTERRUPTED_STATUS = "interrupted"
#: ``sch_run.metadata`` key a continuation run carries (``continuation.py``).
RUN_CONTINUATION_KEY = "continuation"
