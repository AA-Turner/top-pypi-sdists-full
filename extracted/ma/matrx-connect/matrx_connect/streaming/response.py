from __future__ import annotations

import asyncio
import sys
import traceback
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi.responses import StreamingResponse
from matrx_utils import vcprint

from matrx_utils import client_error_text
from matrx_connect.context.app_context import AppContext, set_app_context
from matrx_connect.context.app_context import _app_context as _app_context_var
from matrx_connect.context.data_types import ConversationIdData
from matrx_connect.context.emitter_protocol import Emitter
from matrx_connect.context.events import (
    END_REASON_CANCELLED,
    END_REASON_ERROR,
    EventType,
    InfoPayload,
    RecordReservedPayload,
    build_event,
)
from matrx_connect.context.phases import PhasePayload
from matrx_connect.emitters.stream_emitter import (
    StreamEmitter,
    register_active_stream,
    unregister_active_stream,
)
from matrx_connect.lane import RequestLane
from matrx_connect.lane.contextvar import (
    get_current_lane,
    reset_current_lane,
    set_current_lane,
)
from matrx_connect.reservations import get_tracker
from matrx_connect.streaming.error_capture import capture_error
from matrx_connect.streaming.journal import create_stream_journal_sink
from matrx_connect.streaming.run_tracking import (
    STREAM_RUN_CANCELLED,
    STREAM_RUN_COMPLETED,
    STREAM_RUN_FAILED,
    StreamRun,
    StreamRunHandle,
    host_is_shutting_down,
    open_stream_run,
)
from matrx_connect.streaming.turn_failure import persist_turn_failure
from matrx_connect.streaming.failure_classification import (
    GENERIC_CRASH_MESSAGE,
    classify_infrastructure_failure,
    stable_error_type,
    strip_ansi,
)

# Bounded wait for the work task to stop (cancel + cancel-handler persist) before
# the lane drains. Generous enough for the task's shielded cancel-persist (itself
# bounded by the persistence drain timeout) to finish; bounded so teardown can't
# hang on a wedged task.
_WORK_TASK_JOIN_TIMEOUT_SECONDS: float = 45.0

# Strong references to detached background supervisors so the event loop's weak
# task set can't garbage-collect a still-running pipeline mid-flight. Cleared by
# each supervisor's own done-callback once its work task + lane drain finish.
_DETACHED_SUPERVISORS: set[asyncio.Task[None]] = set()


async def _supervise_detached_task(
    task: asyncio.Task[None],
    lane: RequestLane,
    debug_label: str,
) -> None:
    """Run a detached (client-disconnected) work task to completion, then drain
    its lane so deferred persistence lands. Fully decoupled from the original
    HTTP response — lives only on the event loop.

    The work task already carries the lane in its copied context (it was spawned
    after ``set_current_lane``), so its writes and any child agents/steps it
    forks stay attributed correctly. We only need the lane reference here to run
    the post-completion drain."""
    failed = False
    try:
        await task
        if task.cancelled():
            failed = True
        elif task.exception() is not None:
            failed = True
    except asyncio.CancelledError:
        # Only happens on server shutdown — the task's own cancel handler
        # shield-persists in-flight state; nothing more to do here.
        failed = True
    except Exception:
        failed = True

    try:
        # Full (non-soft) drain: the client is gone, so there's no live stream to
        # protect — let ALL lane work (blocking, normal, deferred) finish so the
        # pipeline's writes are durable.
        await lane.begin_drain(failed=failed, soft=False)
    except Exception as drain_exc:  # noqa: BLE001
        vcprint(
            f"[{debug_label}] detached lane drain raised: {type(drain_exc).__name__}: {drain_exc}",
            color="yellow",
        )
    else:
        vcprint(
            f"[{debug_label}] detached work task finished + lane drained (failed={failed})",
            color="green",
        )


async def _end_after_normal_return(emitter: Emitter) -> None:
    """End the stream for a task that returned without ending it.

    THE CLASS THIS CLOSES (live 2026-09-27, Knowledge Ask): the journal publishes a
    frame to the reader only after it commits, and ``StreamEmitter.generate`` closes
    the response when it sees the task done on an idle tick. A task that returned
    without ``send_end()`` therefore lost every frame still committing — the last
    ones, the answer's citations — and the wire carried no END. ``send_end`` closes
    the sink (flushing every accepted frame) before it puts the terminator, so the
    reader sees every frame, then END. Idempotent: a task that already ended its
    stream (or abandoned it for another runner) is left alone. No route has to
    remember ``send_end()``. Guard: tests/test_stream_ends_after_journal_flush.py.
    """
    if _emitter_has_ended(emitter) or getattr(emitter, "_ending", False):
        return
    send_end = getattr(emitter, "send_end", None)
    if callable(send_end):
        await send_end()


def _emitter_has_ended(emitter: Emitter) -> bool:
    """Has this emitter already published a terminal END frame?

    Read through ``getattr`` because ``Emitter`` is a structural protocol with
    many host implementations (console, silent, sub-pipeline, workflow, test
    doubles). An emitter that does not expose the flag is treated as NOT ended:
    announcing a crash is the safe default; the emitter's own ``_ended`` guard
    still drops the frames if it really was finished.
    """
    ended = getattr(emitter, "has_ended", False)
    return ended is True


async def _force_error_terminal(emitter: Emitter, debug_label: str) -> None:
    """Last-resort terminal when the normal fatal_error path itself raised.

    A client reading NDJSON has exactly two acceptable endings: a terminal
    event, or a dead socket it must treat as a failure. What it must NEVER get
    is a success word, so this only ever sends a non-success one — and never
    raises, because it runs on a path that is already handling a crash.
    """
    send_end = getattr(emitter, "send_end", None)
    if not callable(send_end):
        return
    try:
        await send_end(reason=END_REASON_ERROR)
    except asyncio.CancelledError:
        raise
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[{debug_label}] could not force a non-success terminal event: "
            f"{type(exc).__name__}: {exc}",
            color="red",
        )



