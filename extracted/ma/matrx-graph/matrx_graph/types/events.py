"""Workflow run event payloads.

Every event the scheduler emits on the stream is modeled here as a typed
Pydantic model. The frontend consumes NDJSON lines of the shape
``{"event": "data", "data": {"event": "<one_of>", ...}}`` and narrows on
``data.event`` to pick the right model. This IS the single source of truth for
the event vocabulary — the UI's canvas state machine depends on it.

Every consumer's TypeScript is GENERATED from these models: aidream's
``scripts/generate_types.py workflow-events`` emits one artifact that
workflow-studio imports (``src/types/generated/workflow-events.ts``) and
matrx-frontend receives through ``pnpm sync-types`` (bundle
``workflow-events-ts``). Change a model here → regenerate in the same change;
``generate_types.py --check`` screams in ``release.sh`` if a copy is stale.
Never hand-edit a TS mirror — there were two, and they drifted.

Emission convention:

- ``run_started``   — fired once at the top of a run
- ``node_started``  — before a node executor is invoked
- ``node_completed``— after the executor returns successfully
- ``node_failed``   — executor raised (non-interrupt) exception
- ``node_skipped``  — idempotency replay skipped re-invocation
- ``checkpoint_saved`` — after each super-step, before the next
- ``run_interrupted`` — scheduler caught GraphInterrupt; payload carries
  the interrupt's prompt/schema/context
- ``run_completed`` — terminal success
- ``run_failed``    — terminal error
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_graph.types.primitives import RunStatus

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# THE LIVENESS VOCABULARY (SPEC-workflow-ui-contract §5.1)
# ---------------------------------------------------------------------------
# While a step works, the screen shows what it is DOING — never a spinner.
# The set of things it may say is CLOSED: a new phase is a code change to this
# constant, never a string a runner invents. Free text produced by older call
# sites is folded onto this set exactly ONCE, at the emitter chokepoint, by
# ``map_agent_step_phase`` below.

AGENT_STEP_PHASE_PREPARING = "preparing"
AGENT_STEP_PHASE_STREAMING = "streaming"
AGENT_STEP_PHASE_TOOL = "tool"
AGENT_STEP_PHASE_REASONING = "reasoning"
AGENT_STEP_PHASE_FINALIZING = "finalizing"
AGENT_STEP_PHASE_RETRYING = "retrying"
AGENT_STEP_PHASE_COMPLETE = "complete"

#: The closed vocabulary, in the order a healthy step walks it.
AGENT_STEP_PHASES: tuple[str, ...] = (
    AGENT_STEP_PHASE_PREPARING,
    AGENT_STEP_PHASE_STREAMING,
    AGENT_STEP_PHASE_TOOL,
    AGENT_STEP_PHASE_REASONING,
    AGENT_STEP_PHASE_FINALIZING,
    AGENT_STEP_PHASE_RETRYING,
    AGENT_STEP_PHASE_COMPLETE,
)

AgentStepPhase = Literal[
    "preparing",
    "streaming",
    "tool",
    "reasoning",
    "finalizing",
    "retrying",
    "complete",
]

#: Every free-text phase label any live call site emits today, folded onto the
#: closed set. Keys are lowercased and stripped before lookup. Adding a key
#: here is how a legacy label is retired — never by widening the vocabulary.
_AGENT_STEP_PHASE_ALIASES: dict[str, str] = {
    # already-closed members map to themselves (cheap, and makes the table
    # the single answer to "is this label known?")
    **{phase: phase for phase in AGENT_STEP_PHASES},
    # -- before the provider call ------------------------------------------
    # "processing" is emitted when the orchestrator has decided to make ANOTHER
    # provider call (tool results folded in, corrective turn forced): the step
    # is preparing a request, not streaming one.
    "processing": AGENT_STEP_PHASE_PREPARING,
    "starting": AGENT_STEP_PHASE_PREPARING,
    "start": AGENT_STEP_PHASE_PREPARING,
    "initializing": AGENT_STEP_PHASE_PREPARING,
    "prepare": AGENT_STEP_PHASE_PREPARING,
    "queued": AGENT_STEP_PHASE_PREPARING,
    # -- tokens arriving ----------------------------------------------------
    "generating": AGENT_STEP_PHASE_STREAMING,
    "streaming_response": AGENT_STEP_PHASE_STREAMING,
    "responding": AGENT_STEP_PHASE_STREAMING,
    # -- tool work ----------------------------------------------------------
    "tool_call": AGENT_STEP_PHASE_TOOL,
    "tools": AGENT_STEP_PHASE_TOOL,
    "executing_tools": AGENT_STEP_PHASE_TOOL,
    # -- structured output --------------------------------------------------
    "parsing": AGENT_STEP_PHASE_FINALIZING,
    "validating": AGENT_STEP_PHASE_FINALIZING,
    "finalize": AGENT_STEP_PHASE_FINALIZING,
    # -- retry --------------------------------------------------------------
    "retry": AGENT_STEP_PHASE_RETRYING,
    # -- settled ------------------------------------------------------------
    "completed": AGENT_STEP_PHASE_COMPLETE,
    "done": AGENT_STEP_PHASE_COMPLETE,
    "end": AGENT_STEP_PHASE_COMPLETE,
    "finished": AGENT_STEP_PHASE_COMPLETE,
}

#: One WARNING per distinct unmapped label per process — an unmapped phase is a
#: gap in the table worth fixing, but a fast model must not turn it into a log
#: flood.
_unmapped_phases_seen: set[str] = set()


def map_agent_step_phase(raw: str | None) -> str | None:
    """Fold a phase label onto :data:`AGENT_STEP_PHASES`.

    THE mapping chokepoint (SPEC §5.1): existing free-text phases map onto the
    closed set exactly once, here. An unmapped string **passes through** and is
    logged at WARNING — never dropped, because a label nobody anticipated is
    still better on screen than a spinner, and the log is how the alias table
    learns about it.

    ``reasoning:<state>`` (thinking-block open/close from a reasoning model) is
    a family, not a member: any ``reasoning:*`` label folds to ``reasoning``.
    """
    if raw is None:
        return None
    label = raw.strip()
    if not label:
        return None
    key = label.lower()
    mapped = _AGENT_STEP_PHASE_ALIASES.get(key)
    if mapped is not None:
        return mapped
    # Family prefixes — "reasoning:started", "reasoning:ended", ...
    head = key.split(":", 1)[0]
    mapped = _AGENT_STEP_PHASE_ALIASES.get(head)
    if mapped is not None:
        return mapped
    if key not in _unmapped_phases_seen:
        _unmapped_phases_seen.add(key)
        logger.warning(
            "unmapped agent step phase %r — passing through unchanged. Add it to "
            "_AGENT_STEP_PHASE_ALIASES in matrx_graph.types.events or stop emitting it; "
            "the phase vocabulary is CLOSED (SPEC-workflow-ui-contract §5.1).",
            label,
        )
    return label


class WithheldValue(BaseModel):
    """A value a screen view left out (kept on the server, MKT-167) — announced, never silent (2026-10-29).

    ``path`` runs from the event's root (``["output", "pages"]``) or, on a run record, from its output
    (``["website", "pages"]``). ``ref`` names the stored copy ``GET /runs/{id}/values?hash=`` returns to a
    permitted viewer; None when the value is not held by reference (a run record's inline value)."""

    path: list[str | int]
    value_type: Literal["object", "list", "text", "number", "boolean", "null", "unknown"]
    bytes: int
    items: int | None = None
    chars: int | None = None
    ref: str | None = None


class _EventBase(BaseModel):
    model_config = ConfigDict(frozen=True)

    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="before")
    @classmethod
    def _client_safe_error_prose(cls, data: Any) -> Any:
        """Every event is client-bound: its error prose never carries a terminal
        banner, SQL, bound args, a traceback or maintainer hints.

        Live 2026-09-17 a Studio node inspector rendered matrx-orm's full
        ``UnknownDatabaseError`` banner (ANSI, the INSERT, its Args) from a
        ``node_failed`` event. Enforced HERE, at construction, so no emit site
        — engine or host — can put one on the wire. See
        ``matrx_utils.client_error_text``.
        """
        if not isinstance(data, dict):
            return data
        from matrx_graph.failure import client_safe_error_payload

        if not any(k in data for k in ("error_message", "error", "wrapper")):
            return data
        out = client_safe_error_payload(data)
        wrapper = out.get("wrapper")
        if isinstance(wrapper, dict):
            out["wrapper"] = client_safe_error_payload(wrapper)
        return out


