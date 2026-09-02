"""Slim client-side flow tracing for CLI MCP handling (port of backend flow_trace).

Mirrors the API and semantics of ``backend/app/core/observability/flow_trace.py``
(``flow()`` / ``step()`` / ``operation()`` / ``mark_error()``), stripped down for
the client: no Sentry, no OTel SDK, no collection policy, no background emitter.
A completed flow is rendered to a plain-dict summary and handed to an injected
sink (``enable_flow_tracing``). Delivery to the backend rides existing HTTP
calls (see ``flow_delivery`` for the ``runlayer run`` lag-one queue and
``flow_spool`` for the one-shot ``aiwatch hook`` spool file); the backend
re-records summaries as ``runlayer.flow.*`` OTel metrics after validating them
against the closed vocabularies in ``flow_contract`` and applying the collection
allowlist server-side, so this module stays dumb about legal gating.

Constraints (cli/AGENTS.md): the import closure stays stdlib-only — the module is
in the ``aiwatch`` PyInstaller closure, which excludes ``fastmcp``/``mcp`` and
keeps ``anyio`` off the hook hot path; the ``hook_io`` sibling qualifies because
its own closure is stdlib-only. structlog
is also avoided because its unconfigured default sink is stdout, the hook's
strict protocol channel. Two regimes only: true no-op (no sink configured, or the
``RUNLAYER_FLOW_TRACE=0`` kill switch) and full recording — client volume is
human-interactive, so the backend's sampled-out middle regime buys nothing.

Design rules (same as backend):
- Best-effort: instrumentation never raises into MCP traffic or hook stdout.
  A step recorded with no active flow is a silent no-op; sink failures are
  swallowed.
- Re-entrant: only the outermost ``flow()`` owns start/emit; nested ``flow()``
  calls attach their steps to the active flow.
- No payloads/PII: summaries carry only bounded enums (operation, step name,
  kind, status, exception class name), an optional bounded session identifier,
  and relative timings. Tool names, server names, and arguments never enter a
  summary.
"""

from __future__ import annotations

import asyncio
import contextlib
import contextvars
import functools
import inspect
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any, Literal, TypeVar, cast

from runlayer_cli.flow_summary import build_summary
from runlayer_cli.hook import hook_io

StepKind = Literal["local", "cpu", "remote", "db", "redis", "http", "cache"]

# Kinds that represent "blocked waiting for something else" (external I/O).
_BLOCKING_KINDS: frozenset[str] = frozenset({"remote", "db", "redis", "http", "cache"})

_MAX_IDENTIFIER_LEN = 128

FlowSink = Callable[[dict[str, Any]], None]

# Maps a caught exception to a sanitized ``(error_category, http_status)``
# pair from ``flow_contract.CLIENT_FLOW_ERROR_CATEGORIES``. Injected (see
# ``set_error_classifier``) because classification needs httpx/mcp types,
# which must stay out of this module's stdlib-only import closure
# (cli/AGENTS.md); the classifier lives in ``error_classification.py``.
ErrorClassifier = Callable[[BaseException], "tuple[str | None, int | None]"]

_KILL_SWITCH_ENV = "RUNLAYER_FLOW_TRACE"

# Process-global sink. Hook daemon requests install the same spool sink
# concurrently; request-local kill-switch state is checked when each flow starts.
_sink: FlowSink | None = None

# Process-global exception classifier (see ``ErrorClassifier``).
_error_classifier: ErrorClassifier | None = None

# Process-global server id stamped onto every flow summary. ``runlayer run``
# serves exactly one server per process, so a module global (set once after
# the id resolves, before any flow starts) is sufficient; hook entrypoints
# never set it and their summaries simply omit the field.
_server_id: str | None = None


def _kill_switch_active() -> bool:
    value = hook_io.getenv(_KILL_SWITCH_ENV, "") or ""
    return value.strip().lower() in {"0", "false", "off"}


def enable_flow_tracing(sink: FlowSink) -> None:
    """Install the flow sink.

    Each entrypoint wires its own sink (``runlayer run`` → delivery queue +
    log line; ``aiwatch hook`` → spool file). Without a sink, ``flow()`` is a
    true no-op. The kill switch is checked per flow so daemon requests cannot
    change each other's tracing state.
    """
    global _sink
    _sink = sink


def disable_flow_tracing() -> None:
    global _sink
    _sink = None


def set_error_classifier(classifier: ErrorClassifier | None) -> None:
    """Install (or clear) the sanitized exception classifier.

    Wired by the ``runlayer run`` entrypoint alongside the sink. Classifier
    failures are swallowed at the call site — classification is best-effort
    metadata and must never raise into MCP traffic.
    """
    global _error_classifier
    _error_classifier = classifier


