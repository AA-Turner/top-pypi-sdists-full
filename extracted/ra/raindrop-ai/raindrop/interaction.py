from __future__ import annotations
import logging
import time
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TYPE_CHECKING,
    Union,
    Iterator,
)
from datetime import datetime, timezone
from uuid import uuid4
from dataclasses import dataclass

from .models import Attachment, PartialTrackAIEvent
from . import analytics as _core
from opentelemetry import context as context_api

if TYPE_CHECKING:
    from .analytics import ManualSpan
    from .subagent import SubagentDispatch


# ``finish(*, output=None, **extra)`` salvage sets (DEV-1184). ``**extra`` used
# to be splatted straight into ``PartialTrackAIEvent(**extra)``; because the
# models are ``extra="forbid"`` a single unknown key raised a ValidationError
# that finish()'s crash-guard swallowed, silently dropping the ENTIRE final
# update — output included. Instead we route each extra key: recognized
# top-level fields pass through, known AI fields are nested under ``ai_data``
# (the same wire contract begin(model=...) uses), and anything unknown is
# dropped with a loud, rate-limited warning while the valid fields still ship.
_FINISH_PASSTHROUGH_FIELDS = frozenset(
    {"user_id", "event", "timestamp", "properties", "attachments"}
)
_FINISH_AI_DATA_ALIASES = frozenset({"model", "input", "convo_id"})


