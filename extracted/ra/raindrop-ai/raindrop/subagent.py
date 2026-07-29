"""Declare and resume detached async sub-agents.

The two halves of the hand-off contract in :mod:`raindrop.handoff`:

* **Caller** — ``Interaction.subagent()`` mints the child's event id
  before dispatching, records the dispatch on a span, and hands back the
  headers to send with the job. Dispatching the job stays the caller's.
* **Child** — ``Raindrop.resume_subagent()`` (or the module-level
  ``raindrop.analytics.resume_subagent()``) adopts that event id, opens the
  child's own event, and stamps the reverse reference on every span the child
  emits until it reports a result.

Nothing about this is nested: the child has its own trace, its own event, and
its own lifecycle, and the two are joined only by the attributes both sides
write. See :mod:`raindrop.handoff` for the contract itself and the trust
boundary that governs carriers.
"""

from __future__ import annotations

import asyncio
import logging
import secrets
from concurrent import futures
from typing import Any, Dict, Mapping, Optional, TYPE_CHECKING
from uuid import uuid4

from raindrop import _tracing as _rd_tracing
from raindrop import handoff
from raindrop.handoff import TraceContext

if TYPE_CHECKING:  # pragma: no cover - typing only
    from raindrop._state import RaindropState
    from raindrop.interaction import Interaction

logger = logging.getLogger("raindrop.analytics")

DEFAULT_SUBAGENT_NAME = "subagent"
# The span's tool name: what the TURN did, which is launch a sub-agent. Unlike
# the SDK call, the turn really does launch one — the caller dispatches the job
# moments later — so this stays as it reads in the UI.
DEFAULT_DISPATCH_TOOL_NAME = "launch_subagent"

# A dispatch returns a handle, not an answer: the answer is the child's, and it
# arrives in the child's own event long after this turn closed.
_DISPATCH_ACCEPTED = "accepted"

# Distinct from the reason the context manager records for a block that ended
# without reporting: the outcome is identical, but which of the two happened is
# the whole of the difference between a caller that forgot to report and one
# that reported nothing, and only the reason text can say which.
_FINISHED_EMPTY = "sub-agent finished without output"


class SubagentDispatch:
    """The record of one detached dispatch, returned by ``subagent``.

    ``child_event_id`` is allocated before the job is handed off, which is what
    makes the link resolvable immediately — the caller's conversation can point
    at the child's event from the moment the dispatch is recorded, before the
    child has emitted anything.
    """

    __slots__ = ("context", "dispatch_span_id")

    def __init__(self, context: TraceContext, dispatch_span_id: str | None) -> None:
        self.context = context
        self.dispatch_span_id = dispatch_span_id

    @property
    def child_event_id(self) -> str:
        """The child's own event id — the job handle to pass to the worker."""
        return self.context.child_event_id or ""

    @property
    def name(self) -> str | None:
        return self.context.name

    @property
    def parent_event_id(self) -> str:
        return self.context.event_id

    @property
    def headers(self) -> Dict[str, str]:
        """Native carrier headers: W3C ``traceparent`` + ``baggage``, plus
        ``x-raindrop-handoff``.

        Send all of them. The standard pair is what other readers understand, and
        the Raindrop one is what survives an instrumented HTTP client, which
        rewrites both of the others in transit.

        TRUST BOUNDARY: send these only to services inside your own trust
        boundary (see :mod:`raindrop.handoff`).
        """
        return handoff.to_headers(self.context)

    @property
    def langsmith_headers(self) -> Dict[str, str]:
        """The same carrier in LangSmith's header shape, for services that
        still parse ``langsmith-trace``."""
        return handoff.to_langsmith_headers(self.context)

    def __repr__(self) -> str:  # pragma: no cover - debugging nicety
        return (
            f"SubagentDispatch(child_event_id={self.child_event_id!r}, "
            f"name={self.name!r}, dispatch_span_id={self.dispatch_span_id!r})"
        )


def _random_hex(num_bytes: int) -> str:
    return secrets.token_hex(num_bytes)


