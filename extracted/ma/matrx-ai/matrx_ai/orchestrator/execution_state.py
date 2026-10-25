"""Per-execution mutable state — owned by exactly one executor task.

This module is the new home for everything that used to live as scratch keys
on ``AppContext.metadata``: reserved cx_request / cx_message UUIDs, the
in-flight provider snapshot payload, the current iteration number, and any
other strictly per-execution data the orchestrator needs to thread between
its own helpers and the persistence / snapshot writers.

Design contract
---------------
``AppContext`` is request-stable identity + scope.  ``ExecutionState`` is
the *mutable, owned, per-executor* slot.  The two MUST stay separate:

- ``AppContext`` may legitimately be shared across concurrent tasks within
  one request (one HTTP stream, one workflow run).  Mutating shared state
  there is a category-of-bugs we want gone forever.
- ``ExecutionState`` is created exactly once per ``execute_until_complete``
  call.  Concurrent executors (parallel agents inside a workflow super-step,
  child agents, sub-workflows) each get their own instance via the
  ContextVar fork that ``asyncio.create_task`` performs implicitly.

Background tasks (the snapshot writer, fire-and-forget persistence) MUST
NOT read the live state object — they read a frozen ``ExecutionStateSnapshot``
copied at task-creation time.
"""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # Avoid a circular import — matrx_ai.persistence imports execution_state.
    from matrx_ai.persistence.coordinator import WriteCoordinator


@dataclass(slots=True)
class ExecutionStateSnapshot:
    """Frozen point-in-time copy of an ExecutionState.

    Use this for fire-and-forget background tasks (snapshot writer) so the
    background task never reads a dict that the main loop is still mutating.
    """

    iteration: int
    reserved_message_ids: dict[int, str]
    reserved_request_ids: dict[int, str]
    last_model: str | None