def set_server_id(server_id: str | None) -> None:
    """Set the server UUID stamped onto every subsequent flow summary.

    Canonicalized to hyphenated-lowercase UUID form: ``runlayer run`` accepts
    any ``uuid.UUID``-parseable target (32-hex, braces, URN, uppercase) and
    passes it through verbatim, but backend ingest only keeps canonical UUIDs
    — a raw non-canonical form would silently lose the field. Non-UUID values
    are kept as-is (bounded); ingest nulls them.
    """
    global _server_id
    value = _coerce_identifier(server_id)
    if value is not None:
        try:
            value = str(uuid.UUID(value))
        except ValueError:
            pass
    _server_id = value


def _classify_exception(exc: BaseException) -> tuple[str | None, int | None]:
    """Run the installed classifier defensively; ``(None, None)`` on any miss."""
    classifier = _error_classifier
    if classifier is None:
        return (None, None)
    try:
        category, http_status = classifier(exc)
    except Exception:
        return (None, None)
    if category is not None and not isinstance(category, str):
        category = None
    if http_status is not None and (
        isinstance(http_status, bool) or not isinstance(http_status, int)
    ):
        http_status = None
    return (category, http_status)


def is_enabled() -> bool:
    return _sink is not None and not _kill_switch_active()


def _is_blocking(kind: StepKind, blocking: bool | None) -> bool:
    if blocking is not None:
        return blocking
    return kind in _BLOCKING_KINDS


def _coerce_identifier(value: str | None) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value:
        return None
    return value[:_MAX_IDENTIFIER_LEN]


@dataclass(frozen=True, slots=True)
class StepRecord:
    """One completed arrow-step in a flow."""

    id: int
    parent_id: int | None
    name: str
    kind: StepKind
    blocking: bool
    start_offset_ms: float
    duration_ms: float
    status: Literal["ok", "error"]
    error_type: str | None
    # Serialized request-body size for HTTP steps (ENG-5125). A byte count
    # only — payload content never enters a summary (module docstring rule).
    payload_bytes: int | None = None


@dataclass(slots=True)
class FlowTrace:
    """Accumulates steps for one top-level operation.

    Mutable and shared by reference across async child tasks (contextvars copy
    the reference, not the value), so concurrent steps interleave into one
    trace. Appends and the id counter are lock-guarded for thread concurrency.
    """

    operation: str
    started_perf: float
    session_id: str | None = None
    # Client-reported pre-flow startup overhead (process exec + stdin read +
    # IPC handoff before the flow timer), set via ``set_startup_ms()``.
    startup_ms: float | None = None
    # Set via ``mark_error()`` when a handler returns an in-band error result
    # instead of raising, so the flow still records status="error".
    errored: bool = False
    error_type: str | None = None
    # Sanitized failure classification (flow_contract.CLIENT_FLOW_ERROR_CATEGORIES)
    # plus the optional integer HTTP status behind it. Category + status only —
    # never free-text exception messages (module docstring rule).
    error_category: str | None = None
    error_http_status: int | None = None
    # Server UUID this process is running (``runlayer run`` path; None for hooks).
    server_id: str | None = None
    steps: list[StepRecord] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _next_id: int = 0

    def claim_id(self) -> int:
        with self._lock:
            step_id = self._next_id
            self._next_id += 1
            return step_id

    def add(self, record: StepRecord) -> None:
        with self._lock:
            self.steps.append(record)

    def snapshot_steps(self) -> list[StepRecord]:
        """Copy the steps under the lock (a leaked child task may still append)."""
        with self._lock:
            return list(self.steps)

    def now_offset_ms(self) -> float:
        return (time.perf_counter() - self.started_perf) * 1000.0


_flow_var: contextvars.ContextVar[FlowTrace | None] = contextvars.ContextVar(
    "rl_cli_flow_trace", default=None
)
_parent_step_var: contextvars.ContextVar[int | None] = contextvars.ContextVar(
    "rl_cli_flow_parent_step", default=None
)


def current_flow() -> FlowTrace | None:
    """Return the active flow, or ``None`` if no top-level operation is in scope."""
    return _flow_var.get()