def allow_tool_events(interaction: "Interaction") -> None:
    """Opt this turn into event creation from a tool-call-only turn.

    Ingest builds an event from an outermost LLM span only when it has content
    OR this opt-in: a turn whose entire content is sub-agent launches finishes
    with ``finishReason = "tool-calls"`` and no assistant text, so without it
    **the caller's event is never created** and the hand-off has nothing to
    attach to.

    Applies to every span started later in this execution context, and to the
    span that is current right now (typically the turn's still-open root). A
    span that has already ended cannot be amended, so a supervisor whose
    dispatch decision comes out of an already-closed LLM span should call this
    *before* that model call — ``Interaction.subagent`` calls it too, which
    covers the common case where the launches happen inside the turn's span.
    """
    if getattr(interaction, "_disabled", False):
        return
    attributes = {handoff.TOOL_EVENTS_ATTRIBUTE: handoff.TOOL_EVENTS_ALLOW}
    _stamp_current_span(attributes)
    # Bound for the rest of the turn, so a model span that opens after the
    # dispatch carries the opt-in too — and removed when the interaction
    # finishes, exactly like its routing binding. A reused worker thread keeps
    # its context between requests, so an opt-in left bound would let a later
    # turn that launched nothing become an event. Once per turn: a supervisor
    # that dispatches ten sub-agents needs one frame, not ten.
    if getattr(interaction, "_tool_events_frame", None) is None:
        interaction._tool_events_frame = _rd_tracing.bind_span_attributes(
            attributes, interaction
        )


def _current_recording_span() -> Any:
    """The span that is current right now, or ``None``.

    A non-recording no-op span (tracing disabled) counts as none: there is
    nothing to write on it.
    """
    from opentelemetry.trace import get_current_span

    span = get_current_span()
    if not getattr(span, "is_recording", None) or not span.is_recording():
        return None
    return span


def _span_started_under(frame: Any) -> Any:
    """The open span IF this run started it, otherwise ``None``.

    Under HTTP auto-instrumentation a request span is already current when the
    run resumes, and that span is the host's, not the child's: it predates the
    run, so it carries none of the run's reverse reference and ingest does not
    attribute it to the child's event. Writing the run's outcome there would
    redden the host's request while leaving the child with no errored span of
    its own — which derives as *finished*, the silent wrong answer ``fail()``
    exists to prevent. Every span the run itself opens carries its whole frame,
    so that is the test.
    """
    span = _current_recording_span()
    if span is None or not _rd_tracing.frame_applies_to(span, frame):
        return None
    return span


def _stamp_current_span(attributes: Mapping[str, str]) -> None:
    """Set attributes on the span that is current right now, if any.

    Best effort by nature: the current span may be a non-recording no-op span
    (tracing disabled) or already ended, and neither is a reason to fail the
    caller's code.
    """
    try:
        span = _current_recording_span()
        if span is None:
            return
        for key, value in attributes.items():
            span.set_attribute(key, value)
    except Exception as exc:
        logger.debug("[raindrop] could not stamp the current span: %s", exc)


def _fail_this_runs_span(reason: str | BaseException, frame: Any) -> bool:
    """Mark this run's open span as failed, if it has one.

    Returns whether anything was marked, because the answer changes what the
    run reports: with no errored span a failed run is derived as *finished*.

    Best effort by nature, like ``_stamp_current_span``: the current span may
    be a non-recording no-op span (tracing disabled), already ended, or not
    this run's at all, and none of those is a reason to fail the caller's code.
    """
    try:
        from opentelemetry.trace import Status, StatusCode

        span = _span_started_under(frame)
        if span is None:
            return False
        span.set_status(Status(StatusCode.ERROR, _reason_text(reason)))
        if isinstance(reason, BaseException):
            span.record_exception(reason)
        return True
    except Exception as exc:
        logger.debug("[raindrop] could not mark the run's span failed: %s", exc)
        return False


