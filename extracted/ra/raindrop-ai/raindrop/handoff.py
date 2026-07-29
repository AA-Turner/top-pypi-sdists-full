"""Detached async sub-agent contract (``raindrop.handoff.*``) and its carrier.

A **detached** sub-agent runs outside the caller's process and reports as its
OWN Raindrop event with its OWN lifecycle, instead of as spans nested inside
the caller's trace. It crosses both the OTel trace boundary and the Raindrop
event boundary, so nothing in OTel's parent/child model links the two — the
link is carried explicitly on span attributes.

This is deliberately distinct from a *continuation*, where the remote process
joins the caller's event by reusing its event id (``resume_interaction``).
Continuations need none of the attributes here: event-id grouping already
merges those traces. The distinction is not "same machine vs different
machine", it is "does the caller's turn own this work" — a synchronous call to
a remote service is a continuation; a fire-and-forget job on the same box is
detached.

Written by the caller, on the exact dispatch span::

    raindrop.handoff.mode         = "detached"
    raindrop.handoff.childEventId = <the child's event id>
    raindrop.handoff.name         = <sub-agent name>

Written by the child, on EVERY span it emits::

    raindrop.handoff.parentEventId = <the caller's event id>
    raindrop.handoff.parentSpanId  = <the dispatch span id>
    raindrop.handoff.name          = <sub-agent name>
    raindrop.agent.role            = "subagent"
    raindrop.handoff.terminal      = "cancelled"   (only when cancelled)

Status is NOT part of the contract. The caller returned a job handle and moved
on, so any status it wrote would be a guess that goes stale; readers derive
status from the child event itself. ``cancelled`` is the single exception,
because a cancelled run is span-for-span identical to a finished one, and it is
written BY THE CHILD on itself so the child stays the only writer of its own
lifecycle.

This module is intentionally dependency-free (no OpenTelemetry, no analytics
pipeline): a web handler can import it to read a carrier off an inbound request
without pulling in the tracing stack. The runtime API that emits spans lives in
``raindrop.subagent``.

TRUST BOUNDARY
--------------
A carrier names the event a child will be attributed to, so accepting one from
an untrusted caller lets that caller write into another tenant's trace. Only
accept carriers from services inside your own trust boundary — the same
constraint LangSmith documents for distributed tracing.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional, Sequence

logger = logging.getLogger("raindrop.analytics")

# --- Span attribute names (the single source of truth) ------------------------
#
# Bare keys, exactly as dawn's prefix-tolerant reader (`@dawn/schemas/handoff`)
# looks them up. That reader also accepts an `ai.telemetry.metadata.` or
# `ai.settings.context.` prefix, because the Vercel AI SDK nests user metadata;
# this SDK emits the bare form, which is the one it can set directly on a span.

MODE_ATTRIBUTE = "raindrop.handoff.mode"
CHILD_EVENT_ID_ATTRIBUTE = "raindrop.handoff.childEventId"
PARENT_EVENT_ID_ATTRIBUTE = "raindrop.handoff.parentEventId"
PARENT_SPAN_ID_ATTRIBUTE = "raindrop.handoff.parentSpanId"
NAME_ATTRIBUTE = "raindrop.handoff.name"
TERMINAL_ATTRIBUTE = "raindrop.handoff.terminal"
AGENT_ROLE_ATTRIBUTE = "raindrop.agent.role"

DETACHED_MODE = "detached"
SUBAGENT_ROLE = "subagent"
TERMINAL_CANCELLED = "cancelled"

# The terminal marker is the one part of the contract a reader of the CHILD
# EVENT alone needs (the caller's pill has the child's event, not its spans).
# Ingest copies `ai.telemetry.metadata.*` onto the event with the prefix
# trimmed and allow-lists this key, so the child writes the prefixed form on
# its spans and the plain form lands in the event's `properties`.
TERMINAL_METADATA_ATTRIBUTE = f"ai.telemetry.metadata.{TERMINAL_ATTRIBUTE}"
TERMINAL_PROPERTY_KEY = TERMINAL_ATTRIBUTE

# Ingest creates an event from an outermost LLM span only if it has a finish
# reason, a user id, and either content or this opt-in. A supervisor turn whose
# entire content is launches finishes with `tool-calls` and no assistant text,
# so WITHOUT this the caller's event is never created and the hand-off has
# nothing to attach to. See `deriveEventRoots` in dawn.
#
# The prefix is load-bearing, unlike the keys above: this one is NOT read through
# the prefix-tolerant reader but by its single spelling, so `raindrop.toolEvents`
# would opt nothing in — and the failure is silent, because ingest 200s a turn it
# then drops. Write it prefixed, exactly as spelled here.
TOOL_EVENTS_ATTRIBUTE = "ai.telemetry.metadata.raindrop.toolEvents"
TOOL_EVENTS_ALLOW = "allow"

# A run that fails before it ever opens a span has nothing to carry the error,
# and a failure with no error span is derived as *finished*. The SDK records
# this span instead — the shape below is shared with the TypeScript SDK so both
# emit the same thing.
#
# `ai.operationId` is not decoration: ingest keeps only spans carrying it (or a
# traceloop key, or `gen_ai.*`) and returns 200 for the rest, so a span without
# it is dropped in silence. The value is deliberately not a model-call id —
# dawn's classifier falls through to INTERNAL for it, so the span states a
# failure without impersonating a generation.
OPERATION_ID_ATTRIBUTE = "ai.operationId"
ABORT_OPERATION_ID = "ai.subagent.failed"
ABORT_SPAN_NAME = ABORT_OPERATION_ID

# What attaches a span to an event: ingest reads the event id from here and
# falls back to the trace id when it is absent, which for a child sharing its
# launcher's trace would silently credit the launcher instead.
#
# Prefixed, and by exact spelling like the opt-in above — this is a traceloop
# convention, not a hand-off key, so nothing accepts a bare `event_id`. It is
# also NOT the reverse reference: `parentEventId` names the launch a span belongs
# to, while this names the event the span IS part of. A span that carries only
# the reverse reference attaches to the wrong event, which reads as the child
# never having errored.
ASSOCIATION_PROPERTY_PREFIX = "traceloop.association.properties."

# --- Carrier -----------------------------------------------------------------

TRACEPARENT_HEADER = "traceparent"
BAGGAGE_HEADER = "baggage"
# A Raindrop-owned header, because BOTH standard headers belong to propagators
# rather than to us: OTel's HTTP instrumentations rewrite `traceparent` from the
# current span as the request goes out, and `W3CBaggagePropagator.inject`
# REPLACES `baggage` with the context's own entries — so a caller that propagates
# a tenant id in baggage loses the entire carrier, `from_headers` returns None,
# and the child is unlinked while the launcher waits on `queued` forever.
#
# No propagator writes this one. It carries the whole context, so it is read
# first and is sufficient on its own; the standard headers stay as the fallback
# for a carrier written by another SDK.
HANDOFF_HEADER = "x-raindrop-handoff"
LANGSMITH_TRACE_HEADER = "langsmith-trace"
LANGSMITH_METADATA_BAGGAGE_KEY = "langsmith-metadata"

BAGGAGE_EVENT_ID = "raindrop-event-id"
BAGGAGE_CHILD_EVENT_ID = "raindrop-child-event-id"
BAGGAGE_NAME = "raindrop-handoff-name"
BAGGAGE_CONVO_ID = "raindrop-convo-id"
BAGGAGE_USER_ID = "raindrop-user-id"
# The dispatch span id, carried in baggage as well as in the trace header.
# Not redundant: OTel's HTTP instrumentations inject `traceparent` from whatever
# span is current as the request goes out, overwriting ours, so by the time the
# child reads it the id names the HTTP client span instead of the dispatch. The
# child would then point its reverse reference at a span the launcher's UI does
# not know as a dispatch. Baggage is only rewritten by a caller that sets OTel
# baggage of its own, which is rare, and states which span it means rather than
# meaning "whoever wrote this header last".
BAGGAGE_DISPATCH_SPAN_ID = "raindrop-dispatch-span-id"
# The trace, for the same reason: with `traceparent` rewritten it names the
# client's trace, and a dispatch whose span ended earlier may not even be in it.
BAGGAGE_TRACE_ID = "raindrop-trace-id"


class TraceContext:
    """The parent context a detached child is launched with.

    ``event_id`` is the caller's event (what the child references), and
    ``child_event_id`` is the child's OWN event id, minted by the caller before
    dispatch so the link is resolvable the moment the launch happens.
    """

    __slots__ = (
        "trace_id",
        "span_id",
        "event_id",
        "child_event_id",
        "name",
        "convo_id",
        "user_id",
    )

    def __init__(
        self,
        *,
        trace_id: str,
        span_id: str,
        event_id: str,
        child_event_id: str | None = None,
        name: str | None = None,
        convo_id: str | None = None,
        user_id: str | None = None,
    ) -> None:
        self.trace_id = trace_id
        self.span_id = span_id
        self.event_id = event_id
        self.child_event_id = child_event_id
        self.name = name
        self.convo_id = convo_id
        self.user_id = user_id

    def __repr__(self) -> str:  # pragma: no cover - debugging nicety
        return (
            f"TraceContext(trace_id={self.trace_id!r}, span_id={self.span_id!r}, "
            f"event_id={self.event_id!r}, child_event_id={self.child_event_id!r}, "
            f"name={self.name!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TraceContext):
            return NotImplemented
        return all(
            getattr(self, field) == getattr(other, field) for field in self.__slots__
        )


def _encode_baggage(entries: Mapping[str, Optional[str]]) -> str:
    return ",".join(
        f"{key}={urllib.parse.quote(value, safe='')}"
        for key, value in entries.items()
        if value
    )


def _decode_baggage(header: str | None) -> Dict[str, str]:
    """Parse a baggage-shaped value, refusing one that names a field twice.

    Duplicate HEADERS are not the only way to steal attribution: every container
    that joins duplicates — WSGI does, and so does anything built on it — turns
    them into one comma-separated value, where a repeated key would simply
    last-win. Same attack, one layer down, so it gets the same answer.

    Scoped to the fields this carrier acts on. A third party's baggage repeating
    its own key is not ours to police, and cannot steer anything we read.
    """
    if not header:
        return {}
    parsed: Dict[str, str] = {}
    for part in header.split(","):
        key, separator, value = part.partition("=")
        if not separator:
            continue
        key = key.strip()
        value = urllib.parse.unquote(value.strip())
        if key in _CARRIER_KEYS and key in parsed and parsed[key] != value:
            raise _ConflictingCarrier(key)
        parsed[key] = value
    return parsed


_CARRIER_KEYS = frozenset(
    {
        BAGGAGE_EVENT_ID,
        BAGGAGE_CHILD_EVENT_ID,
        BAGGAGE_NAME,
        BAGGAGE_CONVO_ID,
        BAGGAGE_USER_ID,
        BAGGAGE_DISPATCH_SPAN_ID,
        BAGGAGE_TRACE_ID,
        LANGSMITH_METADATA_BAGGAGE_KEY,
    }
)


def _baggage_fields(context: TraceContext) -> Dict[str, Optional[str]]:
    return {
        BAGGAGE_EVENT_ID: context.event_id,
        BAGGAGE_CHILD_EVENT_ID: context.child_event_id,
        BAGGAGE_NAME: context.name,
        BAGGAGE_CONVO_ID: context.convo_id,
        BAGGAGE_USER_ID: context.user_id,
        BAGGAGE_DISPATCH_SPAN_ID: context.span_id,
        BAGGAGE_TRACE_ID: context.trace_id,
    }


def to_headers(context: TraceContext) -> Dict[str, str]:
    """Serialize a parent context as W3C ``traceparent`` + ``baggage``.

    Both headers are standard, so proxies and gateways pass them through
    untouched. Mirrors LangSmith's ``RunTree.to_headers()`` so migrating from
    LangSmith is a rename rather than a redesign.

    Three headers, not two: the standard pair is what other readers understand,
    and ``x-raindrop-handoff`` is what survives a fully instrumented caller —
    instrumentation owns ``traceparent`` and the baggage propagator owns
    ``baggage``, so neither is ours to rely on. See ``HANDOFF_HEADER``.

    Send all three. Anything that reads a mapping works too — :func:`from_headers`
    does not care whether the carrier arrived in headers or in the job payload.

    TRUST BOUNDARY: send these only to services inside your own trust
    boundary — the carrier names the event the receiver will be attributed to
    (see the module docstring).
    """
    return {
        TRACEPARENT_HEADER: f"00-{context.trace_id}-{context.span_id}-01",
        BAGGAGE_HEADER: _encode_baggage(_baggage_fields(context)),
        HANDOFF_HEADER: _encode_baggage(_baggage_fields(context)),
    }


def _dotted_order(trace_id: str, span_id: str) -> str:
    """Build LangSmith's dotted order: ``<timestamp>Z<id>`` per segment, root
    first and current run last."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    return f"{stamp}Z{trace_id}.{stamp}Z{span_id}"


