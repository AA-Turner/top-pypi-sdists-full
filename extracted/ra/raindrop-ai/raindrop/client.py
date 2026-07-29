"""Instance-based Raindrop client.

``Raindrop`` is the instance-shaped counterpart of the module-level API in
``raindrop.analytics`` — the same shape as the JS (``new Raindrop({...})``),
Go (``raindrop.New(...)``), Rust (``Client::builder()``), and Java
(``new Raindrop(config)``) SDKs. Each instance owns its full configuration
and event pipeline (buffers, background flush thread, partial-event merge
tables, shutdown lifecycle), so one process can run several clients routing
to different projects concurrently::

    from raindrop import Raindrop

    rd_support = Raindrop(api_key=KEY, project_id="support-agent",
                          tracing_enabled=True)
    rd_billing = Raindrop(api_key=KEY, project_id="billing-agent")

    interaction = rd_billing.begin(user_id="u1", event="chat", input="...")
    interaction.finish(output="...")
    rd_support.track_ai(user_id="u1", event="chat", input="q", output="a")

Manual events (track / track_ai / begin / finish / signals / identify) ship on the
instance's own connections with its own ``Authorization`` and
``X-Raindrop-Project-Id`` headers — fully isolated per instance.

OpenTelemetry tracing is a PROCESS singleton (one tracer provider, one
exporter, global auto-instrumentation): the first client constructed with
``tracing_enabled=True`` initializes it; later tracing clients share it.
Per-project span routing rides the ``raindrop.project_id`` span attribute,
stamped from the execution context bound by ``begin()`` / ``as_current()``.
Sharing the pipeline across DIFFERENT api_keys (different orgs) is
unsupported: those spans are dropped at export with a warning rather than
delivered to the wrong org.

The module-level API (``raindrop.analytics.init()`` etc.) remains fully
supported and is simply the default, process-wide instance of this same
machinery.
"""

from __future__ import annotations

import weakref
from typing import (
    Any,
    ContextManager,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
)

from raindrop import _tracing as _rd_tracing
from raindrop import analytics as _analytics
from raindrop import subagent as _subagent
from raindrop._state import ClientState
from raindrop.handoff import TraceContext
from raindrop.interaction import Interaction
from raindrop.local_debugger import UNSET
from raindrop.models import Attachment, PartialTrackAIEvent
from raindrop.subagent import SubagentRun