def subagent(
    interaction: "Interaction",
    *,
    name: str,
    input: Any | None = None,
    child_event_id: str | None = None,
    tool_name: str | None = None,
    properties: Optional[Dict[str, Any]] = None,
) -> SubagentDispatch:
    """Record a detached sub-agent dispatch on ``interaction`` (see
    ``Interaction.subagent`` for the public docstring)."""
    resolved_child_event_id = child_event_id or str(uuid4())
    resolved_name = name or DEFAULT_SUBAGENT_NAME
    trace_id: str | None = None
    dispatch_span_id: str | None = None

    try:
        # Order matters: the child event id exists before anything is
        # dispatched, so the caller can hand it to the worker AND record it,
        # and a reader that follows the link finds an id that is already the
        # child's own.
        allow_tool_events(interaction)

        dispatch_attributes = handoff.dispatch_attributes(
            child_event_id=resolved_child_event_id, name=resolved_name
        )
        with _rd_tracing.span_attributes(dispatch_attributes):
            span = interaction.start_span(
                "tool", tool_name or DEFAULT_DISPATCH_TOOL_NAME
            )
            try:
                # Read the ids FIRST. They are what the child points back at, and
                # anything below can raise — `record_input` serializes caller data,
                # `set_properties` hands caller values to OTel — into the crash
                # guard, which would then return a carrier with freshly minted ids
                # while this span really existed under different ones, leaving the
                # child's `parentSpanId` naming a span nobody can find.
                trace_id = span.trace_id
                dispatch_span_id = span.span_id
                if input is not None:
                    span.record_input(input)
                # The dispatch's "result" is the job handle; the answer
                # belongs to the child's event and never appears here.
                span.record_output(
                    {"jobId": resolved_child_event_id, "status": _DISPATCH_ACCEPTED}
                )
                if properties:
                    span.set_properties(properties)
            finally:
                span.end()

        if dispatch_span_id is None:
            # No span pipeline (tracing disabled, or a disabled interaction):
            # the child can still reference this event, but the caller's own
            # conversation has no dispatch span to render the sub-agent from.
            logger.warning(
                "[raindrop] Interaction.subagent(%s): no dispatch span was recorded, "
                "so event %s will not show the launch. The returned carrier "
                "still links the child back to it. Tracing must be enabled "
                "(tracing_enabled=True) for dispatches to be recorded.",
                resolved_name,
                interaction.id,
            )
    except Exception:
        # Crash protection: a telemetry hand-off must never take the host app
        # down, and the caller still needs a child event id and a carrier to
        # dispatch with.
        logger.error(
            "[raindrop] Interaction.subagent(%s) failed to record the dispatch; "
            "returning a carrier so the child still links back.",
            resolved_name,
            exc_info=True,
        )

    context = TraceContext(
        # traceparent needs both ids; without a span there is nothing to
        # continue, so a fresh pair keeps the carrier well-formed for the
        # child's own W3C parsing.
        trace_id=trace_id or _random_hex(16),
        span_id=dispatch_span_id or _random_hex(8),
        event_id=interaction.id,
        child_event_id=resolved_child_event_id,
        name=resolved_name,
        convo_id=getattr(interaction, "_convo_id", None),
        user_id=getattr(interaction, "_user_id", None),
    )
    return SubagentDispatch(context, dispatch_span_id)