def to_langsmith_headers(context: TraceContext) -> Dict[str, str]:
    """Serialize the same context in LangSmith's header shape.

    Provided for symmetry with :func:`from_headers`'s LangSmith acceptance —
    useful when a Raindrop-instrumented caller dispatches to a service that
    still parses ``langsmith-trace``. New call sites should prefer
    :func:`to_headers`.

    The trace header is a two-segment dotted order — the trace as the root and
    the dispatch span as the current run — because that is the position, not the
    value, that tells a reader which id is which. A single segment would leave
    the trace id nowhere to live.
    """
    return {
        LANGSMITH_TRACE_HEADER: _dotted_order(context.trace_id, context.span_id),
        BAGGAGE_HEADER: _encode_baggage(
            {
                LANGSMITH_METADATA_BAGGAGE_KEY: json.dumps(
                    {
                        key: value
                        for key, value in _baggage_fields(context).items()
                        if value
                    }
                )
            }
        ),
        # Carried here too: a LangSmith-shaped carrier is rewritten by
        # instrumentation exactly like the native one, and `_split_ids` prefers
        # an injected `traceparent` over the dotted order.
        HANDOFF_HEADER: _encode_baggage(_baggage_fields(context)),
    }


class _ConflictingCarrier(Exception):
    """A carrier header arrived repeated with values that disagree."""