class RunStartedEvent(_EventBase):
    event: Literal["run_started"] = "run_started"
    run_id: str
    thread_id: str
    definition_id: str
    definition_hash: str
    # ``server_restart`` = the recovery lane is starting this run again from its inputs:
    # the server running it stopped before its first checkpoint, so the steps in
    # ``restarted_node_ids`` were cut off and start again (see ``RunResumedEvent.reason``).
    reason: Literal["server_restart"] | None = None
    restarted_node_ids: list[str] = Field(default_factory=list)


class NodeStartedEvent(_EventBase):
    event: Literal["node_started"] = "node_started"
    run_id: str
    step: int
    node_id: str
    spec_type: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    invocation_count: int = 1
    inputs: dict[str, Any] = Field(default_factory=dict)
    # Shape system: the node's DECLARED output kind (CompiledNode.output_kind —
    # spec default overridden by ``data.output_kind``, resolved once at
    # compile time). Announced at start so consumers can reserve/render the
    # kind's loading silhouette while the node streams, instead of waiting
    # for node_completed. Declaration only — the settled/verified kind (with
    # self-description fallback and drift verdict) still arrives on
    # NodeCompletedEvent. None = kindless node.
    output_kind: str | None = None


class NodeCompletedEvent(_EventBase):
    event: Literal["node_completed"] = "node_completed"
    run_id: str
    step: int
    node_id: str
    spec_type: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    invocation_count: int = 1
    duration_ms: int
    output: dict[str, Any] = Field(default_factory=dict)
    # Shape system: the platform kind the output conforms to (the node's
    # compiled output_kind). Lets consumers render/route the output through
    # the kind registry without a second lookup. None = inline/untyped.
    output_kind: str | None = None
    # Shape-verification truth (additive, Content-IR Studio spec §5): the
    # scheduler's output-drift check result, surfaced instead of discarded.
    # True = output validated against the declared kind's registered schema;
    # False = drift (per-field errors below); None = neutral — no output_kind
    # declared OR the kind lookup loud-skipped (never render None as a pass).
    output_kind_ok: bool | None = None
    output_kind_errors: list[str] | None = None
    # Version of the registry kind the verdict was computed against
    # (content_ir.kind_definition.version at resolution time). None = no kind
    # declared or the kind never resolved. Additive — carried so verdicts are
    # version-addressable (contract_kinds fingerprints; this pins the ref).
    output_kind_version: int | None = None
    # Named degraded mode (KindDegradedReason slug) when the kind check
    # loud-skipped: kind_not_registered | kind_inactive | schema_unavailable |
    # schema_invalid | catalog_unreachable. None = the check ran (see
    # output_kind_ok) or no kind was declared. A skipped check is NEVER a
    # pass — consumers render this as a distinct degraded state.
    output_kind_degraded: str | None = None
    # Content IR envelope hand-off (additive, Studio spec §6 P3 / D2): when
    # the output kind check ran and PASSED, ``metadata["__ir"]`` carries the
    # canonical CanonicalBlockIR built by matrx_graph.content_ir.envelope
    # so consumers render the output through the
    # twin's trusted-envelope path without re-parsing. Out-of-band posture:
    # ``output`` itself is NEVER mutated (no __kind injection). None = no
    # kind declared, check degraded/failed, or stamping loudly failed open —
    # consumers fall back to their own classification. Same wire contract as
    # the chat pipeline (PYTHON_ENVELOPE_CONTRACT.md).
    metadata: dict[str, Any] | None = None
    # THE PACKET (KINDS_EVERYWHERE_PLAN §10b item 8): this same completion as a
    # self-describing ``node_outcome`` runtime-wrapper kind instance —
    # run/workflow/node identity + timing + the kind verdict, with the data
    # kind nested under ``output``. Built by
    # ``matrx_graph.content_ir.runtime_view.node_outcome_view``; present on
    # every completion (the wrapper describes the INVOCATION, not the payload's
    # luck) and always ELIDED: ``output`` is null and ``output_ref="output"``
    # names this event's own ``output`` field, so no payload is serialized
    # twice per streamed event / per wf_node_events row.
    #
    # Additive by design — every field above stays exactly where it is while
    # consumers migrate to the wrapper; only once they have does a field the
    # wrapper duplicates become derived. None = wrapper assembly loudly failed
    # open (a platform defect, screamed in the log), never a silent change of
    # shape. Complete-only, like ``__ir``: a still-arriving kind is the
    # ``__ir_partial`` contract's business, never a wrapper's.
    wrapper: dict[str, Any] | None = None
    # Run once per key (``data.once``): ``"reused"`` when the step did NOT run because a
    # stored success for its key was reused; ``reused_from`` then names where it came from
    # (``{run_id, node_id, step, dispatch_id, item_index, attempt, at}``) so the run page can
    # show a "Reused" badge linking to that run. None on every ordinary completion.
    source: Literal["executor", "reused"] | None = None
    reused_from: dict[str, Any] | None = None
    # What a screen view left out of ``output`` (kept on the server): one entry per cut, so the screen draws a
    # stub where each value was. None on a full (debug) view and whenever nothing was left out.
    withheld: list[WithheldValue] | None = None
    # How many further cuts were left out of ``withheld`` (it lists at most the ``workflow.event_payload.withheld_list_max`` knob).
    withheld_more: int | None = None


