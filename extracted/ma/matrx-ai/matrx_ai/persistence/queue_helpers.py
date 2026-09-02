"""cx_-specific queue helpers — what every cx_ call site should use.

These wrap :meth:`WriteCoordinator.queue` with the right table name, the
right ``depends_on`` declaration, and the right primary-key extraction.
Call sites read like the original ``cxm.X.create_*`` / ``update_*`` they
replace — but they never await and never touch the DB.

The coordinator is resolved from the current :class:`ExecutionState` (a
ContextVar). On the first call within a request, we:

    1. Construct the coordinator (lazy init).
    2. Attach it to ``state.writes``.
    3. Register a lane finalizer so end-of-stream / error / cancel all
       reach ``coordinator.flush()`` via the same code path.
    4. Lazily register every cx_ table → Model class binding in the
       persistence registry so the flush executor can find them.

If no ExecutionState is set, the queue call is logged + dropped — that's
a programmer bug (the queue helpers are not meant for non-request scopes).
Scheduled and background owners use :func:`standalone_coordinator`, which
provides its own synchronous commit barrier without requiring a RequestLane.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any

from matrx_connect.lane import FinalizerContext, get_current_lane
from matrx_utils import detached_task, vcprint

from matrx_ai.orchestrator.execution_state import try_get_execution_state
from matrx_ai.persistence.coordinator import Coordinator
from matrx_ai.persistence.postgres_text import sanitize_postgres_text
from matrx_ai.persistence.registry import register_table

logger = logging.getLogger("matrx_ai.persistence.queue_helpers")


# cx_ tables that carry a NOT-NULL organization_id (2026-06 schema reorg). Every
# INSERT into one of these must stamp the request's org or the not-null constraint
# rejects it. This is the single chokepoint for cx_message / cx_tool_call (which
# never pass through the conversation gate); conversation / user_request are also
# stamped here as belt-and-suspenders behind their gate-side stamp. Tables WITHOUT
# the column (request / request_snapshot / tool_trace / media) MUST NOT appear here
# — stamping a non-existent column would fail the INSERT.
_ORG_SCOPED_INSERT_TABLES: frozenset[str] = frozenset(
    {
        "chat.conversation",
        "chat.user_request",
        "chat.message",
        "chat.tool_call",
        "chat.observational_memory",
        "chat.agent_memory",
    }
)


# ContextVar fallback for the coordinator — used when ExecutionState isn't
# yet set (the conversation gate runs before execute_until_complete creates
# the ExecutionState). Lives per task scope via asyncio.create_task's
# copy_context(), so concurrent requests don't share a coordinator.
_coordinator_cv: ContextVar[Coordinator | None] = ContextVar("matrx_coordinator", default=None)


# ---------- coordinator resolution / lifecycle ----------------------------


def _ensure_cx_registered() -> None:
    """Bind every cx_ table → Model class. Idempotent; safe to call repeatedly."""
    # Lazy import — cxm depends on the host having called matrx_ai.configure().
    from matrx_ai.db.cx_managers import cxm

    register_table("chat.conversation", cxm.conversation.model)
    register_table("chat.user_request", cxm.user_request.model)
    register_table("chat.message", cxm.message.model)
    register_table("chat.request", cxm.request.model)
    register_table("chat.request_snapshot", cxm.request_snapshot.model)
    register_table("chat.tool_call", cxm.tool_call.model)
    register_table("chat.tool_trace", cxm.tool_trace.model)
    register_table("chat.observational_memory", cxm.om_memory.model)
    register_table("chat.observational_memory_event", cxm.om_event.model)
    register_table("chat.media", cxm.media.model)
    register_table("chat.agent_memory", cxm.agent_memory.model)


def _resolve_app_context() -> Any | None:
    """Best-effort fetch of AppContext for correlation IDs. Never raises."""
    try:
        from matrx_connect import try_get_app_context

        return try_get_app_context()
    except Exception:
        return None


def _capture_late_lane_boundary(
    lane: Any,
    ctx: Any | None,
    *,
    table: str,
    op_type: str,
    primary_key: tuple[str, str] | None,
) -> None:
    """Capture the lifecycle defect without retaining the attempted row."""

    async def _capture() -> None:
        from matrx_connect.streaming.error_capture import capture_error

        exc = RuntimeError(
            "Persistence write first reached its coordinator after the request "
            "lane stopped accepting finalizers"
        )
        await capture_error(
            exc,
            kind="persistence_after_lane_drain",
            request_id=getattr(ctx, "request_id", None) if ctx else None,
            user_id=getattr(ctx, "user_id", None) if ctx else None,
            conversation_id=getattr(ctx, "conversation_id", None) if ctx else None,
            route="matrx_ai.persistence.queue_helpers",
            error_type="LatePersistenceBoundary",
            context={
                "lane_phase": getattr(lane, "phase", "unknown"),
                "table": table,
                "op_type": op_type,
                "primary_key_field": primary_key[0] if primary_key else None,
                "primary_key": primary_key[1] if primary_key else None,
            },
        )

    detached_task(_capture(), name="capture_late_persistence_boundary")


def get_coordinator() -> Coordinator | None:
    """Return the current request's :class:`Coordinator`, lazily creating it on first call.

    The Coordinator wraps a :class:`matrx_orm.Session` and is flushed by
    the lane finalizer on every exit path (stream_end / error / cancelled).
    Returns ``None`` when there is no lane to bind to (out-of-request
    code paths log + drop the queue call).

    Resolution order:
      1. :class:`ExecutionState` — set by execute_until_complete (preferred).
      2. The module ContextVar — set by gate code that runs before the
         executor initializes ExecutionState.
      3. Lane is active → create a fresh coordinator and stash it on both.
      4. No lane → return None. Caller (queue helper) logs + drops.

    The lane requirement matters: without a lane, the coordinator's flush
    has no trigger to fire (lane finalizer is the universal exit hook).
    Calls from non-request scopes get dropped — that's a programmer bug
    they should fix by routing through the streaming response infra.

    CLIENT HOST: when a ``conversation_store`` seam is configured, ALL
    conversation persistence delegates to the store at the gate/persist/
    logger choke points — the WriteCoordinator is a server-lane concept and
    must never construct (its ``_ensure_cx_registered`` imports the ORM cx
    managers → ``DBNotConfiguredError`` mid-request). Short-circuit to None
    BEFORE the lane check; matrx-connect always opens a RequestLane, so the
    lane check alone cannot protect a client host.
    """
    from matrx_ai.client_host import get_conversation_store

    if get_conversation_store() is not None:
        return None

    # Register the child-fork hook on first use (idempotent, process-global).
    # This is how sub-agents get their own coordinator scope — see
    # _child_coordinator_scope below.
    _register_child_fork_hook_once()

    state = try_get_execution_state()
    if state is not None:
        coord_from_state: Coordinator | None = getattr(state, "writes", None)
        if coord_from_state is not None:
            return coord_from_state

    coord = _coordinator_cv.get(None)
    if coord is not None:
        # If ExecutionState was just initialized after the coordinator,
        # link the two so the executor's state.writes points at the same
        # object — keeps the convenience reference accurate.
        if state is not None and getattr(state, "writes", None) is None:
            state.writes = coord  # type: ignore[attr-defined]
        # Keep failure-row correlation aligned with the live AppContext.
        # A late request_id override (independent_request fork, test harness
        # reuse) must not leave system_write_failure.request_id pointing at
        # a different UUID than tool_call.user_request_id.
        ctx_live = _resolve_app_context()
        live_rid = getattr(ctx_live, "request_id", None) if ctx_live else None
        if live_rid and getattr(coord, "_request_id", None) != live_rid:
            coord.set_correlation(request_id=live_rid)
        return coord

    lane = get_current_lane()
    if lane is None:
        # No lane → no place to register the flush finalizer → don't bother
        # creating a coordinator that would never flush.
        return None

    ctx = _resolve_app_context()
    lane_accepts_finalizers = getattr(lane, "phase", None) == "active"
    coord = Coordinator(
        request_id=getattr(ctx, "request_id", None) if ctx else None,
        user_id=getattr(ctx, "user_id", None) if ctx else None,
        conversation_id=getattr(ctx, "conversation_id", None) if ctx else None,
        late_write_only=not lane_accepts_finalizers,
    )
    _coordinator_cv.set(coord)
    if state is not None:
        state.writes = coord  # type: ignore[attr-defined]
    _ensure_cx_registered()
    if lane_accepts_finalizers:
        _register_lane_finalizer(coord, lane)
    return coord


@asynccontextmanager
async def standalone_coordinator(
    *,
    reason: str,
    request_id: str | None = None,
    user_id: str | None = None,
    conversation_id: str | None = None,
    database: str | None = None,
) -> AsyncIterator[Coordinator]:
    """Open an isolated, synchronously committed Coordinator for background work."""
    if not reason.strip():
        raise ValueError("standalone_coordinator requires a non-empty reason")

    from matrx_orm.session.session import _session_stack

    _ensure_cx_registered()

    # Background callbacks can inherit both ContextVars and the mutable
    # ExecutionState object from the task that scheduled them. Neither is valid
    # ownership for an independent write: the parent may already be flushing or
    # sealed, and mutating state.writes would also mutate the parent's object.
    # Reset both lookups and restore the ORM Session stack on exit so this scope
    # remains safe even when it is consumed from a long-lived worker task.
    parent_coord_token = _coordinator_cv.set(None)
    parent_state_token = None
    session_stack_token = _session_stack.set(_session_stack.get())
    coordinator: Coordinator | None = None
    try:
        try:
            from matrx_ai.orchestrator.execution_state import _execution_state

            parent_state_token = _execution_state.set(None)
        except ImportError:
            pass

        coordinator = Coordinator(
            database=database,
            request_id=request_id,
            user_id=user_id,
            conversation_id=conversation_id,
        )
        _coordinator_cv.set(coordinator)

        try:
            yield coordinator
        except BaseException:
            # Preserve the caller's exception, but first secure any operation it
            # queued. Session fallback captures failed writes for replay.
            import asyncio

            await asyncio.shield(
                coordinator.drain_and_confirm(reason=f"{reason}_error")
            )
            raise
        else:
            # This scope has no RequestLane finalizer. Durability must therefore
            # be established before control returns to the caller.
            import asyncio

            await asyncio.shield(coordinator.finalize(reason=reason))
    finally:
        try:
            if coordinator is not None:
                await coordinator.seal()
        finally:
            _session_stack.reset(session_stack_token)
            _coordinator_cv.reset(parent_coord_token)
            if parent_state_token is not None:
                from matrx_ai.orchestrator.execution_state import _execution_state

                _execution_state.reset(parent_state_token)


@asynccontextmanager
async def _child_coordinator_scope(label: str, child_ctx: Any):
    """Open a fresh WriteCoordinator scope for a sub-agent.

    Registered as a child-fork hook on matrx-connect's child_agent_context.
    When a sub-agent enters its context:
        0. We finalize the PARENT's coordinator FIRST (fork-side SYNC commit),
           so every ancestor row the child FK-depends on is durable on disk
           before the child writes anything — closing the post-turn-barrier
           window where a detached-but-not-yet-landed ancestor INSERT is
           invisible to the child and gets re-queued as a duplicate. See the
           block comment below for the full race.
        1. We push None into ``_coordinator_cv`` so the sub-agent's first
           queue() call lazily creates its OWN coordinator (not the
           parent's).
        2. We push None into ``_execution_state`` (matrx_ai) so the
           sub-agent's execute_until_complete creates a fresh state —
           which itself owns the new coordinator via the
           ``state.writes`` field.

    When the sub-agent exits:
        3. We flush the sub-agent's coordinator BEFORE the parent's scope
           resumes. After this point, the sub-agent's writes are durably
           on disk. The parent can read them, the labeler can read them,
           the context-state emit can read them.
        4. We restore the parent's coordinator to ``_coordinator_cv``.

    This is the fix for the race documented in the user-reported sub-agent
    bug: a sub-agent's cx_conversation INSERT was being queued in the
    PARENT's coordinator (because ContextVars are inherited on copy_context)
    and only landed at parent stream end — far after the sub-agent's
    labeler / context-state emit tried to read the row.

    See docs/persistence/ORM_SESSION_VISION.md §6.1 — "Session scope =
    Unit of Work scope".
    """
    # ── FORK-SIDE SYNC COMMIT: force ancestor rows durable BEFORE fan-out ──
    #
    # The child opens its OWN coordinator/Session below; the cx_request /
    # cx_message rows it writes FK-depend on ancestor rows the parent already
    # ensured (cx_user_request, cx_conversation). The pending-aware read across
    # the Session stack (matrx_orm.pending_ops_across_stack) makes those ancestor
    # rows VISIBLE so the child never re-queues a duplicate — but that visibility
    # only holds while the parent's INSERT is still pending in an on-stack
    # Session. Once the parent crosses a turn barrier, commit_async ROLLS its
    # Session: the INSERT detaches to a background commit that is no longer on the
    # stack and may not yet be on disk. In that window the child can't see the
    # ancestor (off-stack) and the DB read misses it (commit in flight) → the
    # child re-queues a duplicate INSERT → a *_pkey violation at flush.
    # Finalizing the parent synchronously here closes that window: the ancestor is
    # durable on disk before any child writes, so the child's read sees it and its
    # FK always resolves.
    #
    # This is the "fork" half of the sub-agent fork/join SYNC commit point the
    # persistence contract sanctions (CLAUDE.md). finalize() keeps the parent
    # coordinator OPEN (rolls a fresh empty Session — see Coordinator.seal), so
    # the parent resumes writing normally after the child returns. The
    # individual-write pkey swallow in matrx_orm Session stays as the
    # belt-and-suspenders backstop for a true SIBLING race (two children racing
    # each other, independent of the parent) that this fork-side commit can't see.
    #
    # FAIL FAST: if the parent flush errors, finalize() has already recorded it to
    # system_write_failure and flipped the coordinator to ERRORED; we let it raise
    # (shield protects the in-flight flush from an outer cancel) rather than fork a
    # child whose FK-dependent writes are already doomed.
    parent_coord = _coordinator_cv.get(None)
    if parent_coord is None:
        _parent_state_now = try_get_execution_state()
        parent_coord = getattr(_parent_state_now, "writes", None) if _parent_state_now else None
    if parent_coord is not None:
        import asyncio

        await asyncio.shield(parent_coord.finalize(reason="pre_fan_out"))

    # Save the parent's coordinator (if any) so we can restore it on exit.
    parent_coord_token = _coordinator_cv.set(None)

    # ExecutionState is inherited via copy_context too. Reset it so the
    # child's execute_until_complete creates a fresh one.
    parent_state_token = None
    try:
        from matrx_ai.orchestrator.execution_state import _execution_state

        parent_state_token = _execution_state.set(None)
    except Exception:
        # _execution_state isn't accessible — best effort. The child's
        # execute_until_complete will still build its own state.
        pass

    try:
        # Pin the child's owner before its body can spawn work.  asyncio tasks
        # copy ContextVars at creation time; leaving this scope lazily bound to
        # None lets a child-created task outlive the request lane and first
        # materialize a terminal coordinator after drain.  This is the child
        # equivalent of the MCP edge's eager owner pin.
        lane = get_current_lane()
        if lane is not None and getattr(lane, "phase", None) == "active":
            get_coordinator()
            yield
        elif lane is not None:
            # A child may be launched by an already-scheduled callback after
            # its request lane has completed.  The inherited terminal lane is
            # not an owner: registering a finalizer is impossible and lazily
            # creating against it is precisely persistence_after_lane_drain.
            # Give this independent child an explicit synchronous lifetime.
            async with standalone_coordinator(
                reason="child_agent_after_parent_lane",
                request_id=getattr(child_ctx, "request_id", None),
                user_id=getattr(child_ctx, "user_id", None),
                conversation_id=getattr(child_ctx, "conversation_id", None),
            ):
                yield
        else:
            yield
    finally:
        # Flush the child's coordinator (if it created one). The flush
        # is shielded so an outer cancellation can't interrupt it.
        child_coord = _coordinator_cv.get(None)
        if child_coord is not None:
            try:
                import asyncio

                # Fork/join is a deliberate SYNC commit point: flush the child's
                # cache + drain its in-flight commits before the parent resumes.
                await asyncio.shield(child_coord.finalize(reason="child_agent_exit"))
            except Exception as exc:
                vcprint(
                    f"[child_coordinator_scope] child flush failed: "
                    f"{type(exc).__name__}: {exc}. Watchdog backstop.",
                    color="red",
                )

        # Restore parent's coordinator + execution state.
        _coordinator_cv.reset(parent_coord_token)
        if parent_state_token is not None:
            try:
                from matrx_ai.orchestrator.execution_state import _execution_state

                _execution_state.reset(parent_state_token)
            except Exception:
                pass


def _register_child_fork_hook_once() -> None:
    """Idempotently register the child-coordinator-scope hook with matrx-connect.

    Called on first ``get_coordinator()`` invocation so we don't require an
    explicit configure() step from the host. The registration is process-
    global; subsequent calls are no-ops.
    """
    global _CHILD_FORK_HOOK_REGISTERED
    if _CHILD_FORK_HOOK_REGISTERED:
        return
    try:
        from matrx_connect.context.app_context import register_child_fork_hook

        register_child_fork_hook(_child_coordinator_scope)
        _CHILD_FORK_HOOK_REGISTERED = True
    except Exception as exc:
        # FAIL LOUD, not silent. Without this hook a sub-agent SHARES the
        # parent's coordinator — the exact "closed-parent / can't-find-own-
        # writes" durability failure class this whole system exists to kill
        # (child writes after the parent's session rolled; child reads miss a
        # pending ancestor INSERT → pkey dupes / lost rows). A silent degrade
        # here reintroduces that class invisibly. matrx-connect is a declared
        # hard dependency and ships register_child_fork_hook, so this only
        # fires on genuine version skew / a broken install — which must stop
        # the line, not whisper a warning and run unsafely.
        vcprint(
            f"[queue_helpers] FATAL: could not register the child-fork "
            f"coordinator hook ({type(exc).__name__}: {exc}). Sub-agents would "
            f"SHARE the parent coordinator and silently lose/duplicate writes. "
            f"matrx-connect must expose register_child_fork_hook — upgrade it.",
            color="red",
        )
        raise RuntimeError(
            "child-fork coordinator hook unavailable — refusing to run with "
            "unsafe sub-agent persistence (upgrade matrx-connect)"
        ) from exc


_CHILD_FORK_HOOK_REGISTERED: bool = False


def _register_lane_finalizer(coord: Coordinator, lane: Any) -> None:
    """Hook the coordinator's flush into the lane's drain lifecycle.

    Called exactly once when the coordinator is created. The lane survives
    until drain ends so this registration is safe.
    """

    async def _finalize(ctx: FinalizerContext) -> None:
        reason = ctx.outcome  # "error" | "cancelled" | "stream_end"
        # Backstop on every exit path: DEGRADE-drain (flush the cache + await all
        # in-flight commits, best-effort, never raises). The orchestrator's own
        # finalize / check_pending normally already secured everything; this
        # catches any tail (e.g. an exit before the final commit). Failures are
        # captured to system_write_failure.
        await coord.drain_and_confirm(reason=reason)
        # SEAL after the final drain so any fire-and-forget write that arrives
        # AFTER this point (e.g. a server tool's detached log_completed that
        # finished after a delegation suspend) fires a durable one-shot instead
        # of stranding in a rolled OPEN Session that nothing will ever flush
        # again — the cx_tool_call "stuck at running despite success" class.
        await coord.seal()

    try:
        lane.add_finalizer(_finalize, name="coordinator.commit")
    except Exception as exc:
        vcprint(
            f"[Coordinator] failed to register lane finalizer: "
            f"{type(exc).__name__}: {exc}. Flush will not run automatically.",
            color="red",
        )


def _queue_or_drop(
    table: str,
    payload: dict[str, Any],
    *,
    op_type: str,
    primary_key: tuple[str, str] | None = None,
    depends_on: Sequence[tuple[str, str]] = (),
) -> str:
    """Common entry — resolve coordinator, queue, or log+drop."""
    sanitization = sanitize_postgres_text(payload)
    if sanitization.replacements:
        payload = sanitization.value
        ctx = _resolve_app_context()
        vcprint(
            f"[Coordinator] Replaced {sanitization.replacements} PostgreSQL-invalid "
            f"NUL byte(s) before queueing {op_type} on {table}; paths="
            f"{list(sanitization.paths)}.",
            color="red",
        )

        async def _capture_sanitization() -> None:
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                ValueError("PostgreSQL-invalid NUL bytes were replaced before persistence"),
                kind="persistence_payload_sanitized",
                request_id=getattr(ctx, "request_id", None) if ctx else None,
                user_id=getattr(ctx, "user_id", None) if ctx else None,
                conversation_id=getattr(ctx, "conversation_id", None) if ctx else None,
                route="matrx_ai.persistence.queue_helpers",
                error_type="PostgresTextSanitization",
                context={
                    "table": table,
                    "op_type": op_type,
                    "replacement_count": sanitization.replacements,
                    "paths": list(sanitization.paths),
                },
            )

        detached_task(_capture_sanitization(), name="capture_persistence_payload_sanitized")

    # Stamp the request's organization_id onto org-scoped cx_ INSERTs. This is the
    # only stamp point for cx_message / cx_tool_call. Personal scope (no org on
    # ctx) leaves it unset and the DB backstop trigger fills the creator's personal
    # org. setdefault keeps any org the gate already stamped.
    if (
        op_type == "insert"
        and table in _ORG_SCOPED_INSERT_TABLES
        and "organization_id" not in payload
    ):
        ctx = _resolve_app_context()
        org_id = getattr(ctx, "organization_id", None) if ctx else None
        if org_id:
            payload["organization_id"] = org_id

    coord = get_coordinator()
    if coord is None:
        # No lane → no coordinator → this write would VANISH. Callers that can
        # run out-of-request (e.g. persist_completed_request, the executor's
        # message reservation) now guard against this with a direct-cxm fallback
        # or by skipping; reaching here means an UNGUARDED queue call in a
        # background scope — a silent-data-loss bug. SCREAM so it can never hide
        # the way the 2026-06-15 cx_message loss did (910 conversations, no
        # system_write_failure, just a quiet log).
        _pk = primary_key[1] if primary_key else (payload.get("id") or "?")
        vcprint(
            f"[Coordinator] DATA LOSS: queue {op_type} on {table} (pk={_pk}) "
            f"called with NO coordinator/lane — op DROPPED. This write needs a "
            f"direct-cxm fallback or a streaming lane. See queue_helpers._queue_or_drop.",
            color="red",
        )
        return ""
    lane = get_current_lane()
    if (
        lane is not None
        and getattr(lane, "phase", None) != "active"
        and not coord._late_boundary_captured
    ):
        # get_coordinator() is also an ownership probe. A probe after drain is
        # harmless and must not manufacture a persistence incident. Capture
        # only at this actual queue boundary, once per terminal coordinator.
        coord._late_boundary_captured = True
        _capture_late_lane_boundary(
            lane,
            _resolve_app_context(),
            table=table,
            op_type=op_type,
            primary_key=(
                primary_key
                or (("id", str(payload["id"])) if payload.get("id") is not None else None)
            ),
        )
    return coord.queue(
        table,
        payload,
        op_type=op_type,  # type: ignore[arg-type]
        primary_key=primary_key,
        depends_on=depends_on,
    )


# ---------- cx_conversation -----------------------------------------------


def queue_conversation_create(*, id: str, **fields: Any) -> str:
    # Do not delegate this canonical access value to a generated-model default.
    # A stale production process once injected the retired "private" enum label
    # after platform.visibility had renamed it to "personal", even though the
    # queued payload itself was valid. Stamping at the conversation funnel keeps
    # the durable operation self-contained and replay-safe across model regen.
    fields.setdefault("visibility", "personal")

    # Ownership guard (second, loud layer). Every conversation MUST be owned by
    # its creator via ``created_by`` — the org backstop trigger derives the
    # personal org from it, and an unowned conversation violates the per-user
    # ownership doctrine. This SCREAMS the class of bug where a caller stamps the
    # owner under the wrong key (e.g. ``user_id=`` — a column chat.conversation
    # does NOT have — which was silently dropped, landing NULL created_by + NULL
    # org and crashing the INSERT on the not-null org constraint, 2026-07-17).
    if not fields.get("created_by"):
        vcprint(
            f"[queue_conversation_create] conversation {id} queued WITHOUT "
            f"created_by — an UNOWNED conversation. The owner column is "
            f"'created_by' (chat.conversation has no 'user_id'). Pass "
            f"created_by=<user_id>; got keys={sorted(fields)}.",
            color="red",
        )
    return _queue_or_drop(
        "chat.conversation",
        {"id": id, **fields},
        op_type="insert",
    )


def queue_conversation_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.conversation",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


# ---------- cx_user_request -----------------------------------------------


def queue_user_request_create(*, id: str, **fields: Any) -> str:
    # cx_user_request has NO conversation_id — it is one backend API call,
    # keyed solely by id. The request↔conversation bridge lives on cx_request,
    # so there is no cx_conversation FK dependency to order this INSERT behind.
    return _queue_or_drop(
        "chat.user_request",
        {"id": id, **fields},
        op_type="insert",
    )


def queue_user_request_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.user_request",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


# ---------- cx_message ----------------------------------------------------


def queue_message_create(*, id: str, conversation_id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.message",
        {"id": id, "conversation_id": conversation_id, **fields},
        op_type="insert",
        depends_on=(("chat.conversation", conversation_id),),
    )


def queue_message_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.message",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


# ---------- cx_request ----------------------------------------------------


def queue_request_create(
    *,
    id: str,
    user_request_id: str,
    conversation_id: str,
    **fields: Any,
) -> str:
    return _queue_or_drop(
        "chat.request",
        {
            "id": id,
            "user_request_id": user_request_id,
            "conversation_id": conversation_id,
            **fields,
        },
        op_type="insert",
        depends_on=(
            ("chat.user_request", user_request_id),
            ("chat.conversation", conversation_id),
        ),
    )


def queue_request_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.request",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


# ---------- cx_tool_call --------------------------------------------------


def queue_tool_call_create(*, id: str, conversation_id: str, **fields: Any) -> str:
    # FK deps: conversation (required) + user_request when stamped. The ORM
    # DAG also reads ForeignKey fields off the Model; declaring both here
    # keeps the explicit queue contract aligned with chat.tool_call's schema
    # (cx_tool_call_user_request_id_fkey) so a same-Session parent INSERT
    # always lands first when present.
    user_request_id = fields.get("user_request_id")
    deps: list[tuple[str, str]] = [("chat.conversation", conversation_id)]
    if user_request_id:
        deps.append(("chat.user_request", str(user_request_id)))
    return _queue_or_drop(
        "chat.tool_call",
        {"id": id, "conversation_id": conversation_id, **fields},
        op_type="insert",
        depends_on=tuple(deps),
    )


def queue_tool_call_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.tool_call",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


# ---------- cx_request_snapshot -------------------------------------------


def queue_request_snapshot_create(
    *,
    id: str,
    user_request_id: str,
    conversation_id: str,
    **fields: Any,
) -> str:
    return _queue_or_drop(
        "chat.request_snapshot",
        {
            "id": id,
            "user_request_id": user_request_id,
            "conversation_id": conversation_id,
            **fields,
        },
        op_type="insert",
        depends_on=(
            ("chat.user_request", user_request_id),
            ("chat.conversation", conversation_id),
        ),
    )


# ---------- cx_tool_trace -------------------------------------------------


def queue_tool_trace_create(*, id: str, **fields: Any) -> str:
    # chat.tool_trace.conversation_id is a real FK. Keep the dependency
    # explicit for coordinator telemetry/back-compat even though the current
    # matrx-orm Session also infers it from model metadata.
    conversation_id = fields.get("conversation_id")
    deps: tuple[tuple[str, str], ...] = (
        (("chat.conversation", conversation_id),) if conversation_id else ()
    )
    return _queue_or_drop(
        "chat.tool_trace",
        {"id": id, **fields},
        op_type="insert",
        depends_on=deps,
    )


# ---------- cx_observational_memory ---------------------------------------


def queue_om_memory_create(*, id: str, **fields: Any) -> str:
    conversation_id = fields.get("conversation_id")
    deps: tuple[tuple[str, str], ...] = (
        (("chat.conversation", conversation_id),) if conversation_id else ()
    )
    return _queue_or_drop(
        "chat.observational_memory",
        {"id": id, **fields},
        op_type="insert",
        depends_on=deps,
    )


def queue_om_memory_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.observational_memory",
        fields,
        op_type="update",
        primary_key=("id", id),
    )


def queue_om_event_create(*, id: str, **fields: Any) -> str:
    """Queue a ``cx_observational_memory_event`` INSERT.

    Depends on the parent OM row (when stamped) and the conversation so the
    flush DAG never FK-violates against a still-pending insert.
    """
    deps: list[tuple[str, str]] = []
    memory_record_id = fields.get("memory_record_id")
    if memory_record_id:
        deps.append(("chat.observational_memory", str(memory_record_id)))
    conversation_id = fields.get("conversation_id")
    if conversation_id:
        deps.append(("chat.conversation", str(conversation_id)))
    return _queue_or_drop(
        "chat.observational_memory_event",
        {"id": id, **fields},
        op_type="insert",
        depends_on=tuple(deps),
    )


# ---------- cx_agent_memory -----------------------------------------------


def queue_agent_memory_create(*, id: str, **fields: Any) -> str:
    return _queue_or_drop("chat.agent_memory", {"id": id, **fields}, op_type="insert")


def queue_agent_memory_update(id: str, **fields: Any) -> str:
    return _queue_or_drop(
        "chat.agent_memory", fields, op_type="update", primary_key=("id", id)
    )


def queue_agent_memory_delete(id: str) -> str:
    return _queue_or_drop(
        "chat.agent_memory", {}, op_type="delete", primary_key=("id", id)
    )
