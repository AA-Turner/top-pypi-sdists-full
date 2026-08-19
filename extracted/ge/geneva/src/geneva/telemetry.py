"""OpenTelemetry (OTLP) metrics + tracing bootstrap for Geneva.

Geneva jobs run as ephemeral, multi-process Ray workloads: the dispatch driver,
the remote pipeline task, and the per-worker actors are each a separate Python
process. A Prometheus-style scrape can't see short-lived workers, so we *push*
both metrics and trace spans over OTLP directly to the collector -- mirroring the
indexer (``src/rust/core/src/telemetry.rs`` in the sophon repo): metrics export
on a fixed interval, and we ``force_flush`` before a process exits so the final
data isn't lost.

Bootstrap is **lazy, idempotent, and process-global**. The first ``get_meter`` /
``get_tracer`` / ``record_ms`` / ``span`` call in a process builds the providers
(only if ``LANCEDB_OTEL_COLLECTOR_URL`` is set) and registers an ``atexit``
flush. A process that never emits anything pays nothing, and a process with no
collector URL configured is a silent no-op.

When metrics are enabled, Lance's object-store metrics are bridged into the same
provider via ``lance.otel`` (disable with ``GENEVA_ENABLE_OTEL_LANCE_METRICS=false``).
Ray workers init at ``import geneva``, gated by ``GENEVA_TELEMETRY_INIT_ON_IMPORT``.

Tracing: a single job's execution lifecycle runs inside one Ray task process, so
a root ``geneva.job`` span there plus nested in-process child spans (``plan`` /
``execute`` / ...) forms one trace per job. If a real ``TracerProvider`` is
already installed in the process (e.g. by geneva_driver), we reuse it so spans
share the same exporter rather than clobbering it.

Per-job identity (``job_id`` / ``job_type`` / ``table`` / ``column`` / ``stage``)
is attached as *metric/span attributes* at record time, never as ``Resource``
attributes: Ray reuses worker processes across tasks and jobs, so the
process-static ``Resource`` only carries values that don't change for the life of
the process (``service.name``, ``service.instance.id`` and, when configured,
``env`` / ``cluster``).

For *metrics* specifically only the bounded labels (``job_type`` / ``stage``) are
attached by default; the high-cardinality ones (``job_id`` / ``table`` /
``column``) are a Prometheus cardinality bomb and are gated behind
``GENEVA_OTEL_METRIC_HIGH_CARDINALITY_LABELS`` (off by default) -- see
:func:`metric_attributes`. Trace spans always carry the full per-job set;
cardinality is not a concern there.
"""

from __future__ import annotations

import atexit
import contextlib
import logging
import os
import socket
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from opentelemetry.metrics import Counter, Histogram, Meter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.trace import Span, Tracer

_LOG = logging.getLogger(__name__)

#: Env var holding the OTLP/gRPC collector endpoint. When unset, telemetry is a
#: no-op. Set on Geneva pods via the ``global.otelCollectorUrl`` Helm value and
#: forwarded into Ray worker processes by ``geneva.runners.ray._mgr``.
OTEL_COLLECTOR_URL_ENV = "LANCEDB_OTEL_COLLECTOR_URL"

#: Matches the indexer's 10s push interval.
_EXPORT_INTERVAL_MS = 10_000

_SERVICE_NAME = "geneva"

#: Env var gating whether high-cardinality labels (``job_id`` / ``table`` /
#: ``column``) are attached to OTLP *metrics*. Off by default: per-job / per-table
#: series explode Prometheus cardinality. Trace spans always carry them.
METRIC_HIGH_CARDINALITY_LABELS_ENV = "GENEVA_OTEL_METRIC_HIGH_CARDINALITY_LABELS"

#: Opt-out for the Lance object-store metrics bridge (default on). Set to
#: ``false`` to disable; unrecognized values also disable, with a warning.
LANCE_METRICS_ENV = "GENEVA_ENABLE_OTEL_LANCE_METRICS"

#: Internal: set on Ray workers by ``geneva.runners.ray._mgr`` so that
#: ``import geneva`` calls :func:`init` before the worker's first I/O.
TELEMETRY_INIT_ON_IMPORT_ENV = "GENEVA_TELEMETRY_INIT_ON_IMPORT"