class NodeSkippedEvent(_EventBase):
    """The node was not invoked this time: its output came from somewhere else.

    Three roads lead here and a screen must not paint them alike (W1.1, 2026-10-02 — a held
    write the person APPROVED read "Skipped"): the person skipped it (``user_skip``), a mock
    stood in (``mocked``), or a recorded outcome was replayed — which is how an answered pause
    or an approved held write reaches the run on resume (``executor`` / ``user_manual``).
    ``source`` is the replayed outcome's own ``NodeOutcome.source`` (same vocabulary as
    ``matrx_graph.checkpoint.protocol.OutcomeSource``); ``None`` only on events written before
    it existed.
    """

    event: Literal["node_skipped"] = "node_skipped"
    run_id: str
    step: int
    node_id: str
    spec_type: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    invocation_count: int = 1
    output: dict[str, Any] = Field(default_factory=dict)
    source: Literal["executor", "user_skip", "user_manual", "retry", "mocked", "reused"] | None = None
    #: Why the run itself did not invoke the node (``ready_when`` unmet: "not ready:
    #: confirmed.name is missing"); None for a person's skip or a replay.
    reason: str | None = None
    #: True when a TEST run answered this step from its declared sample (``sample_steps``):
    #: the output is the sample, never a real result. ``source`` stays ``"mocked"``.
    sampled: bool = False


