"""Process-global tracing state shared by all Raindrop clients.

OpenTelemetry/Traceloop is a per-process singleton: there is one tracer
provider, one exporter (with one static header set), and auto-instrumentation
is global monkey-patching. Multiple ``Raindrop`` clients therefore SHARE one
span pipeline; what varies per client is:

- which project a span routes to — carried per span as the
  ``raindrop.project_id`` attribute (OTLP batches spans from concurrent
  requests into one export, so routing cannot ride the per-request header;
  the ingest boundary routes on the attribute and falls back to the header
  project when absent);
- which write key the span was produced under — carried as a non-reversible
  ``raindrop.auth_hint`` attribute so the export guard can DROP spans that
  would otherwise be exported under a different org's credential (the server
  cannot tell org A's unknown slug from org B's leaked span; only the client
  knows which key a span was intended for).

Both are read from a ``contextvars.ContextVar`` bound by ``begin()`` /
``Raindrop.as_current()``: contextvars are isolated per thread AND per
asyncio task and propagate across ``await``, so concurrent requests bound to
different clients never stomp each other.
"""

from __future__ import annotations

import contextvars
import hashlib
import logging
import threading
import weakref
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional, Sequence

logger = logging.getLogger("raindrop.analytics")

PROJECT_ID_SPAN_ATTRIBUTE = "raindrop.project_id"
AUTH_HINT_SPAN_ATTRIBUTE = "raindrop.auth_hint"


def auth_hint_for_key(write_key: str | None) -> str | None:
    """Non-reversible identity for a write key (first 8 hex of SHA-256).

    Stamped on spans (and compared by the export guard) instead of the key
    itself so the credential can never leak through span attributes, while
    still letting us tell two keys apart.
    """
    if not write_key:
        return None
    return hashlib.sha256(write_key.encode("utf-8")).hexdigest()[:8]


class _BoundContext:
    """One live routing binding on the context stack.

    ``owner_ref`` (when set) weakly tracks the Interaction that pushed this
    binding: a binding is only honored while its owner is still reachable,
    so an ABANDONED ``begin()`` (caller raised or returned without
    ``finish()``, then dropped the Interaction) stops routing spans as soon
    as the object is collected — readers skip and prune dead entries. An
    interaction the caller still holds open is not abandoned; its binding
    stays active, which is the documented bind-at-begin semantics.
    ``as_current`` bindings have no owner (always live) — their lifetime is
    the ``with`` block via ``finally``.
    """

    __slots__ = ("project_id", "auth_hint", "owner_ref")

    def __init__(
        self,
        project_id: Optional[str],
        auth_hint: Optional[str],
        owner_ref: "weakref.ref | None" = None,
    ) -> None:
        self.project_id = project_id
        self.auth_hint = auth_hint
        self.owner_ref = owner_ref

    def is_live(self) -> bool:
        return self.owner_ref is None or self.owner_ref() is not None


# Stack of live bindings for the current execution context. A STACK (not a
# single value) because interaction lifetimes are caller-controlled and may
# interleave non-LIFO on one thread/task: finishing the FIRST of two open
# interactions must neither clobber the still-open sibling's routing (top of
# stack) nor — as plain contextvar token-reset semantics would — resurrect
# its own predecessor when the sibling finishes later. Each entry is removed
# by IDENTITY when its interaction finishes, wherever it sits in the stack.
# Immutable tuples: every mutation is a fresh ``set``, so contextvar
# copy-on-inherit semantics across tasks/threads stay intact.
_current: "contextvars.ContextVar[tuple[_BoundContext, ...]]" = (
    contextvars.ContextVar("raindrop_current_client", default=())
)

# Bound memory on pathological never-finished begin() loops on one context:
# beyond this many live bindings the oldest are dropped (they were shadowed
# anyway and could only resurface if everything above them finished).
_MAX_BINDING_STACK = 128


def bind_current(
    project_id: str | None,
    auth_hint: str | None,
    owner: "Any | None" = None,
) -> _BoundContext:
    """Push a client's routing identity onto the current context's stack.

    ``begin()`` calls this so that everything between ``begin()`` and
    ``finish()`` in the same request/task (including auto-instrumented
    library spans) routes with the interaction's client; ``finish()``
    removes the binding via :func:`unbind_current`. On frameworks that REUSE
    worker threads for sequential requests, this bind/unbind pairing keeps a
    later request that emits spans without its own ``begin()`` /
    ``as_current()`` from inheriting a stale project binding (asyncio tasks
    and anyio ``run_sync`` already isolate context per request).

    ``owner`` (the Interaction) is held weakly: an abandoned interaction —
    never finished AND no longer referenced — stops routing as soon as it is
    collected, closing the leak where an exception between ``begin()`` and
    ``finish()`` would otherwise leave the binding active on a reused
    thread indefinitely.
    """
    bound = _BoundContext(
        project_id,
        auth_hint,
        weakref.ref(owner) if owner is not None else None,
    )
    stack = _current.get()
    if len(stack) >= _MAX_BINDING_STACK:
        stack = stack[-(_MAX_BINDING_STACK - 1) :]
    _current.set(stack + (bound,))
    return bound