class SubagentRun:
    """A detached sub-agent's own run, as seen from inside the sub-agent.

    Wraps the child's own Raindrop event (``interaction``) and keeps the
    reverse reference bound to the execution context, so **every** span the
    child emits while the run is open carries it — spans are ingested and
    projected independently, so a reference on the root alone would be
    invisible to anything reading a child span on its own.

    Use it as a context manager so an abort is always reported::

        with rd.resume_subagent(headers=request.headers) as run:
            run.finish(output=answer)

    A run that leaves the block without reporting output is closed with its
    abort reason. That is not cosmetic: an event is only created from a span
    with non-empty output, so a child that dies silently produces no event at
    all, and the caller's launch stays ``queued`` forever — indistinguishable
    from a job that never started.
    """

    __slots__ = (
        "_interaction",
        "_parent",
        "_name",
        "_convo_id",
        "_frame",
        "_finished",
        # So the reverse-reference frame can hold this run weakly: a run
        # abandoned without finishing stops stamping when it is collected.
        "__weakref__",
    )

    def __init__(
        self,
        interaction: "Interaction",
        parent: TraceContext | None,
        name: str,
        convo_id: str | None,
        frame: Any,
    ) -> None:
        self._interaction = interaction
        self._parent = parent
        self._name = name
        self._convo_id = convo_id
        self._frame = frame
        self._finished = False

    # -- identity ------------------------------------------------------------ #

    @property
    def interaction(self) -> "Interaction":
        """The child's own Raindrop event."""
        return self._interaction

    @property
    def event_id(self) -> str:
        return self._interaction.id

    @property
    def name(self) -> str:
        return self._name

    @property
    def convo_id(self) -> str | None:
        """The conversation this run reports into — the launcher's when linked."""
        return self._convo_id

    @property
    def parent(self) -> TraceContext | None:
        """The launching context, or ``None`` when invoked without a carrier.

        ``None`` is a legitimate state — the sub-agent was called directly
        rather than launched — and the run still reports as its own event, just
        without a link back.
        """
        return self._parent

    @property
    def linked(self) -> bool:
        return self._parent is not None

    # -- lifecycle ----------------------------------------------------------- #

    def finish(self, *, output: str | None = None, **extra: Any) -> None:
        """Complete the child's event with its result.

        An output that says nothing is not a report. An event needs non-empty
        output to exist, so closing on one produces no event and leaves the
        launcher on ``queued`` forever — the same outcome as never calling this
        at all, which :meth:`__exit__` already rescues. Without this guard the
        call would still latch ``_finished`` and that rescue would be skipped,
        so the one shape of the failure that arrives through the ANSWER path
        would be the one shape nothing catches: no event, and no warning
        either. ``run.finish(output=result)`` where ``result`` came back
        ``None`` is the ordinary way to reach it.

        Reported rather than rejected, and by the same route as the silent
        block: the child did not answer, and that reads as an abort whether it
        stopped answering one line before this call or one line after. Any
        other fields the caller passed still ship, so the guard costs nothing
        it was not already losing.
        """
        if not (output or "").strip():
            logger.warning(
                "[raindrop] sub-agent run %s (%s) finished with no output; "
                "closing it with an abort reason instead. An event needs "
                "non-empty output to exist, so finishing empty would leave its "
                "launcher showing 'queued' forever — pass the child's result to "
                "finish(output=...), or call fail(reason) / cancel() when there "
                "is no result to pass.",
                self.event_id,
                self._name,
            )
            self._abort(_FINISHED_EMPTY, **extra)
            return
        self._close(output=output, **extra)

    def fail(self, reason: str | BaseException) -> None:
        """Report that the run aborted: error the child's span, say why in the
        output.

        Both halves matter, and they answer different readers:

        * The ERROR status on the child's own span is what makes the run read
          as *failed*. Status is derived from the child's telemetry, and a run
          with output but no errored span is indistinguishable from one that
          succeeded — it would report as finished.
        * The output is what makes the run exist at all: an event needs
          non-empty output, so a child that closes empty leaves its launcher on
          ``queued`` forever.

        The span it errors is whichever one is open. When none is — a job
        killed before it reached the model, which is much of what ``fail()``
        exists for — it records one, so the failure is visible at all.

        The child erroring its own span is not a second writer — the contract's
        single-writer rule is about the CALLER never writing the child's status.
        Failure is meant to be legible from the child's own spans, which is why
        only ``cancelled`` needs an explicit marker.

        A cancellation handed to ``fail()`` is reported as a cancellation, not a
        failure: ``except asyncio.CancelledError as exc: run.fail(exc)`` is the
        natural way to write it, and erroring spans for it would collapse the
        distinction the contract depends on. Call :meth:`cancel` directly when
        you know it was cancelled.
        """
        self._abort(reason)

    def _abort(self, reason: str | BaseException, **extra: Any) -> None:
        # First, ahead of the cancellation branch: a cancellation raised past a
        # child that already answered is the same rewrite as an abort would be.
        # An explicit finish() followed by one leaves the answer alone, and
        # closing the event through `run.interaction` must not behave differently.
        # An explicit cancel() is still honoured — a caller saying so outranks
        # bookkeeping — but nothing arriving on the way out of the block relabels
        # an outcome the child already reported.
        if self._reported():
            self._warn_if_closed_behind_our_back()
            self._release()
            return
        if _is_cancellation(reason):
            # A cancellation that arrives as an exception is still a
            # cancellation. Reporting it as a failure would error the child's
            # spans, and error spans are the only thing that separates
            # cancelled from failed.
            self.cancel(reason)
            return
        # A failure has to leave an errored span behind or it is derived as
        # finished. Mark whatever is open; if nothing is and the child has not
        # errored a span already, record one — the killed-before-it-reached-the-
        # model case, which is much of what aborting is.
        if not _fail_this_runs_span(reason, self._frame):
            if not getattr(self._frame, "saw_error_span", False):
                self._record_abort_span(reason)
        self._close(output=f"Aborted: {_reason_text(reason)}", **extra)

    def _reported(self) -> bool:
        """Whether this child has already said how it went, by either route."""
        return self._finished or self._interaction.finished

    def _warn_if_closed_behind_our_back(self) -> None:
        if self._finished:
            return
        logger.warning(
            "[raindrop] sub-agent run %s (%s) was finished through "
            "run.interaction rather than run.finish(); its outcome stands, "
            "but call run.finish(output=...) so a cancellation or failure "
            "can be recorded as one.",
            self.event_id,
            self._name,
        )

    def _record_abort_span(self, reason: str | BaseException) -> bool:
        """Record the errored span a failure needs when nothing else is open.

        Frequently the child's ONLY span, so it carries the full reverse
        reference: anything reading it alone still knows which launch it
        belongs to.
        """
        from raindrop import analytics as _core

        try:
            state = _core._resolve_state(self._interaction._state)
            if not state._tracing_enabled or not _core.TracerWrapper.verify_initialized():
                # Nothing emits spans in this configuration, so there is no span
                # shape to get wrong; the event still reports the reason.
                logger.debug(
                    "[raindrop] tracing is off, so sub-agent run %s reports its "
                    "failure as output only.",
                    self.event_id,
                )
                return False

            from opentelemetry.trace import Status, StatusCode

            with _core.get_tracer() as tracer:
                span = tracer.start_span(handoff.ABORT_SPAN_NAME)
            try:
                span.set_attribute(
                    handoff.OPERATION_ID_ATTRIBUTE, handoff.ABORT_OPERATION_ID
                )
                _core._rd_tracing.stamp_span(span, state.project_id, state.auth_hint)
                # From the run's own frame rather than the ambient stack: fail()
                # is often called from a different task or thread than the one
                # that opened the run, and this span is the one that can least
                # afford to lose the link.
                for key, value in getattr(self._frame, "attributes", {}).items():
                    span.set_attribute(key, value)
                for key, value in (
                    ("event_id", self.event_id),
                    ("user_id", self._interaction._user_id),
                    ("event", self._interaction._event),
                    ("convo_id", self._convo_id),
                ):
                    if value:
                        span.set_attribute(
                            f"{handoff.ASSOCIATION_PROPERTY_PREFIX}{key}", value
                        )
                span.set_status(Status(StatusCode.ERROR, _reason_text(reason)))
                if isinstance(reason, BaseException):
                    span.record_exception(reason)
            finally:
                span.end()
            return True
        except Exception as exc:
            logger.debug("[raindrop] could not record the abort span: %s", exc)
            return False

    def cancel(self, reason: str | BaseException | None = None) -> None:
        """Mark the run cancelled — the one state its telemetry cannot express.

        A cancelled run is span-for-span identical to a finished one (spans
        close, nothing errors, there is simply no answer), so it needs an
        explicit marker. The child writes it on itself, on its own event and its
        own spans, so the child stays the only writer of its lifecycle.

        A cancellation raised into the run (``asyncio.CancelledError``) lands
        here too, whether it was handed to ``fail()`` or left the run's block.
        Spans it passed through on the way out keep the error they recorded —
        that is what happened to them — and the marker still names the outcome,
        because a reader consults it before it counts error spans.
        """
        text = _reason_text(reason) if reason is not None else "cancelled by caller"
        cancelled = handoff.cancelled_attributes()
        # The run's own span, if the cancellation was noticed inside one, states
        # it too — that is what a reader of the child's spans alone sees.
        # Deliberately NOT bound to the execution context: this closes the run
        # on the next line, so a binding could only reach spans started after
        # the run ended, while outliving the context on a reused thread or task
        # and marking another event's spans cancelled. Unlike fail(), reaching
        # no span is not a silent wrong answer here: the marker also rides the
        # event's properties, which is what the launcher reads.
        span = _span_started_under(self._frame)
        if span is not None:
            for key, value in cancelled.items():
                span.set_attribute(key, value)
        self._close(
            output=f"Cancelled: {text}",
            # The caller's view of the child is its EVENT, not its spans, so the
            # marker has to be a property of the event as well.
            properties={handoff.TERMINAL_PROPERTY_KEY: handoff.TERMINAL_CANCELLED},
        )

    def _close(self, *, output: str | None = None, **extra: Any) -> None:
        if self._finished:
            return
        self._finished = True
        try:
            self._interaction.finish(output=output, **extra)
        finally:
            self._release()

    def _release(self) -> None:
        """Stop stamping, without reporting anything.

        The frame is weakly owned and would be pruned eventually, but "eventually"
        is whenever this object is collected, and until then every span on the
        thread carries this child's reverse reference.
        """
        self._finished = True
        if self._frame is None:
            return
        _rd_tracing.unbind_span_attributes(self._frame)
        self._frame = None

    # -- context manager ----------------------------------------------------- #

    def __enter__(self) -> "SubagentRun":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        if exc is not None:
            # The exception propagated out through whatever spans were open,
            # so they already recorded it — and if it passed through none, the
            # abort span is what makes the failure visible at all. A
            # cancellation raised into the task is routed to cancel() instead
            # (see _abort); returning False re-raises it either way, because
            # swallowing a cancellation would strand the task that raised it.
            self._abort(exc)
            return False
        if self._reported():
            # Reported, just not through this object: `run.interaction` is public
            # so the child can attach its spans and tools, and finishing through
            # it is an easy thing to reach for. Aborting anyway would append
            # "Aborted: ..." over a real answer and record an error span, turning
            # a child that succeeded into one that reads as `failed` — so the
            # event's own state settles this, not only this object's bookkeeping.
            self._warn_if_closed_behind_our_back()
            self._release()
            return False
        if not self._finished:
            # Closing empty would produce no event at all; say what happened
            # instead, and say it loudly enough to get fixed.
            logger.warning(
                "[raindrop] sub-agent run %s (%s) ended without reporting "
                "output; closing it with an abort reason. An event needs "
                "non-empty output to exist, so a silent child leaves its "
                "launcher showing 'queued' forever — call finish(output=...), "
                "fail(reason) or cancel() before leaving the block.",
                self.event_id,
                self._name,
            )
            self._abort("sub-agent ended without reporting output")
        return False


