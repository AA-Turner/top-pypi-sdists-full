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

    # Reserved cx_message.id keyed by message position.  Populated by the
    # executor before the user/assistant rows are touched so the frontend
    # has stable anchors and persistence can do UPDATE-by-id later.
    reserved_message_ids: dict[int, str] = field(default_factory=dict)

    # Reserved cx_request.id keyed by iteration number.  The duplicate-key
    # bug that drove this redesign came from this dict being shared across
    # parallel agents via ``ctx.metadata``.  It now lives here, owned.
    reserved_request_ids: dict[int, str] = field(default_factory=dict)

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
    writes: "WriteCoordinator | None" = None

    # In-flight persist context. The main loop keeps these current as it runs
    # so that if the request is CANCELLED mid-stream (client disconnect, server
    # shutdown), the outer ``execute_until_complete`` can shield-persist the
    # accumulated cost/usage instead of losing it. ``cancel_persist_done`` is
    # the idempotency guard so a normal completion that races a cancel doesn't
    # double-persist. This is the close-the-loop guarantee: a disconnect can
    # never again eat the cost data.
    current_request: Any | None = None
    trigger_position: int = 0
    pre_execution_message_count: int = 0
    # cx_message.id of every message ALREADY persisted (loaded from the DB)
    # before this execution started. Persistence must never re-INSERT these —
    # on a retry (user_input=None) the conversation's existing messages are
    # reloaded into config.messages, and without this guard the loaded user
    # message gets a fresh UUID and is duplicated. Captured once at start.
    pre_existing_message_ids: set[str] = field(default_factory=set)
    persisted: bool = False

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