def mark_error(
    error_type: str | None = None,
    *,
    override: bool = False,
    category: str | None = None,
    http_status: int | None = None,
) -> None:
    """Mark the active flow as errored without an exception propagating.

    For handlers that catch a failure and return an in-band error result (e.g.
    the middleware returning a synthetic "server not running" ToolResult). Safe
    no-op when there is no active flow. The first value provided wins for each
    field, except ``error_type`` when ``override`` is set — for terminal
    outcomes (e.g. a fail-closed deny that exits the process) that must
    supersede an earlier provisional classification (e.g. Protect's fail-open
    mark). ``category`` is a sanitized ``CLIENT_FLOW_ERROR_CATEGORIES`` value
    computed by the caller (classification lives outside this closure);
    ``http_status`` is the optional integer status behind an HTTP category.
    """
    trace = _flow_var.get()
    if trace is None:
        return
    trace.errored = True
    if error_type is not None and (override or trace.error_type is None):
        trace.error_type = error_type
    if category is not None and trace.error_category is None:
        trace.error_category = category
    if http_status is not None and trace.error_http_status is None:
        trace.error_http_status = http_status


def set_session_id(session_id: str | None) -> None:
    """Attach a session identifier to the active flow summary."""
    trace = _flow_var.get()
    if trace is None:
        return
    trace.session_id = _coerce_identifier(session_id)


def set_startup_ms(startup_ms: float) -> None:
    """Attach pre-flow client startup overhead to the active flow summary.

    Safe no-op without an active flow. Callers clamp before calling; negative
    values are dropped here as a final guard so a bad clamp cannot ship a
    nonsensical summary.
    """
    trace = _flow_var.get()
    if trace is None or startup_ms < 0:
        return
    trace.startup_ms = startup_ms


def reset_flow() -> None:
    """Belt-and-suspenders clear of flow context.

    Normal teardown happens via the ``flow()`` context manager; this guards
    against a leaked flow if a caller bypasses the context manager.
    """
    _flow_var.set(None)
    _parent_step_var.set(None)


@contextlib.contextmanager
def flow(operation: str, *, session_id: str | None = None) -> Iterator[FlowTrace]:
    """Scope a top-level operation. Re-entrant; only the outermost call emits.

    ``operation`` is a stable, low-cardinality flow name from
    ``CLIENT_FLOW_OPERATIONS``. True no-op when no sink is configured: the flow
    contextvar is not set, so ``step()`` / ``mark_error()`` short-circuit with
    zero allocation; a non-recording trace is still yielded so callers using
    ``with flow(...) as trace`` keep working.
    """
    existing = _flow_var.get()
    if existing is not None:
        # Nested flow: reuse the outer operation; do not start/emit again.
        yield existing
        return

    if not is_enabled():
        yield FlowTrace(
            operation=operation,
            started_perf=time.perf_counter(),
            session_id=_coerce_identifier(session_id),
            server_id=_server_id,
        )
        return

    trace = FlowTrace(
        operation=operation,
        started_perf=time.perf_counter(),
        session_id=_coerce_identifier(session_id),
        server_id=_server_id,
    )
    flow_token = _flow_var.set(trace)
    parent_token = _parent_step_var.set(None)
    status: Literal["ok", "error"] = "ok"
    error_type: str | None = None
    error_category: str | None = None
    error_http_status: int | None = None
    try:
        yield trace
    except Exception as exc:
        status = "error"
        error_type = type(exc).__name__
        error_category, error_http_status = _classify_exception(exc)
        raise
    except asyncio.CancelledError as exc:
        # Cancellation is BaseException, so the branch above never sees it —
        # without this the `cancelled` category could never be emitted.
        # Record and RE-RAISE IMMEDIATELY: cancellation must never be
        # swallowed. Other BaseExceptions (SystemExit, KeyboardInterrupt)
        # deliberately stay unhandled — an operator ^C is not a flow error.
        status = "error"
        error_type = type(exc).__name__
        error_category, error_http_status = _classify_exception(exc)
        raise
    finally:
        _flow_var.reset(flow_token)
        _parent_step_var.reset(parent_token)
        if status == "ok" and trace.errored:
            # A caught-but-marked error (in-band error result) still counts.
            status = "error"
        if trace.error_type is None and error_type is not None:
            trace.error_type = error_type
        if trace.error_category is None and error_category is not None:
            trace.error_category = error_category
        if trace.error_http_status is None and error_http_status is not None:
            trace.error_http_status = error_http_status
        _emit_flow(trace, status=status)


_F = TypeVar("_F", bound=Callable[..., Any])


def operation(name: str) -> Callable[[_F], _F]:
    """Decorate a function so its whole body runs inside ``flow(name)``.

    Works on sync and async callables. Re-entrant via ``flow()``: calling a
    decorated callable from inside an active flow reuses the outer operation.
    """

    def decorator(fn: _F) -> _F:
        if inspect.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                with flow(name):
                    return await fn(*args, **kwargs)

            return cast(_F, async_wrapper)

        @functools.wraps(fn)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with flow(name):
                return fn(*args, **kwargs)

        return cast(_F, sync_wrapper)

    return decorator