@dataclass(slots=True)
class ExecutionState:
    """Mutable scratch for one ``execute_until_complete`` invocation.

    Owned by the executor task that created it.  Read by the executor's
    helpers (``_finalize_and_persist``, the snapshot writer, the persistence
    layer) via the ``execution_state`` ContextVar.
    """

    # Iteration counter — incremented at the top of each main-loop pass.
    iteration: int = 0

    # TIME TO FIRST TOKEN — one definition for every run (chat, agent, mandate,
    # batch, MCP, sub-agent), owned by the execution, never by an emitter.
    # ``time.time()`` stamped ONCE by ``send_once`` (orchestrator/first_output.py)
    # at the first text or reasoning delta, or at the first provider response
    # when nothing streamed. Measured from the SAME origin as total_duration:
    # the first iteration's ``TimingUsage.start_time``.
    ttft_first_output_at: float | None = None

    # Reserved cx_message.id keyed by message position.  Populated by the
    # executor before the user/assistant rows are touched so the frontend
    # has stable anchors and persistence can do UPDATE-by-id later.
    reserved_message_ids: dict[int, str] = field(default_factory=dict)

    # Reserved cx_request.id keyed by iteration number.  The duplicate-key
    # bug that drove this redesign came from this dict being shared across
    # parallel agents via ``ctx.metadata``.  It now lives here, owned.
    reserved_request_ids: dict[int, str] = field(default_factory=dict)

    # The metadata of the request this execution runs (``AIMatrixRequest.metadata``), read-only.
    # The conversation and message writers under this execution hand it to the host's
    # stored-values screen (``db/stored_values_screen.active_request_metadata``): a door that
    # names its run on the REQUEST (a held code call, a NamedAgent, a raw mandate agent) is seen
    # as that run before its conversation row is created, never only on the context.
    request_metadata: dict[str, Any] | None = None

    # The provider's final SDK-ready request dict for the most recent
    # iteration.  Set by ``capture_request_payload`` (in
    # ``matrx_ai.providers.snapshot``) right before each provider call;
    # popped by the executor immediately after.  Strictly transient.
    snapshot_payload: Any | None = None

    # The provider that produced ``snapshot_payload``, stamped at the SAME
    # seam by the SAME call (each provider's ``execute()`` passes its own
    # literal name to ``capture_request_payload``). This is the authoritative
    # provider identity for the snapshot row: ``UnifiedResponse.metadata`` does
    # NOT carry a "provider" key, so the writer's metadata read always fell
    # through to "unknown" on the success path — invisible while capture was
    # opt-in (2 rows/day), a corrupt `provider` column on every row once
    # capture went always-on (D-33). Popped with the payload.
    snapshot_provider: str | None = None

    # Every setting this turn's outbound seams dropped, clamped or translated —
    # ``outbound_params.publish_settings_adjustments`` appends, the executor pops
    # it WITH ``snapshot_payload`` into ``chat.request_snapshot.metadata``
    # (PB-03 defect 7: an adjustment is stored with the request, never only logged).
    settings_adjustments: list[dict[str, Any]] | None = None

    # Where this send's translator put the platform's per-turn text (owner decision,
    # defects 23 + 35, ruling L29: its own host turn on every provider, or the end of the
    # system message for a ``strict_role_alternation`` model). Set by ``base_translator.record_platform_text_placement``;
    # the executor pops it WITH ``snapshot_payload`` into
    # ``chat.request_snapshot.metadata.platform_text_placement``.
    platform_text_placements: list[dict[str, Any]] | None = None

    # The id the provider-call-failure snapshot WILL be written under, allocated
    # before each provider call of a persisted run. A settings-rejection record
    # (failure_report, filed from inside the call) links it as
    # ``request_snapshot_id`` before the snapshot row exists; the failure writer
    # then uses exactly this id. None on ephemeral runs (no snapshot is written).
    failure_snapshot_id: str | None = None

    # Best-effort label of the last model the executor talked to — used by
    # the snapshot writer when the response object doesn't carry it.
    last_model: str | None = None

    # Serve-once value-store keys from the MOST RECENT tool batch. Stubbed only
    # after the NEXT provider response consumes them (the turn-directive drain
    # in the loop / at finalize) — stamping at tool completion would let a
    # rebuild in the completion→send window stub content the model never saw.
    pending_auto_stub_keys: list[str] = field(default_factory=list)

    # Per-request deferred-write coordinator. Lazily created by the persistence
    # module's queue helpers on first queue() call; lives until the lane's
    # drain finalizer flushes it. NEVER read in fire-and-forget background
    # tasks — they should use a fresh coordinator scoped to the parent task
    # via the ContextVar fork that asyncio.create_task() performs implicitly.
    writes: WriteCoordinator | None = None

    # In-flight persist context. The main loop keeps these current as it runs
    # so that if the request is CANCELED mid-stream (client disconnect, server
    # shutdown), the outer ``execute_until_complete`` can shield-persist the
    # accumulated cost/usage instead of losing it. ``cancel_persist_done`` is
    # the idempotency guard so a normal completion that races a cancel doesn't
    # double-persist. This is the close-the-loop guarantee: a disconnect can
    # never again eat the cost data.
    current_request: Any | None = None
    trigger_position: int = 0
    pre_execution_message_count: int = 0
    # The trigger message OBJECT at execution start. Every position above is an
    # index into the live list, so the list may only GROW during a turn. The
    # barrier checks this object is still at ``trigger_position`` and screams
    # (``persisted_history_shifted``) when anything removed or inserted history
    # mid-turn — the class that silently stopped admin@admin.com's staff thread
    # from writing chat.message (Lane AZ, 2026-09-28).
    trigger_message: Any | None = None
    # The history as the ledger knew it: the list at execution start, refreshed after
    # every turn barrier. Object refs only (no copies). When a mutator shifts the live
    # list mid-turn, the barrier restores this prefix and keeps what was appended after
    # it, so the reply is stored instead of refused (defect 50, 2026-10-19).
    recorded_history: list[Any] | None = None
    # cx_message.id of every message ALREADY persisted (loaded from the DB)
    # before this execution started. Persistence must never re-INSERT these —
    # on a retry (user_input=None) the conversation's existing messages are
    # reloaded into config.messages, and without this guard the loaded user
    # message gets a fresh UUID and is duplicated. Captured once at start.
    pre_existing_message_ids: set[str] = field(default_factory=set)
    # First message position this turn persists: one past the stored history. Equal to the
    # trigger on a continuation; on turn 1 it is 0, so every authored input message before the
    # trigger (few-shot pairs, the template a client-carried door sends) is stored in order and
    # turn 2 reloads exactly the history the model saw.
    persist_from_position: int | None = None
    persisted: bool = False
    # The provider response whose tool calls are being dispatched RIGHT NOW —
    # set just before ``handle_tool_calls`` and cleared the moment the loop's
    # ``add_response`` carries it (with its real results) into
    # ``current_request``. While set, the assistant tool_use turn exists ONLY
    # here: an interrupt (cancel / disconnect / iteration error) must attach it
    # with an honest result per call, or the tool_use and its tool-result
    # message are never persisted and every chat.tool_call row of the turn is
    # left with message_id NULL (see ``_attach_interrupted_tool_turn``).
    tool_dispatch_response: Any | None = None

    # Per-turn commit-barrier cursors (the high-water-mark of what has been
    # DURABLY committed). The orchestrator advances these only after a turn's
    # synchronous ``coordinator.finalize()`` succeeds. Per-turn persistence is
    # scoped to rows ABOVE these marks, so a rolled Session never re-INSERTs an
    # already-committed row. ``committed_position`` is the highest cx_message
    # position committed; ``committed_iteration`` is the highest cx_request
    # iteration committed. See the persistence contract in CLAUDE.md.
    committed_position: int = -1
    committed_iteration: int = 0

    # Loop-guard intervention flags. When the rolling tool-failure window trips
    # the guard, we DON'T silently end the run — we disable all tools and let
    # the model do ONE final tool-less turn to explain the situation to the
    # user (resumable). ``loop_guard_intervened`` records that this happened so
    # the normal no-tool-calls completion path finalizes the run as 'paused'
    # rather than 'completed'. ``loop_guard_warned`` makes the approaching-limit
    # caution fire at most once.
    loop_guard_intervened: bool = False
    loop_guard_warned: bool = False

    # THE CEILING NEVER ENDS WITHOUT AN ANSWER (2026-10-21). When the run reaches
    # its iteration ceiling after a tool round, it does not just stop on a tool
    # call: tools are switched off and the model gets ONE more turn to write its
    # result (what is done, what is left, where it stopped). ``ceiling_wrap_up``
    # marks that turn — the completion path records it as
    # ``max_iterations_exceeded`` (never a clean 'completed'), and the loop allows
    # exactly one iteration past the ceiling for it. ``ceiling_warned`` makes the
    # "few rounds left" notice fire at most once.
    ceiling_wrap_up: bool = False
    ceiling_warned: bool = False

    # THE CEILINGS IN FORCE FOR THIS RUN. Resolved once, from the org's
    # ``orchestration.loop_guard`` settings rows, and reused every iteration —
    # a per-iteration read would put a Postgres round trip on the hot loop for
    # numbers that cannot change mid-run. ``LoopGuardThresholds``; typed Any so
    # execution_state stays free of the guard module.
    loop_guard_thresholds: Any | None = None

    # ONE TOOL, NOT EVERY TOOL (2026-09-20). Tools this run has already switched
    # off. The run CONTINUES on the rest, so the guard must never re-blame a
    # tool it has already removed — the failures are still in the window and it
    # would trip forever on an answer it already gave.
    loop_guard_disabled_tools: list[str] = field(default_factory=list)

    # At most one "keep going" verdict per run. A standoff decision that says
    # continue is a real second chance; an unbounded stream of them is a way to
    # spend the user's money on the same broken tool forever.
    loop_guard_standoff_continued: bool = False

    # THE GUARD'S REASON TRAVELS. The guard knows WHICH tool failed, HOW MANY
    # times and WHAT it said; captured here at the moment it trips so the
    # finalizing turn — which runs with tools already stripped and a fresh
    # health verdict — can still put that evidence in the completion metadata.
    # Without it the run recorded ``paused_loop_guard: no error detail
    # recorded`` while the executor held the whole diagnosis (live 2026-09-12,
    # workflow run ``6fa6ad90``, node ``n_check``).
    loop_guard_health: dict[str, Any] | None = None
    loop_guard_evidence: dict[str, Any] | None = None

    # Required-member (designated member, C-26) intervention flags. When the
    # run tries to finish without successfully calling a member its Orchestra
    # declared required, the executor injects a course-correction notice and
    # forces ONE turn restricted to the missing member tool(s)
    # (tool_choice='required'). ``required_member_intervened`` is the one-shot
    # flag — a second miss is terminal (chat: paused_required_member_skipped;
    # workflow step: failed). ``required_member_forced_pending`` marks that the
    # NEXT provider turn runs restricted; the loop restores the saved toolset
    # (``required_member_saved_tools`` = (tools, custom_tools, tool_choice))
    # before dispatching that turn's tool calls.
    required_member_intervened: bool = False
    required_member_forced_pending: bool = False
    required_member_saved_tools: Any | None = None

    # THE CHANGE-CLAIM GATE (``orchestrator/change_claims.py``). How many forced
    # correction turns this run has already spent because a reply asserted a
    # change the turn never wrote. Bounded by the mandate's own budget knob
    # (``mandate_honesty.change_claim_correction_turns``), which the host hands
    # over with the authoring declaration; when it is spent the person is TOLD
    # nothing was saved rather than the run quietly accepting the claim.
    change_claim_corrections: int = 0

    # THE ANSWER CHECK (``orchestrator/answer_checks.py``): corrective turns spent because the finishing answer broke
    # a rule its own kind sets (host seam ``answer_check``; knob ``mandate_honesty.answer_check_correction_turns``).
    answer_check_corrections: int = 0

    # BLANK-TURN CONTINUATION (``_drop_blank_turn_for_continuation``). A model
    # that ends a turn with no visible output (reasoning only / nothing at all
    # — live: Gemini Pro after tool results) gets ONE continuation turn that
    # asks for the answer before the run is failed. One-shot per run.
    empty_reply_continuations: int = 0

    # A TOOL CALL WRITTEN AS TEXT (``orchestrator/text_tool_calls.py``). A turn
    # whose text carried tool-call markup and made no real call is re-asked ONCE
    # with a host notice; a second time ends with the markup removed and a note.
    text_tool_call_reasks: int = 0

    def snapshot(self) -> ExecutionStateSnapshot:
        """Return a frozen copy safe to hand to a background task."""
        return ExecutionStateSnapshot(
            iteration=self.iteration,
            reserved_message_ids=dict(self.reserved_message_ids),
            reserved_request_ids=dict(self.reserved_request_ids),
            last_model=self.last_model,
        )