_lock = threading.Lock()
_initialized = False
_meter_provider: MeterProvider | None = None
_meter: Meter | None = None
_histograms: dict[str, Histogram] = {}
_counters: dict[str, Counter] = {}
_tracer_provider: TracerProvider | None = None
_tracer: Tracer | None = None
# Whether *we* created the TracerProvider (vs reusing one geneva_driver set).
# Only providers we own are shut down.
_owns_tracer_provider = False


def _build_resource() -> Resource:
    from opentelemetry.sdk.resources import Resource

    attributes: dict[str, str] = {"service.name": _SERVICE_NAME}
    # Process-static identity only -- never the per-job axes (see module docs).
    host = os.environ.get("HOSTNAME") or socket.gethostname()
    attributes["service.instance.id"] = f"{host}-{os.getpid()}"
    for env_key, attr_key in (
        ("LANCEDB_ENV", "env"),
        ("GENEVA_CLUSTER_NAME", "cluster"),
    ):
        value = os.environ.get(env_key)
        if value:
            attributes[attr_key] = value
    return Resource.create(attributes)


def _init_metrics(url: str, resource: Resource) -> None:
    global _meter_provider, _meter
    try:
        from opentelemetry import metrics
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
            OTLPMetricExporter,
        )
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

        exporter = OTLPMetricExporter(endpoint=url, insecure=True)
        reader = PeriodicExportingMetricReader(
            exporter, export_interval_millis=_EXPORT_INTERVAL_MS
        )
        provider = MeterProvider(metric_readers=[reader], resource=resource)
        metrics.set_meter_provider(provider)
        _meter_provider = provider
        _meter = provider.get_meter(_SERVICE_NAME)
    except Exception:
        _LOG.warning("failed to initialize geneva metrics", exc_info=True)
        _meter_provider = None
        _meter = None


def _lance_metrics_enabled() -> bool:
    """Whether the Lance metrics bridge is enabled (default on). Unrecognized
    values disable with a warning: the var only appears in an environment to
    turn the bridge off, so a typo must not silently leave it on."""
    value = os.environ.get(LANCE_METRICS_ENV, "").strip().lower()
    if value in ("", "1", "true", "yes", "on"):
        return True
    if value not in ("0", "false", "no", "off"):
        _LOG.warning(
            "unrecognized %s value %r; treating as 'false'", LANCE_METRICS_ENV, value
        )
    return False


def _init_lance_metrics(provider: MeterProvider) -> None:
    """Bridge Lance's object-store metrics into ``provider`` (best-effort).

    Requires pylance >= 9.0.0b21; any failure disables Lance metrics without
    breaking telemetry or the job.
    """
    if not _lance_metrics_enabled():
        _LOG.info("lance object-store metrics disabled via %s", LANCE_METRICS_ENV)
        return
    try:
        from lance.otel import instrument_lance_metrics
    except ImportError:
        _LOG.info(
            "lance object-store metrics unavailable (requires pylance >= 9.0.0b21)"
        )
        return
    try:
        # False: another library holds the process's one Rust recorder slot.
        if not instrument_lance_metrics(provider):
            _LOG.warning(
                "lance object-store metrics disabled: another metrics recorder "
                "is already installed in this process"
            )
    except Exception:
        _LOG.warning("failed to enable lance object-store metrics", exc_info=True)


def _init_tracing(url: str, resource: Resource) -> None:
    global _tracer_provider, _tracer, _owns_tracer_provider
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider

        existing = trace.get_tracer_provider()
        if isinstance(existing, TracerProvider):
            # A real provider is already installed (e.g. by geneva_driver).
            # Reuse it so our spans share its exporter / trace context.
            _tracer_provider = existing
            _tracer = existing.get_tracer(_SERVICE_NAME)
            _owns_tracer_provider = False
            return

        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        provider = TracerProvider(resource=resource)
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=url, insecure=True))
        )
        trace.set_tracer_provider(provider)
        _tracer_provider = provider
        _tracer = provider.get_tracer(_SERVICE_NAME)
        _owns_tracer_provider = True
    except Exception:
        _LOG.warning("failed to initialize geneva tracing", exc_info=True)
        _tracer_provider = None
        _tracer = None
        _owns_tracer_provider = False