class _Step:
    """Context manager for one arrow-step; usable with ``with`` and ``async with``."""

    __slots__ = (
        "_name",
        "_kind",
        "_blocking",
        "_trace",
        "_start_offset_ms",
        "_start_perf",
        "_id",
        "_parent_id",
        "_parent_token",
        "_payload_bytes",
    )

    def __init__(
        self,
        name: str,
        kind: StepKind,
        blocking: bool | None,
        payload_bytes: int | None = None,
    ) -> None:
        self._name = name
        self._kind = kind
        self._blocking = _is_blocking(kind, blocking)
        self._trace: FlowTrace | None = None
        self._start_offset_ms = 0.0
        self._start_perf = 0.0
        self._id: int | None = None
        self._parent_id: int | None = None
        self._parent_token: contextvars.Token[int | None] | None = None
        self._payload_bytes = payload_bytes

    def _enter(self) -> None:
        trace = _flow_var.get()
        if trace is None:
            return
        self._trace = trace
        self._start_offset_ms = trace.now_offset_ms()
        self._start_perf = time.perf_counter()
        self._parent_id = _parent_step_var.get()
        self._id = trace.claim_id()
        self._parent_token = _parent_step_var.set(self._id)

    def _exit(self, exc_type: type[BaseException] | None) -> None:
        trace = self._trace
        if trace is None or self._id is None:
            return
        duration_ms = (time.perf_counter() - self._start_perf) * 1000.0
        status: Literal["ok", "error"] = "ok" if exc_type is None else "error"
        error_type = exc_type.__name__ if exc_type is not None else None
        if self._parent_token is not None:
            _parent_step_var.reset(self._parent_token)
        trace.add(
            StepRecord(
                id=self._id,
                parent_id=self._parent_id,
                name=self._name,
                kind=self._kind,
                blocking=self._blocking,
                start_offset_ms=self._start_offset_ms,
                duration_ms=duration_ms,
                status=status,
                error_type=error_type,
                payload_bytes=self._payload_bytes,
            )
        )

    def __enter__(self) -> _Step:
        self._enter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self._exit(exc_type)
        return False

    async def __aenter__(self) -> _Step:
        self._enter()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        self._exit(exc_type)
        return False


class _NullStep:
    """Shared zero-allocation no-op step for when there is no active flow."""

    __slots__ = ()

    def __enter__(self) -> _NullStep:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        return False

    async def __aenter__(self) -> _NullStep:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        return False


_NULL_STEP = _NullStep()


def step(
    name: str,
    *,
    kind: StepKind = "local",
    blocking: bool | None = None,
    payload_bytes: int | None = None,
) -> _Step | _NullStep:
    """Record one arrow-step. Use as ``with`` (sync) or ``async with`` (async).

    ``blocking`` defaults from ``kind`` (``remote``/``db``/``redis``/``http``/
    ``cache`` block, ``local``/``cpu`` do not). ``payload_bytes`` is the
    serialized request-body size for HTTP steps (a count, never content).
    Returns a shared no-op when there is no active flow so the hot path
    allocates nothing.
    """
    if _flow_var.get() is None:
        return _NULL_STEP
    return _Step(name, kind, blocking, payload_bytes)


def marker(name: str, *, kind: StepKind = "local") -> None:
    """Record a zero-duration cohort marker in the active flow."""
    trace = _flow_var.get()
    if trace is None:
        return
    trace.add(
        StepRecord(
            id=trace.claim_id(),
            parent_id=_parent_step_var.get(),
            name=name,
            kind=kind,
            blocking=False,
            start_offset_ms=trace.now_offset_ms(),
            duration_ms=0.0,
            status="ok",
            error_type=None,
        )
    )


def _emit_flow(trace: FlowTrace, *, status: Literal["ok", "error"]) -> None:
    """Render the completed flow to a summary dict and hand it to the sink.

    ``wall_ms`` is captured before any rendering so summary-build cost never
    inflates the measured duration. Never raises: a broken sink cannot reach
    MCP traffic or hook stdout.
    """
    sink = _sink
    if sink is None:
        return
    wall_ms = trace.now_offset_ms()
    try:
        steps = trace.snapshot_steps()
        sink(build_summary(trace, status=status, steps=steps, wall_ms=wall_ms))
    except Exception:
        pass