class NodeFailedEvent(_EventBase):
    """Terminal failure of one node invocation (raised exception OR a
    returned ``Failure`` envelope, after retries). ``error`` is a
    self-describing ``node_error`` KIND instance (plan §10d-B3) — the same dict
    persisted to ``workflow.node_outcome.error`` and delivered on ERROR edges,
    carrying ``__kind`` plus the structured superset
    ``{code, message, type, details?, cause?, step_id?, …}``; ``error_type`` /
    ``error_message`` are kept as flat mirrors for existing consumers."""

    event: Literal["node_failed"] = "node_failed"
    run_id: str
    step: int
    node_id: str
    spec_type: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    invocation_count: int = 1
    error_type: str
    error_message: str
    error: dict[str, Any] | None = None
    # THE PACKET, FAILURE SIDE (plan §10d-B3) — the twin of
    # ``NodeCompletedEvent.wrapper``. The same ``node_outcome`` runtime-wrapper
    # kind instance, ``status="failed"``, with the ``node_error`` kind nested
    # under its own ``error``. A consumer that renders completions through the
    # wrapper renders failures through the identical path instead of needing a
    # second, untyped branch. Additive; ``None`` = assembly loudly failed open.
    wrapper: dict[str, Any] | None = None


class NodeRetryScheduledEvent(_EventBase):
    """A node attempt raised; the scheduler is sleeping then re-executing.

    Fired in-line during a super-step when a node's RetryPolicy has remaining
    attempts AND the raised exception is retryable. The next attempt runs in
    the same super-step (it does NOT consume one of the run's max_steps).
    The UI uses this to render an amber "retrying" badge with the backoff
    countdown — the run is still RUNNING, not ERRORED.
    """

    event: Literal["node_retry_scheduled"] = "node_retry_scheduled"
    run_id: str
    step: int
    node_id: str
    spec_type: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    invocation_count: int = 1
    next_attempt: int
    delay_ms: int
    error_type: str
    error_message: str