def _read_header(
    headers: Mapping[str, Any], name: str, *, list_valued: bool = False
) -> Optional[str]:
    """Read one header case-insensitively, tolerating list values.

    Frameworks disagree on header container shape (WSGI dicts,
    ``http.server``'s ``Message``, ASGI lists of pairs already normalized by
    the caller), and a repeated header arrives as a list.

    A repeated header with DIFFERING values raises, and :func:`from_headers`
    turns that into no carrier at all. Picking the first would let anything that
    can prepend a value decide the event this process is attributed to, and
    picking the last would hand that to whatever appends one — no order is safe
    when the values disagree about whose trace we are writing into. The whole
    carrier goes rather than the one header, because a conflict is evidence that
    something is trying to steer attribution, and the rest of it came from the
    same request. Refusing leaves an unlinked child, a state the child already
    handles; choosing wrong writes into another tenant's trace. Identical repeats
    are not a conflict and read normally.

    Duplicates have to be ASKED for, which is the part that is easy to get wrong:
    almost every container hides them behind one value. ``HTTPMessage.get`` — what
    ``http.server`` hands a request handler — returns the first occurrence, and
    WSGI joins them into one comma-separated string, so a check that only inspects
    lists reads as though it covers this while never firing. Each multi-value
    accessor below belongs to a container a real framework hands you: ``get_all``
    to ``email.message.Message`` and werkzeug, ``getlist`` to Starlette, and
    ``get_list`` to httpx. The joined shape is caught in
    :func:`_decode_baggage` instead, since there the duplication is inside the
    value.
    """
    value = _all_values(headers, name)
    if value is None:
        value = headers.get(name)
    if value is None:
        value = headers.get(name.lower())
    if value is None:
        # Last resort for plain dicts with mixed-case keys.
        for key, candidate in headers.items():
            if isinstance(key, str) and key.lower() == name.lower():
                value = candidate
                break
    if isinstance(value, (list, tuple)):
        distinct = [text for text in dict.fromkeys(map(_as_text, value)) if text]
        if len(distinct) > 1:
            if not list_valued:
                raise _ConflictingCarrier(name)
            # A list-valued header is additive by definition, so two senders each
            # naming a different field is ordinary rather than suspicious — a
            # middleware appending its own baggage is the common case. Join and
            # let the decoder refuse only a field that disagrees with itself.
            return ",".join(distinct)
        value = distinct[0] if distinct else None
    text = _as_text(value)
    if text is not None and not list_valued and "," in text:
        # The same duplication, already joined by the container. Two trace
        # headers cannot be merged into one meaning the way baggage can.
        if len({part.strip() for part in text.split(",") if part.strip()}) > 1:
            raise _ConflictingCarrier(name)
    return text