def _outcome_from_end_reason(emitter: Emitter) -> str:
    """Map the END word a task left on the wire onto its run's outcome.

    A task may report its own failure (``fatal_error``) and return normally;
    its run must say failed, not completed."""
    reason = getattr(emitter, "end_reason", None)
    if reason == END_REASON_ERROR:
        return STREAM_RUN_FAILED
    if reason == END_REASON_CANCELLED:
        return STREAM_RUN_CANCELLED
    return STREAM_RUN_COMPLETED


async def _settle_stream_run(
    handle: StreamRunHandle | None,
    outcome: str,
    debug_label: str,
    *,
    error_type: str | None = None,
    message: str | None = None,
) -> None:
    """Settle the stream's durable run. Never raises into the work: the run
    lease and the host reaper are the backstop for a settle that cannot land."""
    if handle is None:
        return
    try:
        await handle.settle(outcome, error_type=error_type, message=message)
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[{debug_label}] stream run settle raised ({type(exc).__name__}: {exc}) — "
            "the run lease keeps it visible; the reaper settles it if nothing else does",
            color="yellow",
        )


class _RunSettlePlan:
    """What the stream run should become when the work task is over. Filled in
    by the work task as it learns the outcome; applied exactly once in a
    ``finally`` (see ``_finish_stream_run``) so no exit path skips it."""

    __slots__ = ("handle", "outcome", "error_type", "message", "cancelled")

    def __init__(self) -> None:
        self.handle: StreamRunHandle | None = None
        self.outcome: str | None = None  # None -> abandon (lease/reaper decides)
        self.error_type: str | None = None
        self.message: str | None = None
        self.cancelled = False


async def _finish_stream_run(plan: _RunSettlePlan, debug_label: str) -> None:
    """Settle the plan's outcome, or abandon the run when there is none (a
    cancel/shutdown, or an exit that never learned its outcome). Never raises."""
    handle = plan.handle
    if handle is None:
        return
    try:
        if plan.outcome is None:
            handle.abandon()
            return
    except Exception:  # noqa: BLE001 — teardown must never raise here
        return
    await _settle_stream_run(
        handle,
        plan.outcome,
        debug_label,
        error_type=plan.error_type,
        message=plan.message,
    )


class _StartState:
    """How far one response got toward starting its work (see _stream)."""

    __slots__ = (
        "journal_done", "frames", "published", "task", "refused",
        "unread_scheduled", "main_failed", "main_cancelled", "cancelled_by_disconnect",
    )

    def __init__(self) -> None:
        self.journal_done = False
        self.frames: list[str | bytes] | None = None
        self.published = 0
        self.task: asyncio.Task[None] | None = None
        self.refused = False
        self.unread_scheduled = False
        self.cancelled_by_disconnect = False
        self.main_failed = False
        self.main_cancelled = False


class _WorkStartsStreamingResponse(StreamingResponse):
    """A StreamingResponse whose work starts even when nobody reads the body.

    Starlette drives the body only while a client is connected: on ASGI spec
    2.3 a queued ``http.disconnect`` cancels the body task group, on 2.4 the
    first ``send`` raises. Either can happen before the body generator spawns
    the work. ``on_call_end`` runs when the ASGI call ends however it ended and
    starts the work detached if the body never did."""

    def __init__(self, content: Any, *, on_call_end: Callable[[], None], **kwargs: Any) -> None:
        super().__init__(content, **kwargs)
        self._on_call_end = on_call_end

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        try:
            await super().__call__(scope, receive, send)
        finally:
            self._on_call_end()