class CheckpointSavedEvent(_EventBase):
    event: Literal["checkpoint_saved"] = "checkpoint_saved"
    run_id: str
    checkpoint_id: str
    step: int
    parent_checkpoint_id: str | None = None


class RunInterruptedEvent(_EventBase):
    event: Literal["run_interrupted"] = "run_interrupted"
    run_id: str
    node_id: str
    payload: dict[str, Any]
    checkpoint_id: str | None = None


class RunCompletedEvent(_EventBase):
    event: Literal["run_completed"] = "run_completed"
    run_id: str
    status: RunStatus = RunStatus.COMPLETED
    steps_executed: int
    last_outputs: dict[str, Any] = Field(default_factory=dict)
    channel_values: dict[str, Any] = Field(default_factory=dict)
    # Why the run ended early, when it did: ``{reason, says, step}`` (``executor/run_stop.py``),
    # the same record the run store writes to ``workflow.run.metadata.stopped``.
    stopped: dict[str, Any] | None = None


class RunFailedEvent(_EventBase):
    event: Literal["run_failed"] = "run_failed"
    run_id: str
    status: RunStatus = RunStatus.FAILED
    steps_executed: int
    error_type: str
    error_message: str


class RunCancelledEvent(_EventBase):
    """Fired when the scheduler observed a cancel signal between super-steps.

    Produced by the cancel_check hook (router or worker writes
    ``wf_run.status = 'cancelling'``; scheduler polls between steps, sees
    the flag, emits this event + terminates). A final checkpoint is saved
    before this event so a resume could in theory un-cancel — but the
    default UX treats canceled as terminal.

    ``reason`` distinguishes the two cancel paths: 'graceful' (default —
    scheduler observed canceling status between steps and exited cleanly)
    vs 'immediate' (the router canceled the asyncio task, the scheduler's
    per-node CancelledError handler recorded the partial state) vs
    'candidate_stopped' (a mandate-candidate run reached a node containment
    does not allow — ``RunResult.candidate_stopped`` names it; see
    ``matrx_graph.candidate``).
    """

    event: Literal["run_cancelled"] = "run_cancelled"
    run_id: str
    status: RunStatus = RunStatus.CANCELLED
    steps_executed: int
    reason: Literal["graceful", "immediate", "candidate_stopped"] = "graceful"


class RunPausedEvent(_EventBase):
    """Fired when the scheduler observed a pause request between super-steps.

    Same mechanic as RunCancelledEvent but the run stays alive — its status
    becomes ``paused`` and resume-from-pause re-enters the loop at the last
    saved checkpoint. The user keeps full access to upstream node outputs
    while the run is paused.
    """

    event: Literal["run_paused"] = "run_paused"
    run_id: str
    status: RunStatus = RunStatus.PAUSED
    steps_executed: int
    checkpoint_id: str | None = None