def _as_text(value: Any) -> Optional[str]:
    if isinstance(value, bytes):
        value = value.decode("utf-8", "replace")
    return value if isinstance(value, str) else None


# One accessor per container family, in the order of how likely the container is
# to be the one holding a hand-off: `email.message.Message` (`http.server`,
# `http.client`) and werkzeug, then Starlette, then httpx.
_MULTI_VALUE_ACCESSORS = ("get_all", "getlist", "get_list", "getall")


def _all_values(headers: Mapping[str, Any], name: str) -> Optional[list]:
    """Every value sent for a header, when the container can still tell us.

    Without this the duplicate check is unreachable on the most ordinary server
    in Python: ``HTTPMessage.get`` answers with the first occurrence and says
    nothing about the second.
    """
    for accessor in _MULTI_VALUE_ACCESSORS:
        method = getattr(headers, accessor, None)
        if not callable(method):
            continue
        try:
            values = method(name)
        except Exception:
            continue
        if isinstance(values, (list, tuple)) and len(values) > 1:
            return list(values)
    return None


def _parse_langsmith_metadata(raw: str) -> Dict[str, str]:
    try:
        parsed = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return {
        key: value for key, value in parsed.items() if isinstance(value, str) and value
    }


def _split_ids(
    traceparent: str | None, langsmith_trace: str | None
) -> tuple[Optional[str], Optional[str]]:
    if traceparent:
        # `00-<trace 32 hex>-<span 16 hex>-<flags>`
        parts = traceparent.split("-")
        if len(parts) >= 3 and parts[1] and parts[2]:
            return parts[1], parts[2]
        return None, None
    if langsmith_trace:
        # LangSmith's dotted order: the trace root comes first and the current
        # run last, separated by `.`; each segment is `<timestamp>Z<uuid>`.
        segments = [segment for segment in langsmith_trace.split(".") if segment]
        if not segments:
            return None, None
        return segments[0].split("Z")[-1], segments[-1].split("Z")[-1]
    return None, None