_CANCELLATIONS: tuple[type[BaseException], ...] = (
    asyncio.CancelledError,
    futures.CancelledError,
)


def _is_cancellation(reason: Any) -> bool:
    """Whether an abort reason IS a cancellation rather than a failure.

    asyncio cancels a task by raising into it, so the most likely shape of a
    cancelled child is an ``except``/``finally`` that reports the exception it
    caught, or the exception simply leaving the run's block. Both arrive here
    looking exactly like a failure, and calling them one would error the child's
    spans — the only thing that separates cancelled from failed.

    Both cancellation types are listed because they are genuinely different
    classes, not aliases: ``asyncio.CancelledError`` is raised INTO a task and
    inherits ``BaseException``, while ``concurrent.futures.CancelledError`` is an
    ``Exception`` raised OUT of ``Future.result()`` when the work was cancelled —
    which is how a thread-pool worker learns its job is gone, and a very common
    shape for a Python sub-agent.

    A ``TimeoutError`` is deliberately NOT cancellation: a job that ran out of
    time failed to do its work, and nothing superseded it.
    """
    return isinstance(reason, _CANCELLATIONS)


def _reason_text(reason: str | BaseException) -> str:
    if isinstance(reason, BaseException):
        # Bare cancellations carry no message, and "CancelledError: " reads as
        # truncated output rather than as the whole reason.
        message = str(reason)
        name = type(reason).__name__
        return f"{name}: {message}" if message else name
    return str(reason)