def create_streaming_response(
    ctx: AppContext,
    task_fn: Callable[..., Awaitable[None]],
    *task_args: Any,
    initial_message: str = "Initializing Matrx...",
    debug_label: str = "stream",
    detach_on_disconnect: bool = True,
    existing_lane: RequestLane | None = None,
    existing_lane_token: Any = None,
    run: StreamRun | None = None,
) -> StreamingResponse:
    """Wire a streaming task to an NDJSON response.

    THE CTX YOU PASS IS THE CTX THE TASK RUNS UNDER. To add a route-specific
    field (organization_id, conversation_id, debug, ...) for the streaming
    task, ``ctx = ctx.with_overrides(field=value)`` and pass THAT — this
    builder installs it into the ContextVar before spawning the task, so every
    ambient ``get_app_context()`` downstream sees your override. Calling
    ``set_app_context(ctx)`` yourself first is harmless and no longer required;
    until 2026-09-20 it WAS required and six routes forgot, so their tasks ran
    under the middleware ctx and re-read the organization from the database to
    survive. (``ctx.extend()`` was removed in Phase 1 and now raises.)

    ``detach_on_disconnect`` — DEFAULT TRUE, and you should essentially never
    set it False. We are a server: a client disconnect must NEVER stop work.
    The instant we issue a paid provider call (LLM tokens, image/video/TTS
    generation, embeddings) we are billed for the WHOLE thing whether or not
    the browser is still reading — so killing the task on disconnect throws
    away money AND the result. With detach on, a disconnect stops the outbound
    stream but the work task keeps running to completion on the event loop;
    a background supervisor drains the lane (deferred persistence) when it
    finishes. The client simply reloads the finished result from the DB.

    This applies to EVERYTHING, chat included — the assistant turn is billed
    the moment the request leaves us, so we finish it and persist it rather
    than canceling. (Server shutdown still cancels tasks; that path is handled
    by the orchestrator's shielded cancel-persist.)

    NO STREAM RUNS UNTRACKED. Before the task starts, the host's stream-run
    opener (``run_tracking.configure_stream_run_opener``) opens a durable run
    for this request, and the run is settled on every exit: ``completed``,
    ``failed`` (a raise, or a task that ended its own wire with an error), or
    ``cancelled``. A canceled task (shutdown) is abandoned to the host's lease
    reaper. ``run=StreamRun(feature=, link_kind=, link_id=)`` names what the run
    is about so a returning client finds it by the feature record; without it
    the run is labeled with the route path and the request id is the handle.
    """
    if ctx.emitter is None:
        raise RuntimeError("AppContext.emitter must be set before create_streaming_response()")
    emitter: Emitter = ctx.emitter
    replayable_emitter = emitter if isinstance(emitter, StreamEmitter) else None
    replay_request_id = str(ctx.request_id or "")

    # Opt the emitter out of disconnect-cancellation when requested. Guarded so
    # any Emitter implementation lacking the hook still works (it just won't
    # detach — falls back to the safe cancel-on-disconnect default).
    if detach_on_disconnect:
        setter = getattr(emitter, "set_detach_on_disconnect", None)
        if callable(setter):
            setter(True)

    tracker = get_tracker()

    # Open the RequestLane for this user action. The lane owns every async
    # operation spawned during the request — including DEFERRED tail work
    # like the conversation labeler that runs AFTER the response ends.
    # Lane id = request_id (cx_user_request.id) when present; fork operations
    # (fork_for_child_agent, fork_for_workflow_step) preserve request_id so
    # child agents and parallel steps automatically join this same lane.
    #
    # ADOPT a pre-opened lane when given. `create_prepared_streaming_response`
    # opens + installs the lane BEFORE request prep so prep-phase writes
    # (cx_user_request, …) queue into the coordinator instead of blocking on
    # one-shot Sessions. In that case the lane is already current in this
    # task's ContextVar; we reuse it and its install token rather than opening
    # a second lane / re-installing.
    lane = existing_lane or RequestLane.open(
        lane_id=ctx.request_id,
        scope_kind="request",
        context_snapshot={
            "user_id": ctx.user_id,
            "request_id": ctx.request_id,
            "conversation_id": ctx.conversation_id,
            "source_app": ctx.source_app,
            "agent_id": ctx.agent_id,
        },
    )

    # ── THE WORK STARTS WHETHER OR NOT ANYONE READS THE BODY ──────────────
    # The opening (journal attach, opening frames, staged prep frames) and the
    # work task's spawn are split into idempotent steps held on ``start``, so
    # the SAME steps can finish from two places: the body generator (a reader
    # is attached) or ``_begin_unread_work`` (the client left before the body
    # got that far — FX-N 2026-09-30, web chat 265953a3: the page reloaded
    # during prep, Starlette canceled the body before the task existed, and
    # the run plus every write queued in its lane vanished without a trace).
    start = _StartState()

    async def _attach_journal() -> None:
        """Open the host journal once. Raises when the host sink cannot open."""
        if start.journal_done:
            return
        if replayable_emitter is not None and replay_request_id:
            sink = await create_stream_journal_sink(ctx)
            if sink is not None:
                replayable_emitter.attach_journal_sink(sink)
        start.journal_done = True

    def _opening_frames() -> list[str | bytes]:
        """Every frame that opens the wire, in wire order, built once.

        Take (and thereby open) the wire only after the journal is attached,
        holding the prep-phase frames aside so the opening events still go
        first; the staged frames follow them."""
        if start.frames is not None:
            return start.frames
        staged_prep_frames: list[str | bytes] = (
            replayable_emitter.take_staged_wire() if replayable_emitter is not None else []
        )
        frames: list[str | bytes] = [
            build_event(EventType.PHASE, PhasePayload(phase="connected")).to_jsonl()
        ]
        # The route's initial_message reaches the client as the stream's first
        # INFO event — the FE renders it as the opening progress line until a
        # real phase/info arrives. (Historically this parameter was accepted
        # and silently dropped.)
        if initial_message:
            frames.append(build_event(
                EventType.INFO,
                InfoPayload(
                    code="initial_message",
                    system_message=initial_message,
                    user_message=initial_message,
                ),
            ).to_jsonl())
        if ctx.conversation_id:
            frames.append(build_event(
                EventType.DATA,
                ConversationIdData(conversation_id=ctx.conversation_id),
            ).to_jsonl())
            # Typed record_reserved events for rows that already exist at this point
            tracker.register_existing("matrx", "conversation", ctx.conversation_id)
            frames.append(build_event(EventType.RECORD_RESERVED, RecordReservedPayload(
                db_project="matrx",
                table="conversation",
                record_id=ctx.conversation_id,
                parent_refs={},
                metadata={},
            )).to_jsonl())
        if ctx.request_id:
            parent_refs: dict[str, str] = {}
            if ctx.conversation_id:
                parent_refs["conversation_id"] = ctx.conversation_id
            tracker.register_existing("matrx", "user_request", ctx.request_id)
            frames.append(build_event(EventType.RECORD_RESERVED, RecordReservedPayload(
                db_project="matrx",
                table="user_request",
                record_id=ctx.request_id,
                parent_refs=parent_refs,
                metadata={},
            )).to_jsonl())
        # Publish every frame staged during request preparation (MCP
        # attachments, tool routing, sandbox arming). The emitter held them so
        # the journal could still attach; they now ride the journal and the
        # replay buffer exactly like any later frame, landing right after the
        # opening events and before the run's own output.
        frames.extend(staged_prep_frames)
        start.frames = frames
        return frames

    async def _opening(frame: str | bytes):
        if replayable_emitter is not None:
            await replayable_emitter.publish_wire(frame)
            return None
        return frame

    # The work task's outcome lives on ``start`` (main_failed / main_cancelled) so
    # the generator's finally drains in success / failure / soft-cancel mode.

    def _capture_fields() -> dict[str, Any]:
        # Pull whatever correlation context is available off the ctx so the
        # captured record is as rich as system_write_failure. All optional —
        # a crash before auth resolves has none of these.
        return {
            "request_id": getattr(ctx, "request_id", None),
            "user_id": getattr(ctx, "user_id", None),
            "conversation_id": getattr(ctx, "conversation_id", None),
            "agent_id": getattr(ctx, "agent_id", None),
            "source_app": getattr(ctx, "source_app", None),
            # BOTH halves of the one two-level categorization (app, then
            # the feature inside it). A stream crash that names only the
            # app cannot be told apart from any other crash in that app.
            "source_feature": getattr(ctx, "source_feature", None),
            "route": debug_label,
            "context": {"debug_label": debug_label},
        }

    async def _run_with_error_handling():
        from matrx_connect.chat_timing import chat_timing_mark

        chat_timing_mark("stream_task_started", "streaming background task started")
        plan = _RunSettlePlan()
        try:
            await _run_body(plan)
        except asyncio.CancelledError:
            # A cancel that lands anywhere (including inside the crash handler)
            # must never leave the run heartbeating: no settle -> abandon.
            if not plan.cancelled:
                plan.cancelled = True
                plan.outcome = None
            raise
        finally:
            # GUARANTEED: whatever happened above, the run is settled or
            # abandoned here, so its heartbeat can never renew for hours.
            await _finish_stream_run(plan, debug_label)

    async def _run_body(plan: _RunSettlePlan) -> None:
        try:
            # The durable run opens before any work. A DECLARED run the host
            # cannot open raises here and fails the task through the one crash
            # path below — the work never starts untracked.
            plan.handle = await open_stream_run(ctx, run, debug_label, task_fn)
            await task_fn(emitter, *task_args)
            await _end_after_normal_return(emitter)
            plan.outcome = _outcome_from_end_reason(emitter)
        except asyncio.CancelledError as e:
            start.main_cancelled = True
            if start.cancelled_by_disconnect:
                # The route opted out of detaching and the client left: the
                # work was stopped on purpose, so the run says canceled.
                plan.outcome = STREAM_RUN_CANCELLED
            else:
                # Shutdown: never settle — the lease lapses and the host
                # reaper records the run as failed, the same contract chat
                # runs follow. (`plan.outcome` stays None -> abandon.)
                plan.outcome = None
            plan.cancelled = True
            print(
                f"\n[{debug_label}] Task canceled (client disconnected)",
                file=sys.stderr,
                flush=True,
            )
            vcprint("Task canceled (client disconnected)", f"[{debug_label}]", color="yellow")
            # CLOSE THE LOOP universally: a client disconnect must leave a
            # queryable record, not just a stderr line. record_error writes
            # to system_error on a fresh connection, shielded so this
            # cancellation can't interrupt it. (cx_ chat cost is ALSO
            # persisted by the orchestrator's own cancel handler; this is
            # the catch-all so NO stream type can vanish silently.)
            await capture_error(
                e,
                kind="stream_cancelled",
                error_text=f"{debug_label} canceled (client disconnect or shutdown)",
                **_capture_fields(),
            )
            # Preserve the original swallow-and-flag behavior (the lane
            # drain + generator teardown rely on not re-raising here).
        except Exception as e:
            start.main_failed = True
            # The run is FAILED from this line on; the finally in the caller
            # settles it even if the handler below raises or is canceled.
            plan.outcome = STREAM_RUN_FAILED
            plan.error_type = stable_error_type(debug_label)
            plan.message = str(e)
            tb = traceback.format_exc()
            print(
                f"\n[{debug_label}] TASK CRASHED — {type(e).__name__}: {e}\n{tb}",
                file=sys.stderr,
                flush=True,
            )
            vcprint(e, f"[{debug_label}] TASK CRASHED — {type(e).__name__}", color="red")
            # A CALLER REFUSAL (``is_caller_refusal`` — e.g. a guest whose free AI
            # actions are used up) is an expected, classified outcome: it still
            # ends the stream with its own error_type below, but it is not a crash
            # and files no system_error. Matched by attribute: matrx-connect does
            # not import the package that raises it.
            if not getattr(e, "is_caller_refusal", False):
                await capture_error(
                    e,
                    kind="stream_crash",
                    error_type=getattr(getattr(e, "error_info", None), "error_type", None),
                    **_capture_fields(),
                )

            # If the provider layer attached a classified error with a
            # user-facing message, propagate it instead of the generic label.
            error_info = getattr(e, "error_info", None)
            if error_info is not None:
                user_msg = getattr(error_info, "user_message", None) or f"{debug_label} failed."
                error_type = getattr(error_info, "error_type", None) or stable_error_type(
                    debug_label
                )
                message = getattr(error_info, "message", None) or str(e)
                code = getattr(error_info, "code", None)
                raw_details = getattr(error_info, "details", None)
                details = dict(raw_details) if isinstance(raw_details, dict) else {}
                # A typed refusal names the HTTP status it would have answered before the
                # stream opened (a declared prompt block missing is a 422). Clients that tell a
                # deterministic refusal from a retryable crash read it here.
                status_code = getattr(error_info, "status_code", None)
                if isinstance(status_code, int) and status_code:
                    details.setdefault("status_code", status_code)
            else:
                # Unclassified crash. Two things must NOT happen here:
                # the error type must not carry this run's id (it would be
                # a new type per session — ungroupable, unalertable), and
                # a server-side infrastructure failure must not be
                # reported to the user as something they can fix by
                # "adjusting settings". See failure_classification.py.
                details = {}
                error_type = stable_error_type(debug_label)
                message = str(e)
                code = None
                infrastructure = classify_infrastructure_failure(e)
                if infrastructure is not None:
                    error_type = infrastructure.error_type
                    user_msg = infrastructure.user_message
                    details["debug_label"] = debug_label
                else:
                    # A person reads this: never the route's log label or the
                    # exception's class name (both travel in ``details`` and the
                    # durable record), and never "adjust your settings" for a
                    # crash they did not cause (live 2026-10-22: "DataFetch failed
                    # unexpectedly (UndefinedFunctionError)").
                    user_msg = GENERIC_CRASH_MESSAGE

            # The exception's TYPE is the one piece of machine detail that is
            # always safe to hand a client: it names the failure class without
            # a traceback, a file path, a statement or a bound value. It is
            # what a person pastes into a bug report and what support greps.
            details.setdefault("exception_type", type(e).__name__)

            # Operator banners are ANSI-colored; a browser renders those
            # escapes literally. Strip them from anything client-bound —
            # the durable system_error record above keeps the raw text.
            # ...and never the statement or its bound args: a matrx-orm
            # banner carries both (live 2026-09-17). client_error_text cuts
            # them; the raw render stays in the durable record and the log.
            message = client_error_text(strip_ansi(message)) or user_msg

            if ctx.request_id:
                details.setdefault("request_id", ctx.request_id)

            # TERMINALIZE THE ORPHANED TURN BEFORE ANNOUNCING IT.
            #
            # The emit below is live-only: reload the page and it is gone.
            # A crash here means the orchestrator never reached its own
            # failure finalizer, so without this the transcript just STOPS
            # after the last successful row and the request keeps whatever
            # status its previous iteration left behind (2026-09-12: a dead
            # turn read `status=completed finish_reason=tool_calls`).
            #
            # Persist FIRST: the same honest text goes to the durable row and
            # to the wire, and if the database is unreachable at this exact
            # moment the seam screams once and the wire message is the only —
            # loudly recorded — residue.
            # A caller refusal is not a dead turn: no failed assistant row.
            if not getattr(e, "is_caller_refusal", False):
                await persist_turn_failure(
                    conversation_id=getattr(ctx, "conversation_id", None),
                    request_id=getattr(ctx, "request_id", None),
                    user_id=getattr(ctx, "user_id", None),
                    error_type=error_type,
                    message=message,
                    user_message=user_msg,
                    route=debug_label,
                )

            # ANNOUNCE THE CRASH ON THE WIRE — OR SAY OUT LOUD WHY WE CANNOT.
            #
            # THE LIE THIS CLOSES (live 2026-09-17): a streaming task raised,
            # the framework logged "TASK CRASHED", and the client's stream
            # still ended with {"event":"end","data":{"reason":"complete"}} —
            # a SUCCESSFUL stream that happened to produce nothing.
            # ``fatal_error`` now terminates the wire with reason="error"
            # (StreamEmitter.fatal_error), so every stream on the platform —
            # chat, workflows, media, scraping, any route at all — ends with
            # a word that matches what actually happened.
            #
            # IDEMPOTENCY: if the task already terminalized its own stream
            # (it sent its end and then crashed in a tail step), a SECOND
            # terminal event must not be bolted on behind it. A frame the
            # client already read cannot be retracted, so that case screams
            # into the operator log instead of quietly evaporating.
            if _emitter_has_ended(emitter):
                print(
                    f"\n[{debug_label}] TASK CRASHED AFTER THE STREAM ALREADY "
                    f"ENDED — {type(e).__name__}. The client was already told "
                    f"this stream was over, so no error event can reach it. "
                    f"The failure is recorded (system_error + turn failure) "
                    f"and MUST be root-caused: a task that ends its own stream "
                    f"and then raises makes the crash invisible to the user.",
                    file=sys.stderr,
                    flush=True,
                )
            else:
                try:
                    await emitter.fatal_error(
                        error_type=error_type,
                        message=message,
                        user_message=user_msg,
                        code=code,
                        details=details or None,
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as emit_exc:  # noqa: BLE001
                    # The announcement path itself broke. Never leave the
                    # client on an open stream or a success word: put a
                    # non-success terminal on the wire by hand.
                    print(
                        f"\n[{debug_label}] fatal_error emission raised "
                        f"({type(emit_exc).__name__}: {emit_exc}) while "
                        f"reporting {type(e).__name__} — forcing a "
                        f"non-success terminal event.",
                        file=sys.stderr,
                        flush=True,
                    )
                    await _force_error_terminal(emitter, debug_label)

            plan.error_type = error_type
            plan.message = message

    def _start_work() -> asyncio.Task[None]:
        """Spawn the work task exactly once, under the CURRENT context (which must
        already carry ``ctx`` and the lane — create_task copies it)."""
        if start.task is not None:
            return start.task
        # Register only once the work actually starts. A StreamingResponse can
        # be constructed and abandoned before its body iterator starts;
        # registering earlier would leave an emitter that never receives a task
        # or cleanup callback.
        registered = replayable_emitter is not None and bool(replay_request_id)
        if registered:
            register_active_stream(replay_request_id, replayable_emitter)
        work = _run_with_error_handling()
        try:
            task = asyncio.create_task(work)
        except BaseException:
            work.close()
            if registered:
                unregister_active_stream(replay_request_id, replayable_emitter)
            raise
        start.task = task
        callback_registered = False
        try:
            if registered:
                task.add_done_callback(
                    lambda _task: unregister_active_stream(replay_request_id, replayable_emitter)
                )
                callback_registered = True
            emitter.set_task(task)
        except BaseException:
            if registered and not callback_registered:
                unregister_active_stream(replay_request_id, replayable_emitter)
            raise
        return task

    async def _begin_unread_work() -> None:
        """The client left before the body spawned the work: finish the opening
        without a reader, start the work, and supervise it to its lane drain.

        Runs as its own task (a copy of the request's context), so installing
        ``ctx`` and the lane here needs no reset."""
        if not detach_on_disconnect:
            # The route opted into cancel-on-disconnect: no work runs, but the
            # writes prep already queued in the lane still land — never lost.
            if replayable_emitter is not None:
                replayable_emitter.discard_staged_wire()
            await lane.begin_drain(failed=False, soft=True)
            return
        vcprint(
            f"[{debug_label}] client left before the stream opened — STARTING the work "
            f"task detached (a disconnect never stops server work)",
            color="cyan",
        )
        try:
            await _attach_journal()
        except Exception as exc:  # noqa: BLE001 — the journal is a sink, not a gate
            start.journal_done = True
            await capture_error(
                exc,
                kind="operation_stream_journal_open_failed",
                request_id=ctx.request_id,
                user_id=ctx.user_id,
                route=debug_label,
            )
        frames = _opening_frames()
        if replayable_emitter is not None:
            replayable_emitter.release_primary_reader()
            while start.published < len(frames):
                await replayable_emitter.publish_wire(frames[start.published])
                start.published += 1
        set_current_lane(lane)
        set_app_context(ctx)
        await _supervise_detached_task(_start_work(), lane, debug_label)

    def _ensure_work_started() -> None:
        """Called when the response call ends, read or not. A no-op once the
        body spawned the work, or when the journal refused and said so."""
        if start.task is not None or start.refused or start.unread_scheduled:
            return
        start.unread_scheduled = True
        supervisor = asyncio.create_task(_begin_unread_work())
        _DETACHED_SUPERVISORS.add(supervisor)
        supervisor.add_done_callback(_DETACHED_SUPERVISORS.discard)

    async def _stream():
        # The host journal is opened before any response bytes.  Its sink owns
        # commit-before-fanout; without it StreamEmitter retains its established
        # in-process behavior for package-only consumers.
        try:
            await _attach_journal()
        except Exception as exc:
            start.refused = True
            # Headers are already committed when a StreamingResponse body
            # starts. Never turn an unavailable recovery journal into an
            # empty 200 that the browser mistakes for a live attachment.
            await capture_error(
                exc,
                kind="operation_stream_journal_open_failed",
                request_id=ctx.request_id,
                user_id=ctx.user_id,
                route=debug_label,
            )
            assert replayable_emitter is not None  # only a StreamEmitter opens a journal
            await replayable_emitter.fatal_error(
                error_type="operation_stream_journal_unavailable",
                message="The live response journal could not be opened.",
                user_message="This response could not start. Please send it again.",
            )
            async for item in replayable_emitter.generate():
                yield item
            return

        frames = _opening_frames()
        while start.published < len(frames):
            # Counted after the publish: a disconnect that lands mid-publish
            # re-sends that one frame from _begin_unread_work rather than lose it.
            opening = await _opening(frames[start.published])
            start.published += 1
            if opening is not None:
                yield opening

        # Install the lane into the current ContextVar. Tasks spawned from
        # the task function (and any child agent/workflow it forks) inherit
        # it automatically via asyncio.create_task's copy_context().
        # When adopting a lane opened before prep, it is ALREADY current —
        # reuse the install token from create_prepared_streaming_response
        # instead of re-installing (re-installing would make reset restore the
        # lane-still-set state and leak it).
        if existing_lane is not None:
            lane_token = existing_lane_token
        else:
            lane_token = set_current_lane(lane)

        # 🚨 THE CTX HANDED TO THIS BUILDER IS THE CTX THE TASK RUNS UNDER.
        #
        # `with_overrides()` returns a NEW AppContext and, by design, does not
        # touch the ContextVar — the docstring above told every caller to call
        # set_app_context() themselves before coming here. Six did not
        # (workflow.py x3, retry_checkpoints.py, definition_run.py,
        # pdf_processing.py — census 2026-09-20), and the task they spawned
        # read the MIDDLEWARE ctx ambiently instead of the one they had just
        # derived: a run whose organization_id was "" or a conversation_id of
        # "" crashing cx_* persistence with `invalid input syntax for type
        # uuid`. Seven call sites then grew workarounds that re-read the
        # organization from the run row because "the ContextVar may not be
        # visible here". A contract that six careful callers all missed is the
        # wrong contract: the builder installs what it is handed, so the task
        # (which inherits the current Context through create_task's
        # copy_context) runs under exactly the ctx the route passed.
        # Idempotent when the caller already installed the same object.
        ctx_token = set_app_context(ctx)

        def _release_lane() -> None:
            # Reset the lane ContextVar exactly once. Endpoint + stream
            # generator run in the same request Task (one Context), so the
            # token resets cleanly; the except is a defensive backstop that
            # still clears the lane so it can never leak past the request.
            try:
                reset_current_lane(lane_token)
            except (ValueError, LookupError):
                set_current_lane(None)
            # The ctx install above is scoped to this response exactly like
            # the lane. A reset that fails (different Context) is not an error
            # here: the request Task is ending and its Context dies with it.
            try:
                _app_context_var.reset(ctx_token)
            except (ValueError, LookupError):
                pass

        task: asyncio.Task[None] | None = None
        startup_failed = False
        try:
            # The body reached the spawn: the work starts here, with a reader.
            # (When it never gets this far, _ensure_work_started starts it.)
            try:
                task = _start_work()
            except BaseException:
                # `_start_work` can fail after create_task has succeeded (for
                # example, an emitter rejecting its task hook). The task and
                # lane still belong to this response and must be finalized;
                # this flag prevents the disconnect-detach path from hiding
                # the startup failure or leaving the new task running.
                startup_failed = True
                raise

            async for item in emitter.generate():
                yield item

            if task.done() and not task.cancelled():
                exc = task.exception()
                if exc is not None:
                    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                    print(
                        f"\n[{debug_label}] TASK EXCEPTION ESCAPED HANDLER — "
                        f"{type(exc).__name__}: {exc}\n{tb}",
                        file=sys.stderr,
                        flush=True,
                    )
        finally:
            # `_start_work` records the task before calling emitter hooks. If
            # one of those hooks raises, its return assignment above never
            # happens, but the allocated task must still be joined here.
            if task is None:
                task = start.task

            # DETACH PATH: the client went away but the work task is still
            # running and the route opted into completion-regardless. Do NOT
            # cancel it. Hand it to a background supervisor that awaits the task
            # then drains the lane — fully decoupled from this dying response.
            # This is the fix for "30s of browser inactivity threw away an
            # expensive, mostly-done pipeline" — the work now finishes and all
            # its DB writes land no matter what the browser does.
            if not startup_failed and task is not None and detach_on_disconnect and not task.done():
                vcprint(
                    f"[{debug_label}] client disconnected — DETACHING work task "
                    f"to run to completion in the background (not canceled)",
                    color="cyan",
                )
                supervisor = asyncio.create_task(_supervise_detached_task(task, lane, debug_label))
                _DETACHED_SUPERVISORS.add(supervisor)
                supervisor.add_done_callback(_DETACHED_SUPERVISORS.discard)
                # The supervisor owns the lane lifecycle now; just drop our
                # ContextVar reference and let this response finish.
                _release_lane()
                return

            try:
                # FIRST stop the work task, THEN drain the lane — never let them
                # touch the coordinator concurrently. On a client disconnect the
                # generator's `async for` ends with the work task still running;
                # draining while the task may still fire a commit_async or run its
                # own cancel-handler persist would race the same coordinator.
                # Cancel + await (bounded) so the task's cancel handler finishes
                # its shielded persist BEFORE the lane drain runs. This dissolves
                # the cancel-path commit/drain races at the source.
                if task is not None and not task.done():
                    # A teardown with the task still running is a CLIENT disconnect
                    # unless the host says the SERVER is going away (deploy drain):
                    # shutdown is never "cancelled" — the run is abandoned and the
                    # host's lease reaper records it failed, as for any canceled task.
                    start.cancelled_by_disconnect = not host_is_shutting_down()
                    task.cancel()
                    try:
                        await asyncio.wait_for(
                            asyncio.shield(task),
                            timeout=_WORK_TASK_JOIN_TIMEOUT_SECONDS,
                        )
                    except asyncio.CancelledError:
                        # A task canceled during startup is expected to finish
                        # with CancelledError. Do not let that replace the
                        # original emitter/startup exception; a cancellation
                        # of this response task itself must still propagate.
                        current = asyncio.current_task()
                        if current is not None and current.cancelling():
                            raise
                        if not task.cancelled():
                            raise
                    except (TimeoutError, Exception):
                        # Task's own cancel handler captured to system_write_failure;
                        # the lane drain below is the backstop. Bounded so a wedged
                        # task can't hang teardown.
                        pass
                # Drain the lane so DEFERRED tail work (labeler, deferred
                # persistence, metrics) gets to finish. Clients have seen
                # send_end() already; the connection holds open just long enough
                # for deferred work to land. Soft mode (client cancel) cancels
                # BLOCKING/NORMAL in flight but lets DEFERRED finish.
                await lane.begin_drain(
                    failed=start.main_failed or startup_failed,
                    soft=start.main_cancelled and not startup_failed,
                )
            except Exception as drain_exc:
                # Drain itself must never break the response.
                vcprint(
                    f"[{debug_label}] lane drain raised: {type(drain_exc).__name__}: {drain_exc}",
                    color="yellow",
                )
            finally:
                _release_lane()

    headers: dict[str, str] = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    if ctx.request_id:
        headers["X-Request-ID"] = ctx.request_id
    if ctx.conversation_id:
        headers["X-Conversation-ID"] = ctx.conversation_id

    return _WorkStartsStreamingResponse(
        _stream(),
        on_call_end=_ensure_work_started,
        media_type="application/x-ndjson",
        headers=headers,
    )


class RouteLane:
    """Handle yielded by :func:`open_route_lane` — the lane opened at ROUTE
    entry plus its ContextVar install token. Pass ``.lane`` / ``.token`` to
    ``create_prepared_streaming_response(existing_lane=..., existing_lane_token=...)``
    and call :meth:`hand_off` once that call returns a response — from that
    point the streaming generator owns the drain + ContextVar release."""

    __slots__ = ("lane", "token", "_handed_off")

    def __init__(self, lane: RequestLane, token: Any) -> None:
        self.lane = lane
        self.token = token
        self._handed_off = False

    def hand_off(self) -> None:
        """Mark the lane as owned by a streaming response (skip exit drain)."""
        self._handed_off = True


class open_route_lane:
    """Async context manager for KD-1 Phase 2 — open + install the RequestLane
    at ROUTE entry, BEFORE any prep work runs, so every prep-phase DB write
    (cx_conversation, cx_user_request, …) queues into the request's
    WriteCoordinator instead of blocking on a one-shot Session — and becomes
    visible to pending-aware reads for the rest of the request.

    Guarantees finalization on EVERY exit: unless :meth:`RouteLane.hand_off`
    was called (a streaming response took ownership of the lane), the exit
    path drains the lane (``begin_drain(failed=True)`` — idempotent, no-op
    when nothing queued) and releases the ContextVar. This covers the
    HTTPException paths (404/409/422), any unexpected raise, and non-stream
    returns — queued prep writes can never leak.

    Opening the lane is a pure constructor (no DB connection is pinned; the
    Session acquires its connection lazily at flush), so holding it open
    across prep costs nothing.

    Usage::

        async with open_route_lane(ctx) as route_lane:
            ...prep that may queue writes...
            resp = await create_prepared_streaming_response(
                ctx, prepare_fn, run_fn,
                existing_lane=route_lane.lane,
                existing_lane_token=route_lane.token,
            )
            route_lane.hand_off()
            return resp
    """

    __slots__ = ("_ctx", "_debug_label", "_route_lane")

    def __init__(self, ctx: AppContext, *, debug_label: str = "route") -> None:
        self._ctx = ctx
        self._debug_label = debug_label
        self._route_lane: RouteLane | None = None

    async def __aenter__(self) -> RouteLane:
        ctx = self._ctx
        lane = RequestLane.open(
            lane_id=ctx.request_id,
            scope_kind="request",
            context_snapshot={
                "user_id": ctx.user_id,
                "request_id": ctx.request_id,
                "conversation_id": ctx.conversation_id,
                "source_app": ctx.source_app,
                "agent_id": ctx.agent_id,
            },
        )
        token = set_current_lane(lane)
        self._route_lane = RouteLane(lane, token)
        return self._route_lane

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        route_lane = self._route_lane
        if route_lane is None or route_lane._handed_off:
            return False
        # No streaming response took ownership → drain queued prep writes NOW
        # (data first), then release the ContextVar. begin_drain is idempotent
        # and a no-op when nothing was queued.
        try:
            await route_lane.lane.begin_drain(failed=True, soft=False)
        except Exception as drain_exc:  # noqa: BLE001 — drain must never mask the real error
            vcprint(
                f"[{self._debug_label}] route-entry lane drain raised: "
                f"{type(drain_exc).__name__}: {drain_exc}",
                color="yellow",
            )
        try:
            reset_current_lane(route_lane.token)
        except (ValueError, LookupError, RuntimeError):
            # Token already used — the adopted-lane path inside
            # create_prepared_streaming_response reset it on its own
            # not-handed-off exit (its redundant safety layer). Only
            # force-clear if OUR lane is somehow still installed; never
            # clobber a state someone else restored.
            if get_current_lane() is route_lane.lane:
                set_current_lane(None)
        return False


async def create_prepared_streaming_response(
    ctx: AppContext,
    prepare_fn: Callable[[], Awaitable[tuple[Any, ...]]],
    run_fn: Callable[..., Awaitable[None]],
    *,
    initial_message: str = "Initializing Matrx...",
    debug_label: str = "stream",
    detach_on_disconnect: bool = True,
    existing_lane: RequestLane | None = None,
    existing_lane_token: Any = None,
    run: StreamRun | None = None,
) -> StreamingResponse:
    """Run fallible request preparation, THEN stream — so a preparation failure
    reaches the client as a structured error event instead of a raw 500 that
    the browser surfaces as an opaque "Failed to fetch".

    The problem this solves: routers historically did all their fallible prep
    (tool/capability resolution, conversation setup, …) BEFORE calling
    ``create_streaming_response``. Any exception there became an HTTP 500/JSON
    body, the NDJSON stream never opened, and the streaming client — which only
    knows how to read a 200 NDJSON body — reported a generic transport error
    with no real cause.

    ``prepare_fn`` is an awaitable returning a tuple whose FIRST element is the
    (possibly-updated) ``AppContext`` and whose remaining elements are the
    positional business args for ``run_fn(emitter, *args)``. On success this
    delegates to ``create_streaming_response`` unchanged (so happy-path opening
    events — conversation id, record-reserved — are emitted exactly as before,
    since prep has already populated the context).

    On failure:
      * ``HTTPException`` (auth 401, ownership 404/409, body validation 422) is
        re-raised unchanged — those are genuine HTTP outcomes the client
        handles via status code, not chat-stream errors.
      * Any other exception is deferred into the streaming task and re-raised
        there, so it flows through the EXISTING task error handler — one error
        path — which captures it to the error-tracking system and emits a
        ``fatal_error`` event carrying ``exc.error_info`` (e.g. a
        ``ToolMergeError``'s ``tool_merge_error`` + human ``user_message``).

    The lane is opened and installed BEFORE ``prepare_fn`` runs, so prep-phase
    DB writes (cx_user_request, etc.) queue into the request's WriteCoordinator
    instead of blocking on one-shot Sessions — and they become visible to
    pending-aware reads for the rest of the request. The streaming task then
    ADOPTS this lane (so finalization still happens at work-end). The critical
    safety rule: if prep raises (HTTPException, or anything before a streaming
    response takes ownership of the lane), we MUST drain the lane here so any
    queued prep write still flushes — otherwise opening the lane early would
    silently lose those writes.

    ``existing_lane`` / ``existing_lane_token`` — KD-1 Phase 2 (lane at ROUTE
    entry). Routes whose prep work starts BEFORE this helper is called (e.g.
    ``run_chat_request`` resolves/creates the conversation upstream of its
    prep_fn) open + install the lane at route entry and pass it here so the
    upstream writes queue into the same coordinator. When adopting, this
    function does NOT open or install a second lane; the route entry owns the
    final drain/ContextVar-release on the not-handed-off path (the drain here
    still runs as a redundant, idempotent safety layer).
    """
    from fastapi import HTTPException  # noqa: F401  (re-raised as-is below)

    from matrx_connect.chat_timing import chat_timing_mark

    # Open + install the lane BEFORE prep so prep writes queue (see docstring) —
    # unless the route already did (lane-at-route-entry), in which case adopt it.
    if existing_lane is not None:
        lane = existing_lane
        lane_token = existing_lane_token
    else:
        lane = RequestLane.open(
            lane_id=ctx.request_id,
            scope_kind="request",
            context_snapshot={
                "user_id": ctx.user_id,
                "request_id": ctx.request_id,
                "conversation_id": ctx.conversation_id,
                "source_app": ctx.source_app,
                "agent_id": ctx.agent_id,
            },
        )
        lane_token = set_current_lane(lane)
    # True once a StreamingResponse takes ownership of the lane (it then owns
    # the drain + ContextVar release via the generator). Until then, THIS
    # function must drain/release on every exit so queued prep writes never leak.
    handed_off = False

    chat_timing_mark("prep_begin", "streaming prep begin")
    try:
        try:
            prepared = await prepare_fn()
        except HTTPException:
            # Genuine HTTP outcome (401/404/409/422). Re-raise unchanged — but
            # the finally below FIRST drains the lane so any write prep already
            # queued (e.g. cx_user_request) still lands. Without this drain,
            # opening the lane before prep would lose those writes.
            raise
        except Exception as exc:
            if getattr(exc, "is_caller_refusal", False) and getattr(exc, "http_status", None):
                # A CALLER REFUSAL decided during prep (e.g. a guest whose free AI
                # actions are used up) is a genuine HTTP outcome, exactly like an
                # HTTPException: nothing has streamed and no turn exists, so the
                # host's exception handler answers it (403 + its own envelope)
                # instead of opening a stream that would only carry an error.
                raise
            # Defer into the task so the single, shared error path (capture_error
            # + fatal_error, reading exc.error_info) handles it identically to a
            # mid-stream crash. Hand the already-open lane (which holds prep's
            # queued writes) to that task so they flush in its drain.
            async def _raise_prepare_error(emitter: Emitter, _exc: BaseException = exc) -> None:
                raise _exc

            from matrx_connect.context.app_context import try_get_app_context

            current_ctx = try_get_app_context()
            error_ctx = (
                current_ctx if current_ctx is not None and current_ctx.emitter is not None else ctx
            )
            resp = create_streaming_response(
                error_ctx,
                _raise_prepare_error,
                initial_message=initial_message,
                debug_label=debug_label,
                detach_on_disconnect=detach_on_disconnect,
                existing_lane=lane,
                existing_lane_token=lane_token,
                run=run,
            )
            handed_off = True
            return resp

        prepared_ctx = prepared[0]
        run_args = tuple(prepared[1:])
        chat_timing_mark("prep_complete", "streaming prep complete — opening NDJSON response")
        resp = create_streaming_response(
            prepared_ctx,
            run_fn,
            *run_args,
            initial_message=initial_message,
            debug_label=debug_label,
            detach_on_disconnect=detach_on_disconnect,
            existing_lane=lane,
            existing_lane_token=lane_token,
            run=run,
        )
        handed_off = True
        return resp
    finally:
        if not handed_off:
            # Nothing will ever open a body for this request, so staged
            # pre-wire frames have no wire to reach. Drop them loudly rather
            # than leaving them to look delivered.
            staged_emitter = getattr(ctx, "emitter", None)
            discard = getattr(staged_emitter, "discard_staged_wire", None)
            if callable(discard):
                discard()
            # No streaming response took ownership of the lane → drain the
            # queued prep writes NOW (data first), then release the ContextVar.
            # Covers the HTTPException path and any raise from
            # create_streaming_response itself. begin_drain is idempotent and a
            # no-op when nothing was queued.
            try:
                await lane.begin_drain(failed=True, soft=False)
            except Exception as drain_exc:
                vcprint(
                    f"[{debug_label}] prep-path lane drain raised: "
                    f"{type(drain_exc).__name__}: {drain_exc}",
                    color="yellow",
                )
            finally:
                try:
                    reset_current_lane(lane_token)
                except (ValueError, LookupError):
                    set_current_lane(None)