def _init_locked() -> None:
    """Build the process-global providers. Caller must hold ``_lock``."""
    global _initialized
    # Latch first so a failed/absent init doesn't re-run on every call.
    _initialized = True

    url = os.environ.get(OTEL_COLLECTOR_URL_ENV)
    if not url:
        _LOG.info("telemetry disabled: %s is unset", OTEL_COLLECTOR_URL_ENV)
        return

    resource = _build_resource()
    _init_metrics(url, resource)
    if _meter_provider is not None:
        _init_lance_metrics(_meter_provider)
    _init_tracing(url, resource)
    atexit.register(shutdown)
    _LOG.info("telemetry initialized; exporting to %s", url)


def _ensure_initialized() -> None:
    if not _initialized:
        with _lock:
            if not _initialized:
                _init_locked()


def init() -> None:
    """Eagerly bootstrap telemetry for this process (idempotent, thread-safe).

    Call at a process/job entrypoint to build the providers and emit the init
    log up front, instead of waiting for the first span/metric. A no-op when
    ``LANCEDB_OTEL_COLLECTOR_URL`` is unset; safe to call repeatedly.
    """
    _ensure_initialized()


def get_meter() -> Meter | None:
    """Return the process-global meter, lazily bootstrapping on first call.

    Returns ``None`` when telemetry is disabled (``LANCEDB_OTEL_COLLECTOR_URL``
    unset) or initialization failed.
    """
    _ensure_initialized()
    return _meter


def get_tracer() -> Tracer | None:
    """Return the process-global tracer, lazily bootstrapping on first call.

    Returns ``None`` when telemetry is disabled or initialization failed.
    """
    _ensure_initialized()
    return _tracer


# Self-documenting descriptions for known metrics, rendered as the Prometheus
# `# HELP` text by the OTel collector's prometheus exporter. Keyed by metric name
# (the persisted geneva metric names); ``record_ms`` / ``add_count`` apply these
# automatically, so callers don't pass them. Durations are in ms.
_METRIC_DESCRIPTIONS: dict[str, str] = {
    "udf_processing_time": "Wall time executing the UDF for a read task (ms).",
    "batch_checkpointing_time": "Time writing per-batch checkpoints for a task (ms).",
    "read_io_time_ms": "Object-store read I/O time for a task (ms).",
    "checkpoint_load_time_ms": "Time loading existing checkpoints for a task (ms).",
    "checkpoint_exists_time_ms": "Time spent on checkpoint existence checks (ms).",
    "checkpoint_list_time_ms": "Time spent listing checkpoints (ms).",
    "read_task_total_time_ms": (
        "Total wall time to process one ReadTask; overlaps the other "
        "read-path timings (ms)."
    ),
    "fragment_checkpointing_time": "Time checkpointing a written fragment (ms).",
    "writer_align_time": "Time aligning batches before writing a fragment (ms).",
    "writer_write_time": "Time writing a fragment to storage (ms).",
    "writer_queue_wait_time_ms": (
        "Time a writer task waited in the queue before running (ms)."
    ),
    "writer_checkpoint_read_time_ms": (
        "Time the writer spent reading checkpoints (ms)."
    ),
    "commit_time_ms": "Time committing fragments to the dataset (ms).",
    "plan_read_time_ms": (
        "Time building the read plan during the planning phase (ms)."
    ),
    "rows_skipped_on_error": "Rows dropped by error handling.",
    "direct_fragment_writes": "Fragments written directly, without a checkpoint.",
    "checkpoint_fragment_writes": "Fragments written via a checkpoint.",
    "tasks_completed": "ReadTasks completed.",
    "writer_fragments": "Fragments written.",
    # UDTF / matview refresh (per-partition).
    "udtf_execute_time": "Wall time executing the UDTF for one partition (ms).",
    "udtf_checkpoint_time": (
        "Time checkpointing fragment metadata for a UDTF partition (ms)."
    ),
    "udtf_rows_produced": "Rows produced by a UDTF partition.",
    "udtf_batches": "Output batches written by a UDTF partition.",
    "udtf_partitions_completed": "UDTF partitions completed.",
}


def get_histogram(
    name: str, *, unit: str = "", description: str = ""
) -> Histogram | None:
    """Get-or-create a cached histogram, or ``None`` when telemetry is disabled.

    Caching avoids the duplicate-instrument warning the SDK emits when the same
    name is created twice in a process.
    """
    meter = get_meter()
    if meter is None:
        return None
    histogram = _histograms.get(name)
    if histogram is None:
        with _lock:
            histogram = _histograms.get(name)
            if histogram is None:
                histogram = meter.create_histogram(
                    name, unit=unit, description=description
                )
                _histograms[name] = histogram
    return histogram


