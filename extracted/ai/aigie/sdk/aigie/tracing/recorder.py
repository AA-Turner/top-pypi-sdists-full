"""Framework-agnostic span lifecycle tracker.

The recorder is the bridge between a framework's native callback/hook
events and the typed events the platform consumes. Adapters call
`start_span(run_id, kind, ...)` when something begins and
`complete_span(run_id, ...)` / `error_span(run_id, ...)` when it ends.
The recorder maintains the in-flight state (start time, input, parent,
metadata) and produces typed `SpanCreate` / `SpanComplete` events at the
right moments.

Unlike the LangChain `BaseCallbackHandler` this is **framework-agnostic**:
- The API is one pair of methods per phase (start / complete / error),
  parameterized by `SpanType` (NODE, LLM, TOOL, RETRIEVER, etc.), not
  separate methods per kind.
- It does not import anything framework-specific. Adapters translate
  their native events into recorder calls.
- It does not write to any sink. The adapter takes the returned typed
  event and hands it to a `TraceEmitter`.

LLM-specific accessories (streaming tokens, usage, cost) are exposed as
helpers that work on any active run, so a recorder can carry them when
the framework reports them. Callers are free to ignore them.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from aigie.tracing.types import (
    SpanComplete,
    SpanCreate,
    SpanStatus,
    SpanType,
    TraceCreate,
    TraceUpdate,
)
from aigie.uuid7 import uuidv7


class _ActiveRun:
    """Internal in-flight bookkeeping for a single span or trace."""

    __slots__ = (
        "first_token_time",
        "input",
        "kind",
        "metadata",
        "name",
        "parent_id",
        "span_id",
        "start_time",
        "trace_id",
    )

    def __init__(
        self,
        *,
        span_id: str,
        trace_id: str,
        parent_id: str | None,
        kind: SpanType,
        name: str,
        input: Any,
        metadata: dict[str, Any],
    ) -> None:
        self.span_id = span_id
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.kind = kind
        self.name = name
        self.input = input
        self.metadata = metadata
        self.start_time = datetime.now(timezone.utc)
        self.first_token_time: datetime | None = None


class SpanRecorder:
    """In-flight span and trace tracker.

    State is keyed by the caller's `run_id` — typically the framework's
    own run identifier (LangChain run_id, OpenAI Agents step id, etc.).
    The recorder generates its own span_ids; callers do not need to.

    Thread-safety: not thread-safe by itself. Each adapter installs one
    recorder per `app.invoke()` invocation (the natural unit of
    concurrency), so contention is not expected. If multiple threads
    share a recorder, wrap the calls in a lock.
    """

    def __init__(self) -> None:
        self._active_runs: dict[str, _ActiveRun] = {}

    # ------------------------------------------------------------------
    # Trace lifecycle
    # ------------------------------------------------------------------

    def start_trace(
        self,
        run_id: str,
        trace_id: str,
        name: str,
        input: Any = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> TraceCreate:
        """Register the root run and return a `TraceCreate` event.

        The root run is also tracked as an active span so that nested
        children can resolve their `parent_id` to it when they start
        before any explicit span has been opened.
        """
        meta = dict(metadata or {})
        if input is not None:
            # Mirror the historical wire format that places inputs under
            # metadata for trace_create events.
            meta.setdefault("inputs", input)
        self._active_runs[run_id] = _ActiveRun(
            span_id=trace_id,
            trace_id=trace_id,
            parent_id=None,
            kind=SpanType.WORKFLOW,
            name=name,
            input=input,
            metadata=dict(meta),
        )
        return TraceCreate(
            id=trace_id,
            name=name,
            status=SpanStatus.RUNNING,
            metadata=meta,
            tags=list(tags or []),
        )

    def complete_trace(
        self,
        run_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> TraceUpdate:
        """Finalize the root run; returns a success `TraceUpdate`."""
        self._active_runs.pop(run_id, None)
        return TraceUpdate(
            id=run_id,
            status=SpanStatus.SUCCESS,
            end_time=datetime.now(timezone.utc),
            metadata=dict(metadata or {}),
        )

    def error_trace(
        self,
        run_id: str,
        error: BaseException,
        metadata: dict[str, Any] | None = None,
    ) -> TraceUpdate:
        """Finalize the root run with an error; returns an error `TraceUpdate`."""
        self._active_runs.pop(run_id, None)
        msg = str(error)
        return TraceUpdate(
            id=run_id,
            status=SpanStatus.ERROR,
            end_time=datetime.now(timezone.utc),
            error=msg,
            error_message=msg,
            error_type=type(error).__name__,
            metadata=dict(metadata or {}),
        )

    # ------------------------------------------------------------------
    # Span lifecycle (generic over SpanType)
    # ------------------------------------------------------------------

    def start_span(
        self,
        run_id: str,
        kind: SpanType,
        name: str,
        trace_id: str | None = None,
        parent_id: str | None = None,
        input: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> SpanCreate:
        """Open a span and return a `SpanCreate` event.

        `parent_id` defaults to the most recently started active run on
        the same trace, so callers don't have to thread it manually for
        simple cases. `trace_id` is resolved from the parent when
        omitted.
        """
        parent_id, trace_id = self._resolve_lineage(parent_id, trace_id)
        span_id = uuidv7()
        meta = dict(metadata or {})
        run = _ActiveRun(
            span_id=span_id,
            trace_id=trace_id,
            parent_id=parent_id,
            kind=kind,
            name=name,
            input=input,
            metadata=meta,
        )
        self._active_runs[run_id] = run
        return SpanCreate(
            id=span_id,
            trace_id=trace_id,
            parent_id=parent_id,
            name=name,
            type=kind,
            input=input,
            start_time=run.start_time,
            created_at=run.start_time,
            metadata=meta,
        )

    def complete_span(
        self,
        run_id: str,
        output: Any = None,
        metadata: dict[str, Any] | None = None,
        usage: dict[str, int] | None = None,
    ) -> SpanComplete | None:
        """Finalize a span with success; returns a `SpanComplete` event.

        `usage` (typed token-usage dict) is merged into the span metadata
        and its `total_tokens` key populates `SpanComplete.total_tokens`.
        """
        run = self._active_runs.pop(run_id, None)
        if not run:
            return None
        return self._build_complete(
            run,
            status=SpanStatus.SUCCESS,
            output=output,
            extra_metadata=metadata,
            usage=usage,
        )

    def error_span(
        self,
        run_id: str,
        error: BaseException,
        output: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> SpanComplete | None:
        """Finalize a span with an error; returns a `SpanComplete` event
        carrying error / error_message / error_type."""
        run = self._active_runs.pop(run_id, None)
        if not run:
            return None
        return self._build_complete(
            run,
            status=SpanStatus.ERROR,
            output=output,
            extra_metadata=metadata,
            error=error,
        )

    # ------------------------------------------------------------------
    # Streaming-token accessories (optional; useful for LLM spans)
    # ------------------------------------------------------------------

    def mark_first_token(self, run_id: str) -> None:
        """Capture `first_token_time` for the active run.

        Idempotent; subsequent calls are ignored. `complete_span` reads
        this to derive `ttft_ms`. Safe on a non-existent run (no-op).
        """
        run = self._active_runs.get(run_id)
        if run is None or run.first_token_time is not None:
            return
        run.first_token_time = datetime.now(timezone.utc)

    def enrich_metadata(self, run_id: str, **fields: Any) -> None:
        """Merge fields into the active run's metadata. Useful when
        adapters discover model name, document count, etc. partway
        through a span's lifecycle."""
        run = self._active_runs.get(run_id)
        if run is None:
            return
        run.metadata.update(fields)

    # ------------------------------------------------------------------
    # Inspection helpers (mainly for tests / debugging)
    # ------------------------------------------------------------------

    def is_active(self, run_id: str) -> bool:
        """True if `run_id` has an open span/trace on this recorder."""
        return run_id in self._active_runs

    def active_run_ids(self) -> list[str]:
        return list(self._active_runs.keys())

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _resolve_lineage(
        self,
        parent_id: str | None,
        trace_id: str | None,
    ) -> tuple[str | None, str]:
        """Fill in missing parent_id / trace_id from the most recent
        active run. Raises ValueError if the recorder has no active run
        and the caller didn't supply a trace_id — empty-string trace
        ids are worse than a loud crash at the adapter boundary."""
        if parent_id is not None and trace_id is not None:
            return parent_id, trace_id

        last = next(reversed(self._active_runs.values()), None)
        if last is not None:
            if parent_id is None:
                parent_id = last.span_id
            if trace_id is None:
                trace_id = last.trace_id

        if trace_id is None:
            raise ValueError(
                "trace_id required when no active run is registered; "
                "call start_trace(...) first or pass trace_id explicitly"
            )
        return parent_id, trace_id

    def _build_complete(
        self,
        run: _ActiveRun,
        *,
        status: SpanStatus,
        output: Any,
        extra_metadata: dict[str, Any] | None,
        error: BaseException | None = None,
        usage: dict[str, int] | None = None,
    ) -> SpanComplete:
        now = datetime.now(timezone.utc)
        duration_s = (now - run.start_time).total_seconds()
        duration_ns = int(duration_s * 1_000_000_000)

        metadata = dict(run.metadata)
        if extra_metadata:
            metadata.update(extra_metadata)
        if usage:
            metadata["usage"] = dict(usage)
        if run.first_token_time is not None:
            ttft_ms = (run.first_token_time - run.start_time).total_seconds() * 1000
            metadata["completion_start_time"] = run.first_token_time.isoformat()
            metadata["ttft_ms"] = round(ttft_ms, 2)

        total_tokens = int(usage["total_tokens"]) if usage and "total_tokens" in usage else 0

        return SpanComplete(
            id=run.span_id,
            trace_id=run.trace_id,
            parent_id=run.parent_id,
            name=run.name,
            type=run.kind,
            status=status,
            start_time=run.start_time,
            end_time=now,
            input=run.input,
            output=output,
            duration_ns=duration_ns,
            latency_seconds=duration_s,
            total_tokens=total_tokens,
            metadata=metadata,
            error=str(error) if error else None,
            error_message=str(error) if error else None,
            error_type=type(error).__name__ if error else None,
        )