def unbind_current(bound: "_BoundContext | None") -> None:
    """Remove a binding pushed by ``bind_current`` (by identity, any position).

    Non-LIFO safe: finishing the first of two interleaved interactions
    removes only ITS entry, leaving the still-open sibling on top. A
    ``finish()`` on a different thread/task than its ``begin()`` is a no-op
    (the entry isn't in that context's stack; the origin context's entry
    dies with the context or is dropped by the stack cap). Never raises into
    caller code.
    """
    if bound is None:
        return
    try:
        stack = _current.get()
        pruned = tuple(b for b in stack if b is not bound)
        if len(pruned) != len(stack):
            _current.set(pruned)
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("[raindrop] unbind_current ignored error: %s", exc)


@contextmanager
def as_current(project_id: str | None, auth_hint: str | None) -> Iterator[None]:
    """Scope spans in the ``with`` block to a client (see Raindrop.as_current)."""
    bound = bind_current(project_id, auth_hint)
    try:
        yield
    finally:
        unbind_current(bound)


def current_context() -> _BoundContext | None:
    """Topmost LIVE binding; prunes bindings whose owner was collected."""
    stack = _current.get()
    if not stack:
        return None
    top = stack[-1]
    if top.is_live():
        return top
    pruned = tuple(b for b in stack if b.is_live())
    _current.set(pruned)
    return pruned[-1] if pruned else None


# --- Contextual span attributes ------------------------------------------------
#
# Raw attributes stamped on EVERY span started in the current execution
# context, on top of the routing attributes above. Used by the detached
# sub-agent hand-off (``raindrop.subagent``), whose contract requires the
# child's reverse reference on every span it emits — spans are ingested and
# projected independently, so a reference on the root alone would be invisible
# to anything reading a child span on its own.
#
# A STACK of frames removed by IDENTITY, for the same reason the routing
# bindings are (see ``unbind_current``): a run's lifetime is caller-controlled
# and two runs on one context may end out of order, and plain contextvar token
# reset would then resurrect a finished run's attributes.


class _AttributeFrame:
    """One set of contextual span attributes on the stack.

    Holds its owner WEAKLY, like ``_BoundContext``: a caller who abandons an
    interaction or a sub-agent run without finishing it should not leave the
    thing it described stamped on the next turn to reuse this context. Readers
    skip and prune frames whose owner is gone. A frame with no owner is always
    live — its lifetime is a ``with`` block's ``finally``.
    """

    __slots__ = ("attributes", "saw_error_span", "owner_ref")

    def __init__(
        self,
        attributes: Dict[str, str],
        owner_ref: "weakref.ref | None" = None,
    ) -> None:
        self.attributes = attributes
        # Whether a span ended in error while this frame was bound. A detached
        # sub-agent run uses it to tell "the failure is already on a span" from
        # "nothing recorded it", so it records one only in the second case.
        self.saw_error_span = False
        self.owner_ref = owner_ref

    def is_live(self) -> bool:
        return self.owner_ref is None or self.owner_ref() is not None


_span_attribute_frames: "contextvars.ContextVar[tuple[_AttributeFrame, ...]]" = (
    contextvars.ContextVar("raindrop_span_attributes", default=())
)

# Same bound, same reasoning as _MAX_BINDING_STACK: a pathological loop that
# binds without unbinding must not grow unboundedly.
_MAX_ATTRIBUTE_FRAMES = 128


def bind_span_attributes(
    attributes: Dict[str, str], owner: Any = None
) -> "_AttributeFrame | None":
    """Stamp ``attributes`` on every span started later in this context.

    Returns the frame to hand to :func:`unbind_span_attributes`, or ``None``
    when there is nothing to bind. Unbind it when whatever it describes ends: a
    sync worker thread keeps its context between requests, so a frame left
    bound stamps the next unrelated turn on that thread. Pass the ``owner`` it
    describes and an abandoned one stops applying when that object is collected,
    even if the unbind never comes.
    """
    if not attributes:
        return None
    owner_ref = None
    if owner is not None:
        try:
            owner_ref = weakref.ref(owner)
        except TypeError:
            # Not weak-referenceable: the frame is simply always live, exactly
            # as it was before owners existed.
            owner_ref = None
    frame = _AttributeFrame(dict(attributes), owner_ref)
    try:
        frames = _span_attribute_frames.get()
        if len(frames) >= _MAX_ATTRIBUTE_FRAMES:
            frames = frames[-(_MAX_ATTRIBUTE_FRAMES - 1) :]
        _span_attribute_frames.set(frames + (frame,))
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("[raindrop] bind_span_attributes ignored error: %s", exc)
        return None
    return frame