def record_ms(
    name: str, value: float, attributes: dict | None = None, description: str = ""
) -> None:
    """Record a millisecond duration to the named histogram (best-effort).

    ``description`` is applied when the instrument is first created and surfaces
    as the Prometheus ``# HELP`` text; when omitted it defaults to
    :data:`_METRIC_DESCRIPTIONS` for known metrics. Never raises: a telemetry
    failure must not break the pipeline.
    """
    try:
        description = description or _METRIC_DESCRIPTIONS.get(name, "")
        histogram = get_histogram(name, unit="ms", description=description)
        if histogram is not None:
            histogram.record(value, attributes=attributes or {})
    except Exception:
        _LOG.debug("failed to record metric %s", name, exc_info=True)


def get_counter(name: str, *, unit: str = "", description: str = "") -> Counter | None:
    """Get-or-create a cached counter, or ``None`` when telemetry is disabled."""
    meter = get_meter()
    if meter is None:
        return None
    counter = _counters.get(name)
    if counter is None:
        with _lock:
            counter = _counters.get(name)
            if counter is None:
                counter = meter.create_counter(name, unit=unit, description=description)
                _counters[name] = counter
    return counter


def add_count(
    name: str, value: float, attributes: dict | None = None, description: str = ""
) -> None:
    """Add to the named counter (best-effort). ``description`` is applied on first
    creation and surfaces as the Prometheus ``# HELP`` text; when omitted it
    defaults to :data:`_METRIC_DESCRIPTIONS` for known metrics. No-op on falsy
    value; never raises."""
    if not value:
        return
    try:
        description = description or _METRIC_DESCRIPTIONS.get(name, "")
        counter = get_counter(name, description=description)
        if counter is not None:
            counter.add(value, attributes=attributes or {})
    except Exception:
        _LOG.debug("failed to add metric %s", name, exc_info=True)