def from_headers(headers: Mapping[str, Any] | None) -> Optional[TraceContext]:
    """Resume a parent context from an inbound request's headers.

    Understands two carriers:

    * **Native** — ``x-raindrop-handoff``, plus W3C ``traceparent`` and
      ``baggage`` of ``raindrop-*`` keys. The Raindrop header wins where they
      disagree, because it is the only one no propagator rewrites in transit.
    * **LangSmith** — ``langsmith-trace`` (dotted order) plus LangSmith's
      ``baggage`` (``langsmith-metadata`` JSON). Accepted so a service already
      propagating LangSmith headers links with no call-site change.

    Returns ``None`` when no carrier is present. That is a legitimate state —
    the child was invoked directly rather than launched — not an error, so it is
    reported as an absence rather than an exception.

    TRUST BOUNDARY: the returned context names the event this process will be
    attributed to. Only call this on requests from inside your own trust
    boundary; a carrier from an untrusted caller lets that caller write into
    another tenant's trace.
    """
    try:
        if headers is None:
            return None

        baggage = _decode_baggage(
            _read_header(headers, BAGGAGE_HEADER, list_valued=True)
        )
        langsmith_metadata = baggage.get(LANGSMITH_METADATA_BAGGAGE_KEY)
        fields: Dict[str, str] = (
            {**baggage, **_parse_langsmith_metadata(langsmith_metadata)}
            if langsmith_metadata
            else dict(baggage)
        )
        # Last, so it wins: the standard headers may have been rewritten in
        # transit by a propagator, this one is only ever written by us.
        fields.update(
            _decode_baggage(_read_header(headers, HANDOFF_HEADER, list_valued=True))
        )

        trace_id, span_id = _split_ids(
            _read_header(headers, TRACEPARENT_HEADER),
            _read_header(headers, LANGSMITH_TRACE_HEADER),
        )
        # An explicit id names the dispatch; the trace header names whichever span
        # last wrote it, which is the HTTP client's once instrumentation is on.
        # Prefer the explicit ones, keeping the trace header as the fallback for a
        # carrier from another SDK or one written before these keys existed.
        trace_id = fields.get(BAGGAGE_TRACE_ID) or trace_id
        span_id = fields.get(BAGGAGE_DISPATCH_SPAN_ID) or span_id

        event_id = fields.get(BAGGAGE_EVENT_ID)
        if not trace_id or not span_id or not event_id:
            return None

        return TraceContext(
            trace_id=trace_id,
            span_id=span_id,
            event_id=event_id,
            child_event_id=fields.get(BAGGAGE_CHILD_EVENT_ID),
            name=fields.get(BAGGAGE_NAME),
            convo_id=fields.get(BAGGAGE_CONVO_ID),
            user_id=fields.get(BAGGAGE_USER_ID),
        )
    except _ConflictingCarrier as exc:
        logger.warning(
            "[raindrop] refusing a hand-off carrier: the %s header arrived "
            "repeated with conflicting values, and the carrier names the event "
            "this process is attributed to. The child will report as unlinked.",
            exc,
        )
        return None
    except Exception as exc:
        # A malformed carrier is a link that cannot be honored, never a reason
        # to fail the request the child is serving.
        logger.debug("[raindrop] could not read a hand-off carrier: %s", exc)
        return None


