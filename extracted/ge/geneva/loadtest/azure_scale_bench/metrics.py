# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Azure storage-op & throughput metrics (GEN-626).

Geneva emits no object-storage counters today (GEN-636), so this captures them at
the workbench level via three pluggable sources:

1. ``lance`` in-process telemetry — ``io_stats`` (read/write iops+bytes) and
   ``tracing`` throttle/retry events (target ``lance::object_store::throttle``,
   surfaced only when AIMD is enabled via the worker manifest env, see
   ``worker_aimd_env``). Account-key friendly; captures the *current process*.
2. ``azure_monitor`` — account-level Transactions (GetBlob/Put/List, 429/503),
   Egress/Ingress, latency for a time window. The ground truth across all nodes,
   but ARM/AAD-authenticated (needs ``Monitoring Reader`` + a subscription/RG),
   not the storage account key. Opt-in.
3. derived normalization (per-node, per-cpu, throttle rate).

The schema is stable so a future ``geneva_jobtracker`` backend (GEN-636) can fill
the same fields once Geneva emits counters.
"""

from __future__ import annotations

import contextlib
import logging
import threading
import time
from typing import TYPE_CHECKING, Any

import attrs

if TYPE_CHECKING:
    from collections.abc import Iterator

_LOG = logging.getLogger(__name__)

# Tracing targets that carry AIMD throttle / retry telemetry.
_THROTTLE_TARGETS = frozenset(
    {"lance::object_store::throttle", "lance_io::object_store::throttle"}
)


@attrs.define
class StorageOpMetrics:
    """Per-(run, stage) storage-op metrics; total + normalized views."""

    stage: str
    suffix: str
    source: str = "lance"
    wall_seconds: float = 0.0
    num_nodes: int | None = None
    num_cpus: int | None = None
    # lance in-process IO (driver, or rolled up from workers).
    read_iops: int = 0
    read_bytes: int = 0
    write_iops: int = 0
    written_bytes: int = 0
    # throttle / retry, from tracing (worker-side under AIMD).
    throttle_events: int = 0
    retry_events: int = 0
    max_backoff_ms: int = 0
    # account-level Azure Monitor block (optional).
    azure: dict[str, Any] | None = None

    def normalized(self) -> dict[str, float]:
        """Per-node and per-cpu rates for the scaling-curve comparison."""
        out: dict[str, float] = {}
        total_ops = self.read_iops + self.write_iops
        if self.wall_seconds > 0:
            out["ops_per_s"] = round(total_ops / self.wall_seconds, 2)
            out["bytes_per_s"] = round(
                (self.read_bytes + self.written_bytes) / self.wall_seconds, 2
            )
        if self.num_nodes:
            out["ops_per_node"] = round(total_ops / self.num_nodes, 2)
        if self.num_cpus:
            out["ops_per_cpu"] = round(total_ops / self.num_cpus, 2)
        return out

    def to_dict(self) -> dict[str, Any]:
        data = attrs.asdict(self)
        data["normalized"] = self.normalized()
        return data


# --- lance in-process tracing capture -------------------------------------
# capture_trace_events registers a process-global callback that cannot be
# unregistered, so throttle counts accumulate in a module-global and callers
# snapshot deltas (mirrors io_stats_incremental).

_THROTTLE = {"throttle_events": 0, "retry_events": 0, "max_backoff_ms": 0}
_CAPTURE_STARTED = False
# capture_trace_events runs the callback on a dedicated thread, so guard the
# accumulator (the read-modify-writes below race with snapshot reads).
_THROTTLE_LOCK = threading.Lock()


def _coerce_int(value: Any) -> int | None:
    """lance stringifies all trace-event arg values, so coerce defensively."""
    if value is None:
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _on_trace_event(event: Any) -> None:
    target = getattr(event, "target", "") or ""
    if target not in _THROTTLE_TARGETS:
        return
    args = dict(getattr(event, "args", {}) or {})
    backoff = _coerce_int(args.get("backoff_ms"))
    with _THROTTLE_LOCK:
        _THROTTLE["throttle_events"] += 1
        if "attempt" in args or "retries" in args:
            _THROTTLE["retry_events"] += 1
        if backoff is not None:
            _THROTTLE["max_backoff_ms"] = max(_THROTTLE["max_backoff_ms"], backoff)


def start_trace_capture() -> bool:
    """Register the throttle-event callback once. Returns True if active."""
    global _CAPTURE_STARTED
    if _CAPTURE_STARTED:
        return True
    try:
        import lance.tracing as tracing

        tracing.capture_trace_events(_on_trace_event)
        _CAPTURE_STARTED = True
    except Exception as exc:  # noqa: BLE001 - telemetry is best-effort
        _LOG.debug("lance trace capture unavailable: %s", exc)
    return _CAPTURE_STARTED


def throttle_snapshot() -> dict[str, int]:
    """A consistent snapshot of the cumulative throttle counters."""
    with _THROTTLE_LOCK:
        return dict(_THROTTLE)


@contextlib.contextmanager
def capture_stage(
    stage: str,
    suffix: str,
    *,
    dataset: Any | None = None,
    num_nodes: int | None = None,
    num_cpus: int | None = None,
) -> Iterator[StorageOpMetrics]:
    """Time a stage and capture in-process IO + throttle deltas.

    ``dataset`` (a ``lance.LanceDataset``) enables io_stats deltas — note this is
    the *driver's* handle, so during a Ray backfill it sees commit/manifest IO,
    not the workers' blob traffic (use Azure Monitor or the AIMD worker seam for
    cluster-wide counts).
    """
    start_trace_capture()
    metrics = StorageOpMetrics(
        stage=stage, suffix=suffix, num_nodes=num_nodes, num_cpus=num_cpus
    )
    t0 = throttle_snapshot()
    io0 = _io_snapshot(dataset)
    start = time.time()
    try:
        yield metrics
    finally:
        metrics.wall_seconds = round(time.time() - start, 2)
        t1 = throttle_snapshot()
        metrics.throttle_events = t1["throttle_events"] - t0["throttle_events"]
        metrics.retry_events = t1["retry_events"] - t0["retry_events"]
        # Cumulative (monotonic) max backoff since process start — not per-stage;
        # a global accumulator can't yield a windowed max.
        metrics.max_backoff_ms = t1["max_backoff_ms"]
        io1 = _io_snapshot(dataset)
        if io0 is not None and io1 is not None:
            metrics.read_iops = io1["read_iops"] - io0["read_iops"]
            metrics.read_bytes = io1["read_bytes"] - io0["read_bytes"]
            metrics.write_iops = io1["write_iops"] - io0["write_iops"]
            metrics.written_bytes = io1["written_bytes"] - io0["written_bytes"]


def _io_snapshot(dataset: Any | None) -> dict[str, int] | None:
    if dataset is None:
        return None
    try:
        stats = dataset.io_stats_snapshot()
        return {
            "read_iops": stats.read_iops,
            "read_bytes": stats.read_bytes,
            "write_iops": stats.write_iops,
            "written_bytes": stats.written_bytes,
        }
    except Exception as exc:  # noqa: BLE001
        _LOG.debug("io_stats unavailable: %s", exc)
        return None


# --- worker AIMD seam ------------------------------------------------------

# AIMD *tuning* knobs + throttle-event logging, for the MANIFEST env_vars (driver
# os.environ does not propagate to KubeRay workers). NOTE: these tune AIMD and
# enable its WARN logging; they do NOT by themselves guarantee the AIMD throttled
# store is *enabled* — that is selected at object-store construction (likely a
# storage_option). Verify the enable path before relying on worker throttle
# counts; if AIMD is off there are no events to count.
DEFAULT_AIMD_ENV = {
    "LANCE_AIMD_MAX_RETRIES": "10",
    "LANCE_AIMD_MIN_BACKOFF_MS": "50",
    "LANCE_AIMD_MAX_BACKOFF_MS": "10000",
    "RUST_LOG": (
        "lance::object_store::throttle=warn,lance_io::object_store::throttle=warn"
    ),
}


def worker_aimd_env(
    *, enable: bool = True, overrides: dict[str, str] | None = None
) -> dict[str, str]:
    """Manifest env_vars that tune AIMD + enable its throttle-event logging.

    See ``DEFAULT_AIMD_ENV``: enabling the throttled store itself is separate.
    """
    if not enable:
        return {}
    env = dict(DEFAULT_AIMD_ENV)
    if overrides:
        env.update(overrides)
    return env


# --- Azure Monitor backend (opt-in) ----------------------------------------


def metrics_window(minutes: int) -> tuple[Any, Any]:
    """A (start, end) UTC window of the last ``minutes`` for a metrics query."""
    if minutes <= 0:
        raise ValueError(f"minutes must be > 0, got {minutes}")
    from datetime import datetime, timedelta, timezone

    end = datetime.now(timezone.utc)
    return end - timedelta(minutes=minutes), end


def blob_resource_id(subscription_id: str, resource_group: str, account: str) -> str:
    """ARM resource id for a storage account's blob service."""
    return (
        f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
        f"/providers/Microsoft.Storage/storageAccounts/{account}/blobServices/default"
    )