def metric_high_cardinality_labels_enabled() -> bool:
    """Whether ``job_id`` / ``table`` / ``column`` may be attached to *metric*
    attributes. Gated by ``GENEVA_OTEL_METRIC_HIGH_CARDINALITY_LABELS`` (default
    off); trace spans are unaffected.
    """
    return os.environ.get(METRIC_HIGH_CARDINALITY_LABELS_ENV, "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def metric_attributes(bounded: dict, high_cardinality: dict | None = None) -> dict:
    """Build attributes for an OTLP metric emit.

    ``bounded`` labels (e.g. ``job_type`` / ``stage``) are always included. The
    ``high_cardinality`` labels (``job_id`` / ``table`` / ``column``) are merged
    only when :func:`metric_high_cardinality_labels_enabled` is true, since
    per-job / per-table series explode Prometheus cardinality. ``None`` values are
    dropped on both.
    """
    attrs = {k: v for k, v in bounded.items() if v is not None}
    if high_cardinality and metric_high_cardinality_labels_enabled():
        attrs.update({k: v for k, v in high_cardinality.items() if v is not None})
    return attrs


@contextlib.contextmanager
def span(name: str, attributes: dict | None = None) -> Iterator[Span | None]:
    """Start a span as the current span, or a no-op when tracing is disabled.

    Nested ``span()`` calls in the same process become children automatically
    via the OTEL context, which is how a job's root span and its per-operation
    child spans form a single trace. Exceptions are recorded on the span and set
    its status to ERROR (OTEL defaults), then re-raised.
    """
    tracer = get_tracer()
    if tracer is None:
        yield None
        return
    with tracer.start_as_current_span(name, attributes=attributes or {}) as sp:
        yield sp


def open_span(
    name: str, attributes: dict | None = None, *, parent: Span | None = None
) -> Span | None:
    """Start a span *without* making it current, and return it (or ``None`` when
    tracing is disabled). End it with :func:`close_span`.

    By default the span is a child of the current span; pass ``parent`` to nest
    it under a specific span instead (e.g. a sub-span of another ``open_span``
    span, which -- being non-attached -- is not the current span).

    Use this to time a code segment inline -- avoiding a ``with`` re-indent of a
    large block -- when the segment has no telemetry children of its own (any
    nested ``span()`` would attach under the current span, not this one). Sibling
    segments timed this way don't nest under each other. Best-effort: a leaked
    span (``close_span`` skipped on a raised exception) is acceptable for
    telemetry, and there is no context token to leak.
    """
    tracer = get_tracer()
    if tracer is None:
        return None
    try:
        ctx = None
        if parent is not None:
            from opentelemetry import trace

            ctx = trace.set_span_in_context(parent)
        return tracer.start_span(name, context=ctx, attributes=attributes or {})
    except Exception:
        _LOG.debug("failed to start span %s", name, exc_info=True)
        return None


@contextlib.contextmanager
def attach_span(sp: Span | None) -> Iterator[None]:
    """Make an :func:`open_span` span the current span for the block *without*
    ending it, so spans started inside nest under it.

    Pairs a single ``open_span`` + :func:`close_span` (which spans a large inline
    block with no ``with`` re-indent) with an attached sub-region, so telemetry
    children created there (e.g. ``plan_read`` sub-spans) parent to it. No-op
    when ``sp`` is None (tracing disabled).
    """
    if sp is None:
        yield
        return
    from opentelemetry.trace import use_span

    with use_span(sp, end_on_exit=False):
        yield


def close_span(sp: Span | None, exc: BaseException | None = None) -> None:
    """End a span from :func:`open_span` (best-effort); pass an in-flight
    exception to mark its status ERROR."""
    if sp is None:
        return
    try:
        if exc is not None:
            from opentelemetry.trace import Status, StatusCode

            sp.record_exception(exc)
            sp.set_status(Status(StatusCode.ERROR, str(exc)))
        sp.end()
    except Exception:
        _LOG.debug("failed to end span", exc_info=True)


def set_span_attrs(sp: Span | None, attributes: dict) -> None:
    """Set ``attributes`` on an open span; no-op when ``sp`` is None.

    Companion to :func:`open_span`/:func:`span` for attributes that are only
    known after the span starts (e.g. row/fragment counts resolved mid-phase).
    ``None`` values are skipped since OTel attributes may not be null.
    """
    if sp is None:
        return
    try:
        for _k, _v in attributes.items():
            if _v is not None:
                sp.set_attribute(_k, _v)
    except Exception:
        _LOG.debug("failed to set span attributes", exc_info=True)


def set_current_span_attrs(attributes: dict) -> None:
    """Set ``attributes`` on the currently active span (best-effort).

    Useful where the relevant span (e.g. ``geneva.job``) is attached but not
    held locally. No-op when tracing is disabled or no span is recording.
    """
    if get_tracer() is None:
        return
    try:
        from opentelemetry import trace

        sp = trace.get_current_span()
        if sp is not None and sp.is_recording():
            for _k, _v in attributes.items():
                if _v is not None:
                    sp.set_attribute(_k, _v)
    except Exception:
        _LOG.debug("failed to set current span attributes", exc_info=True)


def add_span_event(name: str, attributes: dict | None = None) -> None:
    """Record a timestamped event on the currently active span (best-effort).

    Used to mark phase transitions (e.g. ``phase.planning``) on the timeline of
    whatever span is active. No-op when tracing is disabled or no span records.
    """
    if get_tracer() is None:
        return
    try:
        from opentelemetry import trace

        sp = trace.get_current_span()
        if sp is not None and sp.is_recording():
            sp.add_event(name, attributes=attributes or {})
    except Exception:
        _LOG.debug("failed to add span event %s", name, exc_info=True)


def start_job_span(
    attributes: dict | None = None, *, name: str = "geneva.job"
) -> tuple[Span | None, object | None]:
    """Start a root span and attach it as the current context span.

    Returns ``(span, token)``; pass both to :func:`end_job_span` in a ``finally``.
    Returns ``(None, None)`` when tracing is disabled. Use this -- rather than
    :func:`span` -- at a job/process boundary where wrapping the whole body in a
    ``with`` is awkward; child ``span()`` calls then nest under it via the
    attached context, forming one trace per job.
    """
    tracer = get_tracer()
    if tracer is None:
        return None, None
    try:
        from opentelemetry import context as context_api
        from opentelemetry import trace

        sp = tracer.start_span(name, attributes=attributes or {})
        token = context_api.attach(trace.set_span_in_context(sp))
        return sp, token
    except Exception:
        _LOG.debug("failed to start job span", exc_info=True)
        return None, None


def end_job_span(
    job_span: Span | None, token: object | None, exc: BaseException | None = None
) -> None:
    """End a span started by :func:`start_job_span` and detach its context.

    Pass the in-flight exception (if any) to mark the span's status ERROR.
    """
    try:
        if token is not None:
            from opentelemetry import context as context_api

            context_api.detach(token)  # type: ignore[arg-type]
        if job_span is not None:
            if exc is not None:
                from opentelemetry.trace import Status, StatusCode

                job_span.record_exception(exc)
                job_span.set_status(Status(StatusCode.ERROR, str(exc)))
            job_span.end()
    except Exception:
        _LOG.debug("failed to end job span", exc_info=True)


def inject_context() -> dict:
    """Serialize the current trace context into a W3C carrier dict.

    Call on the *caller* side, inside the span you want as the parent, then pass
    the returned dict across the Ray RPC boundary; the worker rebuilds the parent
    with :func:`start_linked_span`. Returns ``{}`` when tracing is disabled.
    """
    if get_tracer() is None:
        return {}
    try:
        from opentelemetry.propagate import inject

        carrier: dict = {}
        inject(carrier)
        return carrier
    except Exception:
        _LOG.debug("failed to inject trace context", exc_info=True)
        return {}


def start_linked_span(
    carrier: dict | None, name: str, attributes: dict | None = None
) -> tuple[Span | None, object | None]:
    """Start ``name`` parented to the remote context in ``carrier``.

    The span is attached as the current span (so its own children nest under it)
    and returned as ``(span, token)`` -- end it with :func:`end_job_span`. Used on
    the *worker* side to tie a Ray-actor span back into the originating job's
    trace. Returns ``(None, None)`` when tracing is disabled.
    """
    tracer = get_tracer()
    if tracer is None:
        return None, None
    try:
        from opentelemetry import context as context_api
        from opentelemetry import trace
        from opentelemetry.propagate import extract

        parent = extract(carrier or {})
        sp = tracer.start_span(name, context=parent, attributes=attributes or {})
        token = context_api.attach(trace.set_span_in_context(sp))
        return sp, token
    except Exception:
        _LOG.debug("failed to start linked span", exc_info=True)
        return None, None


def flush(timeout_millis: int = 5_000) -> None:
    """Force-export buffered metrics and spans. No-op when disabled.

    Call this at a process/task boundary (e.g. a Ray task ``finally``) so the
    final data is exported before the worker is reclaimed.
    """
    if _meter_provider is not None:
        try:
            _meter_provider.force_flush(timeout_millis=timeout_millis)
        except Exception:
            _LOG.debug("metrics force_flush failed", exc_info=True)
    if _tracer_provider is not None:
        try:
            _tracer_provider.force_flush(timeout_millis=timeout_millis)
        except Exception:
            _LOG.debug("traces force_flush failed", exc_info=True)


def shutdown(timeout_millis: int = 5_000) -> None:
    """Flush and tear down providers we own. No-op when disabled."""
    if _meter_provider is not None:
        try:
            _meter_provider.shutdown(timeout_millis=timeout_millis)
        except Exception:
            _LOG.debug("metrics shutdown failed", exc_info=True)
    # Only shut down a tracer provider we created -- never one owned by
    # geneva_driver or another component in this process.
    if _tracer_provider is not None and _owns_tracer_provider:
        try:
            _tracer_provider.shutdown()
        except Exception:
            _LOG.debug("traces shutdown failed", exc_info=True)


def _reset_state() -> None:
    """Reset module state. For tests only."""
    global _initialized, _meter_provider, _meter
    global _tracer_provider, _tracer, _owns_tracer_provider
    with _lock:
        _initialized = False
        _meter_provider = None
        _meter = None
        _histograms.clear()
        _tracer_provider = None
        _tracer = None
        _owns_tracer_provider = False


def _reset_after_fork() -> None:
    # Runs in the child immediately after os.fork(): drop the inherited providers
    # (their exporter / background threads don't survive fork) so the child
    # re-inits lazily only if it emits, and never double-flushes on exit. geneva
    # forks subprocesses for multiprocess UDF execution. Must NOT take _lock --
    # another thread may have held it at fork time.
    global _initialized, _meter_provider, _meter
    global _tracer_provider, _tracer, _owns_tracer_provider
    _initialized = False
    _meter_provider = None
    _meter = None
    _histograms.clear()
    _tracer_provider = None
    _tracer = None
    _owns_tracer_provider = False


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)