# ---------------------------------------------------------------------------
# ContextVar plumbing — task-local; child asyncio tasks inherit a snapshot
# of the parent's value at create_task() time, which is the property the
# executor relies on for child-agent / parallel-step isolation.
# ---------------------------------------------------------------------------

_execution_state: ContextVar[ExecutionState | None] = ContextVar(
    "execution_state", default=None
)


def set_execution_state(state: ExecutionState) -> Token:
    return _execution_state.set(state)


def get_execution_state() -> ExecutionState:
    state = _execution_state.get(None)
    if state is None:
        raise RuntimeError(
            "No ExecutionState is set.  Code that reads execution-scoped "
            "scratch (reserved IDs, snapshot payload, iteration counter) "
            "must run inside execute_until_complete() — which sets the "
            "ContextVar via set_execution_state() at entry."
        )
    return state


def try_get_execution_state() -> ExecutionState | None:
    return _execution_state.get(None)


def clear_execution_state(token: Token) -> None:
    _execution_state.reset(token)


# ---------------------------------------------------------------------------
# Run usage sink — what an agent run spent, readable even when it ended early.
#
# ``run_agent`` opens a sink before ``Agent.execute``; the FIRST
# ``execute_until_complete`` under it binds its ExecutionState. When the run is
# canceled (a per-call time limit, a client disconnect, a sibling's gather
# cancel, a budget stop) or crashes out of the loop, ``Agent.execute`` raises
# instead of returning — and the usage accumulated on the in-flight request
# would otherwise never reach the run's settle, which then recorded $0 (news
# run 70601b15, 2026-10-05: ~$0.70 under-recorded). The sink is how the early
# exit settles the real spend.
#
# Binding is first-wins: a tool that calls the loop directly inside the run
# (no ``run_agent`` of its own) must never re-point the run's sink at its own
# request. A nested ``run_agent`` opens its own sink, so a child's spend stays
# on the child (matching ``usage_history``'s own no-double-count rule).
# ---------------------------------------------------------------------------


@dataclass
class RunUsageSink:
    state: ExecutionState | None = None

    def usage_history(self) -> list[Any]:
        request = self.state.current_request if self.state is not None else None
        return list(getattr(request, "usage_history", None) or [])


_run_usage_sink: ContextVar[RunUsageSink | None] = ContextVar("run_usage_sink", default=None)


def open_run_usage_sink() -> tuple[RunUsageSink, Token]:
    sink = RunUsageSink()
    return sink, _run_usage_sink.set(sink)


def close_run_usage_sink(token: Token) -> None:
    try:
        _run_usage_sink.reset(token)
    except ValueError:  # token from another Context (a task hop) — just unbind
        _run_usage_sink.set(None)


def bind_run_usage_sink(state: ExecutionState) -> None:
    sink = _run_usage_sink.get(None)
    if sink is not None and sink.state is None:
        sink.state = state