class Raindrop:
    """A self-contained Raindrop client bound to one project/config."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        project_id: str | None = None,
        tracing_enabled: bool = False,
        auto_instrument: bool = True,
        bypass_otel_for_tools: bool = False,
        endpoint: str | None = None,
        local_workshop_url: Any = UNSET,
        max_text_field_chars: int | None = None,
        max_queue_size: int | None = None,
        redact_pii: bool = False,
        debug_logs: bool = False,
        wizard_session: str | None = None,
        **traceloop_kwargs: Any,
    ) -> None:
        """Create an independent client. Arguments mirror ``analytics.init()``.

        Additional per-instance knobs:
            max_queue_size: In-memory event buffer bound (default 10,000).
            redact_pii: Apply PII redaction to this client's events.
            debug_logs: Raise the SDK's process-wide log verbosity (logging
                configuration is global by nature).

        ``max_text_field_chars`` is per-instance here: it caps THIS client's
        payload fields only and never mutates the process-wide default
        (which module-level ``init()`` continues to own).
        """
        self._state = ClientState()
        if max_queue_size is not None and max_queue_size > 0:
            self._state.max_queue_size = max_queue_size
        self._state.redact_pii = bool(redact_pii)

        if debug_logs:
            _analytics.set_debug_logs(True)

        # Crash protection (AGENTS.md): constructing a client at app startup
        # must never take the host down. _configure degrades tracing failures
        # internally; this outer guard covers anything unexpected — worst
        # case the client comes up partially configured (e.g. no write key →
        # warn-and-no-op on use) instead of raising.
        try:
            _analytics._configure(
                self._state,
                api_key=api_key,
                wizard_session=wizard_session,
                tracing_enabled=tracing_enabled,
                auto_instrument=auto_instrument,
                bypass_otel_for_tools=bypass_otel_for_tools,
                endpoint=endpoint,
                local_workshop_url=local_workshop_url,
                max_text_field_chars=max_text_field_chars,
                project_id=project_id,
                **traceloop_kwargs,
            )
        except Exception as e:
            _analytics.logger.error(
                "[raindrop] Raindrop(...) configuration failed (%s: %s); "
                "client may be partially configured.",
                type(e).__name__,
                e,
            )
        self._state.auth_hint = _rd_tracing.auth_hint_for_key(self._state.write_key)
        # Lets this client's background flush loop notice when the host app
        # dropped the client, so the thread drains once more and exits.
        self._state.client_ref = weakref.ref(self)

        # Register the STATE for the shared atexit drain. States are held
        # strongly while their pipeline is live so buffered events survive to
        # process exit even if the host drops the client object; the flush
        # loop unregisters the state after its collected-client final drain.
        _analytics._instance_states.add(self._state)

    # -- identity ----------------------------------------------------------- #

    @property
    def project_id(self) -> str | None:
        """The validated project slug this client routes to (None = default)."""
        return self._state.project_id

    @property
    def write_key(self) -> str | None:
        """This client's write (API) key, or None if it was not configured.

        A public read-only accessor for the key backing this instance's
        pipeline, so callers (e.g. integration wrappers comparing whether two
        clients are equivalent) do not have to reach into ``_state``.
        """
        return self._state.write_key

    def __repr__(self) -> str:  # pragma: no cover - debugging nicety
        return (
            f"Raindrop(project_id={self._state.project_id!r}, "
            f"endpoint={self._state.api_url!r}, "
            f"tracing_enabled={self._state._tracing_enabled!r})"
        )

    # -- context binding ----------------------------------------------------- #

    def as_current(self) -> ContextManager[None]:
        """Scope auto-instrumented spans in the ``with`` block to this client.

        ::

            with rd_billing.as_current():
                openai_client.chat.completions.create(...)  # spans route to
                                                            # billing's project

        Needed only for LLM/library calls made OUTSIDE an interaction —
        ``begin()`` already binds the context for its request/task.
        Concurrency-safe (contextvars are per-thread and per-asyncio-task);
        nesting restores the outer client on exit.
        """
        return _rd_tracing.as_current(self._state.project_id, self._state.auth_hint)

    # -- event tracking ------------------------------------------------------ #

    def track(
        self,
        user_id: str,
        event: str,
        event_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[Attachment]] = None,
    ) -> str | None:
        return _analytics.track(
            user_id=user_id,
            event=event,
            event_id=event_id,
            timestamp=timestamp,
            properties=properties,
            attachments=attachments,
            state=self._state,
        )

    def track_ai(
        self,
        user_id: str,
        event: str,
        event_id: Optional[str] = None,
        model: Optional[str] = None,
        input: Optional[str] = None,
        output: Optional[str] = None,
        convo_id: Optional[str] = None,
        properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
        timestamp: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
    ) -> str | None:
        return _analytics.track_ai(
            user_id=user_id,
            event=event,
            event_id=event_id,
            model=model,
            input=input,
            output=output,
            convo_id=convo_id,
            properties=properties,
            timestamp=timestamp,
            attachments=attachments,
            state=self._state,
        )

    def track_signal(
        self,
        event_id: str,
        name: str,
        signal_type: Literal["default", "feedback", "edit"] = "default",
        timestamp: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        attachment_id: Optional[str] = None,
        comment: Optional[str] = None,
        after: Optional[str] = None,
        sentiment: Optional[Literal["POSITIVE", "NEGATIVE"]] = None,
    ) -> None:
        return _analytics.track_signal(
            event_id=event_id,
            name=name,
            signal_type=signal_type,
            timestamp=timestamp,
            properties=properties,
            attachment_id=attachment_id,
            comment=comment,
            after=after,
            sentiment=sentiment,
            state=self._state,
        )

    def identify(
        self, user_id: str, traits: Dict[str, Union[str, int, bool, float]]
    ) -> None:
        return _analytics.identify(user_id, traits, state=self._state)

    def track_ai_partial(self, event: PartialTrackAIEvent) -> None:
        """Merge a partial ``track_ai`` patch into THIS client's buffers.

        For integration wrappers that stream incremental event updates: the
        patch merges into this instance's partial-event tables and flushes on
        ``is_pending=False`` (or after the inactivity timeout), on the
        instance's own connections. The module-level
        ``raindrop.analytics._track_ai_partial`` is the default-client
        equivalent.
        """
        return _analytics._track_ai_partial(event, state=self._state)

    # -- interactions --------------------------------------------------------- #

    def begin(
        self,
        user_id: str,
        event: str,
        event_id: str | None = None,
        properties: Optional[Dict[str, Any]] = None,
        input: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
        convo_id: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Interaction:
        """Start an interaction bound to this client (and bind the current
        execution context to this client's project for span routing)."""
        return _analytics.begin(
            user_id=user_id,
            event=event,
            event_id=event_id,
            properties=properties,
            input=input,
            attachments=attachments,
            convo_id=convo_id,
            model=model,
            state=self._state,
        )

    def resume_interaction(self, event_id: str | None = None) -> Interaction:
        return _analytics.resume_interaction(event_id, state=self._state)

    # -- detached sub-agents ---------------------------------------------------- #

    def resume_subagent(
        self,
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
    ) -> SubagentRun:
        """Open this sub-agent's OWN event for a detached launch.

        Pass the inbound request's headers; the carrier on them names the event
        that launched this run and the event id it allocated for it::

            with rd.resume_subagent(headers=request.headers) as run:
                answer = do_work()
                run.finish(output=answer)

        Every span emitted while the run is open carries the reverse reference
        back to the launcher, and leaving the block without reporting output
        closes the event with an abort reason rather than silently producing no
        event at all (which would pin the launcher's view on ``queued``).

        A request with no carrier is not an error — the sub-agent was invoked
        directly — and the run still reports as its own (unlinked) event, with
        ``run.parent`` set to ``None``.

        Identity arguments (``event_id``, ``convo_id``, ``user_id``, ``name``)
        are the one place the carrier overrides rather than the other way
        round. The launcher allocated them before dispatching and its own
        record points at them, so a child that substitutes its own breaks the
        link — most severely for ``event_id``, where the launcher would be left
        pointing at an event that never appears. They apply when there is no
        carrier, which is exactly when the sub-agent's own labels are right.

        A user id is the one thing this cannot supply for you: it identifies
        the launcher's user. A Raindrop-launched child gets it from the carrier;
        anything else has to pass ``user_id``, or the run has no event to report
        on and the launcher stays on ``queued`` (logged as a warning).

        TRUST BOUNDARY: a carrier names the event this process will be
        attributed to. Only resume from requests that came from inside your own
        trust boundary (see :mod:`raindrop.handoff`).
        """
        return _subagent.resume_subagent(
            headers=headers,
            parent=parent,
            user_id=user_id,
            event=event,
            name=name,
            input=input,
            convo_id=convo_id,
            event_id=event_id,
            properties=properties,
            model=model,
            state=self._state,
        )

    # -- spans ----------------------------------------------------------------- #

    def set_span_properties(self, properties: Dict[str, Any]) -> None:
        """Set association properties on the current span (gated on THIS
        client's tracing flag, unlike the module-level function)."""
        _analytics.set_span_properties(properties, state=self._state)

    def task_span(
        self, name: str, version: int | None = None
    ) -> "_analytics._EntitySpanContext":
        return _analytics.task_span(name, version, state=self._state)

    def tool_span(
        self, name: str, version: int | None = None
    ) -> "_analytics._EntitySpanContext":
        return _analytics.tool_span(name, version, state=self._state)

    def start_span(
        self,
        kind: Literal["task", "tool"],
        name: str,
        version: int | None = None,
        event_id: str | None = None,
        user_id: str | None = None,
        event: str | None = None,
        convo_id: str | None = None,
    ) -> "_analytics.ManualSpan":
        return _analytics.start_span(
            kind,
            name,
            version,
            event_id=event_id,
            user_id=user_id,
            event=event,
            convo_id=convo_id,
            state=self._state,
        )

    # -- lifecycle -------------------------------------------------------------- #

    def flush(self) -> None:
        """Drain this client's buffers to the API (blocking)."""
        _analytics.flush(state=self._state)

    def shutdown(self) -> None:
        """Flush and stop this client under the standard 10s deadline."""
        _analytics.shutdown(state=self._state)

    # Context-manager sugar: ``with Raindrop(...) as rd:`` flushes on exit.
    def __enter__(self) -> "Raindrop":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.shutdown()