def azure_monitor_metrics(
    *,
    subscription_id: str,
    resource_group: str,
    account: str,
    start_time: Any,
    end_time: Any,
    interval_minutes: int = 1,
) -> dict[str, Any]:
    """Pull account-level transaction/throughput metrics for a window.

    Returns the GEN-626 breakdown: Transactions split by ResponseType (Success,
    ClientThrottlingError=429, ServerBusyError=503, ...) and by ApiName (GetBlob,
    PutBlob, ListBlobs, ...), plus Egress/Ingress totals and SuccessE2ELatency
    (averaged). Requires ``azure-monitor-query`` + ``azure-identity`` and an AAD
    identity with ``Monitoring Reader`` on the account (NOT the storage account
    key). Raises a clear error when those are unavailable.

    Not exercisable in this environment (deps + AAD absent); verify against a live
    account when credentials are configured.
    """
    try:
        from azure.core.exceptions import (  # pyright: ignore[reportMissingImports]
            AzureError,
        )
        from azure.identity import DefaultAzureCredential
        from azure.monitor.query import (  # pyright: ignore[reportMissingImports]
            MetricAggregationType,
            MetricsQueryClient,
        )
    except ImportError as exc:
        raise RuntimeError(
            "azure_monitor backend needs `azure-monitor-query` and `azure-identity`; "
            "install them and authenticate an identity with the Monitoring Reader "
            "role on the storage account (account key is not sufficient)."
        ) from exc

    from datetime import timedelta

    try:
        client = MetricsQueryClient(DefaultAzureCredential())
        resource_id = blob_resource_id(subscription_id, resource_group, account)
        window = (start_time, end_time)
        granularity = timedelta(minutes=interval_minutes)

        def _by_dimension(metric: str, dimension: str, agg: Any) -> dict[str, float]:
            """Sum a metric per value of one dimension (e.g. ResponseType, ApiName)."""
            response = client.query_resource(
                resource_id,
                metric_names=[metric],
                timespan=window,
                granularity=granularity,
                aggregations=[agg],
                filter=f"{dimension} eq '*'",
            )
            out: dict[str, float] = {}
            for m in response.metrics:
                for series in m.timeseries:
                    key = _series_dimension_value(series) or "unknown"
                    total = sum(
                        v
                        for p in series.data
                        if (v := _point_value(p, agg)) is not None
                    )
                    out[key] = out.get(key, 0.0) + total
            return out

        def _scalar(metric: str, agg: Any) -> float:
            """Sum the datapoints for a TOTAL metric; mean them for an AVERAGE one
            (summing per-minute averages is meaningless)."""
            response = client.query_resource(
                resource_id,
                metric_names=[metric],
                timespan=window,
                granularity=granularity,
                aggregations=[agg],
            )
            averaging = "average" in str(agg).lower()
            values = [
                v
                for m in response.metrics
                for series in m.timeseries
                for p in series.data
                if (v := _point_value(p, agg)) is not None
            ]
            if not values:
                return 0.0
            return sum(values) / len(values) if averaging else sum(values)

        by_response = _by_dimension(
            "Transactions", "ResponseType", MetricAggregationType.TOTAL
        )
        by_api = _by_dimension("Transactions", "ApiName", MetricAggregationType.TOTAL)
        return {
            "resource_id": resource_id,
            "transactions_by_response_type": by_response,
            "transactions_by_api": by_api,
            "txn_total": sum(by_response.values()),
            "err_429": by_response.get("ClientThrottlingError", 0.0),
            "err_503": by_response.get("ServerBusyError", 0.0),
            "egress_bytes": _scalar("Egress", MetricAggregationType.TOTAL),
            "ingress_bytes": _scalar("Ingress", MetricAggregationType.TOTAL),
            "e2e_latency_ms_avg": _scalar(
                "SuccessE2ELatency", MetricAggregationType.AVERAGE
            ),
        }
    except AzureError as exc:
        raise RuntimeError(
            "azure_monitor query failed: "
            f"{exc}. Check AAD identity, Monitoring Reader permissions on the "
            "storage account, and the subscription/resource group."
        ) from exc


def _series_dimension_value(series: Any) -> str | None:
    """Extract the dimension value from a timeseries' metadata."""
    for meta in getattr(series, "metadata_values", None) or []:
        name = getattr(meta, "name", None)
        # name may be a localizable object with .value, or a plain string.
        if name is not None:
            return getattr(meta, "value", None)
    return None


def _point_value(point: Any, agg: Any) -> float | None:
    """Read total/average off a data point; None for empty buckets (so they are
    excluded from sums and don't drag an average down)."""
    average = "average" in str(agg).lower()
    value = point.average if average else point.total
    return float(value) if value is not None else None