def _carrier_first(local: str | None, carried: str | None, field: str) -> str | None:
    """Resolve one identity field, with the CARRIER authoritative.

    The launcher allocated these identities before dispatching, and they are
    what its own record points at, so a child that substitutes its own breaks
    the link it exists to complete:

    * ``event_id`` — the caller's pill points at the id it minted; a different
      one leaves that pill on ``queued`` forever, pointing at nothing.
    * ``convo_id`` — the child lands in a different conversation than its
      supervisor, which is the view this hand-off exists to populate.
    * ``user_id`` — the child is attributed to someone other than the person
      whose turn launched it.
    * ``name`` — the child's spans disagree with the dispatch about what was
      launched.

    Arguments are demoted to fallbacks for the direct-invocation case (no
    carrier), which is exactly when a sub-agent service's own labels are the
    right ones. This is inverted from normal Python precedence, so a conflict
    says so rather than silently discarding the caller's value. Matches the
    TypeScript SDK.
    """
    if carried and local and local != carried:
        logger.warning(
            "[raindrop] resume_subagent: ignoring %s=%r in favor of the "
            "launcher's %r from the carrier; the launcher allocated it, and a "
            "child that substitutes its own breaks the link back to it.",
            field,
            local,
            carried,
        )
    return carried or local


def resume_subagent(
    *,
    headers: Mapping[str, Any] | None = None,
    parent: TraceContext | None = None,
    user_id: str | None = None,
    event: str | None = None,
    name: str | None = None,
    input: str | None = None,
    convo_id: str | None = None,
    event_id: str | None = None,
    properties: Optional[Dict[str, Any]] = None,
    model: str | None = None,
    state: "RaindropState | None" = None,
) -> SubagentRun:
    """Open the child's own event for a launched sub-agent (see
    ``Raindrop.resume_subagent`` for the public docstring)."""
    from raindrop import analytics as _core

    resolved_parent = parent or handoff.from_headers(headers)

    def carried(field: str) -> str | None:
        return getattr(resolved_parent, field) if resolved_parent else None

    resolved_name = (
        _carrier_first(name, carried("name"), "name") or DEFAULT_SUBAGENT_NAME
    )
    resolved_event_id = (
        _carrier_first(event_id, carried("child_event_id"), "event_id")
        or str(uuid4())
    )
    resolved_user_id = _carrier_first(user_id, carried("user_id"), "user_id")
    resolved_convo_id = _carrier_first(convo_id, carried("convo_id"), "convo_id")

    if resolved_parent is None:
        logger.debug(
            "[raindrop] resume_subagent(%s): no hand-off carrier on the request; "
            "reporting as an unlinked event %s.",
            resolved_name,
            resolved_event_id,
        )

    frame = None
    if resolved_parent is not None:
        frame = _rd_tracing.bind_span_attributes(
            handoff.subagent_attributes(
                parent_event_id=resolved_parent.event_id,
                parent_span_id=resolved_parent.span_id,
                name=resolved_name,
            )
        )

    try:
        interaction = _core.begin(
            user_id=resolved_user_id or "",
            event=event or f"subagent.{resolved_name}",
            event_id=resolved_event_id,
            input=input,
            convo_id=resolved_convo_id,
            properties=properties,
            model=model,
            state=state,
        )
    except BaseException:
        # The frame has to be bound before the interaction exists, so until the
        # run takes ownership of it below there is nothing whose lifetime bounds
        # it. If begin() never returns — a rejected properties payload is built
        # outside its own crash guard — the frame would keep stamping this
        # thread's later, unrelated turns with another launch's reverse
        # reference.
        _rd_tracing.unbind_span_attributes(frame)
        raise
    if getattr(interaction, "_disabled", False):
        # begin() has already said what was wrong with the arguments; this says
        # what it costs here, because the cost is invisible from the child's
        # side. Every report on this run no-ops, so no child event is ever
        # created and the launcher's reference stays on `queued` — the exact
        # reading a job that never started produces. A user id is not
        # inventable: it identifies the launcher's user, so it comes from the
        # carrier or from the caller, never from us.
        logger.warning(
            "[raindrop] resume_subagent(%s): the interaction was rejected, so "
            "this run cannot report and launch %s will stay queued. Pass "
            "user_id=, or have the launcher send a carrier that carries one.",
            resolved_name,
            resolved_event_id,
        )
    run = SubagentRun(
        interaction, resolved_parent, resolved_name, resolved_convo_id, frame
    )
    # The frame had to be bound before the interaction was begun, so it takes
    # its owner now: an abandoned run cannot leave its reverse reference on a
    # reused worker thread for the next turn to inherit.
    _rd_tracing.own_span_attributes(frame, run)
    return run