def frame_applies_to(span: Any, frame: "_AttributeFrame | None") -> bool:
    """Whether ``span`` was started under ``frame``.

    Every span a frame is bound over carries all of its attributes, and nothing
    that predates the frame — or belongs to a sibling one — does. That is what
    lets a sub-agent run tell its own spans from the host's.
    """
    if frame is None or not frame.attributes:
        return False
    attributes = getattr(span, "attributes", None) or {}
    return all(attributes.get(key) == value for key, value in frame.attributes.items())


def own_span_attributes(frame: "_AttributeFrame | None", owner: Any) -> None:
    """Give a frame its owner after the fact.

    For the caller that has to bind before the object the frame describes
    exists — the sub-agent run's reverse reference has to be in place before the
    interaction that the run wraps is begun.
    """
    if frame is None or owner is None:
        return
    try:
        frame.owner_ref = weakref.ref(owner)
    except TypeError:
        # Not weak-referenceable: always live, as it was before owners existed.
        pass


def unbind_span_attributes(frame: "_AttributeFrame | None") -> None:
    """Remove a frame pushed by :func:`bind_span_attributes` (by identity)."""
    if frame is None:
        return
    try:
        frames = _span_attribute_frames.get()
        pruned = tuple(f for f in frames if f is not frame)
        if len(pruned) != len(frames):
            _span_attribute_frames.set(pruned)
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("[raindrop] unbind_span_attributes ignored error: %s", exc)


@contextmanager
def span_attributes(attributes: Dict[str, str]) -> Iterator[None]:
    """Stamp ``attributes`` on spans started inside the ``with`` block."""
    frame = bind_span_attributes(attributes)
    try:
        yield
    finally:
        unbind_span_attributes(frame)


def live_span_attribute_frames() -> tuple:
    """The bound frames whose owner is still around; prunes the rest."""
    try:
        frames = _span_attribute_frames.get()
    except Exception:  # pragma: no cover - defensive
        return ()
    if all(frame.is_live() for frame in frames):
        return frames
    live = tuple(frame for frame in frames if frame.is_live())
    try:
        _span_attribute_frames.set(live)
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("[raindrop] could not prune abandoned frames: %s", exc)
    return live


def current_span_attributes() -> Dict[str, str]:
    """Merged contextual span attributes, innermost frame winning."""
    merged: Dict[str, str] = {}
    for frame in live_span_attribute_frames():
        merged.update(frame.attributes)
    return merged


# --- Span stamping -----------------------------------------------------------

try:  # SpanProcessor import kept lazy-safe: tracing is optional at runtime.
    from opentelemetry.sdk.trace import SpanProcessor
    from opentelemetry.trace import StatusCode
except Exception:  # pragma: no cover - opentelemetry-sdk is a hard dep today
    SpanProcessor = object  # type: ignore[assignment,misc]
    StatusCode = None  # type: ignore[assignment]


# Flipped (never unflipped) the first time clients with TWO DIFFERENT
# api_keys have existed in the process — regardless of construction order or
# whether the second client enables tracing (global auto-instrumentation
# traces a non-tracing client's code paths all the same). While False —
# every process in existence today — same-key spans are stamped only with
# their project and stay byte-identical on the wire. Once True, provenance
# matters: owner-bound spans also stamp the owner's auth hint so the export
# guard can switch to POSITIVE attribution (export only spans provably bound
# to the owner's context; drop unattributed ones, whose origin is unknowable).
_foreign_client_seen = False
_seen_client_hints: "set[str]" = set()
_seen_hints_lock = threading.Lock()


def register_client_key(auth_hint: str | None) -> None:
    """Record a client credential; flip to positive attribution on the 2nd key.

    Called from EVERY client configuration (module init() and Raindrop
    instances, tracing or not). Keyless clients (local-Workshop-only) are
    excluded: they carry no credential to misattribute to.
    """
    global _foreign_client_seen
    if not auth_hint:
        return
    with _seen_hints_lock:
        _seen_client_hints.add(auth_hint)
        if len(_seen_client_hints) > 1 and not _foreign_client_seen:
            _foreign_client_seen = True
            logger.warning(
                "[raindrop] Multiple API keys detected in one process. The "
                "OTel export guard now requires positive attribution: spans "
                "not bound to any client (no begin()/as_current()) are "
                "dropped, and spans bound to a non-owner key are dropped. "
                "Manual events are unaffected."
            )