class RunResumedEvent(_EventBase):
    """THE paused/parked → running transition, fired at the top of every
    resume leg (``Scheduler.resume``, before the first super-step).

    A resume does NOT re-fire ``run_started`` — this is the only status
    frame the run's own event stream carries between the park event and
    whatever the resumed leg ends in, so a client folding that stream
    depends on it to leave the parked status.

    Carries the mode so the UI can render the right copy ("Resuming from
    pause", "Answering the question"). The seam derives it from the
    checkpoint: an interrupt payload means ``interrupt``, anything else
    (pause park, errored park behind skip / manual / retry) means
    ``pause``. Copy only — no behavior keys off it.
    """

    event: Literal["run_resumed"] = "run_resumed"
    run_id: str
    from_checkpoint_id: str
    mode: Literal["pause", "interrupt", "user_skip", "user_manual", "retry"]
    # WHY the run is resuming, when it is not a person's act. ``server_restart`` = the
    # server running it stopped (a deploy or a crash) and the recovery lane picked it up
    # from its last checkpoint: every step in ``restarted_node_ids`` was cut off mid-way
    # and starts again from scratch. Without it the run log went from a step's progress
    # straight to a bare resume, and the step looked frozen for minutes (run 9453a819).
    reason: Literal["server_restart"] | None = None
    restarted_node_ids: list[str] = Field(default_factory=list)


class RunErroredEvent(_EventBase):
    """Fired when a node raised but the run is parked (recoverable).

    Replaces the terminal RunFailedEvent for the recoverable-error path.
    The scheduler emits this when a node executor throws, records a
    NodeOutcome row with the error set, saves a checkpoint with the failed
    next_invocations preserved, and exits with status=ERRORED. The user
    can recover via /runs/:id/nodes/:nid/{retry,skip,manual-result}.

    RunFailedEvent is still emitted for non-recoverable scheduler errors
    (compile failures, max_steps exceeded, unhandled framework
    exceptions).
    """

    event: Literal["run_errored"] = "run_errored"
    run_id: str
    status: RunStatus = RunStatus.ERRORED
    steps_executed: int
    node_id: str
    step: int
    attempt: int
    error_type: str
    error_message: str
    checkpoint_id: str | None = None


class NodeProgressEvent(_EventBase):
    """Mid-node progress signal (BS-6 — the long-node progress-insight primitive).

    Long actions (multi-source analysis, TTS renders, batch ingestion)
    used to be a black box between node_started and node_completed — the
    canvas froze for minutes and users assumed a hang. Executors emit
    this via ``ctx.progress(...)``: best-effort, NEVER load-bearing
    (a lost progress event changes nothing about execution).

    ``fraction`` is 0.0–1.0 when a total is known; ``current``/``total``
    carry discrete counts ("3/10 sources"); ``message`` is the human
    line ("analyzing example.com").
    """

    event: Literal["node_progress"] = "node_progress"
    run_id: str
    step: int
    node_id: str
    attempt: int = 1
    dispatch_id: str = ""
    item_index: int = 0
    message: str = ""
    fraction: float | None = None
    current: int | None = None
    total: int | None = None