# --- Attribute builders -------------------------------------------------------


def dispatch_attributes(
    *, child_event_id: str, name: str | None = None
) -> Dict[str, str]:
    """Attributes that turn a span into a detached dispatch.

    Both the mode marker and the child event id are required: dawn refuses to
    infer a hand-off from a delegation-shaped tool name, because a name-only
    guess fabricates a link to an event that may not exist.

    ``TOOL_EVENTS_ATTRIBUTE`` rides along because a dispatch-only turn has no
    assistant text; see its definition for what ingest does without it.
    """
    attributes = {
        MODE_ATTRIBUTE: DETACHED_MODE,
        CHILD_EVENT_ID_ATTRIBUTE: child_event_id,
        TOOL_EVENTS_ATTRIBUTE: TOOL_EVENTS_ALLOW,
    }
    if name:
        attributes[NAME_ATTRIBUTE] = name
    return attributes


def subagent_attributes(
    *,
    parent_event_id: str,
    parent_span_id: str | None = None,
    name: str | None = None,
) -> Dict[str, str]:
    """The reverse reference a detached child writes on every span it emits.

    Every span, not just the root: spans are ingested and projected
    independently, so a reference on the root alone is invisible to anything
    reading a child span on its own.
    """
    attributes = {
        PARENT_EVENT_ID_ATTRIBUTE: parent_event_id,
        AGENT_ROLE_ATTRIBUTE: SUBAGENT_ROLE,
    }
    if parent_span_id:
        attributes[PARENT_SPAN_ID_ATTRIBUTE] = parent_span_id
    if name:
        attributes[NAME_ATTRIBUTE] = name
    return attributes


def cancelled_attributes() -> Dict[str, str]:
    """The terminal marker a cancelled child writes on itself.

    Written under the metadata prefix as well as bare: the bare key is what
    span readers use, and the prefixed one is the only form ingest carries onto
    the child's event, which is all the caller's pill can see.
    """
    return {
        TERMINAL_ATTRIBUTE: TERMINAL_CANCELLED,
        TERMINAL_METADATA_ATTRIBUTE: TERMINAL_CANCELLED,
    }


def read_attribute(
    attributes: Mapping[str, Any] | None,
    name: str,
    prefixes: Sequence[str] = ("", "ai.telemetry.metadata.", "ai.settings.context."),
) -> Optional[str]:
    """Read one hand-off attribute, tolerating the AI-SDK metadata prefixes.

    The mirror of dawn's ``readHandoffAttribute``: the same logical field
    arrives bare or nested under a prefix depending on how the emitting process
    is instrumented, so readers must never index the attribute map directly.
    """
    if not attributes:
        return None
    for prefix in prefixes:
        value = attributes.get(f"{prefix}{name}")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None