def mark_foreign_client() -> None:
    global _foreign_client_seen
    _foreign_client_seen = True


def foreign_client_seen() -> bool:
    return _foreign_client_seen


def stamp_span(span: Any, project_id: str | None, auth_hint: str | None) -> None:
    """Stamp a span with its owning client's routing attributes.

    ``raindrop.project_id`` routes the span at ingest. ``raindrop.auth_hint``
    exists solely for the export guard: foreign spans (owning key differs
    from the pipeline owner's) always carry it so they can be dropped; owner
    spans carry it only once a foreign-key client exists in the process, so
    the guard can require positive attribution without changing single-key
    processes' spans by a byte. Used by both the context span processor and
    the explicit-stamp paths (``start_span`` / ``track_tool``), which may run
    outside any bound context.
    """
    try:
        if project_id:
            span.set_attribute(PROJECT_ID_SPAN_ATTRIBUTE, project_id)
        if auth_hint and (
            _foreign_client_seen or auth_hint != pipeline_owner_hint()
        ):
            span.set_attribute(AUTH_HINT_SPAN_ATTRIBUTE, auth_hint)
    except Exception:
        # Telemetry must never crash the host app.
        pass


def stamp_context_attributes(span: Any) -> None:
    """Apply the current context's contextual span attributes to ``span``."""
    try:
        for key, value in current_span_attributes().items():
            span.set_attribute(key, value)
    except Exception:
        # Telemetry must never crash the host app.
        pass


class _RaindropContextSpanProcessor(SpanProcessor):
    """Stamp every span started under a bound context with routing attributes.

    Spans started outside any bound context get no routing attributes and route
    to the exporter's default (header) project — exactly today's behavior.
    Contextual attributes (the hand-off reverse reference) are independent of
    the routing binding, so they are applied either way.
    """

    def on_start(self, span: Any, parent_context: Any = None) -> None:
        try:
            stamp_context_attributes(span)
            bound = current_context()
            if bound is None:
                return
            stamp_span(span, bound.project_id, bound.auth_hint)
        except Exception:
            # Telemetry must never crash the host app.
            pass

    def on_end(self, span: Any) -> None:
        try:
            status = getattr(span, "status", None)
            if status is None or status.status_code is not StatusCode.ERROR:
                return
            # Only the frames this span was started under: an error span that
            # predates a run, or belongs to a sibling run on the same context,
            # is not that run's failure, and treating it as one would let the
            # run skip recording its own — leaving it derived as finished.
            for frame in live_span_attribute_frames():
                if frame_applies_to(span, frame):
                    frame.saw_error_span = True
        except Exception:
            # Telemetry must never crash the host app.
            pass

    def shutdown(self) -> None:  # pragma: no cover - no-op
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:  # pragma: no cover
        return True


# --- Export guard ------------------------------------------------------------