class NodeCostEvent(_EventBase):
    """Cost/usage settlement for one node invocation (the live spend ticker).

    Emitted by the scheduler immediately after ``node_completed`` when the
    node's output carries an AI usage block (the ``AiExecutionResult.usage``
    contract: a dict with ``cost_usd`` / ``input_tokens`` / ``output_tokens``).
    One event per settled node invocation — low frequency, durable (recorded
    in the node-events audit trail) so replay/reconnect shows costs.

    The figures come from the SAME billed-usage aggregation that lands in the
    per-request cost rows — this event is a live projection of that truth,
    never a second pricing derivation. The durable per-run cost rollup stays
    the reconciliation source.
    """

    event: Literal["node_cost"] = "node_cost"
    run_id: str
    step: int
    node_id: str
    spec_type: str | None = None
    attempt: int = 1
    dispatch_id: str = ""
    item_index: int = 0
    cost_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    # Prompt-cache tokens (``AiUsage.cached_input_tokens`` / ``cache_write_tokens``): input read from the cache
    # and input written to it. Billed at their own rates, so a dashboard needs them beside input/output.
    cached_input_tokens: int = 0
    cache_write_tokens: int = 0
    # Primary model (highest-cost contributor) + every model that billed.
    model: str | None = None
    models: list[str] = Field(default_factory=list)
    conversation_id: str | None = None
    request_id: str | None = None
    # True = the spend of an attempt a server restart cut off. The step started again, so
    # this attempt never settled its own cost; the resume settles it from the request
    # ledger so the step's cost counts BOTH attempts (run 9453a819 showed $0.99 of $1.41).
    interrupted: bool = False


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def node_cost_from_output(
    output: dict[str, Any],
    *,
    run_id: str,
    step: int,
    node_id: str,
    spec_type: str,
    attempt: int,
    dispatch_id: str = "",
    item_index: int = 0,
) -> NodeCostEvent | None:
    """Build a ``NodeCostEvent`` from a completed node's output dump, if the
    output carries a non-zero AI usage block. Defensive by contract — this
    runs on EVERY node completion and must never raise; a malformed usage
    shape yields ``None`` (no event), never a broken run.
    """
    try:
        usage = output.get("usage")
        if not isinstance(usage, dict):
            return None
        cost_usd = _num(usage.get("cost_usd")) or 0.0
        input_tokens = int(_num(usage.get("input_tokens")) or 0)
        output_tokens = int(_num(usage.get("output_tokens")) or 0)
        total_tokens = int(_num(usage.get("total_tokens")) or 0) or (input_tokens + output_tokens)
        cached_input_tokens = int(_num(usage.get("cached_input_tokens")) or 0)
        cache_write_tokens = int(_num(usage.get("cache_write_tokens")) or 0)
        if cost_usd <= 0.0 and input_tokens <= 0 and output_tokens <= 0:
            return None

        models_raw = usage.get("models")
        model_names: list[str] = []
        primary: str | None = None
        if isinstance(models_raw, dict) and models_raw:
            model_names = [str(k) for k in models_raw]

            def _model_cost(key: str) -> float:
                entry = models_raw[key]
                if isinstance(entry, dict):
                    # Producers write "cost_usd" (AiUsage per-model buckets);
                    # accept legacy "cost" too so an older shape still ranks.
                    value = _num(entry.get("cost_usd"))
                    if value is None:
                        value = _num(entry.get("cost"))
                    return value or 0.0
                return 0.0

            # Primary model = the one that cost the most this node.
            primary = str(max(models_raw, key=_model_cost))

        conversation_id = output.get("conversation_id")
        request_id = output.get("request_id")
        return NodeCostEvent(
            run_id=run_id,
            step=step,
            node_id=node_id,
            spec_type=spec_type,
            attempt=attempt,
            dispatch_id=dispatch_id,
            item_index=item_index,
            cost_usd=round(cost_usd, 6),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cached_input_tokens=cached_input_tokens,
            cache_write_tokens=cache_write_tokens,
            model=primary,
            models=model_names,
            conversation_id=str(conversation_id) if conversation_id else None,
            request_id=str(request_id) if request_id else None,
        )
    except Exception:  # noqa: BLE001 — cost projection is never load-bearing
        import logging

        logging.getLogger(__name__).warning(
            "node_cost_from_output failed (run=%s node=%s) — cost tick lost",
            run_id[:8],
            node_id,
            exc_info=True,
        )
        return None