class Interaction:
    """
    Thin helper returned by analytics.begin().
    Each mutator just relays a partial update back to Analytics.
    """

    __slots__ = (
        "_event_id",
        "_user_id",
        "_event",
        "_convo_id",
        "_analytics",
        "_state",
        "_bound_ctx",
        "_tool_events_frame",
        "_disabled",
        "_finish_called",
        "__weakref__",
    )

    def __init__(
        self,
        event_id: Optional[str] = None,
        user_id: Optional[str] = None,
        event: Optional[str] = None,
        convo_id: Optional[str] = None,
        disabled: bool = False,
        state: Any = None,
        bound_ctx: Any = None,
    ) -> None:
        self._event_id = event_id or str(uuid4())
        self._user_id = user_id
        self._event = event
        self._convo_id = convo_id
        self._analytics = _core
        # Pipeline state of the client that began this interaction. ``None``
        # means the default (module-level) client — every partial, finish,
        # and tool span relays through it so the interaction routes with its
        # owning client's key/project for its whole lifetime.
        self._state = state
        # The exact binding begin() pushed onto the routing-context stack;
        # finish() removes it by identity (non-LIFO safe) so reused (sync)
        # worker threads can't leak this interaction's project into later
        # requests, and finishing the first of two interleaved interactions
        # can't disturb the still-open sibling's binding.
        self._bound_ctx = bound_ctx
        # The tool-call-only opt-in frame, if this turn asked for one. Scoped to
        # the interaction for the same reason as the routing binding above: a
        # reused worker thread keeps its context, so an opt-in left bound would
        # let a later turn that launched nothing become an event.
        self._tool_events_frame = None
        # When True, every mutator / finish / span / tool call is a no-op so
        # that callers who passed invalid arguments to ``begin()`` don't crash
        # the whole code path. ``analytics.begin()`` is the only place that
        # constructs a disabled Interaction today.
        self._disabled = disabled
        # Whether finish() has been called. Recorded, not enforced: finishing
        # twice remains a legitimate way to revise an event, and only a caller
        # that layers its own lifecycle on top of this one — a sub-agent run —
        # needs to know whether the event was already closed behind its back.
        self._finish_called = False

    @property
    def finished(self) -> bool:
        """Whether ``finish()`` has been called on this interaction."""
        return self._finish_called

    # -- mutators ----------------------------------------------------------- #
    def set_input(self, text: str) -> None:
        if self._disabled:
            return
        # Cap BEFORE buffering: an O(1) length check keeps multi-MB inputs
        # from ever entering the merge/serialize pipeline at full size.
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(
                event_id=self._event_id,
                ai_data={"input": self._analytics._cap_text(text, state=self._state)},
            ),
            state=self._state,
        )

    def add_attachments(self, attachments: List[Attachment]) -> None:
        if self._disabled:
            return
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(event_id=self._event_id, attachments=attachments),
            state=self._state,
        )

    def set_properties(self, props: Dict[str, Any]) -> None:
        if self._disabled:
            return
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(event_id=self._event_id, properties=props),
            state=self._state,
        )

    def set_property(self, key: str, value: Any) -> None:
        if self._disabled:
            return
        self.set_properties({key: value})

    def set_model(self, model: str) -> None:
        """Attach (or overwrite) the AI model for this open interaction.

        Companion to ``begin(model=...)`` for mid-lifecycle updates; the model
        is nested under ``ai_data`` on the wire, matching the TS SDK.
        """
        if self._disabled:
            return
        self._analytics._track_ai_partial(
            PartialTrackAIEvent(
                event_id=self._event_id,
                ai_data={"model": model},
            ),
            state=self._state,
        )

    def finish(self, *, output: str | None = None, **extra: Any) -> None:
        """Mark the interaction complete.

        This call is non-blocking AND O(1) for the caller: the output string
        is capped with a cheap length check, the buffered event object is
        enqueued as-is, and serialization, PII redaction, size checks, and
        the HTTP POST all run on the background flush thread. It is safe to
        call ``finish()`` from a request hot path or an asyncio event loop
        regardless of payload size.

        On process shutdown, ``analytics.shutdown()`` (registered via
        ``atexit``) drains any still-pending partials before exiting, under
        the shutdown deadline.

        Unknown keyword arguments in ``**extra`` never cause silent data loss
        (DEV-1184): recognized fields (``user_id``/``event``/``timestamp``/
        ``properties``/``attachments``) pass through, known AI fields
        (``model``/``input``/``convo_id``) nest under ``ai_data``, and any
        unrecognized key is dropped with a loud, rate-limited warning while
        the valid fields — ``output`` above all — still ship.
        """
        self._finish_called = True
        if self._disabled:
            return
        try:
            capped_output = (
                self._analytics._cap_text(output, state=self._state)
                if output is not None
                else None
            )

            ai_data: Dict[str, Any] = {}
            if capped_output is not None:
                ai_data["output"] = capped_output
            passthrough: Dict[str, Any] = {}
            unknown: List[str] = []
            for key, value in extra.items():
                if key in _FINISH_AI_DATA_ALIASES:
                    ai_data[key] = (
                        self._analytics._cap_text(value, state=self._state)
                        if key == "input" and isinstance(value, str)
                        else value
                    )
                elif key in _FINISH_PASSTHROUGH_FIELDS:
                    passthrough[key] = value
                else:
                    unknown.append(key)

            if unknown:
                self._analytics._rate_limited_log(
                    "interaction-finish-unknown-kwarg",
                    logging.WARNING,
                    "[raindrop] finish() got unsupported keyword argument(s) "
                    "%s for event %s; dropping only those and delivering the "
                    "rest of the final update (including output). Pass AI "
                    "fields such as 'model' — they are nested under ai_data — "
                    "and see the SDK docs for supported finish() arguments.",
                    sorted(unknown),
                    self._event_id,
                )

            payload = self._coalesce_finish_payload(ai_data, passthrough)
            if payload is not None:
                self._analytics._track_ai_partial(payload, state=self._state)
        except Exception:
            # Crash protection (AGENTS.md): a telemetry finish() must never
            # take the host app down. Log with traceback and degrade; the
            # finally below still cleans up the routing binding.
            self._analytics.logger.error(
                "[raindrop] finish() failed for event %s; dropping the final "
                "update.",
                self._event_id,
                exc_info=True,
            )
        finally:
            # Remove the routing binding pushed at begin() even when building
            # or enqueueing the final partial raises (e.g. invalid **extra):
            # on frameworks that reuse sync worker threads, later requests
            # must not inherit this interaction's project. Identity-based and
            # best-effort — a finish() on a different thread/task than its
            # begin() safely no-ops, and finishing the first of two
            # interleaved interactions leaves the still-open sibling's
            # binding in place (see unbind_current).
            self._analytics._rd_tracing.unbind_current(self._bound_ctx)
            self._bound_ctx = None
            self._analytics._rd_tracing.unbind_span_attributes(
                self._tool_events_frame
            )
            self._tool_events_frame = None

    def _coalesce_finish_payload(
        self, ai_data: Dict[str, Any], passthrough: Dict[str, Any]
    ) -> Optional[PartialTrackAIEvent]:
        """Build the final ``PartialTrackAIEvent``, salvaging valid fields.

        A recognized field can still carry an invalid *value* (e.g.
        ``properties`` that isn't a dict, or a non-string ``model``) and trip
        ``extra="forbid"`` validation. Rather than lose the whole update, fall
        back in widening steps so the highest-value payload that validates
        ships: drop the passthrough fields, then drop the invalid AI aliases
        while keeping ``output`` (the crown-jewel field), then a bare close.
        The final ``is_pending=False`` close guarantees the interaction still
        settles instead of lingering until the inactivity timeout.
        """

        def _build(ad: Dict[str, Any], pt: Dict[str, Any]) -> PartialTrackAIEvent:
            return PartialTrackAIEvent(
                event_id=self._event_id,
                ai_data=ad or None,
                is_pending=False,
                **pt,
            )

        # 1. Everything as supplied.
        try:
            return _build(ai_data, passthrough)
        except Exception:
            pass

        # 2. A recognized top-level field carried an invalid value — drop the
        #    passthrough fields, keep the full ai_data (output + model/...).
        if passthrough:
            self._analytics._rate_limited_log(
                "interaction-finish-invalid-field",
                logging.WARNING,
                "[raindrop] finish() got invalid value(s) for %s on event "
                "%s; dropping those fields and still delivering ai_data "
                "(output/model). See the SDK docs for expected types.",
                sorted(passthrough),
                self._event_id,
            )
            try:
                return _build(ai_data, {})
            except Exception:
                pass

        # 3. A known AI alias (model/input/convo_id) carried an invalid value,
        #    poisoning the whole ai_data blob. Keep only ``output`` — a capped
        #    str that is always valid — so the crown-jewel field still ships.
        output_only = {k: v for k, v in ai_data.items() if k == "output"}
        if output_only != ai_data:
            self._analytics._rate_limited_log(
                "interaction-finish-invalid-ai-field",
                logging.WARNING,
                "[raindrop] finish() got invalid AI field value(s) %s on event "
                "%s; dropping them and still delivering output. See the SDK "
                "docs for expected types.",
                sorted(k for k in ai_data if k != "output"),
                self._event_id,
            )
            try:
                return _build(output_only, {})
            except Exception:
                pass

        # 4. Nothing else validates — close the interaction (is_pending=False)
        #    without a body so it settles rather than lingering to the timeout.
        self._analytics.logger.error(
            "[raindrop] finish() could not build the final payload for event "
            "%s; closing the interaction without it.",
            self._event_id,
            exc_info=True,
        )
        try:
            return PartialTrackAIEvent(event_id=self._event_id, is_pending=False)
        except Exception:
            return None

    def allow_tool_events(self) -> None:
        """Let this turn become an event even with no assistant text.

        Ingest creates an event from an outermost LLM span only when the span
        has content or this explicit opt-in, so a turn whose entire content is
        sub-agent launches (``finishReason = "tool-calls"``) would otherwise
        never produce an event — and a hand-off with no caller event has nothing
        to attach to. ``subagent()`` calls this itself; call it directly
        *before* the model call when the launch decision comes out of an LLM
        span that has already closed by the time you dispatch.
        """
        from .subagent import allow_tool_events

        allow_tool_events(self)

    def subagent(
        self,
        *,
        name: str,
        input: Any | None = None,
        child_event_id: str | None = None,
        tool_name: str | None = None,
        properties: Dict[str, Any] | None = None,
    ) -> "SubagentDispatch":
        """Declare a detached (asynchronous, cross-process) sub-agent on this turn.

        Records the dispatch and returns what you need to send the job. It does
        NOT dispatch anything — the transport is yours, whether that is HTTP, a
        queue or a spawned process::

            dispatch = interaction.subagent(name="researcher",
                                            input={"task": task})
            requests.post(worker_url, json=job, headers=dispatch.headers)

        The child's event id is minted here, before the job goes out, so the
        link is resolvable immediately. The child adopts
        ``dispatch.child_event_id`` as its OWN event and reports its own
        lifecycle there; this turn records only that it launched something.
        Nothing here claims to know how the child got on — status is derived
        from the child's event, because this process returned a job handle and
        moved on.

        TRUST BOUNDARY: ``dispatch.headers`` name the event the receiver will be
        attributed to, so dispatch only to services inside your own trust
        boundary (see :mod:`raindrop.handoff`).

        Requires ``tracing_enabled=True``: the dispatch is recorded on a span.
        Without tracing the carrier is still returned (so the child links back)
        and a warning explains what is missing.
        """
        from .subagent import subagent

        return subagent(
            self,
            name=name,
            input=input,
            child_event_id=child_event_id,
            tool_name=tool_name,
            properties=properties,
        )

    def start_span(
        self,
        kind: Literal["task", "tool"],
        name: str,
        version: int | None = None,
    ) -> "ManualSpan":
        """
        Create a manual span tied to this interaction.

        The span automatically inherits association properties from this interaction
        (event_id, user_id, event, convo_id) for proper tracing.

        Args:
            kind: Type of span - "task" or "tool"
            name: Name of the span
            version: Optional version number

        Returns:
            ManualSpan instance that must be explicitly ended with .end()
        """
        if self._disabled:
            # Return a no-op ManualSpan whose record_*/set_properties/end all no-op.
            return self._analytics.ManualSpan(
                None, kind, name, self._event_id, state=self._state
            )
        return self._analytics.start_span(
            kind,
            name,
            version,
            event_id=self._event_id,
            user_id=self._user_id,
            event=self._event,
            convo_id=self._convo_id,
            state=self._state,
        )

    def track_tool(
        self,
        *,
        name: str,
        input: Any | None = None,
        output: Any | None = None,
        duration_ms: float | int | None = None,
        start_time: datetime | int | float | None = None,
        error: BaseException | str | None = None,
        properties: Dict[str, Any] | None = None,
        version: int | None = None,
    ) -> None:
        """
        Retroactively log a tool span tied to this interaction.
        """
        if self._disabled:
            return
        st = _core._resolve_state(self._state)
        if not st._tracing_enabled:
            return

        # Duration normalization
        dur_ms = float(duration_ms) if duration_ms is not None else 0.0
        if dur_ms < 0:
            dur_ms = 0.0
        duration_ns = int(round(dur_ms * 1_000_000))

        # start_time normalization (epoch nanoseconds)
        start_ns: int | None = None
        if isinstance(start_time, datetime):
            dt = start_time
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)

            epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
            delta = dt - epoch
            total_us = (
                delta.days * 86400 + delta.seconds
            ) * 1_000_000 + delta.microseconds
            start_ns = total_us * 1_000
        elif isinstance(start_time, (int, float)):
            v = float(start_time)
            # Heuristic: values smaller than ~1973 in ms are likely epoch-seconds
            start_ns = (
                int(round(v * 1_000_000_000))
                if abs(v) < 1e11
                else int(round(v * 1_000_000))
            )

        if start_ns is None:
            start_ns = time.time_ns() - duration_ns

        end_ns = start_ns + duration_ns

        tlp_kind = _core.TraceloopSpanKindValues.TOOL
        span_name = f"{name}.{tlp_kind.value}"

        association_props = {
            "event_id": self._event_id,
            "user_id": self._user_id,
            "event": self._event,
            "convo_id": self._convo_id,
        }

        merged_association_props: Dict[str, Any] = {
            key: value for key, value in association_props.items() if value is not None
        }

        if properties:
            for key, value in properties.items():
                if key in association_props or value is None:
                    continue
                if isinstance(value, str):
                    merged_association_props[key] = _core._cap_text(value, state=self._state)
                elif isinstance(value, (bool, int, float)):
                    merged_association_props[key] = value
                else:
                    try:
                        merged_association_props[key] = _core._dumps_bounded(
                            value, cls=_core.JSONEncoder, state=self._state
                        )
                    except Exception:
                        merged_association_props[key] = _core._cap_text(
                            str(value), state=self._state
                        )

        serialized_input: str | None = None
        serialized_output: str | None = None
        if _core._should_send_prompts():
            # Bounded serialization: cost is proportional to the configured
            # field cap, not the payload, so huge tool payloads can't stall
            # the calling thread (often the host app's event loop).
            if input is not None:
                try:
                    serialized_input = _core._dumps_bounded(
                        {"args": [input]}, cls=_core.JSONEncoder, state=self._state
                    )
                except Exception as e:
                    _core.logger.debug(
                        f"[raindrop] Could not serialize input for span: {e}"
                    )

            if output is not None:
                try:
                    serialized_output = _core._dumps_bounded(
                        output, cls=_core.JSONEncoder, state=self._state
                    )
                except Exception as e:
                    _core.logger.debug(
                        f"[raindrop] Could not serialize output for span: {e}"
                    )

        error_message = (
            str(error)
            if error is not None
            else None
        )

        if st._bypass_otel_for_tools:
            direct_span = _core._build_direct_tool_span(
                span_name=span_name,
                tool_name=name,
                version=version,
                start_ns=start_ns,
                end_ns=end_ns,
                duration_ms=dur_ms if duration_ms is not None else None,
                input_value=serialized_input,
                output_value=serialized_output,
                error_message=error_message,
                association_properties=merged_association_props,
                extra_attributes=_core._rd_tracing.current_span_attributes(),
            )
            _core._enqueue_direct_tool_span(direct_span, state=self._state)
            if _core.debug_logs:
                _core.logger.debug(
                    f'[raindrop] track_tool (direct): queued tool span "{name}" (duration_ms={duration_ms})'
                )
            return

        if not _core.TracerWrapper.verify_initialized():
            return

        tracer = _core.trace.get_tracer("traceloop.tracer")
        span = tracer.start_span(span_name, start_time=start_ns)

        try:
            span.set_attribute(_core.SpanAttributes.TRACELOOP_SPAN_KIND, tlp_kind.value)
            span.set_attribute(_core.SpanAttributes.TRACELOOP_ENTITY_NAME, name)

            # Pin the owning client's project on the span: track_tool is often
            # called from a different task/thread than the one that bound the
            # context, so the processor's context stamp can't be relied on.
            _core._rd_tracing.stamp_span(span, st.project_id, st.auth_hint)
            _core._rd_tracing.stamp_context_attributes(span)
            if version is not None:
                span.set_attribute(
                    _core.SpanAttributes.TRACELOOP_ENTITY_VERSION, version
                )

            for key, value in merged_association_props.items():
                span.set_attribute(f"traceloop.association.properties.{key}", value)

            if duration_ms is not None:
                span.set_attribute("traceloop.entity.duration_ms", dur_ms)

            if serialized_input is not None:
                span.set_attribute(
                    _core.SpanAttributes.TRACELOOP_ENTITY_INPUT, serialized_input
                )

            if serialized_output is not None:
                span.set_attribute(
                    _core.SpanAttributes.TRACELOOP_ENTITY_OUTPUT, serialized_output
                )

            if error is not None:
                exc = (
                    error if isinstance(error, BaseException) else Exception(str(error))
                )
                span.set_status(_core.Status(_core.StatusCode.ERROR, str(exc)))
                span.record_exception(exc)
            else:
                span.set_status(_core.Status(_core.StatusCode.OK))
        finally:
            span.end(end_time=end_ns)

        if _core.debug_logs:
            _core.logger.debug(
                f'[raindrop] track_tool: logged tool span "{name}" (duration_ms={duration_ms})'
            )

    # convenience
    @property
    def id(self) -> str:
        return self._event_id