class _GuardedSpanExporter:
    """Drop spans produced under a different write key than the exporter's.

    One process has one OTLP exporter authenticating with ONE key. A span
    produced in the context of a client constructed with a different key
    (i.e. a different org) must not ride this exporter: the server would
    attribute it to the exporter's org and either admit it under a
    same-named/unclaimed project or fall back to the header project — a
    silent cross-org leak. Dropping client-side with a loud (rate-limited)
    warning is strictly better than silent mis-delivery; correct routing
    for a second org requires its own process.
    """

    _WARN_INTERVAL_SECONDS = 30.0

    def __init__(self, inner: Any, owner_auth_hint: str | None) -> None:
        self._inner = inner
        self._owner_auth_hint = owner_auth_hint
        self._last_warned = 0.0
        self._dropped_total = 0
        self._lock = threading.Lock()

    def _partition(self, spans: Sequence[Any]) -> "tuple[list[Any], int]":
        allowed = []
        dropped = 0
        # Single-key process (the norm): anything without a FOREIGN hint
        # exports — unstamped spans can only belong to the owner. Once a
        # foreign-key client has existed, provenance of unstamped spans is
        # unknowable (they may come from the foreign client's un-bound
        # code paths), so the guard requires POSITIVE attribution: only
        # spans stamped with the owner's own hint export.
        require_positive = foreign_client_seen()
        for span in spans:
            attrs = getattr(span, "attributes", None) or {}
            hint = attrs.get(AUTH_HINT_SPAN_ATTRIBUTE)
            if require_positive:
                keep = hint == self._owner_auth_hint
            else:
                keep = hint is None or hint == self._owner_auth_hint
            if keep:
                allowed.append(span)
            else:
                dropped += 1
        return allowed, dropped

    def _warn_dropped(self, dropped: int) -> None:
        import time

        with self._lock:
            self._dropped_total += dropped
            now = time.monotonic()
            if now - self._last_warned < self._WARN_INTERVAL_SECONDS:
                return
            self._last_warned = now
            total = self._dropped_total
        logger.warning(
            "[raindrop] Dropped %d span(s) produced under a different API key "
            "than the tracing pipeline's (total dropped: %d). One process has "
            "ONE OTel pipeline authenticating with the first tracing-enabled "
            "client's key; tracing for a different key/org in the same "
            "process is unsupported — run it in its own process. Manual "
            "events (track_ai/begin/finish/signals/identify) are unaffected.",
            dropped,
            total,
        )

    def export(self, spans: Sequence[Any]) -> Any:
        try:
            allowed, dropped = self._partition(spans)
        except Exception:
            if foreign_client_seen():
                # Fail CLOSED where it matters: with a foreign-key client in
                # the process, an unfiltered export could deliver spans under
                # the wrong org's credential — drop the batch instead.
                self._warn_dropped(len(spans))
                from opentelemetry.sdk.trace.export import SpanExportResult

                return SpanExportResult.FAILURE
            # Single-key process: there is nothing to guard against by
            # construction (no foreign spans can exist), so a guard bug must
            # not cost the owner their telemetry.
            return self._inner.export(spans)
        if dropped:
            self._warn_dropped(dropped)
        if not allowed:
            from opentelemetry.sdk.trace.export import SpanExportResult

            return SpanExportResult.SUCCESS
        return self._inner.export(allowed)

    def shutdown(self) -> None:
        return self._inner.shutdown()

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        force = getattr(self._inner, "force_flush", None)
        return force(timeout_millis) if force is not None else True


# --- Pipeline ownership -------------------------------------------------------

# Set when a Raindrop client (or the module-level init()) successfully runs
# Traceloop.init. The owner's key authenticates ALL span exports; its project
# is the header fallback for unstamped spans.
_owner_lock = threading.Lock()
_owner_auth_hint: str | None = None
_owner_project_id: str | None = None

# Serializes the whole claim -> Traceloop.init -> (release on failure)
# sequence. Without it, a client constructed concurrently with the claimer
# could observe "already claimed", skip init, and end up tracing-enabled
# against a pipeline whose init subsequently failed and was released. Held
# only during tracing initialization (startup), never on hot paths.
pipeline_init_lock = threading.Lock()


def pipeline_owner_hint() -> str | None:
    return _owner_auth_hint


def claim_pipeline(auth_hint: str | None, project_id: str | None) -> bool:
    """Record the first tracing initializer. Returns False if already owned."""
    global _owner_auth_hint, _owner_project_id
    with _owner_lock:
        if _owner_auth_hint is not None or _owner_project_id is not None:
            return False
        _owner_auth_hint = auth_hint
        _owner_project_id = project_id
        return True


def release_pipeline_claim() -> None:
    """Forget pipeline ownership.

    Called when the claimer's Traceloop.init subsequently FAILS, so the
    process isn't left believing a pipeline exists — the next tracing-enabled
    client gets a clean attempt instead of silently 'sharing' nothing.
    """
    global _owner_auth_hint, _owner_project_id
    with _owner_lock:
        _owner_auth_hint = None
        _owner_project_id = None


def _reset_pipeline_owner_for_tests() -> None:
    """Testing hook: forget pipeline ownership so each test can re-claim it."""
    global _foreign_client_seen
    release_pipeline_claim()
    _foreign_client_seen = False
    with _seen_hints_lock:
        _seen_client_hints.clear()


def build_guarded_exporter(
    api_endpoint: str, headers: Dict[str, str], owner_auth_hint: str | None
) -> _GuardedSpanExporter:
    """Build the OTLP exporter Traceloop would have built, wrapped in the guard.

    Uses Traceloop's own ``init_spans_exporter`` so endpoint scheme handling
    (http/https/grpc) and the ``/v1/traces`` path join stay byte-identical
    with the default pipeline; only the guard wrapper is new.
    """
    from traceloop.sdk.tracing.tracing import init_spans_exporter

    inner = init_spans_exporter(api_endpoint, headers)
    return _GuardedSpanExporter(inner, owner_auth_hint)