class NodeEmittedEvent(_EventBase):
    """A node sent data to the frontend mid-run (the ``output.to_frontend`` node).

    A non-blocking side-channel: the run continues unaffected. ``mode`` tags
    what is being sent (a confirmation, a summary, the full data, or a
    restructured shape); ``payload`` is the already-transformed content
    (non-dict results are wrapped as ``{"value": ...}``); ``component_ref``
    names a safe, agent-authored custom render component — a
    ``tool_ui.tool_name`` on ``surface`` — or None for the generic renderer.
    ``presentation`` says HOW to show it: ``panel`` (the step's normal window
    panel, the default) or ``showcase`` (a dedicated large, centered
    presentation of just this payload — its kind component when the value is
    a ``__kind`` instance). Recorded in wf_node_events so a re-opened run
    re-renders its emissions.
    """

    event: Literal["node_emitted"] = "node_emitted"
    run_id: str
    step: int
    node_id: str
    # Fan-out identity (SPEC §5.2) — the same two correlation fields every
    # other durable event carries, so fifty emissions from one fanned node are
    # fifty separable cards instead of one indistinguishable pile. Defaults
    # ""/0 keep every existing client byte-compatible.
    dispatch_id: str = ""
    item_index: int = 0
    attempt: int = 1
    mode: Literal["confirmation", "summary", "full", "restructured"] = "full"
    payload: dict[str, Any] = Field(default_factory=dict)
    # What a screen view left out of ``payload`` (see ``NodeCompletedEvent.withheld``).
    withheld: list[WithheldValue] | None = None
    # How many further cuts were left out of ``withheld`` (it lists at most the ``workflow.event_payload.withheld_list_max`` knob).
    withheld_more: int | None = None
    component_ref: str | None = None
    surface: str = "matrx-user/workflow"
    title: str | None = None
    presentation: Literal["panel", "showcase"] = "panel"
    # The emission's kind verdict — the same hand-off as node_completed's
    # output_kind / output_kind_ok / metadata.__ir, for the emitted payload:
    # ``kind`` is what the payload says it is (root ``__kind``), ``kind_ok``
    # the registry verdict (None = no kind / check degraded, never a pass),
    # ``metadata["__ir"]`` the canonical wire-elided envelope on a verified
    # pass (root.value rides ``payload``) so the screen renders the real kind
    # component without re-parsing. All additive; absent = classify locally.
    kind: str | None = None
    kind_ok: bool | None = None
    metadata: dict[str, Any] | None = None
    # A SCREEN NEVER LIES. ``empty_values`` names the top-level keys of this
    # payload whose value is an ALL-ZERO structure — schema-valid and carrying
    # nothing (``matrx_graph.emptiness``) — and ``empty_notice`` is the plain
    # sentence saying so. Live 2026-09-12, run 9347de24…: this event carried a
    # full letter under ``watsons_words`` and a hollow
    # ``{"instructions": [], "headline_finding": "", …}`` under ``the_regimen``,
    # and the parent was shown both as her finished answer with nothing said.
    # A presenter MUST NOT render a named empty value as a completed part of
    # the answer. Additive: absent = nothing was empty.
    empty_values: list[str] = Field(default_factory=list)
    empty_notice: str | None = None


class SubgraphRunLinkedEvent(_EventBase):
    """A subgraph.call node started (or reattached to) a DURABLE child run.

    Emitted on the PARENT run's stream the moment the child's identity is
    known — before the child executes — so the canvas can render a live
    child-run chip on the subgraph node (status + drill-in link) instead of
    a black box. ``reattached`` distinguishes a fresh child from a replay /
    recovery resume of a persisted one. Recorded in wf_node_events so a
    re-opened parent restores the link.
    """

    event: Literal["subgraph_run_linked"] = "subgraph_run_linked"
    run_id: str
    step: int
    node_id: str
    dispatch_id: str = ""
    item_index: int = 0
    child_run_id: str
    child_definition_id: str
    child_definition_name: str | None = None
    reattached: bool = False
    child_status: str = "running"


class WorkSetProgressEvent(_EventBase):
    """Live progress of a run's durable work set (matrx_graph.workset).

    Emitted by ``control.work_queue`` on every firing — one event per wave —
    so the canvas can show incremental-discovery progress ("14 found · 6 in
    progress · 8 done") on the queue's node card. Best-effort, never
    load-bearing (mirrors ctx.progress). Recorded in wf_node_events so a
    re-opened run restores the same badge state.
    """

    event: Literal["work_set_progress"] = "work_set_progress"
    run_id: str
    step: int
    node_id: str
    set_name: str = "default"
    wave: int = 1
    dispatched: int = 0
    pending: int = 0
    in_progress: int = 0
    succeeded: int = 0
    failed: int = 0
    dead_letter: int = 0
    discovered: int = 0
    done: bool = False


WorkflowEvent = (
    RunStartedEvent
    | NodeStartedEvent
    | NodeCompletedEvent
    | NodeSkippedEvent
    | NodeFailedEvent
    | NodeRetryScheduledEvent
    | NodeProgressEvent
    | CheckpointSavedEvent
    | RunInterruptedEvent
    | RunCompletedEvent
    | RunFailedEvent
    | RunCancelledEvent
    | RunPausedEvent
    | RunResumedEvent
    | RunErroredEvent
    | NodeEmittedEvent
    | NodeCostEvent
    | WorkSetProgressEvent
    | SubgraphRunLinkedEvent
)
